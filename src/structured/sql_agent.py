"""Orchestration du pipeline question → SQL → résultat via l'API Claude"""

import re
import time
from pathlib import Path
from typing import NamedTuple

import anthropic
import pandas as pd

from src import config
from src.llm import extract_text, extract_thinking_tokens
from src.logger import log_interaction
from src.structured.duckdb_executor import execute_query
from src.structured.few_shot_selector import format_few_shot, select_examples
from src.structured.schema_loader import load_metrics, load_schema


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


def _format_metrics(metrics: dict) -> str:
    """Formate les métriques en texte lisible pour injection dans le prompt"""

    lines = []
    for name, info in metrics.items():
        lines.append(f"Métrique : {name}")
        lines.append(f"Label : {info['label']}")
        if info.get("description"):
            lines.append(f"Description : {info['description']}")
        lines.append(f"Type : {info['type']}")
        lines.append(f"Mesure : {info['measure']}")
        lines.append("")
    return "\n".join(lines)


class _LLMCall(NamedTuple):
    """Texte et métriques d'un appel réussi ; thinking_tokens est inclus dans output_tokens."""

    text: str
    input_tokens: int
    output_tokens: int
    thinking_tokens: int
    stop_reason: str | None


def _call_llm_with_retry(system_prompt: str, message: str, max_retries: int) -> _LLMCall:
    """Envoie un message à l'API Anthropic avec retry sur erreurs transitoires."""

    if max_retries < 1:
        raise ValueError("max_retries doit être >= 1")

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=config.AGENT_MODEL,
                **config.agent_call_kwargs(temperature=0),
                system=system_prompt,
                messages=[{"role": "user", "content": message}],
            )
            return _LLMCall(
                text=extract_text(response),
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                thinking_tokens=extract_thinking_tokens(response),
                stop_reason=response.stop_reason,
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


def _extract_sql(text: str) -> str:
    """Extrait le bloc SQL d'une réponse Markdown de l'API"""

    match = re.search(r"```sql\n(.*?)```", text, re.DOTALL)
    if not match:
        raise ValueError(f"Pas de SQL trouvé dans la réponse : {text}")

    return match.group(1).strip()


_MAX_RETRIES = 3
_SCHEMA = _format_schema(load_schema())
_METRICS = _format_metrics(load_metrics())
_SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "system_prompt.md").read_text(
    encoding="utf-8"
)


def _build_message_to_llm(question: str) -> str:
    """Construit le message utilisateur à envoyer à l'API."""

    few_shot_str = format_few_shot(select_examples(question))
    return f"""
        {few_shot_str}
        # Question du métier :
        {question}
        # Dataset de l'entreprise :
        {_SCHEMA}
        # Semantic layer :
        {_METRICS}
        """


def agent_main(question: str, eval_question_id: str | None = None) -> tuple[str, pd.DataFrame]:
    """Traduit une question métier en DataFrame via génération et exécution de SQL"""

    message_to_llm = _build_message_to_llm(question)
    start = time.perf_counter()
    # Initialisés ici pour rester accessibles dans le except si _call_llm échoue avant de les setter
    sql_generated = None
    input_tokens = 0
    output_tokens = 0
    thinking_tokens = 0
    stop_reason: str | None = None
    df: pd.DataFrame | None = None

    try:
        for attempt in range(_MAX_RETRIES):
            call = _call_llm_with_retry(_SYSTEM_PROMPT, message_to_llm, _MAX_RETRIES)
            input_tokens, output_tokens = call.input_tokens, call.output_tokens
            thinking_tokens, stop_reason = call.thinking_tokens, call.stop_reason
            sql_generated = _extract_sql(call.text)
            # print(f"[debug] SQL généré : {sql_generated}")
            try:
                df = execute_query(sql_generated)
                break
            except Exception as e:
                if attempt == _MAX_RETRIES - 1:
                    raise
                message_to_llm += f"\n\nErreur SQL à corriger : {e}\nSQL tenté : {sql_generated}"

        log_interaction(
            question=question,
            sql_generated=sql_generated,
            status="success",
            latency_ms=int((time.perf_counter() - start) * 1000),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            thinking_tokens=thinking_tokens,
            stop_reason=stop_reason,
            cost_usd=config.compute_cost(config.AGENT_MODEL, input_tokens, output_tokens),
            eval_question_id=eval_question_id,
        )
        assert sql_generated is not None and df is not None
        return sql_generated, df

    except Exception as e:
        # Catch-all - loggue avant de re-lever pour persister l'erreur quelle que soit son origine
        log_interaction(
            question=question,
            sql_generated=sql_generated,
            status="error",
            latency_ms=int((time.perf_counter() - start) * 1000),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            thinking_tokens=thinking_tokens,
            stop_reason=stop_reason,
            cost_usd=config.compute_cost(config.AGENT_MODEL, input_tokens, output_tokens),
            error_message=str(e),
            eval_question_id=eval_question_id,
        )
        raise
