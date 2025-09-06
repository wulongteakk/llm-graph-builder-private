
import torch
import logging
from typing import List, Dict, Any, Tuple, Callable


class GraphDataTransformer:
    """
    负责将从 Neo4j 检索到的动态子图数据转换为 JointLK 模型所需的张量格式。
    """

    def __init__(self, tokenizer: Callable, max_seq_len: int = 128):
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len
        self.relation_name_to_id = {}  # 动态映射关系类型到整数ID
        self.relation_id_counter = 0

    def map_relation_type(self, relation_name: str) -> int:
        """为关系类型字符串分配一个唯一的整数ID。"""
        if relation_name not in self.relation_name_to_id:
            self.relation_name_to_id[relation_name] = self.relation_id_counter
            self.relation_id_counter += 1
        return self.relation_name_to_id[relation_name]

    def format_for_jointlk(
            self,
            subgraph_nodes: List[Dict[str, Any]],
            subgraph_relationships: List[Dict[str, Any]],
            question: str
    ) -> Dict[str, Any]:
        """
        核心转换函数。

        :param subgraph_nodes: 从 Neo4j 检索到的节点列表。
        :param subgraph_relationships: 从 Neo4j 检索到的关系列表。
        :param question: 用户的输入问题。
        :return: 包含张量化输入的字典，用于 JointLK 模型。
        """
        logging.info(
            f"Starting transformation for JointLK input. Nodes: {len(subgraph_nodes)}, Rels: {len(subgraph_relationships)}")

        # --- 1. 节点处理和本地索引映射 ---
        # a. 收集所有唯一的节点ID，并创建从 Neo4j ID到本地整数索引的映射
        node_id_to_local_index = {}
        local_index_to_node_text = []
        current_local_index = 0
        for node in subgraph_nodes:
            neo4j_id = node.get('id')
            if neo4j_id not in node_id_to_local_index:
                node_id_to_local_index[neo4j_id] = current_local_index
                # 提取节点文本内容用于可能的上下文增强
                node_text = node.get('properties', {}).get('name', '') or node.get('properties', {}).get('text', '')
                local_index_to_node_text.append(node_text)
                current_local_index += 1

        num_nodes = len(node_id_to_local_index)
        if num_nodes == 0:
            logging.warning("No nodes found in subgraph. Proceeding with text only.")

        # --- 2. 边处理和关系类型映射 ---
        edge_list_start = []
        edge_list_end = []
        edge_type_list = []

        for rel in subgraph_relationships:
            start_neo4j_id = rel.get('start_node_id')
            end_neo4j_id = rel.get('end_node_id')
            rel_type_name = rel.get('type')

            # 确保边的两个节点都在我们的子图节点集中
            if start_neo4j_id in node_id_to_local_index and end_neo4j_id in node_id_to_local_index:
                local_start_index = node_id_to_local_index[start_neo4j_id]
                local_end_index = node_id_to_local_index[end_neo4j_id]

                # 分配关系类型ID
                rel_id = self.map_relation_type(rel_type_name)

                edge_list_start.append(local_start_index)
                edge_list_end.append(local_end_index)
                edge_type_list.append(rel_id)

        # --- 3. 构建张量 ---
        if len(edge_list_start) > 0:
            edge_index = torch.tensor([edge_list_start, edge_list_end], dtype=torch.long)
            edge_type = torch.tensor(edge_type_list, dtype=torch.long)
        else:
            edge_index = torch.empty((2, 0), dtype=torch.long)
            edge_type = torch.empty((0), dtype=torch.long)

        # --- 4. 文本处理 ---

        context_string = " ".join(set(local_index_to_node_text))
        input_text = f"{question} [SEP] {context_string}"


        inputs = self.tokenizer(
            input_text,
            max_length=self.max_seq_len,
            padding='max_length',
            truncation=True,
            return_tensors="pt"
        )

        # --- 5. 组装返回字典 ---
        result_batch = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
            "adj": (edge_index, edge_type),  # 图结构 (edge_index, edge_type)
            "num_nodes": num_nodes,
            "metadata": {
                "relation_mapping": self.relation_name_to_id,
                "processed_nodes": num_nodes,
                "processed_edges": len(edge_list_start)
            }
        }
        logging.info(f"Transformation complete. Processed relations map: {self.relation_name_to_id}")
        return result_batch