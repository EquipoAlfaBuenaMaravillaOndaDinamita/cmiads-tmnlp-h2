# Instrucciones para instalar

## Crear ambiente virtual

```bash
python3 -m venv venv

# windows
./venv/Scripts/activate

# instalar librerias
pip install -r requirements.txt
``` 

## Ejecutar crawler
```bash
scrapy crawl pagination -a tokens={tokens} -O data/tokens_{tokens}.csv
```
Donde {tokens} corresponde a la cantidad de tokens que se desea que el crawler obtenga. Por ejemplo:
```bash
scrapy crawl pagination -a tokens=100000 -O data/tokens_100000.csv
```

## Ejecutar jupyter
```bash
jupyter notebook code/main.ipynb
```

# Descripción
Se hizo un scrapper de páginas de wikipedia. Se partió de un artículo base (en este caso: https://es.wikipedia.org/wiki/Tecnolog%C3%ADa, pero el crawler funciona partiendo desde cualquier artículo) y el scrapper obtiene todo el texto del artículo, hace una limpieza básica, obtiene los tokens, los acumula y si no ha llegado a la cantidad deseada busca todos los hipervínculos de wikipedia dentro del artículo y los agrega para continuar scrappeando.
<br/>
Una vez obtenido el texto en formato csv, se procede a ejectuar el archivo de jupyter, en el cual se leen todos los archivos `.csv` dentro de la carpeta `/data` y se grafican tomando en cuenta el crecimiento del vocabulario y los tokens.

# Resultado del crawler
Se utilizó un formato CSV para guardar el resultado. Se guarda en el archivo *tokens_{tokens}.csv*. El CSV contiene únicamente una columna **text** con el texto de los artículos. Cada artículo se dejó en una única línea y la primara oración de cada línea corresponde al título del mismo

# Resultado del jupyter
El script de jupyter lee todos los archivos `.csv` en la carpeta `/data` y realiza la limpieza de las palabras de cada archivo. Para la limpieza se toman todas las palabras en minúsculas y se remueven caracteres como puntos y comas. Una vez realizado esto, se guarda un vector con la cantidad de palabras del vocabulario y la cantidad distinta de tokens para ser graficado.
Palabras hasta el momento | Tokens
--|--
...|...

Se toma cada vector y se grafica como _subplot_ para poder comparar la tendencia de la cantidad de palabras distintas. 
![Image](assets/graph.png "Resultado de Jupyter")

# Artículos Iterados
Como se mencionó anteriormente, el crawler itera buscando todos los links dentro del artículo inicial y posteriormente por todos los links dentro de cada artículo. Por ejemplo, para la corrida de 1.5M de tokens el crawler recorrió 366 artículos:
Artículo | Tokens Artículo | Tokens Acumulados
--|--|--
Tecnología | 8361 | 8361
Turbina de vapor | 1185 | 9546
Griego antiguo | 3597 | 13143
Técnica | 659 | 13802
Habilidad | 6450 | 20252
Método científico | 9292 | 29544
Proceso | 217 | 29761
Bien económico | 3123 | 32884
Sector servicios | 946 | 33830
Investigación | 2086 | 35916
Conocimiento | 8851 | 44767
Máquina | 832 | 45599
Sistema | 1148 | 46747
Entrada | 256 | 47003
Salida (informática) | 284 | 47287
Sistema tecnológico | 1759 | 49046
Economía | 5044 | 54090
Globalización | 11075 | 65165
Externalidad | 7364 | 72529
Contaminación | 20133 | 92662
Recurso natural | 1562 | 94224
Medio ambiente natural | 8176 | 102400
Sostenibilidad | 2784 | 105184
Desigualdad social | 6946 | 112130
Innovación | 4086 | 116216
Valor (axiología) | 1316 | 117532
Ética de la tecnología | 3078 | 120610
Eficiencia | 405 | 121015
Bioética | 5061 | 126076
Estudios de ciencia, tecnología y sociedad | 3908 | 129984
Filosofía de la tecnología | 3520 | 133504
Condición humana | 456 | 133960
Neoludismo | 2305 | 136265
Anarquismo primitivista | 3293 | 139558
Ideología | 5815 | 145373
Transhumanismo | 12560 | 157933
Tecnoprogresismo | 2399 | 160332
Historia de la tecnología | 3454 | 163786
Rueda | 4323 | 168109
Invento | 654 | 168763
Herramienta | 2891 | 171654
Sistema económico | 4017 | 175671
Crecimiento económico | 4308 | 179979
Prehistoria | 14328 | 194307
Domesticación del fuego | 4612 | 198919
Revolución neolítica | 4380 | 203299
Historia de la ciencia | 21133 | 224432
Imprenta | 6074 | 230506
Teléfono | 4234 | 234740
Internet | 10702 | 245442
Comunicación | 4972 | 250414
Funciones de la tecnología | 1372 | 251786
Hedonismo | 6687 | 258473
Marca (registro) | 1359 | 259832
Creencia | 7385 | 267217
Estética | 4088 | 271305
Símbolo | 3358 | 274663
Belleza | 4129 | 278792
Estatus social | 3743 | 282535
Joya | 6280 | 288815
Catedral | 1159 | 289974
Palacio | 6666 | 296640
Rascacielos | 3714 | 300354
Atrio | 1610 | 301964
Atentados del 11 de septiembre de 2001 | 21041 | 323005
World Trade Center (1973-2001) | 13950 | 336955
Nueva York | 22069 | 359024
Organización Mundial del Comercio | 3704 | 362728
Homo sapiens | 7633 | 370361
Astronáutica | 8165 | 378526
Programa Apolo | 4096 | 382622
John F | 15279 | 397901
Guerra Fría | 20450 | 418351
Carrera espacial | 8626 | 426977
Pirámides de Egipto | 2041 | 429018
Experimentación | 396 | 429414
Artesanía | 2760 | 432174
Industria | 4591 | 436765
Sistema de suministro eléctrico | 1124 | 437889
Energía | 5865 | 443754
Información | 4136 | 447890
Martillo | 912 | 448802
Aguja | 1508 | 450310
Máquina simple | 4761 | 455071
Fuego | 4369 | 459440
Instrumento quirúrgico | 1555 | 460995
Instrumentación electrónica | 912 | 461907
Instrumento de medición | 631 | 462538
Instrumentos de navegación náutica | 782 | 463320
Instrumentos de vuelo | 3325 | 466645
Máquina herramienta | 3853 | 470498
Computadora | 4633 | 475131
Invento | 654 | 475785
Artefacto | 198 | 475983
Función técnica | 259 | 476242
Desalinización | 3542 | 479784
Agua potable | 6468 | 486252
Mar Muerto | 3727 | 489979
Temperatura | 4977 | 494956
Fuente de energía | 4338 | 499294
Especificación | 88 | 499382
Material | 618 | 500000


# Contribuciones
Grupo 3 en canvas
- Martín Guzmán: crawler base con parse de artículos de wikipedia y navegación a distintos artículos para satisfacer condición de tokens
- Kevin García: repositorio, jupyter con lectura de archivos y cálculo de tokens únicos
