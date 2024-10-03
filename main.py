import socketio
import time

sio = socketio.Client()

from AgenteNEnRaya import AgenteNEnRaya
from Tablero import Tablero

luis = AgenteNEnRaya(6,6,6)  # Tu IA
tablero = Tablero(6,6)
tablero.insertar_objeto(luis)

id = 1  # ID único para tu IA

@sio.event
def connect():
    print('Conectado al servidor')
    sio.emit('client_message', {'data': 'Conexion', 'id': id})

@sio.on('server_message')
def on_message(data):
    print(f"Mensaje del servidor: {data['data']}")
    
    # Verificar si es el turno de esta IA
    if data["id"] == id:
        return  # Si el mensaje es para la misma IA, no procesarlo

    print(f"Movimiento recibido: {data['data']}")
    
    if data["data"] != "Conexion":
        movida = eval(data["data"])  # Convierte el string en un movimiento válido
        luis.acciones = movida  # Actualiza la jugada de la IA
    else:
        luis.acciones = (None, None)  # Si no hay movimiento, no hacer nada

    
    if luis.testTerminal(tablero.juegoActual): # Suponiendo que el servidor envía un estado
        if tablero.juegoActual.get_utilidad != 0:
            sio.emit('client_message', {'data': str(luis.acciones), 'id': id})
            print("¡Felicidades! Has ganado 1.")
        else:
            sio.emit('client_message', {'data': str(luis.acciones), 'id': id})
            print("¡Es un empate! 1")
        sio.disconnect()  # Desconectarse del servidor
        return

    tablero.avanzar()  # Avanzar en el juego
    print(f"Movida calculada por la IA: {luis.acciones}")
    
    sio.emit('client_message', {'data': str(luis.acciones), 'id': id})


@sio.event
def disconnect():
    print('Desconectado del servidor')

if __name__ == '__main__':
    sio.connect('https://4d3d-2800-cd0-8006-1100-4d10-48a7-a858-a21e.ngrok-free.app')  # Cambia esto a la URL de tu servidor
    sio.wait()
