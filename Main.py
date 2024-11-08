from machine import Pin
from time import sleep
from SimonSays import Buzzer, Juego

#El código va aquí
rojo = Pin(12, Pin.OUT)
verd = Pin(13, Pin.OUT)
amar = Pin(18, Pin.OUT)
azul = Pin(19, Pin.OUT)

bttn_r = Pin(15, Pin.IN, Pin.PULL_DOWN)
bttn_v = Pin(14, Pin.IN, Pin.PULL_DOWN)
bttn_m = Pin(16, Pin.IN, Pin.PULL_DOWN)
bttn_z = Pin(17, Pin.IN, Pin.PULL_DOWN)

buzzer = Buzzer(20)
game = Juego(rojo, verd, azul, amar, buzzer)

while True:
    game.crear_nuevo()
    while game.puede_seguir():
        #Mostrar secuencia inicial
        for n in range(game.pasos_totales()):
            paso = game.obtener_paso_numero(n)
            if paso == 0:
                rojo.value(1)
                buzzer.tocar_tono_segs(440, 0.25)
                rojo.value(0)
            elif paso == 1:
                verd.value(1)
                buzzer.tocar_tono_segs(880, 0.25)
                verd.value(0)
            elif paso == 2:
                azul.value(1)
                buzzer.tocar_tono_segs(330, 0.25)
                azul.value(0)
            else:
                amar.value(1)
                buzzer.tocar_tono_segs(660, 0.25)
                amar.value(0)
            
            #Esperar un poco antes del siguiente paso
            sleep(0.25)

        #Leer entrada del usuario
        for n in range(game.pasos_totales()):
            resp = -1
            while resp == -1:
                if bttn_r.value() == 1:
                    rojo.value(1)
                    buzzer.tocar_tono_segs(440, 0.25)
                    rojo.value(0)
                    resp = 0
                elif bttn_v.value() == 1:
                    verd.value(1)
                    buzzer.tocar_tono_segs(880, 0.25)
                    resp = 1
                    verd.value(0)
                elif bttn_z.value() == 1:
                    azul.value(1)
                    buzzer.tocar_tono_segs(330, 0.25)
                    azul.value(0)
                    resp = 2
                elif bttn_m.value() == 1:
                    amar.value(1)
                    buzzer.tocar_tono_segs(660, 0.25)
                    amar.value(0)
                    resp = 3

            #Si su entrada fue incorrecta, perder
            if not game.respuesta_n_es_correcta(n, resp):
                game.perder()
                break            

        #agregar un paso si todas sus entradas fueron correctas
        game.agrega_paso(2)
    
    #Si ya cumplió todos los pasos y no ha perdido, ganar
    game.ganar()