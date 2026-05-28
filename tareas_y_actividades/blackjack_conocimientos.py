from random import random, randint

class Blackjack:

    def __init__(self):
        self.estados = [(suma_jugador, carta_visible_crupier, as_usable) 
                        for suma_jugador in range(12, 22) 
                        for carta_visible_crupier in range(1, 11) 
                        for as_usable in [False, True]]
        self.acciones = [0, 1]
        self.recompensas = {0: -1, 1: 0, 2: 1, 3: 1.5} 

    def reparte_carta(self):
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
        self.jugador_cartas = [self.reparte_carta(), self.reparte_carta()]
        self.cartas_crupier = [self.reparte_carta(), self.reparte_carta()]
        suma_jugador, as_usable = self.sumar_cartas(self.jugador_cartas)

        while suma_jugador < 12:
            self.jugador_cartas.append(self.reparte_carta())
            suma_jugador, as_usable = self.sumar_cartas(self.jugador_cartas)
        carta_visible_crupier = self.cartas_crupier[0]

        if suma_jugador == 21:
            return (suma_jugador, carta_visible_crupier, as_usable), self.recompensas[3], True
        
        return (suma_jugador, carta_visible_crupier, as_usable), self.recompensas[1], False
        
    def acciones_legales(self, s):
        return self.acciones
        
    def sucesor(self, s, a):
        # Recibe la accion del agente a
        # Si es 1 reparte carta, actualiza la suma y verifica si se paso de 21
        # Si es 0 ejecuta el turno del crupier (pedir hasta llegar a >= 17) y determina quien gano
        # Retorna el siguiente estado s_, la recompensa.
        if a == 1:
            self.jugador_cartas.append(self.reparte_carta())
            nueva_suma, as_usable = self.sumar_cartas(self.jugador_cartas)
            s_nuevo = (nueva_suma, s[1], as_usable)
            terminal = nueva_suma > 21
            return s_nuevo, self.recompensa(s, a, s_nuevo, None), terminal
        else:
            while True:
                suma_crupier, _ = self.sumar_cartas(self.cartas_crupier)
                if suma_crupier >= 17:
                    break
                self.cartas_crupier.append(self.reparte_carta())
            return s, self.recompensa(s, a, s, suma_crupier), True
        
    def recompensa(self, s, a, s_, suma_crupier):
        # Recibe la accion del agente
        # Si es 1 verifica si se paso a 21 y si devuelve 0 o -1 segun el caso
        # Si es 0 ejecuta el turno del crupier (pedir hasta llegar a >= 17) y devuelve 1, 2 o 3 segun el resultado
        if a == 1:
            if s_[0] > 21:           
                return self.recompensas[0]
            return self.recompensas[1]
        else:
            suma_jugador = s[0]
            if suma_crupier > 21 or suma_jugador > suma_crupier:
                return self.recompensas[2]
            elif suma_jugador == suma_crupier:
                return self.recompensas[1]
            else:
                return self.recompensas[0]

'''
Preguntas de la definición de los componentes del MDP:

1. ¿Cual es la cardinalidad del espacio de estado?

Se obtiene al multiplicar los posibles valores de cada componente del estado. La suma del jugador que puede 
tomar valores entre 12 y 21 es decir 10 valores, la carta visible del crupier que puede ser entre 1 y 10 y 
el as que puede ser usable o no. Entonces, es 10 * 10 * 2 = 200.

2. ¿Como se puede encontrar las acciones legales en cada estado?

Como esta version de blackjack es simplificada mientras que no se llegue al estado terminal ambas acciones 
son legales.

'''