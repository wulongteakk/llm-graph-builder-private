

import os
import logging
from .inference_service import JointLKInferenceService
from .data_transformer import GraphDataTransformer

# --- 配置 ---
# 假设模型 checkpoint 存放在项目根目录下的 'models' 文件夹中
MODEL_CHECKPOINT_PATH = r"D:\NEO4J_related\llm-builder\llm\llm-graph-builder\JointLK\saved_models\medqa_usmle\medqa_usmle.model.pt.dev_38.0-test_39.8"
BASE_MODEL_NAME = 'roberta-large'
MAX_RELATIONS = 150  # 预设的最大关系类型数量


class IntegrationFacade:
    """
    集成外观模式，统一管理 JointLK 服务和数据转换器。
    """

    def __init__(self):
        self.inference_service = JointLKInferenceService(
            model_checkpoint_path=MODEL_CHECKPOINT_PATH,
            model_name=BASE_MODEL_NAME,
            num_relations=MAX_RELATIONS
        )
        self.transformer = None

    def initialize(self):
        """加载模型并初始化转换器。"""
        try:
            self.inference_service.load_model()
            self.transformer = GraphDataTransformer(
                tokenizer=self.inference_service.tokenizer,
                max_seq_len=128  # 可配置
            )
            logging.info("JointLK IntegrationFacade initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize IntegrationFacade: {e}")
            raise

    def process_query(self, question: str, nodes: list, relationships: list) -> dict:
        """
        完整的处理流程：转换数据 -> 执行推理。
        """
        if not self.transformer:
            return {"error": "Service not initialized."}

        try:
            # 1. 数据转换
            prepared_data = self.transformer.format_for_jointlk(nodes, relationships, question)

            # 2. 模型推理
            answer = self.inference_service.run_inference(prepared_data)

            return {
                "answer": answer,
                "source": "JointLK Enhanced Reasoning",
                "metadata": prepared_data.get("metadata")
            }
        except Exception as e:
            logging.error(f"Error processing query through JointLK facade: {e}", exc_info=True)
            return {"error": "An internal error occurred during reasoning."}


# --- 单例模式 ---
# 创建一个全局实例，以便在 main.py 中调用
try:
    jointlk_facade = IntegrationFacade()
    jointlk_facade.initialize()
except Exception:
    jointlk_facade = None
    logging.critical("Failed to create and initialize JointLK Facade. JointLK features will be disabled.")