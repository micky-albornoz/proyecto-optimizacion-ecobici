# 🚲 Proyecto de optimización de flota de Ecobici de la Ciudad de Buenos Aires 

## 📝 Descipción general del proyecto

Este proyecto analiza los datos históricos de viajes del sistema público de bicicletas Ecobici de la Ciudad de Buenos Aires para desarrollar un modelo de optimización de la flota.\
**Ecobici** es un excelente sistema público y gratuito de bicicletas compartidas de la Ciudad de Buenos Aires, gestionado por el Gobierno de la Ciudad de Buenos Aires, y actualmente operado por la empresa Tembici.\
El objetivo de este proyecto es identificar patrones de uso, diagnosticar estaciones con desequilibrios crónicos y proponer un **plan de rebalanceo operativo y por hora** para mejorar la calidad del servicio.


### [Ver el informe interactivo en Tableau Public](https://public.tableau.com/views/ProyectoparalaoptimizacindelserviciodeEcobici/Puntosdehistoria?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

---

## 🛠️ Stack tecnológico

* **Lenguaje de programación:** Python
* **Base de datos:** PostgreSQL
* **Análisis y visualización:** Tableau
* **Librerías Python:** Pandas, Psycopg2, python-dotenv
* **Control de versiones:** Git & GitHub

---

## 📈 Metodología

El proyecto se desarrolló siguiendo un flujo de trabajo analítico completo, desde el tratamiento de los datos hasta la comunicación de insights.

1.  **ETL y Modelado de datos:** Se desarrolló un script en Python para realizar la extracción, transformación y carga (ETL) de los datos. Se leyeron múltiples archivos CSV, se limpiaron y se estructuraron en un **esquema de estrella** (dim_stations, fact_trips) cargado en una base de datos PostgreSQL.

2.  **Preparación Avanzada de Datos en Tableau:** Para poder analizar salidas y llegadas de forma simultánea, se utilizó una técnica de **Unión de datos (Union)** dentro de Tableau. Esto permitió reestructurar el set de datos para tratar cada viaje como dos eventos distintos (una salida y una llegada), sentando las bases para un análisis de flujo preciso.

3.  **Ingeniería de métricas:** Se crearon campos calculados avanzados para transformar los datos crudos en insights accionables:
    * **Flujo neto diario promedio:** En lugar de analizar totales anuales, se calculó el patrón de flujo neto promedio para cada hora de cada día de la semana. Esto permite identificar tendencias operativas realistas y comparables.
    * **Acción sugerida:** Se diseñó un **modelo de segmentación estratégica** con umbrales personalizados. Este modelo clasifica cada estación en "Déficit Crítico", "Superávit Probable (Donante)" o "Equilibrado", permitiendo al equipo de operaciones priorizar sus recursos de manera eficiente.

4.  **Análisis de patrones y visualización interactiva:** Se construyeron tres dashboards interconectados para explorar los datos:
    * **Dashboard 1 (Pulso del sistema):** Ofrece una vista macro de la actividad de la red e identifica las estaciones y horas de mayor demanda.
    * **Dashboard 2 (Salud de las estaciones):** Permite un análisis profundo de los patrones de flujo diario para cualquier estación individual, diferenciando el comportamiento entre días laborales y fines de semana.
    * **Dashboard 3 (Plan de rebalanceo):** Es un simulador operativo que, a través de parámetros de hora y día, muestra en un mapa y una tabla las acciones de rebalanceo sugeridas en toda la ciudad.

5.  **Narrativa de datos (Data storytelling):** Finalmente, se consolidaron los hallazgos en una **Puntos de historia de Tableau**. Esta narrativa guía al usuario a través del análisis, desde la identificación del problema general hasta la propuesta de una solución específica y justificada, demostrando el ciclo completo del análisis de datos.

---

## 📊 Vistas previas de los dashboards

**Dashboard 1: Pulso del sistema**
![Dashboard 1 Pulso del sistema](https://github.com/micky-albornoz/proyecto-optimizacion-ecobici/blob/main/images/dashboard-1-pulso-sistema.png)

**Dashboard 3: Plan de rebalanceo**
![Dashboard 3 Plan de rebalanceo](https://github.com/micky-albornoz/proyecto-optimizacion-ecobici/blob/main/images/dashboard-3-plan-rebalanceo.png)

---

## 🚀 Conclusiones y próximos pasos

El análisis revela patrones de movilidad claros y predecibles que podrían causar desequilibrios sistémicos en la flota de Ecobici. El modelo propuesto no sólo diagnostica estos problemas, sino que ofrece **recomendaciones tácticas y por hora** que permiten a un gestor de operaciones tomar decisiones proactivas para optimizar la dotación de bicicletas y mejorar la experiencia del usuario.

**Próximos Pasos:**
* Enriquecer el modelo con datos climáticos o de eventos en la ciudad.
* Desarrollar un modelo de machine learning para predecir la demanda con mayor precisión.
* Calcular las rutas óptimas para los vehículos de rebalanceo (un clásico "problema del viajante").
