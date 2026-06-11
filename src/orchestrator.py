"""Point d'entrée unique : route et délègue à sql_agent ou rag.generator."""

from __future__ import annotations

from typing import Literal

import pandas as pd
from pydantic import BaseModel

from src.rag.generator import generate
from src.router import route
from src.structured.sql_agent import agent_main


class OrchestratorResult(BaseModel):
    """Résultat unifié des deux pipelines SQL et RAG."""

    route: Literal["sql", "rag"]
    question: str
    # SQL branch
    sql_generated: str | None = None
    df: pd.DataFrame | None = None
    # RAG branch
    answer: str | None = None
    sources: list[str] | None = None
    chunks: list[dict] | None = None

    # pd.DataFrame n'est pas un type Pydantic natif
    model_config = {"arbitrary_types_allowed": True}


def orchestrator_main(question: str) -> OrchestratorResult:
    """Route la question et retourne un OrchestratorResult unifié."""

    pipeline = route(question)

    if pipeline == "sql":
        sql, df = agent_main(question)
        return OrchestratorResult(
            route="sql",
            question=question,
            sql_generated=sql,
            df=df,
        )

    rag_result = generate(question)
    return OrchestratorResult(
        route="rag",
        question=question,
        answer=rag_result["answer"],
        sources=rag_result["sources"],
        chunks=rag_result["chunks"],
    )
