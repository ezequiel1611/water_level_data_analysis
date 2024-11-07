import serial
import scipy.io as sio
import time

# Solicitar al usuario el setpoint del nivel del agua
while True:
    try:
        setpoint = int(input("Ingrese el PWM de la bomba de agua (entre 0 y 1023): "))
        if 0 <= setpoint <= 1023:
            break
        else:
            print("Por favor, ingrese un valor entre 10 y 40.")
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número entero.")

# Configurar el puerto serie
ser = serial.Serial('/dev/ttyUSB0', 115200)

# Enviar el setpoint al ESP8266
ser.write(f"{setpoint}\n".encode())
print(f"PWM ingresado: {setpoint}")

# Leer y mostrar la confirmación del ESP8266
while True:
    try:
        confirmation = ser.readline().decode('utf-8').strip()
        if confirmation:
            print(f"Confirmación recibida del ESP8266: {confirmation}")
            break
    except UnicodeDecodeError:
        continue

# Listas para almacenar los datos
QIn_data = []
QOut_data = []
Level_data = []
PWMset_data = []

try:
    while True:
        # Leer una línea del puerto serie
        try:
            line = ser.readline().decode('utf-8').strip()
            print(f"Línea leída del puerto serie: {line}")
        except UnicodeDecodeError:
            continue
        
        # Dividir los datos
        data = line.split(';')
        
        if len(data) == 4:
            # Parsear y almacenar los datos
            QIn_data.append(float(data[0]))
            QOut_data.append(float(data[1]))
            Level_data.append(float(data[2]))
            PWMset_data.append(float(data[3]))
            
        # Guardar los datos en un archivo .mat cada 10 segundos
        if time.time() % 10 == 0:
            sio.savemat('data.mat', {
                'QIn': QIn_data,
                'QOut': QOut_data,
                'Level': Level_data,
                'PWMset': PWMset_data
            })
            
except KeyboardInterrupt:
    # Guardar los datos en un archivo .mat al terminar
    sio.savemat('data.mat', {
        'QIn': QIn_data,
        'QOut': QOut_data,
        'Level': Level_data,
        'PWMset': PWMset_data
    })
    print('Datos guardados en data.mat')
finally:
    ser.close()
