import pygame
import random
import time
import moviepy.editor as mp


# Variables de cuadrícula
GRID_SIZE = 75
GRID_WIDTH = 1050 // GRID_SIZE
GRID_HEIGHT = 600 // GRID_SIZE


#Función para  reproducir introduccion
def reproducir_intro(video_path):
    clip = mp.VideoFileClip(video_path)
    clip.preview()


video_path = "Intro.mp4"

#funcion para configurar la pantalla 
def damePantalla():
    pygame.init()
    pygame.display.set_caption("OFIRCA 2024 - Ronda 1 - Inicio")
    pantalla = pygame.display.set_mode((1152, 648))
    return pantalla

#variable para definir limites del juego
limite_izquierdo = 0
limite_derecho = 1152 - 10
limite_superior = 40
limite_inferior = 648

#funcion para dibujar las bolsas
def crear_bolsas(cantidad):
    bolsas = []
    limite_izquierdo = 0
    limite_derecho = 1152 - 10
    limite_superior = 40
    limite_inferior = 648
    bolsas = []
    for _ in range(int(cantidad * 0.4)):
        bolsas.append(
            {
                "tipo": "verde",
                "rect": pygame.Rect(
                    random.randint(limite_izquierdo, limite_derecho),
                    random.randint(limite_superior, limite_inferior),
                    75,  # ancho de la bolsa
                    75,  # alto de la bolsa
                ),
                "cargada": False,
            }
        )
    for _ in range(int(cantidad * 0.6)):
        bolsas.append(
            {
                "tipo": "gris",
                "rect": pygame.Rect(
                    random.randint(limite_izquierdo, limite_derecho),
                    random.randint(limite_superior, limite_inferior),
                    75,  # ancho de la bolsa
                    75,  # alto de la bolsa
                ),
                "cargada": False,
            }
        )
    return bolsas


area_juego = pygame.Rect(limite_izquierdo, limite_superior, 1152, 648)

#personajes
personajes = ["UAIBOT", "UAIBOTA", "UAIBOTINO", "UABOTINA"]

#Carga de bolsas y capacidades de los personajes para llevar bolsas
capacidades = {"UAIBOT": 2, "UAIBOTA": 2, "UAIBOTINO": 1, "UABOTINA": 1}
cargaActual = {
    "UAIBOT": {"verdes": 0, "grises": 0},
    "UAIBOTA": {"verdes": 0, "grises": 0},
    "UAIBOTINO": {"verdes": 0, "grises": 0},
    "UABOTINA": {"verdes": 0, "grises": 0},
}

#Cambio de personaje
personajeActualIndex = 0
personajeActual = personajes[personajeActualIndex]

pantalla = damePantalla()
pygame.font.init()
tipografia = pygame.font.SysFont("Arial", 15)
tipografiaGrande = pygame.font.SysFont("Arial", 24)
tipografiaMuyGrande = pygame.font.SysFont("Arial", 64)
colorVerde, colorAzul, colorBlanco, colorNegro, colorNaranja, colorBordeaux = (
    (11, 102, 35),
    (0, 0, 255),
    (255, 255, 255),
    (0, 0, 0),
    (239, 27, 126),
    (102, 41, 53),
)
# Variables de bucle de juego

clock = pygame.time.Clock()
juegoEnEjecucion = True
# Nueva variable para controlar el tiempo de cambio de personaje
tiempoCambioPersonaje = 0
intervaloCambio = 50  # Intervalo de 500 ms (0.5 segundos)

# Cargar imágenes
imgFondo = pygame.image.load("fondo.png")
imgUAIBOT = pygame.transform.scale(
    pygame.image.load("UAIBOT.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)
)
imgUAIBOTA = pygame.transform.scale(
    pygame.image.load("UAIBOTA.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)
)
imgUAIBOTINO = pygame.transform.scale(
    pygame.image.load("UAIBOTINO.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)
)
imgUABOTINA = pygame.transform.scale(
    pygame.image.load("UAIBOTINA.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)
)
imgGanaste = pygame.image.load("cartel de victoria.png")
imgPerdiste = pygame.image.load("cartel perdiste.png")
# Cargar imágenes de las bolsas
imgBolsaVerde = pygame.transform.scale(
    pygame.image.load("BolsaVerde.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)
)
imgBolsaGrisOscuro = pygame.transform.scale(
    pygame.image.load("BolsaGrisOscuro.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)
)
imgCestoNegro = pygame.transform.scale(
    pygame.image.load("cestonegro.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)
)
imgCestoVerde = pygame.transform.scale(
    pygame.image.load("cestoverde.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)
)
cesto_negro_rect = imgCestoNegro.get_rect(topleft=(900, 400))
cesto_verde_rect = imgCestoVerde.get_rect(topleft=(900, 200))
# Datos de personaje
avatar = imgUAIBOT
avatar_rect = avatar.get_rect()
avatar_rect.x = 100
avatar_rect.y = 500
rapidezPersonaje = 10
# Crear bolsas
bolsas = []


# Cambiar personaje
def cambiarPersonaje():
    global personajeActual, personajeActualIndex, avatar
    personajeActualIndex = (personajeActualIndex + 1) % len(personajes)
    personajeActual = personajes[personajeActualIndex]
    # Cambiar el avatar según el personaje actual
    if personajeActual == "UAIBOT":
        avatar = imgUAIBOT
        time.sleep(0.1)
    elif personajeActual == "UAIBOTA":
        avatar = imgUAIBOTA
        time.sleep(0.1)
    elif personajeActual == "UAIBOTINO":
        avatar = imgUAIBOTINO
        time.sleep(0.1)
    elif personajeActual == "UABOTINA":
        avatar = imgUABOTINA
        time.sleep(0.1)


tiempoLimite = 40
tiempo_restante = 40


def reiniciar_juego():
    global personajeActualIndex, personajeActual, avatar, avatar_rect, tiempoLimite, tiempo_restante, cargaActual, contadorcestoVer, contadorcestoGri, bolsas, objetivoGanar
    personajeActualIndex = 0
    personajeActual = personajes[personajeActualIndex]
    avatar = imgUAIBOT
    avatar_rect.x = 100
    avatar_rect.y = 500
    tiempoLimite = 40
    tiempo_restante = 40
    cargaActual = {p: {"verdes": 0, "grises": 0} for p in personajes}
    contadorcestoVer = 0
    contadorcestoGri = 0
    bolsas = crear_bolsas(1)
    objetivoGanar = 1


# Movimientos
def arriba():
    avatar_rect.y -= rapidezPersonaje
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))


def abajo():
    avatar_rect.y += rapidezPersonaje
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))


def derecha():
    avatar_rect.x += rapidezPersonaje
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))


def izquierda():
    avatar_rect.x -= rapidezPersonaje
    pygame.mixer.Channel(2).play(pygame.mixer.Sound("mover.wav"))


# Operaciones de renderización
def dibujarFondo():
    pantalla.blit(imgFondo, (0, 0))


def dibujarTexto(
    texto,
    tipografia,
    colorTexto,
    anchoRecuadro,
    altoRecuadro,
    colorRecuadro,
    posX,
    posY,
):
    textoReglas = tipografia.render(texto, False, colorTexto)
    pygame.draw.rect(pantalla, colorRecuadro, (posX, posY, anchoRecuadro, altoRecuadro))
    pantalla.blit(textoReglas, (posX + 5, posY + 5, anchoRecuadro, altoRecuadro))


def dibujarUIyFondo():
    dibujarFondo()


ANCHO_BARRA = 300
ALTO_BARRA = 15
x_barras = 15
y_barras = 30
tiempoL = True


# Función para dibujar la barra de tiempo
def dibujar_barra_de_tiempo(tiempoLimite, tiempo_restante):
    pygame.time.get_ticks()
    proporción = tiempo_restante / tiempoLimite
    ancho_actual = int(ANCHO_BARRA * proporción)
    # Dibujar fondo de la barra (barra vacía)
    pygame.draw.rect(
        pantalla, (255, 0, 0), (x_barras, y_barras, ANCHO_BARRA, ALTO_BARRA)
    )

    # Dibujar la barra de tiempo (barra llena)
    pygame.draw.rect(
        pantalla, (0, 255, 0), (x_barras, y_barras, ancho_actual, ALTO_BARRA)
    )


def contadorDeBolsasEnPantalla():
    bolsas_verdes = sum(
        1 for bolsa in bolsas if bolsa["tipo"] == "verde" and not bolsa["cargada"]
    )
    bolsas_grises = sum(
        1 for bolsa in bolsas if bolsa["tipo"] == "gris" and not bolsa["cargada"]
    )
    dibujarTexto(
        f"Bolsas en la pantalla: {bolsas_verdes + bolsas_grises}",
        tipografia,
        colorBlanco,
        250,
        30,
        colorNegro,
        337,
        0,
    )


bolsas_verdes = sum(
    1 for bolsa in bolsas if bolsa["tipo"] == "verde" and not bolsa["cargada"]
)
bolsas_grises = sum(
    1 for bolsa in bolsas if bolsa["tipo"] == "gris" and not bolsa["cargada"]
)

objetivoGanar = 1
contadorGanar = 0
contadorcestoVer = 0
contadorcestoGri = 0


def ajustar_posicion_bolsa(bolsa):
    x = bolsa["rect"].x
    y = bolsa["rect"].y
    bolsa["rect"].x = (x // GRID_SIZE) * GRID_SIZE
    bolsa["rect"].y = (y // GRID_SIZE) * GRID_SIZE

    if bolsa["rect"].x < limite_izquierdo:
        bolsa["rect"].x = limite_izquierdo
    elif bolsa["rect"].x > limite_derecho - GRID_SIZE:
        bolsa["rect"].x = limite_derecho - GRID_SIZE
    if bolsa["rect"].y < limite_superior:
        bolsa["rect"].y = limite_superior
    elif bolsa["rect"].y > limite_inferior - GRID_SIZE:
        bolsa["rect"].y = limite_inferior - GRID_SIZE

    if bolsa["rect"].colliderect(cesto_negro_rect):
        bolsa["rect"].x = random.randint(960, 1092) // GRID_SIZE * GRID_SIZE
        bolsa["rect"].y = random.randint(460, 588) // GRID_SIZE * GRID_SIZE
    elif bolsa["rect"].colliderect(cesto_verde_rect):
        bolsa["rect"].x = random.randint(960, 1092) // GRID_SIZE * GRID_SIZE
        bolsa["rect"].y = random.randint(260, 588) // GRID_SIZE * GRID_SIZE


def dibujarBasuraYTachos():
    pantalla.blit(imgCestoNegro, (900, 400))
    pantalla.blit(imgCestoVerde, (900, 200))
    for bolsa in bolsas:
        ajustar_posicion_bolsa(bolsa)  # Ajusta la posición de la bolsa
        if not bolsa["cargada"]:
            if bolsa["tipo"] == "verde":
                pantalla.blit(imgBolsaVerde, bolsa["rect"])
            else:  # 'gris'
                pantalla.blit(imgBolsaGrisOscuro, bolsa["rect"])


def hay_colision(rect, lista_objetos):
    for objeto in lista_objetos:
        if rect.colliderect(objeto["rect"]):
            return True
    return False


def cartelCestosVer():
    dibujarTexto(
        f"Cantidad de bolsas: {contadorcestoVer}",
        tipografia,
        colorBlanco,
        0,
        0,
        colorAzul,
        895,
        175,
    )


def cartelCestosGri():
    dibujarTexto(
        f"Cantidad de bolsas: {contadorcestoGri}",
        tipografia,
        colorBlanco,
        0,
        0,
        colorAzul,
        895,
        375,
    )


def dibujarJugador():
    pantalla.blit(avatar, avatar_rect)


perder = False


def dibujarCarga():
    carga_texto = f"{personajeActual} Carga: {cargaActual[personajeActual]['verdes']} bolsas verdes y {cargaActual[personajeActual]['grises']} bolsas grises"
    dibujarTexto(carga_texto, tipografia, colorBlanco, 325, 30, colorNegro, 15, 0)


def dibujarTodo():
    dibujarUIyFondo()
    dibujarBasuraYTachos()
    dibujarJugador()
    dibujarCarga()  # Llamar a la función para dibujar la carga
    contadorDeBolsasEnPantalla()
    cartelCestosVer()
    cartelCestosGri()


def reproducir_cancion_en_bucle(ruta_cancion):
    pygame.mixer.music.load(ruta_cancion)
    pygame.mixer.music.play(-1)


def reiniciar_tiempo():
    global ticksAlComenzar
    ticksAlComenzar = pygame.time.get_ticks()


reproducir_cancion_en_bucle("musicaJugar.wav")
mostrarBarra = False
val = False

reproducir_intro(video_path)

ticksAlComenzar = pygame.time.get_ticks()
while juegoEnEjecucion:
    contadorGanar = 1

    if tiempo_restante > 0:
        tiempoActual = (pygame.time.get_ticks() - ticksAlComenzar) / 1000
        tiempo_restante = tiempoLimite - tiempoActual
        tiempoL = True
    else:
        tiempoL = False

    dibujarTodo()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juegoEnEjecucion = False

    keys = pygame.key.get_pressed()

    # Movimientos
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        arriba()
        if avatar_rect.top < limite_superior:
            avatar_rect.top = limite_superior

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        abajo()
        if avatar_rect.bottom > limite_inferior:
            avatar_rect.bottom = limite_inferior

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        izquierda()
        if avatar_rect.left < limite_izquierdo:
            avatar_rect.left = limite_izquierdo

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        derecha()
        if avatar_rect.right > limite_derecho:
            avatar_rect.right = limite_derecho

    # Cambiar personaje solo si ha pasado el intervalo
    if keys[pygame.K_c]:
        cambiarPersonaje()

    if keys[pygame.K_r]:
        reiniciar_juego()
        reiniciar_tiempo()
        mostrarBarra = False

    # Verificar colisiones con bolsas
    for bolsa in bolsas:
        if not bolsa["cargada"] and avatar_rect.colliderect(bolsa["rect"]):
            if (
                cargaActual[personajeActual]["verdes"]
                + cargaActual[personajeActual]["grises"]
            ) < capacidades[personajeActual]:
                bolsa["cargada"] = True
                if bolsa["tipo"] == "verde":
                    cargaActual[personajeActual]["verdes"] += 1
                    pygame.mixer.Channel(2).play(
                        pygame.mixer.Sound("agarrar bolsa.wav")
                    )
                elif bolsa["tipo"] == "gris":
                    cargaActual[personajeActual]["grises"] += 1
                    pygame.mixer.Channel(2).play(
                        pygame.mixer.Sound("agarrar bolsa.wav")
                    )

    # Dejar bolsas en cestos
    if avatar_rect.colliderect(cesto_negro_rect) and keys[pygame.K_e]:
        if cargaActual[personajeActual]["grises"] > 0:
            time.sleep(0.1)
            cargaActual[personajeActual]["grises"] -= 1
            contadorGanar += 1
            contadorcestoGri += 1

    if avatar_rect.colliderect(cesto_verde_rect) and keys[pygame.K_e]:
        if cargaActual[personajeActual]["verdes"] > 0:
            time.sleep(0.1)
            cargaActual[personajeActual]["verdes"] -= 1
            contadorGanar += 1
            contadorcestoVer += 1

    # Niveles
    if keys[pygame.K_1]:
        time.sleep(0.2)
        ticksAlComenzar = pygame.time.get_ticks()
        reiniciar_juego()
        cargaActual[personajeActual]["verdes"] = 0
        cargaActual[personajeActual]["grises"] = 0
        bolsas = crear_bolsas(5)
        objetivoGanar = 5
        reiniciar_tiempo()
        val = True
        mostrarBarra = True
    elif keys[pygame.K_2]:
        time.sleep(0.2)
        ticksAlComenzar = pygame.time.get_ticks()
        reiniciar_juego()
        cargaActual[personajeActual]["verdes"] = 0
        cargaActual[personajeActual]["grises"] = 0
        bolsas = crear_bolsas(15)
        objetivoGanar = 15
        val = True
        mostrarBarra = True
        reiniciar_tiempo()
    elif keys[pygame.K_3]:
        time.sleep(0.2)
        ticksAlComenzar = pygame.time.get_ticks()
        reiniciar_juego()
        cargaActual[personajeActual]["verdes"] = 0
        cargaActual[personajeActual]["grises"] = 0
        bolsas = crear_bolsas(25)
        objetivoGanar = 25
        val = True
        mostrarBarra = True
        reiniciar_tiempo()
    cestos = contadorcestoGri + contadorcestoVer

    if mostrarBarra == True:
        dibujar_barra_de_tiempo(tiempoLimite, tiempo_restante)

    # Verificar condiciones de victoria
    if (
        cargaActual[personajeActual]["grises"] == 0
        and cargaActual[personajeActual]["verdes"] == 0
    ):

        if val:
            if tiempoLimite > 0:
                tiempoLimite -= 1 / 60
                if mostrarBarra:
                    dibujar_barra_de_tiempo(tiempoLimite, tiempo_restante)

            if cestos == objetivoGanar and tiempoL == True:
                pantalla.blit(imgGanaste, (0, 0))
                pygame.display.flip()
                time.sleep(2)
                reiniciar_juego()
                reiniciar_tiempo()
                mostrarBarra = False
            if tiempoL == False:
                pantalla.blit(imgPerdiste, (0, 0))
                pygame.display.flip()
                time.sleep(4)
                reiniciar_juego()
                reiniciar_tiempo()
                pygame.display.flip()
                mostrarBarra = False

    print(tiempo_restante)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
