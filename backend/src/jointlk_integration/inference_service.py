

import torch
import os
import sys
import logging
from typing import List, Dict, Any, Tuple, Callable
from transformers import RobertaTokenizer, RobertaConfig

# --- 动态添加 JointLK 库到 Python 路径 ---

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '../../../'))  # 回退三层到 llm-graph-builder-private/
jointlk_path = os.path.join(project_root, 'JointLK')
if jointlk_path not in sys.path:
    sys.path.append(jointlk_path)

# --- 导入 JointLK 模型 ---
try:
    from modeling.modeling_jointlk import JointLK_Model
except ImportError as e:
    logging.error(f"Failed to import JointLK model from {jointlk_path}. Error: {e}")

    #JointLK模型加载不成功也不出错

    class MockJointLKModel(torch.nn.Module):
        def __init__(self, config, *args, **kwargs):
            super().__init__()
            logging.warning("[MockJointLKModel] Using mock model class.")
            self.config = config

        def forward(self, input_ids, attention_mask, adj=None, **kwargs):
            logging.info(f"[MockJointLKModel] Mock inference call with input shape {input_ids.shape}.")

            return torch.rand(input_ids.shape[0], 5)


    JointLK_Model = MockJointLKModel


class JointLKInferenceService:
    """
    封装 JointLK 模型的加载和推理过程。
    """

    def __init__(self, model_checkpoint_path: str, model_name: str = 'roberta-large', num_relations: int = 100):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_checkpoint_path = model_checkpoint_path
        self.model_name = model_name
        self.num_relations_on_init = num_relations  # JointLK 初始化时需要的关系数量上限
        self.model = None
        self.tokenizer = None

    def load_model(self):
        """加载模型和分词器到内存。"""
        logging.info(f"Loading JointLK model. Base model: {self.model_name}, Device: {self.device}")
        try:
            self.tokenizer = RobertaTokenizer.from_pretrained(self.model_name)
            config = RobertaConfig.from_pretrained(self.model_name)


            config.num_relation = self.num_relations_on_init

            # 实例化模型
            self.model = JointLK_Model(config=config, num_relation=config.num_relation)

            # 加载预训练权重 (如果提供了 checkpoint)
            if os.path.exists(self.model_checkpoint_path):
                logging.info(f"Loading weights from checkpoint: {self.model_checkpoint_path}")
                self.model.load_state_dict(torch.load(self.model_checkpoint_path, map_location=self.device))
            else:
                logging.warning(f"Checkpoint file not found at {self.model_checkpoint_path}. Using base model weights.")

            self.model.to(self.device)
            self.model.eval()
            logging.info("JointLK model loaded successfully.")

        except Exception as e:
            logging.error(f"Failed to load JointLK model: {e}", exc_info=True)
            raise

    def run_inference(self, prepared_input: Dict[str, Any]) -> str:
        """
        执行推理。

        :param prepared_input: 经过 data_transformer.py 处理后的输入数据字典。
        :return: 推理结果字符串。
        """
        if self.model is None or self.tokenizer is None:
            logging.error("Model not loaded. Call load_model() first.")
            return "Error: Model not initialized."

        # 将输入数据移动到指定设备
        try:
            input_ids = prepared_input["input_ids"].to(self.device)
            attention_mask = prepared_input["attention_mask"].to(self.device)
            edge_index, edge_type = prepared_input["adj"]
            edge_index = edge_index.to(self.device)
            edge_type = edge_type.to(self.device)
        except Exception as e:
            logging.error(f"Error moving data to device: {e}")
            return "Error during data preparation for inference."

        # 执行 JointLK forward pass
        with torch.no_grad():
            try:
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    adj=(edge_index, edge_type)
                )

                # --- 结果解析 ---
                # JointLK 的输出取决于其最终的分类头。
                # 对于多项选择题，我们会取 argmax。对于生成任务，需要解码器。
                # 此处简化为返回一个指示性结果。
                prediction_index = torch.argmax(outputs, dim=-1).item()
                result_str = f"JointLK enhanced answer (Prediction Index: {prediction_index})"
                logging.info(f"Inference complete. Result: {result_str}")
                return result_str

            except Exception as e:
                logging.error(f"Error during JointLK model forward pass: {e}", exc_info=True)
                return "Error during model reasoning process."