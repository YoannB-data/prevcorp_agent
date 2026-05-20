"""Orchestration du pipeline question → SQL → résultat via l'API Claude"""

import re
import time
from pathlib import Path

import anthropic
import pandas as pd

from src import config
from src.duckdb_executor import execute_query
from src.few_shot_selector import format_few_shot, select_examples
from src.logger import log_interaction
from src.schema_loader import load_schema

_MAX_RETRIES = 3


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


def _call_llm_with_retry(system_prompt, message, max_retries) -> tuple[str, int, int]:
    """Envoie un message à l'API Anthropic avec retry sur erreurs transitoires."""

    if max_retries < 1:
        raise ValueError("max_retries doit être >= 1")

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=config.MODEL,
                max_tokens=config.MAX_TOKENS,
                temperature=0,
                system=system_prompt,
                messages=[{"role": "user", "content": message}],
            )
            return (
                response.content[0].text,
                response.usage.input_tokens,
                response.usage.output_tokens,
            )
        except anthropic.AuthenticationError:
            raise  # clé invalide : pas transitoire, retry inutile
        except (
            anthropic.RateLimitError,
            anthropic.APITimeoutError,
            anthropic.APIConnectionError,
            anthropic.APIStatusError,
        ) as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(2**attempt)
    raise last_error


def _extract_sql(text) -> str:
    """Extrait le bloc SQL d'une réponse Markdown de l'API"""

    match = re.search(r"```sql\n(.*?)```", text, re.DOTALL)
    if not match:
        raise ValueError(f"Pas de SQL trouvé dans la réponse : {text}")

    return match.group(1).strip()


def agent_main(
    question: str, eval_question_id: str | None = None
) -> tuple[str, pd.DataFrame]:
    """Traduit une question métier en DataFrame via génération et exécution de SQL"""

    schema_str = _format_schema(load_schema())
    few_shot_str = format_few_shot(select_examples(question))

    with open(
        Path(__file__).parent / "prompts" / "system_prompt.md", encoding="utf-8"
    ) as f:
        system_prompt = f.read()

    message_to_llm = f"""
        {few_shot_str}
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
    df: pd.DataFrame | None = None

    try:
        for attempt in range(_MAX_RETRIES):
            text, input_tokens, output_tokens = _call_llm_with_retry(
                system_prompt, message_to_llm, _MAX_RETRIES
            )
            sql_generated = _extract_sql(text)
            # print(f"[debug] SQL généré : {sql_generated}")
            try:
                df = execute_query(sql_generated)
                break
            except Exception as e:  # pylint: disable=broad-exception-caught
                if attempt == _MAX_RETRIES - 1:
                    raise
                message_to_llm += (
                    f"\n\nErreur SQL à corriger : {e}\nSQL tenté : {sql_generated}"
                )

        log_interaction(
            question=question,
            sql_generated=sql_generated,
            status="success",
            latency_ms=int((time.perf_counter() - start) * 1000),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=(input_tokens * config.COST_PER_INPUT_TOKEN)
            + (output_tokens * config.COST_PER_OUTPUT_TOKEN),
            eval_question_id=eval_question_id,
        )
        return sql_generated, df

    except Exception as e:  # pylint: disable=broad-exception-caught
        # Catch-all - loggue avant de re-lever pour persister l'erreur quelle que soit son origine
        log_interaction(
            question=question,
            sql_generated=sql_generated,
            status="error",
            latency_ms=int((time.perf_counter() - start) * 1000),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=(input_tokens * config.COST_PER_INPUT_TOKEN)
            + (output_tokens * config.COST_PER_OUTPUT_TOKEN),
            error_message=str(e),
            eval_question_id=eval_question_id,
        )
        raise
