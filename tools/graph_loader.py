import yaml
from typing import Any, Dict, List

from agents.rss_reader_agent import RSSReaderAgent
from agents.diff_detector_agent import DiffDetectorAgent
from agents.translator_agent import TranslatorAgent

from schemas.translation_schema import TranslationResult
from schemas.rss_schema import Article

# 利用可能なエージェントクラスをマッピング
AGENT_CLASSES = {
    "RSSReaderAgent": RSSReaderAgent,
    "DiffDetectorAgent": DiffDetectorAgent,
    "TranslatorAgent": TranslatorAgent,
}

class Node:
    def __init__(self, node_id: str, node_type: str, inputs: Dict[str, Any]):
        self.id = node_id
        self.type = node_type
        self.inputs = inputs
        self.output = None

    def run(self, context: Dict[str, "Node"]):
        # 入力を解決（参照ノードの出力を使う）
        resolved_inputs = {}
        for key, val in self.inputs.items():
            if isinstance(val, str) and "." in val:
                ref_node_id, _ = val.split(".")
                resolved_inputs[key] = context[ref_node_id].output
            else:
                resolved_inputs[key] = val

        # エージェントの呼び出し
        AgentClass = AGENT_CLASSES[self.type]

        if self.type == "RSSReaderAgent":
            self.output = AgentClass(resolved_inputs["feed_urls"]).run()

        elif self.type == "DiffDetectorAgent":
            self.output = AgentClass(
                jp_articles=resolved_inputs["jp_articles"],
                intl_articles=resolved_inputs["intl_articles"]
            ).run()

        elif self.type == "TranslatorAgent":
            self.output = [
                AgentClass().run(
                    article if isinstance(article, Article) else Article(**article)
                )
                for article in resolved_inputs["articles"]
            ]

        context[self.id] = self

def load_graph_from_yaml(yaml_path: str) -> List[TranslationResult]:
    """
    YAML に記述された Graph を読み込み、エージェントを順に実行し、結果を返す
    """
    with open(yaml_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nodes_config = config["nodes"]
    context: Dict[str, Node] = {}

    for node_conf in nodes_config:
        node = Node(
            node_id=node_conf["id"],
            node_type=node_conf["type"],
            inputs=node_conf["inputs"]
        )
        node.run(context)

    # 最後のノードの出力を返す
    last_node_id = nodes_config[-1]["id"]
    return context[last_node_id].output
