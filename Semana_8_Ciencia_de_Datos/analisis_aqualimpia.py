
import pandas as pd
import matplotlib.pyplot as plt

# Cargar dataset
df = pd.read_excel("dataset_set_A_aguas_residuales.xlsx")

# Preparar variables
df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])

df["eficiencia_DBO_pct"] = (
    (df["DBO_entrada_mg_L"] - df["DBO_salida_mg_L"])
    / df["DBO_entrada_mg_L"]
) * 100

# Resumen por planta
resumen_planta = df.groupby("planta").agg(
    registros=("planta", "size"),
    caudal_promedio=("caudal_entrada_m3_d", "mean"),
    DBO_entrada_promedio=("DBO_entrada_mg_L", "mean"),
    DBO_salida_promedio=("DBO_salida_mg_L", "mean"),
    eficiencia_DBO_promedio=("eficiencia_DBO_pct", "mean"),
    energia_promedio=("energia_aeracion_kWh", "mean"),
    cumplimiento_promedio=("cumplimiento_norma", "mean")
).round(2)

resumen_planta["cumplimiento_pct"] = (
    resumen_planta["cumplimiento_promedio"] * 100
).round(2)

print("Resumen del desempeño por planta:")
print(resumen_planta)

# Dashboard
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

axes[0, 0].bar(
    resumen_planta.index,
    resumen_planta["DBO_salida_promedio"]
)
axes[0, 0].set_title("DBO de salida promedio por planta")
axes[0, 0].set_ylabel("DBO salida (mg/L)")
axes[0, 0].grid(axis="y", alpha=0.3)

axes[0, 1].bar(
    resumen_planta.index,
    resumen_planta["eficiencia_DBO_promedio"]
)
axes[0, 1].set_title("Eficiencia promedio de remoción de DBO")
axes[0, 1].set_ylabel("Eficiencia (%)")
axes[0, 1].set_ylim(0, 100)
axes[0, 1].grid(axis="y", alpha=0.3)

axes[1, 0].bar(
    resumen_planta.index,
    resumen_planta["cumplimiento_pct"]
)
axes[1, 0].set_title("Cumplimiento normativo por planta")
axes[1, 0].set_ylabel("Cumplimiento (%)")
axes[1, 0].set_ylim(0, 100)
axes[1, 0].grid(axis="y", alpha=0.3)

axes[1, 1].bar(
    resumen_planta.index,
    resumen_planta["energia_promedio"]
)
axes[1, 1].set_title("Consumo promedio de energía de aireación")
axes[1, 1].set_ylabel("Energía (kWh)")
axes[1, 1].grid(axis="y", alpha=0.3)

fig.suptitle(
    "Dashboard exploratorio del desempeño de AquaLimpia S. A.",
    fontsize=16
)

plt.tight_layout()
plt.show()
