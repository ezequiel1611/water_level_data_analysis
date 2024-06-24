#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP085.h>
#include <SimpleKalmanFilter.h>

// CONSTANTES
#define KInput 0.201  //Constante del Caudalimetro de entrada
#define KOutput 0.218 //Constante del Caudalimetro de salida
#define SOUND_VELOCITY 331 // m/s Velocidad del sonido a T amb
#define Kp 35.615 //Constante Proporcional
#define Ki 4.58   //Constante Integral
#define HEIGHT 54.79  //Distancia al fondo del tanque
#define STDEV 0.27 // Desviación Estandar del HC-SR04

// FILTRO DE KALMAN
SimpleKalmanFilter kalmanFilter(STDEV, 1, 1);

// PINES
const byte FlowmeterIn = 14, // (D5) Sensor de Entrada al Tanque
    FlowmeterOut = 12,       // (D6) Sensor de Salida del Tanque
    LedOn = 13,              // (D7) LED Indicador de Encendido
    WaterPump = 15,          // (D8) PWM Bomba de Agua
    Adjust = A0,             // ADC  Setear Nivel del Agua
    Trigger = 0,             // (D3) Emisor del HC-SR04
    Echo = 2;                // (D4) Receptor del HC-SR04
Adafruit_BMP085 bmp;         // D1=SCL D2=SDA Sensor de Temperatura

// VARIABLES
double QIn = 0, QOut = 0;               // Caudales medidos
volatile int CountIn = 0, CountOut = 0; // Contadores de pulsos
unsigned long TimeRef = 0, PreviousTime = 0, CurrentTime = 0, Ts = 0;
unsigned long lastTime = 0;
float SoundVel, Level;

// PI CONTROLLER
int setpoint = 0;
int PWMset = 0, PWM_prev = 0;
float error = 0, error_prev = 0, integral = 0;

// put function declarations here:
void SetPins();
void IRAM_ATTR FlowIn();
void IRAM_ATTR FlowOut();
long UltrasonicSensor(byte TPin, byte EPin);
float SetSoundVelocity();
float getLevelDistance();
void SendData();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  SetPins();
  // Seteo el rango del PWM a 0-1023 y la frecuencia a 1KHz
  analogWriteRange(1023);
  analogWriteFreq(1000);
  analogWrite(WaterPump, 0);
  // Configuro los pines de interrupción para los caudalímetros
  attachInterrupt(digitalPinToInterrupt(FlowmeterIn), FlowIn, RISING);
  attachInterrupt(digitalPinToInterrupt(FlowmeterOut), FlowOut, RISING);
  // Inicializo la comunicación SPI con el BMP180
  if (!bmp.begin()){
    Serial.println("Fallo en la comunicacion.");
    while (1){
      ESP.deepSleep(0);
    }
  }
  // Mido la velocidad del sonido
  SoundVel = SetSoundVelocity();
  // Enciendo el LED de Status
  digitalWrite(LedOn, HIGH);
  PreviousTime = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    setpoint = Serial.parseInt();  // Leer el setpoint del puerto serie
  }
  // Mide el caudal de entrada, de salida y el nivel del agua
  QIn = (CountIn * KInput)*2.0;
  QOut = (CountOut * KOutput)*2.0;
  if((millis()-lastTime)>500){
    CountIn = 0;
    CountOut = 0;
    Level = getLevelDistance();
    lastTime = millis();
  }
  // Calcular el periodo de muestreo para el PI
  CurrentTime = millis();
  Ts = (CurrentTime - PreviousTime) / 1000.0; // Convertir a segundos
  PreviousTime = CurrentTime;
  // Calculo el PWM con el controlador PI
  error = setpoint - Level;
  integral = error + error_prev;
  PWMset = (error * Kp) + PWM_prev + (Ki * Ts * 0.5 * integral);
  // Se limita el PWM para no tener valores no válidos
  if (PWMset >= 1023){
    PWMset = 1023;
  }
  if (PWMset <= 0){
    PWMset = 0;
  }
  analogWrite(WaterPump, PWMset);
  error_prev = error;
  PWM_prev = PWMset;
  SendData();
}

// put function definitions here:
void IRAM_ATTR FlowIn() {
  CountIn++;
}

void IRAM_ATTR FlowOut() {
  CountOut++;
}

long UltrasonicSensor(byte TPin, byte EPin) {
  long Response;
  // Asegura el 0 en el trigger
  digitalWrite(TPin, LOW);
  delayMicroseconds(2);
  // Set trigger en 1 por 10us
  digitalWrite(TPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(TPin, LOW);
  Response = pulseIn(EPin, HIGH);
  return Response;
}

float SetSoundVelocity() {
  float Tc, SV;
  Tc = bmp.readTemperature();
  SV = SOUND_VELOCITY * sqrt(1.0 + (Tc / 273.0));
  SV = SV / 10000.0;
  return SV;
}

float getLevelDistance() {
  long Duration = UltrasonicSensor(Trigger, Echo);
  float LevelDistance = HEIGHT - (Duration * SoundVel) / 2.0;
  float filteredDistance = kalmanFilter.updateEstimate(LevelDistance);
  return filteredDistance;
}

void SetPins() {
  pinMode(FlowmeterIn, INPUT);
  pinMode(FlowmeterOut, INPUT);
  pinMode(LedOn, OUTPUT);
  pinMode(WaterPump, OUTPUT);
  pinMode(Adjust, INPUT);
  pinMode(Trigger, OUTPUT);
  pinMode(Echo, INPUT);
}

void SendData(){
  // Formato de los datos Qin[mL/s];Qout[mL/s];H[cm];PWM
  Serial.print(QIn);
  Serial.print(";");
  Serial.print(QOut);
  Serial.print(";");
  Serial.print(Level);
  Serial.print(";");
  Serial.println(PWMset);
}