
import pandas as pd
import numpy as np

def calcular_eficiencia_dbo(dbo_entrada, dbo_salida):
    """
    Calcula el porcentaje de eficiencia de remoción de DBO.
    """
    return ((dbo_entrada - dbo_salida) / dbo_entrada) * 100


def resumen_por_planta(df):
    """
    Genera un resumen de los principales indicadores por planta.
    """
    datos = df.copy()

    datos["eficiencia_DBO_pct"] = calcular_eficiencia_dbo(
        datos["DBO_entrada_mg_L"],
        datos["DBO_salida_mg_L"]
    )

    resumen = datos.groupby("planta").agg(
        registros=("planta", "size"),
        DBO_salida_promedio=("DBO_salida_mg_L", "mean"),
        eficiencia_DBO_promedio=("eficiencia_DBO_pct", "mean"),
        energia_promedio=("energia_aeracion_kWh", "mean"),
        cumplimiento_promedio=("cumplimiento_norma", "mean")
    ).round(2)

    resumen["cumplimiento_pct"] = (
        resumen["cumplimiento_promedio"] * 100
    ).round(2)

    return resumen


def obtener_indicadores_generales(df):
    """
    Obtiene indicadores generales utilizando NumPy.
    """
    return {
        "registros": len(df),
        "DBO_salida_media": round(np.mean(df["DBO_salida_mg_L"]), 2),
        "energia_media": round(np.mean(df["energia_aeracion_kWh"]), 2)
    }
