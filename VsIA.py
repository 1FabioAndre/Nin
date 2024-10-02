from Tablero import Tablero
from AgenteNEnRaya import AgenteNEnRaya

def main():
    import random

    # Configuración del juego
    h = 3  # Altura del tablero
    v = 3  # Anchura del tablero
    k = 3  # Número de piezas en línea para ganar

    # Crear instancias del tablero y del agente
    tablero = Tablero(h, v)
    agente_ia = AgenteNEnRaya(h, v, k)

    # Mostrar las instrucciones
    print("Bienvenido al Tres en Raya!")
    print("Juega como 'X' y la IA jugará como 'O'")
    print("Elige una posición para jugar usando coordenadas (fila, columna) desde 1 hasta", h, "para fila y", v, "para columna.")

    while tablero.juegoActual.movidas:
        # Tu turno
        while True:
            try:
                x = int(input("Introduce la fila (1-{}): ".format(h)))
                y = int(input("Introduce la columna (1-{}): ".format(v)))
                if (x, y) not in tablero.juegoActual.movidas:
                    print("Posición ya ocupada o inválida, intenta de nuevo.")
                    continue
                break
            except ValueError:
                print("Por favor, introduce números válidos.")

        # Actualizar el estado del juego con tu jugada
        tablero.juegoActual = agente_ia.getResultado(tablero.juegoActual, (x, y))
        agente_ia.mostrar(tablero.juegoActual)

        # Verificar si hay un ganador
        if agente_ia.testTerminal(tablero.juegoActual):
            if tablero.juegoActual.get_utilidad != 0:
                print("¡Felicidades! Has ganado.")
            else:
                print("¡Es un empate!")
            break

        tablero.percibir(agente_ia)
        # Jugada de la IA
        print("Es el turno de la IA:")
        agente_ia.acciones = random.choice(tablero.juegoActual.movidas)  # IA elige una jugada aleatoria
        tablero.ejecutar(agente_ia)

        # Mostrar el tablero después de la jugada de la IA
        if agente_ia.testTerminal(tablero.juegoActual):
            if tablero.juegoActual.get_utilidad != 0:
                print("La IA ha ganado.")
            else:
                print("¡Es un empate!")
            break

if __name__ == "__main__":
    main()
