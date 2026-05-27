from random import random, randint

class Blackjack:
    def __init__(self):
        self.estados = [(suma_jugador, carta_visible_crupier, as_usable) 
                        for suma_jugador in range(12, 22) 
                        for carta_visible_crupier in range(1, 11) 
                        for as_usable in [False, True]]
        self.acciones = [0, 1]
        self.recompensas = {0: -1, 1: 0, 2: 1, 3: 1.5} 

    
    def repartir_carta(self):
        carta = randint(1, 13)
        return min(carta, 10)
    
    def sumar_cartas(self, cartas):
        suma = sum(cartas)
        as_usable = False

        if 1 in cartas and suma + 10 <= 21:
            as_usable = True
            suma += 10
        return suma, as_usable
    
    def estado_inicial(self):
        jugador_cartas = [self.repartir_carta(), self.repartir_carta()]
        cartas_crupier = [self.repartir_carta(), self.repartir_carta()]
        suma_jugador, as_usable = self.sumar_cartas(jugador_cartas)
        carta_visible_crupier = cartas_crupier[0]
        jugada_blackjack = (suma_jugador == 21)
        return (suma_jugador, carta_visible_crupier, as_usable), jugada_blackjack