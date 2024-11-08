from machine import Pin, PWM
from time import sleep, time
from random import seed, randint

class Buzzer:
    """
    Clase para manejar un buzzer pasivo
    """
    def __init__(self, pin_num : int):
        """
        Constructor de clase
        
        ARGS:
            pin_num(int): El número del pin al que está conectado el buzzer
        """
        assert isinstance(pin_num, int) #Valida que el pin sea un entero
        self._pin = PWM(Pin(pin_num))
        
    def tocar_tono_segs(self, tono : int, segundos : float):
        """
        Reproduce el tono especificado durante la cantidad de segundos dada
        
        ARGS:
            tono(int): La frecuencia en hz que reproducirá el buzzer
            segundos(float): La cantidad de segundos que durará el tono
        """
        assert isinstance(tono, int) #Valida que el tono sea entero
        assert isinstance(segundos, float) #Valida que los segundos sean float
        assert (tono >= 32 and tono <= 2000) #Valida que el tono esté entre los 32 y 2000 hz
       
        self._pin.duty_u16(1000)
        self._pin.freq(tono) #reproduce tono
        sleep(segundos)     #espera
        self._pin.duty_u16(0) #apaga buzzer
        
class Juego:
    def __init__(self, led_rojo : Pin, led_verde : Pin, led_azul : Pin, led_amarillo : Pin, buzzer : Buzzer):
        """
        Constructor de la clase
        
        ARGS:
            led_pins(list[Pin]): Lista de pines a los que están conectados los led
            buzzer(Buzzer): Buzzer del juego
        """
        self._leds = [led_rojo, led_verde, led_azul, led_amarillo] #Crea una lista con todos los pines de los leds
        assert all(isinstance(n, Pin) for n in self._leds) #Verifica que todos los elementos de la lista sean pines
        assert isinstance(buzzer, Buzzer) #Verifica que el buzzer sea un objeto de tipo buzzer

        seed(time())
        self._buzzer = buzzer
        self._secuencia = []
        self._perdio = False
        
    def crear_nuevo(self):
        """
        Prepara las variables necesarias para un nuevo juego
        """
        
        self._secuencia = [randint(0, 3), randint(0, 3), randint(0, 3)]
        self._perdio = False
    
    def agrega_paso(self, paso : int):
        """
        Añade a la secuencia el paso pasado como parámetro
        
        ARGS:
            paso(int): Un número entre 0 y 3 que representa el número de led que se encendera
        """
        assert isinstance(paso, int) #Valida que paso sea entero
        assert paso >= 0 and paso <=3 #Valida que paso se encuentre entre 0 y 3
        
        self._secuencia.append(paso)
        sleep(0.25) #Espera un poco luego de agregar el paso
        
    def pasos_totales(self) -> int:
        """
        Obtiene cuantos pasos tiene la secuencia que debe aprender el jugador
        """
        
        return len(self._secuencia)

    def obtener_paso_numero(self, n : int) -> int:
        """
        Obtiene el paso en la n-ésima posición

        ARGS:
            n(int): El índice del paso
        
        RETURNS:
            int: El paso en la posición n
        """

        assert isinstance(n, int) #Verifica que n sea entero
        assert (n >= 0 and n < len(self._secuencia)) #Verifica que n sea un índice válido
        
        return self._secuencia[n]
    
    def respuesta_n_es_correcta(self, num_respuesta : int, respuesta : int) -> bool:
        """
        Verifica si la respuesta en la n-ésima posición
        coincide con la respuesta del usuario

        ARGS:
            num_respuesta(int): Índice de la respuesta correcta
            respuesta(int): Respuesta ingresada por el usuario

        RETURNS:
            bool: Verdadero si las respuestas coinciden
        """

        assert isinstance(num_respuesta, int) #Verifica que num_respuesta sea entero
        assert isinstance(respuesta, int) #Verifica que respuesta sea entero
        assert (num_respuesta >= 0 and num_respuesta < len(self._secuencia)) #Verifica que el número de respuesta sea válido 
        assert (respuesta >= 0 and respuesta <= 3) #Verifica que la respuesta sea un número válido

        return self._secuencia[num_respuesta] == respuesta
        
    def puede_seguir(self) -> bool:
        """
        Verifica si el jugador puede seguir jugando

        RETURN:
            bool: Verdadero si el jugador no ha perdido y ha hecho menos de 15 pasos
        """

        return not self._perdio and len(self._secuencia) <= 15
        
    def ganar(self):
        """
        Reproduce una fanfarria en el buzzer y realiza un efecto de parpadeo con los leds
        para indicar que el jugador ganó
        """

        #Si el jugador perdio, no reproduce la señal de victoria
        if self._perdio:
            return

        #Fanfarria ganadora
        self._buzzer.tocar_tono_segs(262, 0.125) #C4
        self._buzzer.tocar_tono_segs(330, 0.125) #E4
        self._buzzer.tocar_tono_segs(392, 0.25)  #G4
        self._buzzer.tocar_tono_segs(523, 0.5)   #C5
        
        #Parpadeo de los leds
        for _ in range(3):
            for led in self._leds:
                led.value(1)
                
            sleep(0.25)
            
            for led in self._leds:
                led.value(0)
            sleep(0.25)
            
    def perder(self):
        """
        Enciende todos los leds y hace sonar el buzzer para indicar al usuario que perdió
        """
        #Enciende los LED de todas las instrucciones
        for led in self._leds:
            led.value(1)
        #Hace sonar al buzzer
        self._buzzer.tocar_tono_segs(187, 0.5)

        #Apaga los LED de todas las instrucciones
        for led in self._leds:
            led.value(0)
            
        self._perdio = True