import tkinter as tk
from tkinter import simpledialog, messagebox
import serial
import scipy.io as sio
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os

class DataAcquisitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Adquisición de Datos")
        
        # Variables para almacenar los datos recibidos
        self.QIn_data = []
        self.QOut_data = []
        self.Level_data = []
        self.PWMset_data = []
        
        # Variables de control de la adquisición de datos
        self.ser = None
        self.running = True
        self.paused = False

        # Configuración del puerto serie
        self.connect_serial_port()
        
        # Solicitar al usuario el valor de PWM
        self.PWM_user = self.get_pwm_from_user()
        self.send_pwm_to_esp()
        
        # Crear la interfaz gráfica
        self.create_interface()
        
        # Configurar la gráfica de matplotlib
        self.setup_plot()
        
        # Iniciar el hilo para recibir y procesar datos
        self.data_thread = threading.Thread(target=self.read_serial_data)
        self.data_thread.daemon = True
        self.data_thread.start()
        
    def connect_serial_port(self):
        # Solicitar al usuario el puerto serie mediante una ventana emergente
        port = simpledialog.askstring("Puerto Serie", "Ingrese el puerto serie:", initialvalue="/dev/ttyUSB0")
        if not port:
            messagebox.showerror("Error", "Debe ingresar un puerto serie.")
            self.root.quit()
            return
        try:
            self.ser = serial.Serial(port, 115200)
        except serial.SerialException:
            messagebox.showerror("Error", f"No se pudo conectar al puerto {port}.")
            self.root.quit()
    
    def get_pwm_from_user(self):
        while True:
            try:
                pwm = int(simpledialog.askstring("PWM", "Ingrese el PWM de la bomba de agua (entre 0 y 1023):"))
                if 0 <= pwm <= 1023:
                    return pwm
                else:
                    messagebox.showerror("Valor fuera de rango", "Ingrese un valor entre 0 y 1023.")
            except ValueError:
                messagebox.showerror("Entrada no válida", "Por favor, ingrese un número entero.")
    
    def send_pwm_to_esp(self):
        if self.ser:
            self.ser.write(f"{self.PWM_user}\n".encode())
            print(f"PWM enviado: {self.PWM_user}")
            # Esperar confirmación del ESP8266
            while True:
                try:
                    confirmation = self.ser.readline().decode('utf-8').strip()
                    if confirmation:
                        print(f"Confirmación recibida del ESP8266: {confirmation}")
                        break
                except UnicodeDecodeError:
                    continue

    def create_interface(self):
        # Crear un frame para organizar los elementos en una fila
        frame = tk.Frame(self.root)
        frame.pack()

        # Etiquetas para mostrar los valores actuales de QIn y QOut
        self.label_QIn = tk.Label(frame, text="QIn: N/A")
        self.label_QIn.grid(row=0, column=0, padx=5, pady=5)

        self.label_QOut = tk.Label(frame, text="QOut: N/A")
        self.label_QOut.grid(row=0, column=1, padx=5, pady=5)

        # Botón para pausar/reanudar la adquisición de datos
        self.pause_button = tk.Button(frame, text="Pausar", command=self.toggle_pause)
        self.pause_button.grid(row=0, column=2, padx=5, pady=5)

        # Botón para cerrar la aplicación
        self.quit_button = tk.Button(frame, text="Salir", command=self.on_closing, bg="red")
        self.quit_button.grid(row=0, column=3, padx=5, pady=5)


    def setup_plot(self):
        # Configurar el gráfico en tiempo real
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Nivel del Agua en Tiempo Real")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Nivel (cm)")
        self.ax.grid(True)
        
        # Agregar el gráfico a la interfaz de tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()
        
        # Inicializar la línea de la gráfica
        self.xdata, self.ydata = [], []
        self.line, = self.ax.plot(self.xdata, self.ydata, 'r-')
    
    def update_plot(self):
        # Actualizar la gráfica con los datos de Level
        self.line.set_xdata(np.arange(len(self.Level_data)))
        self.line.set_ydata(self.Level_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
    
    def read_serial_data(self):
        while self.running and self.ser.is_open:
            if not self.paused and self.ser:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    print(f"Línea leída del puerto serie: {line}")
                    data = line.split(';')
                    if len(data) == 4:
                        # Almacenar los datos
                        QIn = float(data[0])
                        QOut = float(data[1])
                        Level = float(data[2])
                        PWMset = float(data[3])
                        self.QIn_data.append(QIn)
                        self.QOut_data.append(QOut)
                        self.Level_data.append(Level)
                        self.PWMset_data.append(PWMset)
                        
                        # Actualizar los labels de QIn y QOut
                        self.label_QIn.config(text=f"QIn: {QIn}")
                        self.label_QOut.config(text=f"QOut: {QOut}")
                        
                        # Actualizar el gráfico
                        self.update_plot()

                except (UnicodeDecodeError, ValueError):
                    continue
                except serial.SerialException:
                    break
    
    def toggle_pause(self):
        # Alternar entre pausar y reanudar la adquisición de datos
        self.paused = not self.paused
        self.pause_button.config(text="Reanudar" if self.paused else "Pausar")
    
    def on_closing(self):
        # Finalizar el hilo y cerrar el puerto serie al cerrar la aplicación
        self.running = False
        #if self.ser.is_open:
            #self.ser.close()

        #if self.data_thread.is_alive():
            #self.data_thread.join()

        #output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.mat')
        sio.savemat('data.mat', {
            'QIn': self.QIn_data,
            'QOut': self.QOut_data,
            'Level': self.Level_data,
            'PWMset': self.PWMset_data
        })
        print("Datos guardados en data.mat")

        self.root.quit()
        sys.exit()

# Crear la aplicación principal
root = tk.Tk()
app = DataAcquisitionApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
