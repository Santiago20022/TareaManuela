#!/usr/bin/env python3
"""
Genera el reporte PDF del EDA Titanic.
"""
import os
from fpdf import FPDF

class ReportePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "ET0203 - Seminario de la Ciencia de los Datos | Unidad 1 - EDA Kaggle", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Palacio Manuela - 1023774044 | Pagina {self.page_no()}/{{nb}}", align="C")

    def titulo_seccion(self, num, titulo):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(25, 60, 120)
        self.ln(4)
        self.cell(0, 8, f"{num}. {titulo}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(25, 60, 120)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def subtitulo(self, texto):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(50, 50, 50)
        self.cell(0, 6, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def parrafo(self, texto):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, texto)
        self.ln(2)

    def bullet(self, texto):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(6, 5, "-")
        self.multi_cell(0, 5, texto)
        self.ln(1)

    def insertar_figura(self, path, ancho=170, caption=""):
        if os.path.exists(path):
            self.image(path, x=20, w=ancho)
            if caption:
                self.set_font("Helvetica", "I", 8)
                self.set_text_color(100, 100, 100)
                self.cell(0, 5, caption, align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(3)


def main():
    pdf = ReportePDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    fig_dir = "exports/figuras"

    # === PORTADA ===
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(25, 60, 120)
    pdf.cell(0, 12, "Analisis Exploratorio de Datos (EDA)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, "Dataset: Titanic - Machine Learning from Disaster", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    info = [
        ("Estudiante", "Palacio Manuela"),
        ("Codigo", "1023774044"),
        ("Curso", "ET0203 - Seminario de la Ciencia de los Datos"),
        ("Docente", "MSc. Luis Esteban Gomez Cadavid"),
        ("Programa", "Ingenieria de Software - Pascual Bravo"),
        ("Periodo", "2026-1"),
        ("Fecha", "2026-02-26"),
        ("Fuente", "https://www.kaggle.com/competitions/titanic"),
    ]
    for label, val in info:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(40, 7, f"{label}:", align="R")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, f"  {val}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, "Herramientas: pandas, numpy, matplotlib, seaborn, scipy, scikit-learn, statsmodels, missingno", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Semilla: random_state=42 | Python 3.10", align="C", new_x="LMARGIN", new_y="NEXT")

    # === 1. RESUMEN EJECUTIVO ===
    pdf.add_page()
    pdf.titulo_seccion("1", "Resumen ejecutivo")
    pdf.parrafo(
        "Este reporte presenta el Analisis Exploratorio de Datos (EDA) del dataset Titanic de Kaggle, "
        "que contiene informacion de 891 pasajeros del RMS Titanic. El objetivo es demostrar dominio "
        "de preparacion de datos, estadistica descriptiva e inferencial, y visualizaciones."
    )
    bullets_resumen = [
        "Dataset: Titanic - Machine Learning from Disaster (Kaggle). 891 pasajeros, 12 variables.",
        "Unidad de observacion: cada fila es un pasajero con sus caracteristicas demograficas y de viaje.",
        "Variables criticas: Sex (genero), Pclass (clase socioeconomica), Age (edad) y Fare (tarifa).",
        "Calidad: Cabin tiene 77.1% de faltantes. Age tiene 19.87% faltante. 15 registros con Fare=0. Sin duplicados.",
        "Hallazgo principal: solo 38.4% sobrevivio. Las mujeres sobrevivieron 74.2% vs 18.9% de hombres. La 1ra clase tuvo 63% de supervivencia vs 24.2% en 3ra clase.",
        "Relaciones: Pclass-Fare correlacion fuerte (-0.55). Sex-Survived asociacion fuerte (Cramer's V=0.54). Mujeres de 1ra clase: 96.8% de supervivencia.",
        "Outliers: Fare tiene 116 outliers por IQR, pero son casos validos (suites de lujo). No se eliminan.",
        "Tratamiento: Winsorizacion y log1p reducen la asimetria de Fare de 4.79 a valores cercanos a 0.",
        "Inferencia: todas las pruebas significativas (alpha=0.05): t-test (Fare por supervivencia), ANOVA (Age por clase), chi-cuadrado (Sex vs Survived).",
        "Limitaciones: muestra parcial (891 de 2224), Cabin inutilizable, Age faltante en 20%.",
    ]
    for b in bullets_resumen:
        pdf.bullet(b)

    # === 2. AUDITORIA DE CALIDAD ===
    pdf.titulo_seccion("2", "Auditoria de calidad")

    pdf.subtitulo("2.1 Valores faltantes")
    pdf.parrafo(
        "Se identificaron tres variables con valores faltantes: Cabin (687 faltantes, 77.1%), "
        "Age (177 faltantes, 19.87%) y Embarked (2 faltantes, 0.22%). Las demas variables estan completas."
    )
    pdf.parrafo(
        "Decision: Cabin tiene demasiados faltantes para usarse directamente; se puede crear un indicador "
        "binario (tiene_cabina). Embarked se imputa con la moda ('S' - Southampton). Age se analiza con "
        "los 714 valores disponibles."
    )

    pdf.subtitulo("2.2 Duplicados")
    pdf.parrafo("No se encontraron filas duplicadas (0 de 891).")

    pdf.subtitulo("2.3 Rangos y tipos")
    pdf.parrafo(
        "Los tipos de datos son correctos. Se verificaron rangos: Age (0.42-80, razonable), "
        "Fare (0-512.33, con 15 valores en 0 que podrian ser tripulacion o errores). "
        "Survived y Pclass son numericos pero representan categorias (binaria y ordinal respectivamente)."
    )

    pdf.subtitulo("2.4 Cardinalidad")
    pdf.parrafo(
        "Sex: 2 valores (male=577, female=314). Embarked: 3 valores (S=644, C=168, Q=77). "
        "Cabin: 147 valores unicos (alta cardinalidad). Ticket: 681 valores unicos. "
        "No se detectaron typos en las categoricas."
    )

    # Figura: matriz faltantes
    # No tenemos esta exportada, pero incluimos la de calidad general

    # === 3. DESCRIPTIVO + VISUALIZACIONES ===
    pdf.add_page()
    pdf.titulo_seccion("3", "Estadistica descriptiva y visualizaciones")

    pdf.subtitulo("3.1 Variables numericas")
    pdf.parrafo(
        "Age: media 29.7, mediana 28, distribucion ligeramente sesgada a la derecha (skew=0.39). "
        "Fare: media 32.20, mediana 14.45, fuertemente asimetrica (skew=4.79, kurtosis=33.40), "
        "con coeficiente de variacion del 154%. "
        "SibSp y Parch: mayoria viajaba solo (mediana=0), distribucion muy sesgada."
    )

    pdf.subtitulo("3.2 Variables categoricas")
    pdf.parrafo(
        "Survived: 549 muertos (61.6%) vs 342 sobrevivientes (38.4%). "
        "Sex: 577 hombres (64.8%) vs 314 mujeres (35.2%). "
        "Pclass: 3ra clase=491 (55.1%), 1ra=216 (24.2%), 2da=184 (20.7%). "
        "Embarked: Southampton=644 (72.3%), Cherbourg=168 (18.9%), Queenstown=77 (8.6%)."
    )

    pdf.subtitulo("3.3 Analisis por grupos")
    pdf.parrafo(
        "Se realizaron agrupaciones por Sex, Pclass, Embarked, Survived, Sex x Pclass (cruzado), "
        "y grupo de edad (cuartiles con pd.qcut). Hallazgos principales:"
    )
    pdf.bullet("Mujeres: tasa de supervivencia 74.2% vs 18.9% hombres.")
    pdf.bullet("1ra clase: 63.0%, 2da: 47.3%, 3ra: 24.2%.")
    pdf.bullet("Cherbourg tuvo mayor tasa (55.4%), por mayor proporcion de 1ra clase.")
    pdf.bullet("Mujeres de 1ra clase: 96.8% de supervivencia. Hombres de 3ra: 13.5%.")
    pdf.bullet("Jovenes (0-20) tuvieron mayor supervivencia (44.4%), por inclusion de ninos.")

    pdf.subtitulo("3.4 Visualizaciones principales")
    pdf.parrafo(
        "Se generaron 23 graficos en total, incluyendo: histogramas+KDE (3), ECDF (2), "
        "boxplots (3), violin plots (3), scatter plots (3), pairplot, heatmap de correlacion, "
        "jointplot hexbin, FacetGrid, countplots de supervivencia, heatmap de supervivencia, "
        "QQ-plots, y graficos de tratamiento de outliers."
    )

    # Insertar algunas figuras clave
    pdf.insertar_figura(f"{fig_dir}/countplot_supervivencia.png", 160,
                        "Figura 1: Supervivencia por Sexo, Clase y Puerto de embarque")

    pdf.add_page()
    pdf.insertar_figura(f"{fig_dir}/heatmap_correlacion.png", 130,
                        "Figura 2: Heatmap de correlacion de Pearson entre variables numericas")

    pdf.insertar_figura(f"{fig_dir}/heatmap_supervivencia_sex_pclass.png", 120,
                        "Figura 3: Tasa de supervivencia cruzada Sex x Pclass")

    # === 4. OUTLIERS ===
    pdf.add_page()
    pdf.titulo_seccion("4", "Deteccion y tratamiento de outliers")

    pdf.subtitulo("4.1 Deteccion univariada")
    pdf.parrafo(
        "Se aplicaron 4 metodos univariados a las variables Age, Fare, SibSp y Parch:"
    )
    pdf.bullet("IQR 1.5x: Fare=116 outliers, SibSp=46, Parch=213, Age=11.")
    pdf.bullet("IQR 3.0x: Fare=53, SibSp=12, Parch=30, Age=1.")
    pdf.bullet("Z-score >3: Fare=20, SibSp=6, Parch=4, Age=1.")
    pdf.bullet("Modified Z-score (MAD) >3.5: Fare=116, SibSp=46, Age=6, Parch=0 (MAD=0).")
    pdf.parrafo(
        "Fare es la variable con mas outliers. Los valores extremos (>300 libras) corresponden "
        "a pasajeros de 1ra clase en suites de lujo: son casos raros validos, no errores. "
        "SibSp/Parch tienen outliers por familias grandes (eventos reales)."
    )

    pdf.subtitulo("4.2 Deteccion multivariada")
    pdf.parrafo(
        "Se aplicaron 3 algoritmos multivariados sobre las variables transformadas con Yeo-Johnson: "
        "DBSCAN (ruido), Isolation Forest (300 arboles), y LOF (25 vecinos). "
        "Se uso un sistema de votacion: los outliers consensuados (detectados por 2+ metodos) "
        "corresponden principalmente a pasajeros con familias muy grandes y tarifas extremas."
    )
    pdf.parrafo(
        "Decision: no se eliminan outliers porque representan eventos reales del naufragio. "
        "Para modelado se recomienda winsorizar Fare y transformar con log."
    )

    pdf.subtitulo("4.3 Tratamiento (antes vs. despues)")
    pdf.parrafo(
        "Se aplico tratamiento a Fare (variable con mayor asimetria, skew=4.79):"
    )
    pdf.bullet("Winsorizacion al 1%: reduce skewness moderadamente, preserva escala original.")
    pdf.bullet("log1p: reduce drasticamente el skewness, acercando a normalidad. Mejor balance normalizacion-interpretabilidad.")
    pdf.bullet("Yeo-Johnson: mejor simetria (skew cercano a 0), pero pierde interpretabilidad.")

    pdf.insertar_figura(f"{fig_dir}/tratamiento_comparacion_Fare.png", 160,
                        "Figura 4: Comparacion de tratamientos aplicados a Fare")

    pdf.insertar_figura(f"{fig_dir}/boxplot_tratamiento_Fare.png", 160,
                        "Figura 5: Boxplots antes vs. despues del tratamiento de Fare")

    # === 5. INFERENCIA ===
    pdf.add_page()
    pdf.titulo_seccion("5", "Inferencia estadistica")
    pdf.parrafo("Todas las pruebas se realizaron con nivel de significancia alpha = 0.05.")

    pdf.subtitulo("5.1 Normalidad - Shapiro-Wilk")
    pdf.parrafo(
        "H0: la variable sigue una distribucion normal. H1: no es normal.\n"
        "Age: W=0.9815, p=7.34e-08. Conclusion: rechazamos H0, Age no es normal.\n"
        "Fare: W=0.5219, p=1.08e-43. Conclusion: rechazamos H0, Fare no es normal.\n"
        "Esto justifica usar pruebas robustas como Welch t-test y pruebas no parametricas."
    )

    pdf.subtitulo("5.2 t-test de Welch - Fare por Survived")
    pdf.parrafo(
        "H0: no hay diferencia en Fare entre sobrevivientes y no sobrevivientes.\n"
        "H1: hay diferencia significativa.\n"
        "Sobrevivientes: media=48.40. No sobrevivientes: media=22.12.\n"
        "Resultado: t=6.84, p=2.70e-11. Conclusion: rechazamos H0.\n"
        "Los sobrevivientes pagaron tarifas significativamente mas altas, porque la clase alta "
        "tenia prioridad en los botes salvavidas."
    )

    pdf.subtitulo("5.3 ANOVA - Age por Pclass (3 grupos)")
    pdf.parrafo(
        "H0: la edad media es igual en las 3 clases (mu1 = mu2 = mu3).\n"
        "H1: al menos una clase tiene edad media diferente.\n"
        "Clase 1: media=38.23. Clase 2: media=29.88. Clase 3: media=25.14.\n"
        "Resultado: p=7.49e-24. Conclusion: rechazamos H0.\n"
        "Los pasajeros de 1ra clase eran mayores en promedio, consistente con mayor poder adquisitivo."
    )

    pdf.subtitulo("5.4 Correlacion Pearson/Spearman - Age vs Fare")
    pdf.parrafo(
        "H0: no hay correlacion (rho = 0). H1: existe correlacion (rho != 0).\n"
        "Pearson: r=0.096, p=0.010. Spearman: rho=0.135, p=0.0003.\n"
        "Conclusion: correlacion debil pero significativa. La tarifa depende mas de la clase que de la edad."
    )

    pdf.subtitulo("5.5 Chi-cuadrado - Sex vs Survived (adicional)")
    pdf.parrafo(
        "H0: Sex y Survived son independientes. H1: existe asociacion.\n"
        "chi2=260.72, p=1.20e-58, Cramer's V=0.54 (asociacion fuerte).\n"
        "Conclusion: rechazamos H0. El sexo esta fuertemente asociado con la supervivencia, "
        "confirmando la politica de 'mujeres y ninos primero'."
    )

    pdf.insertar_figura(f"{fig_dir}/qqplot_age_fare.png", 155,
                        "Figura 6: QQ-Plots de Age y Fare vs. distribucion normal teorica")

    # === 6. LIMITACIONES Y REPRODUCIBILIDAD ===
    pdf.titulo_seccion("6", "Limitaciones y reproducibilidad")

    pdf.subtitulo("6.1 Limitaciones")
    pdf.bullet("Muestra parcial: solo 891 de 2224 pasajeros (no incluye tripulacion completa).")
    pdf.bullet("Cabin tiene 77.1% de faltantes, lo que impide analizar ubicacion en el barco.")
    pdf.bullet("Age faltante en 19.87% puede sesgar analisis relacionados con edad.")
    pdf.bullet("No se dispone de informacion sobre ubicacion al momento del impacto ni orden de evacuacion.")
    pdf.bullet("Fare=0 en 15 registros podria ser error de registro o tripulacion sin pago.")

    pdf.subtitulo("6.2 Reproducibilidad")
    pdf.bullet("Python >= 3.10 con pandas, numpy, matplotlib, seaborn, scipy, scikit-learn, statsmodels, missingno.")
    pdf.bullet("Semilla fija: random_state=42 en todos los muestreos y algoritmos.")
    pdf.bullet("Ruta de datos: data/train.csv (891 filas x 12 columnas).")
    pdf.bullet("Exportables: exports/tabla_resumen.csv, exports/tests.json, exports/figuras/ (23 PNG).")
    pdf.bullet("Notebook reproducible: Kernel -> Restart & Run All ejecuta sin errores.")

    # Guardar
    out_path = "ET0203_U1_Reporte_1023774044_Palacio.pdf"
    pdf.output(out_path)
    print(f"Reporte generado: {out_path}")
    print(f"Paginas: {pdf.pages_count}")


if __name__ == "__main__":
    main()
