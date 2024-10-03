import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO, emit

# Configuración de Flask y SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)  # Habilitar WebSocket con SocketIO

# Ruta HTTP principal para comprobar si el servidor está funcionando
@app.route('/')
def index():
    return "Servidor WebSocket en Flask-SocketIO funcionando"

# Evento cuando el cliente se conecta
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

# Evento para manejar los mensajes entrantes del cliente
@socketio.on('client_message')
def handle_message(data):
    print(f"Mensaje del cliente: {data}")
    # Verificar si 'data' es un diccionario o un simple mensaje de texto
    if isinstance(data['data'], dict):
        # Si es un diccionario, manejamos la jugada y el estado
        emit('server_message', {'data': data['data'], "id": data['data']['id']}, broadcast=True)
    else:
        # Si es solo un mensaje de texto como "Conexion"
        emit('server_message', {'data': data['data'], "id": data['id']}, broadcast=True)

# Evento cuando el cliente se desconecta
@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

# Iniciar el servidor en el puerto 5001
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
