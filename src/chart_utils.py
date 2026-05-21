"""Utilitaires de visualisation Plotly pour les résultats de requêtes."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ID_PATTERNS = ("_id", "_numero", "_num", "nom", "prenom", "code_")


def _is_id_col(col_name: str) -> bool:
    """Retourne True si le nom de colonne suggère un identifiant ou un libellé individuel.
    Utilisé pour éviter de générer un graphique non pertinent sur des listes de détail.
    """
    return any(pat in col_name.lower() for pat in ID_PATTERNS)


def _is_year_col(series: pd.Series, col_name: str) -> bool:
    """Détecte une colonne d'année entière (ex: 2022, 2023)."""
    year_keywords = ("annee", "année", "year", "an")
    name_match = any(kw in col_name.lower() for kw in year_keywords)
    if not name_match:
        return False
    if not pd.api.types.is_integer_dtype(series):
        return False
    return series.between(1900, 2100).all()


def try_build_chart(df: pd.DataFrame) -> go.Figure | None:  # pylint: disable=too-many-return-statements,too-many-branches
    """Retourne une Figure Plotly adaptée au DataFrame, ou None si non pertinent."""
    if df is None or df.empty or len(df) < 2:
        return None

    # Colonnes années entières → traitées comme dimensions catégorielles, pas métriques
    year_cols = [c for c in df.columns if _is_year_col(df[c], c)]
    if year_cols:
        df = df.copy()
        df[year_cols[0]] = df[year_cols[0]].astype(str)
        # Court-circuit direct : bar chart catégoriel, on ne passe pas par le branch datetime
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            return None
        fig = px.bar(df, x=year_cols[0], y=numeric_cols[0])
        fig.update_xaxes(type="category")  # ← force catégoriel, stoppe l'interpolation
        fig.update_yaxes(rangemode="tozero")
        return fig

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return None
    y_col = numeric_cols[0]

    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    if not date_cols:
        date_cols = [
            c
            for c in df.select_dtypes(include="object").columns
            if any(
                kw in c.lower() for kw in ("date", "mois", "annee", "année", "period")
            )
        ]
        if date_cols:
            df = df.copy()
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors="coerce")
            df = df.dropna(subset=[date_cols[0]])
            if len(df) < 2:
                return None

    if date_cols:
        x_col = date_cols[0]
        # Série temporelle agrégée = chaque date est unique
        # Liste individuelle = dates dupliquées (une par dossier)
        if df[x_col].nunique() < len(df) * 0.8:
            return None
        fig = px.line(df, x=x_col, y=y_col)
        fig.update_traces(mode="lines+markers")
        fig.update_yaxes(rangemode="tozero")
        return fig

    non_numeric_cols = [c for c in df.columns if c not in numeric_cols]
    if non_numeric_cols:
        x_col = non_numeric_cols[0]
        if df[x_col].nunique() > 20 or _is_id_col(x_col):
            return None
    else:
        df = df.reset_index()
        x_col = df.columns[0]
        if df[x_col].nunique() > 20:
            return None

    fig = px.bar(df, x=x_col, y=y_col)
    fig.update_yaxes(rangemode="tozero")
    return fig
