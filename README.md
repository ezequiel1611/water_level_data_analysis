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
al microcontrolador ESP8266, conectarlo a la computadora y ejecutar el script de python 
matFileGenerator.py, una vez se ejecuta debe ingresar un valor número para el setpoint del 
sistema (en centimetros) y así luego el sistema comenzará a funcionar para mantener el nivel
a la altura indicada mientras se envían los datos del nivel, caudal de entrada, caudal de salida y PWM
por puerto serie a la aplicación en python la cual al cerrarla generará un archivo .mat con todos
los datos recopilados desde el momento que el sistema comenzó a funcionar. De esta forma se pueden
analizar los datos con herramientas como GNU Octave o MatLab.

# Requisitos
- Visual Studio Code
- PlatformIO
  - Librería Wire
  - Librería SPI
  - Librería Adafruit_BMP085
  - Librería SimpleKalmanFilter
- Python 3
  - Paquete serial
  - Paquete scipy

# Clonar Repositorio
Para poder usar el sistema mediante la interfaz gráfica desarrollada se debe descargar este repositorio
para así compilar y subir tanto el código de control como la página web al micrcontrolador ESP8266.

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

# Como Usar el Script de Python
Antes de ejecutar el script deberá abrirlo con un editor de texto o su IDE de python de preferencia,
allí deberá corroborar que el puerto usado en el script es el mismo que usted tiene asignado para
el microcontrolador ESP8266. Esto se ve en la línea:
  ```
  ser = serial.Serial('/dev/ttyUSB0', 115200)
  ```
En el caso de Linux coloque el puerto ttyUSB correspondiente y en el caso de Windows coloque el puerto
COM correspondiente para su microcontrolador.

## Linux
1. **Abrir una Terminal de Comandos:** Ubiquese en la carpeta se encuentra el archivo `matFileGenerator.py`,
haga click derecho y seleccione la opción `Abrir en una terminal`.
2. **Ejecute el Script:** Una vez abierta la terminal de comandos debe escribir:
   ```
   python3 matFileGenerator.py
   ```
3. **Use el Script:** Ahora el programa se estará ejecutando en la terminal de comandos, verá que le pide
ingresar un setpoint en centímetros para comenzar a usar el sistema, escriba el setpoint como números enteros
y presione `Enter`. El sistema comenzará a funcionar y usted podrá ver la información que esta mandando en tiempo
real el microcontrolador. Cuando desee detener el sistema y obtener su archivo .mat presione las teclas `Ctrl+C`.
El programa se detendrá y usted verá que se creó un archivo `data.mat` en la carpeta.

## Windows
1. **Configure el Script:** Haga click derecho en el script `matFileGenerator.py` y seleccione `Propiedades`, allí
deberá seleccionar que el archivo se abra con Python.
2. **Ejecute el Script:** Ahora que se estableció que el archivo se abra con Python, solo deberá hacer doble click en
el archivo `matFileGenerator.py`.
3. 3. **Use el Script:** Ahora el programa se estará ejecutando en el símbolo del sistema, verá que le pide
ingresar un setpoint en centímetros para comenzar a usar el sistema, escriba el setpoint como números enteros
y presione `Enter`. El sistema comenzará a funcionar y usted podrá ver la información que esta mandando en tiempo
real el microcontrolador. Cuando desee detener el sistema y obtener su archivo .mat presione las teclas `Ctrl+C`.
El programa se detendrá y usted verá que se creó un archivo `data.mat` en la carpeta.

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
