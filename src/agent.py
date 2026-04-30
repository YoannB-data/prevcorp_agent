import pandas as pd
from pathlib import Path
import anthropic
import re

from src.schema_loader import load_schema
from src.duckdb_executor import execute_query
from src import config

def _format_schema(schema: dict) -> str:
    """Return the schema as a formatted string."""
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
    """ Call Antropic API """
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

    response = client.messages.create(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        system=system_prompt,
        messages=[
            {"role": "user", "content": message}
        ]
    )

    return response.content[0].text

def _extract_sql(text) -> str:
    """ Extract SQL from API's response """
    match = re.search(r"```sql\n(.*?)```", text, re.DOTALL)
    if not match:
        raise ValueError(f"Pas de SQL trouvé dans la réponse : {text}")

    return match.group(1).strip()

def agent_main(question: str) -> pd.DataFrame:
    """ Main agent's fonction """
    schema=load_schema()
    schema_str=_format_schema(schema)
    
    with open(Path(__file__).parent / "prompts" / "system_prompt.md") as f:
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