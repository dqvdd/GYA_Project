# GYA_Project - Global SuperStore

## Problematica
Global Super Store enfrenta problemas clave que afectan su rentabilidad. Existen disparidades significativas entre las ventas y las ganancias en varias subcategorías, como Phones y Tables, donde los altos costos y los descuentos excesivos están erosionando los márgenes. Además, algunas regiones como Western Asia y Western Africa están generando pérdidas considerables debido a un mal manejo de costos y estrategias de ventas ineficientes. Los altos costos de envío también están afectando la rentabilidad en categorías clave. Se recomienda revisar la estrategia de descuentos, optimizar los costos de operación en regiones problemáticas y reducir los costos de envío para mejorar los márgenes de utilidad.

## ¿Que se encuentra en el repositorio?
En el repositorio de este proyecto se encuentran los siguientes archivos clave:

**Limpieza.ipynb:** Este notebook se encarga de la limpieza de los datos originales. Aquí se aplican técnicas de preprocesamiento para manejar valores nulos, estandarizar formatos y eliminar posibles errores en los datos. El objetivo es preparar los datos para que estén listos para su uso en análisis y visualizaciones más avanzadas.

**SQL.ipynb:** Este notebook gestiona la carga de los datos limpios en una base de datos MySQL, específicamente en la base de datos db_superstore. Aquí se realiza el proceso ETL (Extract, Transform, Load), tomando los archivos CSV limpios, transformándolos si es necesario y cargándolos en la base de datos para facilitar consultas y análisis más eficientes.

**streamlit_proyect.py:** Este archivo contiene el código para la aplicación de visualización interactiva utilizando Streamlit. La aplicación se conecta a la base de datos db_superstore en MySQL, donde se han desarrollado gráficos dinámicos para explorar los datos a través de filtros y segmentadores, proporcionando un análisis visual de las ventas, ganancias, costos y descuentos.

## ¿Cuantos datos tomó, de que son y cuantas caracteristicas tiene?

Inicialmente, se trabajó con tres archivos CSV que contenían datos esenciales para el análisis de la tienda Global Super Store:

**Tabla de Órdenes:** Este archivo contenía 51,290 registros con 23 características, donde se almacenaba información detallada sobre las órdenes realizadas. Estas características incluyen datos sobre el producto (precio de venta, ganancias, descuentos), la ubicación de envío, el costo de envío, entre otros. Durante el proceso de limpieza, se eliminó la característica "Código Postal", debido a que contenía muchos valores nulos o poco consistentes, quedando un total de 22 características para el análisis.

**Tabla de Retornos:** Con 1,079 registros y 3 características (Returned, Order ID y Region), este archivo proporcionaba información sobre las órdenes devueltas. Sin embargo, la característica Returned fue omitida en el análisis ya que su información estaba implícita en las órdenes devueltas y resultaba redundante.

**Tabla de Personas:** Este archivo contenía 24 registros con 2 características que proporcionaban información sobre los gerentes de las distintas regiones. Aunque los datos eran relevantes desde un punto de vista organizacional, no se utilizaron en las visualizaciones ya que no aportaban directamente al análisis de ventas y ganancias de los productos.

## ¿Que encontró en los datos?

**Disparidad entre ventas y ganancias por subcategoría:** Subcategorías como Phones y Copiers tienen volúmenes de ventas altos, pero márgenes de ganancia reducidos, lo que indica costos elevados, posiblemente relacionados con la adquisición o la inconsistencia en los descuentos aplicados. El caso de Tables es particularmente preocupante, ya que no solo genera pérdidas netas significativas (pérdidas de $64,084), sino que los descuentos aplicados agravan esta situación.

**Costos elevados en proporción a las ventas en ciertas regiones:** Western Europe lidera en ventas con $1,545,558, pero los costos altos ($1,327,125) limitan sus márgenes de ganancia. A pesar de ser rentable, los altos costos están afectando su potencial de crecimiento. Regiones como Western Asia y Western Africa presentan márgenes negativos, sugiriendo una gestión ineficaz de costos y descuentos.

**Descuentos excesivos en productos específicos:** El análisis de márgenes de ganancia por descuento muestra que, cuando los descuentos superan el 60%, los márgenes de ganancia se vuelven negativos. En subcategorías como Phones y Tables, los descuentos agresivos están erosionando el margen de utilidad, lo que indica que las políticas de descuento no están mejorando las ganancias.

**Pérdidas en regiones específicas:** Regiones como Western Africa y Western Asia registran pérdidas importantes, especialmente en subcategorías como Bookcases, Appliances y Machines. Esto evidencia que la estrategia de ventas en estas regiones no está equilibrada con los costos de operación.

## ¿Como su descubrimiento podria dar valor a una empresa?

Los hallazgos de este análisis aportan un valor significativo a la estrategia operativa y comercial de cualquier empresa, y en particular a Global Super Store, de la siguiente manera:

+ **Optimización de costos y mejoras en la rentabilidad:** El análisis de costos en proporción a las ventas y las ganancias muestra que algunas subcategorías y regiones están incurriendo en costos excesivos, lo que afecta la rentabilidad. Identificar estas áreas permite a la empresa ajustar sus operaciones, renegociar contratos de adquisición, optimizar la logística o reconsiderar su presencia en ciertas regiones para reducir costos y aumentar las ganancias.

+ **Reevaluación de políticas de descuentos:** Los descuentos agresivos no están teniendo el impacto positivo esperado, como lo muestran las subcategorías y regiones donde se aplican descuentos significativos pero se obtienen márgenes negativos. Con este descubrimiento, la empresa puede reevaluar y rediseñar sus estrategias de descuentos para maximizar los márgenes de ganancia sin sacrificar la competitividad.

+ **Reducción de pérdidas y reevaluación de mercados:** Las pérdidas en regiones como Western Africa y Western Asia destacan la necesidad de una reevaluación de las estrategias de ventas y operaciones en estas áreas. Global Super Store puede utilizar estos hallazgos para redirigir recursos hacia mercados más rentables o para optimizar las operaciones en las regiones que actualmente no generan ganancias.

+ **Segmentación y enfoque estratégico:** Los datos revelan que ciertas subcategorías y regiones son mucho más rentables que otras. Al enfocar los esfuerzos de ventas y marketing en estas áreas, la empresa puede maximizar el retorno de la inversión, centrándose en los productos y mercados más rentables, y reduciendo las inversiones en áreas menos lucrativas.

En resumen, el descubrimiento de estos patrones permite a la empresa tomar decisiones basadas en datos para ajustar su estrategia de ventas, optimizar costos, mejorar la rentabilidad y dirigir los esfuerzos a las áreas con mayor potencial de éxito. Estos ajustes pueden generar un impacto positivo a largo plazo en la sostenibilidad y crecimiento del negocio.
