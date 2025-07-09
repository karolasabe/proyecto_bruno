import serial
import time
from pythonosc import udp_client

# Configura el puerto serial del Arduino
arduino = serial.Serial('/dev/tty.usbserial-A7031PSK', 9600)
time.sleep(2)  # Espera que el puerto se estabilice

# Configura el cliente OSC (envía a Sonic Pi)
client = udp_client.SimpleUDPClient("127.0.0.1", 4560)

# Convierte lectura analógica a distancia en cm (ajuste empírico)
def valor_a_distancia(valor):
    if valor < 80:
        return 80
    if valor > 500:
        return 10
    distancia_cm = 4800 / (valor - 20)
    
    return min(max(distancia_cm, 10), 80)

# Bucle principal
while True:
    if arduino.in_waiting:
        try:
            linea = arduino.readline().decode('utf-8').strip()
            valor = int(linea)
            distancia = valor_a_distancia(valor)

            print(f"Enviando OSC /distancia: {distancia:.1f} cm")

            # Asegúrate de que la ruta sea correcta
            client.send_message("/distancia", distancia)

        except Exception as e:
            print("⚠️ Error al leer o enviar:", e)
            time.sleep(0.1)  # evita saturar si hay error
