import socketio
import time
from AgenteNEnRaya import AgenteNEnRaya
from Tablero import Tablero

sio = socketio.Client()

rival = AgenteNEnRaya(6, 6, 6)  # IA del compañero
tablero = Tablero(6, 6)
tablero.insertar_objeto(rival)

id = 2  # ID único para la IA del compañero

# Método para convertir las claves del tablero en strings
def convertir_tablero_a_str(tablero):
    return {str(k): v for k, v in tablero.items()}

# Método para enviar jugada y estado del tablero
def enviar_jugada_estado(jugada, estado):
    mensaje = {
        'jugada': jugada,
        'estado': {
            'jugador': estado.jugador,
            'utilidad': estado.get_utilidad,
            'tablero': convertir_tablero_a_str(estado.tablero),
            'movidas': estado.movidas
        },
        'id': id
    }
    sio.emit('client_message', {'data': mensaje})

@sio.event
def connect():
    print('Conectado al servidor')
    sio.emit('client_message', {'data': 'Conexion', 'id': id})

@sio.on('server_message')
def on_message(data):
    if data["id"] == id:
        return
    print(f"Mensaje del servidor: {data['data']}")

    if rival.testTerminal(tablero.juegoActual):
        if tablero.juegoActual.get_utilidad != 0:
            print("¡Felicidades! Ha ganado.")
        else:
            print("¡Es un empate!")
        sio.disconnect()  # Desconectarse del servidor
        return

    if data["data"] != "Conexion":
        movida = data["data"]["jugada"]  # Asignar directamente sin eval()
        rival.acciones = movida
    tablero.avanzar()

    # Enviar jugada y estado del tablero al servidor
    enviar_jugada_estado(rival.acciones, tablero.juegoActual)

@sio.event
def disconnect():
    print('Desconectado del servidor')

if __name__ == '__main__':
    sio.connect('https://0eaa-2800-cd0-8006-1100-bc56-7e7-535-95b3.ngrok-free.app')  # Cambia esto a la URL de tu servidor
    sio.wait()
