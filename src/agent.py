"""Orchestration du pipeline question → SQL → résultat via l'API Claude"""

import re
import time
from pathlib import Path

import anthropic
import pandas as pd

from src import config
from src.duckdb_executor import execute_query
from src.logger import log_interaction
from src.schema_loader import load_schema


def _format_schema(schema: dict) -> str:
    """Formate le schéma en texte lisible pour injection dans le prompt"""

    lines = []
    for table_name, table_info in schema.items():
        lines.append(f"Table : {table_name}")
        lines.append(f"Description : {table_info['description']}")
        lines.append("Colonnes :")
        for col_name, col_desc in table_info["columns"].items():
            lines.append(f"  - {col_name} : {col_desc}")
        lines.append("")
    return "\n".join(lines)


def _call_llm(system_prompt, message) -> tuple[str, int, int]:
    """Envoie un message à l'API Anthropic et retourne le texte + tokens consommés"""

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": message}],
    )
    return (
        response.content[0].text,
        response.usage.input_tokens,
        response.usage.output_tokens,
    )


def _extract_sql(text) -> str:
    """Extrait le bloc SQL d'une réponse Markdown de l'API"""

    match = re.search(r"```sql\n(.*?)```", text, re.DOTALL)
    if not match:
        raise ValueError(f"Pas de SQL trouvé dans la réponse : {text}")

    return match.group(1).strip()


def agent_main(question: str, eval_question_id: str | None = None) -> tuple[str, pd.DataFrame]:
    """Traduit une question métier en DataFrame via génération et exécution de SQL"""

    schema = load_schema()
    schema_str = _format_schema(schema)

    with open(
        Path(__file__).parent / "prompts" / "system_prompt.md", encoding="utf-8"
    ) as f:
        system_prompt = f.read()

    message_to_llm = f"""
        # Question du métier :
        {question}
        # Dataset de l'entreprise :
        {schema_str}
        """

    start = time.perf_counter()
    # Initialisés ici pour rester accessibles dans le except si _call_llm échoue avant de les setter
    sql_generated = None
    input_tokens = 0
    output_tokens = 0

    try:
        text, input_tokens, output_tokens = _call_llm(system_prompt, message_to_llm)
        sql_generated = _extract_sql(text)
        df = execute_query(sql_generated)
        log_interaction(
            question=question,
            sql_generated=sql_generated,
            status="success",
            latency_ms=int((time.perf_counter() - start) * 1000),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            eval_question_id=eval_question_id,
        )
        return sql_generated, df

    except Exception as exc:
        # Catch-all - loggue avant de re-lever pour persister l'erreur quelle que soit son origine
        log_interaction(
            question=question,
            sql_generated=sql_generated,
            status="error",
            latency_ms=int((time.perf_counter() - start) * 1000),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            error_message=str(exc),
            eval_question_id=eval_question_id,
        )
        raise
