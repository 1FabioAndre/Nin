# from AgenteTresEnRaya import AgenteTresEnRaya
# from Tablero import Tablero
# from HumanoTresEnRaya import HumanoTresEnRaya
#
#
# #LO DE ABAJO ES EL N EN RAYA
# luis = AgenteTresEnRaya()
# juan = HumanoTresEnRaya()
# # juan = AgenteTresEnRaya()
#
# tablero = Tablero()
#
# tablero.insertar_objeto(juan)
# tablero.insertar_objeto(luis)
# tablero.run()



import socketio
import time

sio = socketio.Client()

from AgenteNEnRaya import AgenteNEnRaya
from Tablero import Tablero
from HumanoNEnRaya import HumanoNEnRaya


luis = AgenteNEnRaya()
juan = HumanoNEnRaya()

tablero = Tablero()

tablero.insertar_objeto(juan)
tablero.insertar_objeto(luis)
# tablero.run()
id = 2


@sio.event
def connect():
    print('Conectado al servidor')
    sio.emit('client_message', {'data': 'Conexion', 'id': id})


@sio.on('server_message')
def on_message(data):
    print(len(tablero.juegoActual.movidas))
    if (len(tablero.juegoActual.movidas) == 0):
        sio.disconnect()
    else:
        time.sleep(3)
        if data["id"] == id:
            return
        print(f"Mensaje del servidor*: {data['data']}")
        if data["data"] != "Conexion":
            movida = eval(data["data"])
            juan.acciones = movida
        else:
            juan.acciones = (None, None)
        tablero.avanzar()
        sio.emit('client_message', {'data': str(luis.acciones), 'id': id})


@sio.event
def disconnect():
    print('Desconectado del servidor')


if __name__ == '__main__':
    sio.connect('https://8224-2800-cd0-7603-a00-a91d-465e-aa8c-98ed.ngrok-free.app/')
    print("ASDsadsa")
    if not tablero.juegoActual.movidas:
        print("ASDsadsa")
        sio.disconnect()
    else:
        # Mantener la conexión abierta para recibir mensajes
        sio.wait()




# @sio.on('event_name'): Registra un manejador para un evento específico emitido por los clientes.
# @sio.event: Registra un manejador para eventos generales como conexión y desconexión.
# sio.wait(): Mantiene el servidor en ejecución, escuchando eventos y conexiones.