import serial
import scipy.io as sio
import time

# Configurar el puerto serie
ser = serial.Serial('COM3', 115200)  # Reemplazar 'COM3' con el puerto serie correcto

# Listas para almacenar los datos
QIn_data = []
QOut_data = []
Level_data = []
PWMset_data = []

try:
    while True:
        # Leer una línea del puerto serie
        line = ser.readline().decode('utf-8').strip()
        
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