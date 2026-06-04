"""
Génération augmentée — question + chunks → réponse avec citations
"""

import anthropic
from dotenv import load_dotenv

from src.config import ANTHROPIC_API_KEY, MAX_TOKENS, MODEL
from src.rag.retriever import retrieve

load_dotenv()

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Tu es un assistant expert en assurance prévoyance pour PrevCorp.
Tu réponds aux questions en te basant UNIQUEMENT sur les extraits de documents fournis.
Règles :
- Cite toujours la source entre crochets : [NOM_DU_FICHIER]
- Si la réponse n'est pas dans les extraits, dis explicitement :
  "Je ne trouve pas cette information dans les documents disponibles."
- Sois précis et concis. Pas de remplissage.
- Si plusieurs documents sont pertinents, synthétise en citant chacun."""


def format_context(chunks: list[dict]) -> str:
    """Formate les chunks en bloc de contexte pour le prompt."""
    blocks = []
    for i, chunk in enumerate(chunks, 1):
        blocks.append(
            f"[Extrait {i} — {chunk['source']} | score={chunk['score']}]\n{chunk['text']}"
        )
    return "\n\n---\n\n".join(blocks)


def generate(question: str, top_k: int = 5, doc_type: str | None = None) -> dict:
    """
    Génère une réponse augmentée pour une question.

    Returns:
        dict avec question, answer, sources, chunks
    """
    chunks = retrieve(question, top_k=top_k, doc_type=doc_type)
    context = format_context(chunks)

    user_message = f"""Extraits de documents PrevCorp :

{context}

---

Question : {question}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    answer = response.content[0].text
    sources = list({chunk["source"] for chunk in chunks})

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }


if __name__ == "__main__":
    question = "Quel est le délai de carence pour la garantie ITT ?"
    result = generate(question)
    print(f"Question : {result['question']}")
    print(f"\nRéponse :\n{result['answer']}")
    print(f"\nSources : {result['sources']}")
