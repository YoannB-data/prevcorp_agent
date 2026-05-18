"""Utilitaires de visualisation Plotly pour les résultats de requêtes."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def try_build_chart(df: pd.DataFrame) -> go.Figure | None:
    """Retourne une Figure Plotly adaptée au DataFrame, ou None si non pertinent."""

    if df is None or df.empty or len(df) < 2:
        return None

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return None

    y_col = numeric_cols[0]

    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    if not date_cols:
        # Tentative de détection sur colonnes object dont le nom évoque une date
        date_cols = [
            c for c in df.select_dtypes(include="object").columns
            if any(kw in c.lower() for kw in ("date", "mois", "annee", "année", "period"))
        ]
        if date_cols:
            df = df.copy()
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors="coerce")
            df = df.dropna(subset=[date_cols[0]])
            if len(df) < 2:
                return None

    if date_cols:
        x_col = date_cols[0]
        return px.line(df, x=x_col, y=y_col)

    non_numeric_cols = [c for c in df.columns if c not in numeric_cols]
    if non_numeric_cols:
        x_col = non_numeric_cols[0]
    else:
        df = df.reset_index()
        x_col = df.columns[0]

    return px.bar(df, x=x_col, y=y_col)
