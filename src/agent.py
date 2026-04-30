"""Orchestration du pipeline question → SQL → résultat via l'API Claude"""
import re
from pathlib import Path

import anthropic
import pandas as pd

from src import config
from src.duckdb_executor import execute_query
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


def _call_llm(system_prompt, message) -> str:
    """Envoie un message à l'API Anthropic et retourne le texte de la réponse"""
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    response = client.messages.create(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": message}],
    )

    return response.content[0].text


def _extract_sql(text) -> str:
    """Extrait le bloc SQL d'une réponse Markdown de l'API"""
    match = re.search(r"```sql\n(.*?)```", text, re.DOTALL)
    if not match:
        raise ValueError(f"Pas de SQL trouvé dans la réponse : {text}")

    return match.group(1).strip()


def agent_main(question: str) -> pd.DataFrame:
    """Traduit une question métier en DataFrame via génération et exécution de SQL"""
    schema = load_schema()
    schema_str = _format_schema(schema)

    with open(Path(__file__).parent / "prompts" / "system_prompt.md", encoding="utf-8") as f:
        system_prompt = f.read()

    message_to_llm = f"""
        # Question du métier :
        {question}
        # Dataset de l'entreprise :
        {schema_str}
        """

    text = _call_llm(system_prompt, message_to_llm)

    sql_bloc = _extract_sql(text)

    df = execute_query(sql_bloc)

    return df
