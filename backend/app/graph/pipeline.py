from langgraph.graph import StateGraph, END

from app.models.state import PipelineState
from app.graph.nodes.preprocess import preprocess
from app.graph.nodes.classify import classify
from app.graph.nodes.evidence import evidence
from app.graph.nodes.score import score
from app.graph.nodes.coach import coach
from app.graph.nodes.compose import compose


def build_pipeline() -> StateGraph:
    graph = StateGraph(PipelineState)

    graph.add_node("preprocess", preprocess)
    graph.add_node("classify", classify)
    graph.add_node("evidence", evidence)
    graph.add_node("score", score)
    graph.add_node("coach", coach)
    graph.add_node("compose", compose)

    graph.set_entry_point("preprocess")
    graph.add_edge("preprocess", "classify")
    graph.add_edge("classify", "evidence")
    graph.add_edge("evidence", "score")
    graph.add_edge("score", "coach")
    graph.add_edge("coach", "compose")
    graph.add_edge("compose", END)

    return graph.compile()


pipeline = build_pipeline()
