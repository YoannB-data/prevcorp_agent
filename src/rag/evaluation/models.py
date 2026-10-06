"""Types partagés du runner d'éval RAG."""

from dataclasses import dataclass, field
from enum import Enum, StrEnum


class Famille(StrEnum):
    """Famille d'un diagnostic, qui décide de l'action à mener."""

    SUCCES = "succès"
    ECHEC = "échec"
    SUSPECT = "suspect"
    ALERTE = "alerte"


class Diagnostic(Enum):
    """Diagnostic d'une question, avec sa famille et la piste de correction."""

    SAIN = (Famille.SUCCES, "sain", "rien")
    BRUIT_TOP_K = (
        Famille.ECHEC,
        "bruit du top-k dégrade la génération",
        "k, reranking, ordre des chunks",
    )
    ECHEC_GENERATION = (
        Famille.ECHEC,
        "échec de génération",
        "vérifier question/scorer, puis prompt/modèle",
    )
    ECHEC_RETRIEVAL = (Famille.ECHEC, "échec de retrieval", "chunking, ingestion, requête")
    DOUBLE_ECHEC = (
        Famille.ECHEC,
        "double échec",
        "vérifier question et scorer (I), puis traiter R et E séparément",
    )
    SUCCES_SANS_SOURCE = (Famille.SUSPECT, "succès sans la source attendue", "audit manuel")
    SUCCES_SANS_SOURCE_ISOLE_KO = (
        Famille.SUSPECT,
        "succès sans la source, isolé KO",
        "audit manuel",
    )
    E2E_OK_ISOLE_KO = (
        Famille.SUSPECT,
        "e2e OK mais contexte idéal KO",
        "audit manuel, scorer ou instabilité",
    )
    ALERTE_CHUNK_TENTANT = (
        Famille.ALERTE,
        "ALERTE : le retrieval a ramené un chunk tentant non anticipé",
        "inspecter les chunks e2e loggés, corriger corpus ou ingestion, "
        "ajouter ce chunk comme nouveau contexte_effectif",
    )
    ECHEC_GENERATION_OU_PIEGE = (
        Famille.ECHEC,
        "échec de génération ou piège mal spécifié",
        "vérifier la spécification du piège, puis prompt/modèle",
    )
    SUSPECT_SANS_REPONSE = (Famille.SUSPECT, "e2e OK mais contexte idéal KO", "audit manuel")
    ERREUR = (Famille.ECHEC, "erreur d'exécution (I/O)", "relancer, exclue des scores")

    @property
    def famille(self) -> Famille:
        """Famille du diagnostic."""

        return self.value[0]

    @property
    def libelle(self) -> str:
        """Libellé lisible du diagnostic."""

        return self.value[1]

    @property
    def correction(self) -> str:
        """Piste de correction associée."""

        return self.value[2]


@dataclass(frozen=True)
class Answer:
    """Réponse générée par le modèle."""

    text: str


@dataclass(frozen=True)
class ScoreResult:
    """Résultat d'un scorer : verdict, besoin de relecture manuelle et détail par point."""

    passed: bool
    needs_review: bool
    details: dict[str, bool] = field(default_factory=dict)
