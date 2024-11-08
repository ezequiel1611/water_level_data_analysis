# Resumen del Proyecto
Este proyecto se basa en el diseño, análisis y fabricación de un depósito de agua, con una
salida y una entrada de agua, cuyo nivel del líquido es controlado para mantenerlo estable en
el valor que el usuario desee. Empleando un sensor ultrasónico se mide el nivel del agua en
tiempo real y un controlador PI implementado en el microcontrolador ESP8266, de acuerdo
a la medición del nivel, ajusta la potencia administrada a la bomba controlando así el flujo
de entrada para mantener estable el nivel del líquido. Se realizaron pruebas para calibrar los
sensores de caudal empleados, para verificar como afecta la temperatura al sensor ultrasónico,
para verificar la linealidad del control de potencia de la bomba y para determinar el rango de
linealidad del sistema. Los resultados obtenidos demuestran que es correcto asumir un rango
lineal de funcionamiento y que dentro del mismo el controlador PI funciona correctamente
manteniendo el nivel estable con un error del 5%.

Este programa permite emplear el sistema de control de nivel por medio de la comunicación
por puerte serie entre la computadora y el microcontrolador. El usuario debe cargar el programa
al microcontrolador ESP8266, conectarlo a la computadora y ejecutar la aplicación WaterTank , 
una vez se ejecuta debe ingresar el puerto serie del microcontrolador y luego un valor númerico
para el PWM de la bomba de agua y así el sistema comenzará a funcionar ingresando agua al tanque
y verá que también sale agua del mismo. En algún punto, según el PWM ingresado, el sistema llegará
al punto de equilibrio manteniendo estable el nivel del agua y serán iguales los valores de caudal
de salida y de entrada, todos estos datos se envían por puerto serie a la aplicación la cual
al cerrarla generará un archivo .mat con todos los datos recopilados desde el momento que el 
sistema comenzó a funcionar. De esta forma se pueden analizar los datos con herramientas 
como GNU Octave o MatLab.

# Requisitos
- Git
- Visual Studio Code
- PlatformIO
  - Librería Wire
  - Librería SPI
  - Librería Adafruit_BMP085
  - Librería SimpleKalmanFilter

# Clonar Repositorio
Para poder usar el sistema y almacenar todos los datos en un archivo .mat para su posterior análisis
se debe descargar este repositorio para así compilar y subir el código `main.cpp` al micrcontrolador ESP826,
y usar la aplicación `WaterTank` correspondiente a su sistema operativo.

## Linux
1. **Abrir una Terminal de Comandos:** Ubiquese en la carpeta donde quiera descargar el repositorio y
abra allí una terminal de comandos. También puede usar el acceso rápido `Ctrl+Alt+T` para abrir un terminal
de comandos y moverse a la ubicación deseada con el comando `cd`.
2. **Clonar el Repositorio:** En la terminal de comandos ahora escriba:
  ```
  git clone https://github.com/ezequiel1611/water_level_data_analysis
  ```
y presione `Enter` para crear una copia local de este repositorio en su computadora.

## Windows
1. **Abrir el Símbolo del Sistema:** Presione `Win+R`, escriba `cmd` y presione `Enter` para abrir el 
símbolo del sistema. Muevase hacia la carpeta donde quiere descargar el repositorio usando el comando `cd`.
Por ejemplo, si quiere tener el repositorio en una carpeta llamada `Scripts` en el Escritorio, puede escribir:
  ```
  cd %USERPROFILE%\Desktop\Scripts
  ```
2. **Clonar el Repositorio:** En el símbolo del sistema ahora escriba:
  ```
  git clone https://github.com/ezequiel1611/water_level_data_analysis
  ```
y presione `Enter` para crear una copia local de este repositorio en su computadora.

# Como Usar la Aplicación WaterTank
Verá que en la carpeta `WaterTank` se encuentran dos carpetas `WinDist` y `LinDist` que contienen las
distribuciones de la aplicación para Windows y para Linux respectivamente. Dirigase a la carpeta que
corresponde a su sistema operativo y dentro de del directorio `dist` encontrará el archivo ejecutable
de la aplicación, al hacer doble click la misma se iniciará mostrando una ventana emergente donde
deberá ingresar el puerto serie asociado al ESP8266.

![Configuración del Puerto Serie](https://github.com/ezequiel1611/water_level_data_analysis/blob/main/test/puerto_serie.png)

Una vez ingresado el puerto serie al que se encuentra conectado el microcontorlado, deberá especificar
un valor para el PWM de la bomba de agua (entre 0 y 1023).

![Configuración del PWM de la Bomba](https://github.com/ezequiel1611/water_level_data_analysis/blob/main/test/pwm.png)

Ahora la aplicación comenzará a recopilar datos del microcontrolador, usted podrá ver en la parte
superior de la aplicación la información en tiempo real de los caudales de entrada y de salida
del tanque y en un gráfico central se vera la información en tiempo real del nivel del agua. En todo
momento usted podrá pausar o reanudar la toma de datos haciendo click en el botón `Pausar/Reanudar`.

![Vista Previa de la Aplicación](https://github.com/ezequiel1611/water_level_data_analysis/blob/main/test/ejemplo.png)

Cuando desee terminar la prueba haga click en el botón `Salir` para cerrar así la aplicación y obtener,
en el mismo directorio donde se encuentra el ejecutable, un archivo llamado `data.mat` el cual contiene
la información de los datos de caudal de entrada, caudal de salida, PWM y nível del líquido recibidos
durante la sesión.

# Analisis de los Datos
El archivo `data.mat` puede ser cargado al entorno de GNU Octave o MatLab usando el comando
  ```
  load("data.mat")
  ```
Una vez cargado el archivo usted verá en su espacio de trabajo cuatro vectores: Level, PWMset, QIn y QOut.
Estos vectores representan las lecturas en tiempo real del nivel del líquido, el PWM de la bomba, el caudal
de entrada en ml/s y el caudal de salida en ml/s respectivamente. Usted ahora puede trabajar sobre cada 
dato de forma independiente, como por ejemplo visualizarla de forma gráfica con el comando `plot(Level)`.

![Visualización del Nivel del Líquido](https://github.com/ezequiel1611/water_level_data_analysis/blob/main/test/kalman_data.jpg)

Esta aplicación y generación de archivo de datos está pensada para poder realizar una identificación y
análisis de la respuesta al impulso del sistema.
