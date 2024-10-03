import socketio
import time

sio = socketio.Client()

from AgenteNEnRaya import AgenteNEnRaya
from Tablero import Tablero

rival = AgenteNEnRaya(6,6,6)  # Tu IA
tablero = Tablero(6,6)
tablero.insertar_objeto(rival)

id = 2  # ID único para la IA de tu compañero

@sio.event
def connect():
    print('Conectado al servidor')
    sio.emit('client_message', {'data': 'Conexion', 'id': id})

@sio.on('server_message')
def on_message(data):
    if data["id"] == id:
        return
    print(f"Mensaje del servidor: {data['data']}")
    
    if rival.testTerminal(tablero.juegoActual): # Suponiendo que el servidor envía un estado
        print("hola")
        if tablero.juegoActual.get_utilidad != 0:
            sio.emit('client_message', {'data': str(rival.acciones), 'id': id})
            print("¡Felicidades! Ha ganadado 2.")
        else:
            sio.emit('client_message', {'data': str(rival.acciones), 'id': id})
            print("¡Es un empate! 2")
        sio.disconnect()  # Desconectarse del servidor
        return

    if data["data"] != "Conexion":
        movida = eval(data["data"])
        rival.acciones = movida
    tablero.avanzar()
    sio.emit('client_message', {'data': str(rival.acciones), 'id': id})

@sio.event
def disconnect():
    print('Desconectado del servidor')

if __name__ == '__main__':
    sio.connect('https://4d3d-2800-cd0-8006-1100-4d10-48a7-a858-a21e.ngrok-free.app')  # Cambia esto a la URL de tu servidor
    sio.wait()
