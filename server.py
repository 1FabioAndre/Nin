import eventlet

# # Necesario para manejar múltiples conexiones
#Flask se utiliza para manejar las rutas HTTP tradicionales, como la ruta raíz ('/')
#@socketio.on(...) es un decorador de Flask-SocketIO que se
# utiliza para definir controladores de eventos para WebSocket.
# Este decorador sirve para asociar una función con un evento específico
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)  #esta linea habilita en hecho de que en flask no solo use el decorador de rutas sino tambien decoradores de socketio
#es de cir asocia eventos en tiempo real(socket io)  con las rutas http de flask

@app.route('/')
def index():
    return "Servidor WebSocket en Flask-SocketIO"

# Evento cuando el cliente se conecta
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

# Evento para manejar los mensajes entrantes del cliente
@socketio.on('client_message')
def handle_message(data):
    print(f"Mensaje del cliente: {data}")
    emit('server_message', {'data': data['data'],"id":data["id"]},broadcast=True)

# Evento para manejar desconexión
@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

if __name__ == '__main__':
    # Iniciar el servidor en el puerto 5000
    socketio.run(app, host='0.0.0.0', port=5000)





##primero lanzar el de ngrok, y luego el server y luego a tu agente
##En resumen, SocketIO(app) asocia Flask con SocketIO para habilitar el
##soporte de WebSocket es decir solo es un asociamiento pero correr el servidor con ambas cosas integradas es diferente
##, mientras que socketio.run(app, ...) inicia efectivamente
##el servidor que ejecuta tanto las rutas HTTP como los eventos de WebSocket.
##
##Ngrok crea un túnel desde tu servidor local a una URL pública.
##La URL pública es la dirección que se usa para acceder a tu servidor desde cualquier parte de Internet.