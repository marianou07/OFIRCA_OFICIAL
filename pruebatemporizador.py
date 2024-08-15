import pygame
import random

tiempo_limite = 30 * 1000

tiempo_inicio = pygame.time.get_ticks()


bolsas = []
def crear_bolsas(cantidad):
    bolsas = []
    for _ in range(int(cantidad * 0.4)):
        bolsas.append({'tipo': 'verde', 'rect': pygame.Rect(random.randint(35, 1092), random.randint(60, 523), 50, 50), 'cargada': False})

    for _ in range(int(cantidad * 0.6)):
        bolsas.append({'tipo': 'gris', 'rect': pygame.Rect(random.randint(35, 1092), random.randint(60, 523), 50, 50), 'cargada': False})

    return bolsas

def damePantalla():
    pygame.init()
    pygame.display.set_caption("OFIRCA 2024 - Ronda 1 - Inicio")
    pantalla = pygame.display.set_mode((1152, 648))
    return pantalla

limite_izquierdo = 0
limite_derecho = 1152 - 10
limite_superior = 60
limite_inferior = 648 - 75 

area_juego = pygame.Rect(limite_izquierdo, limite_superior, 1152 , 648)

# Personajes
personajes = ['UAIBOT', 'UAIBOTA', 'UAIBOTINO', "UABOTINA"]
capacidades = {'UAIBOT': 2, 'UAIBOTA': 2, 'UAIBOTINO': 1, 'UABOTINA': 1}
cargaActual = {'UAIBOT': {'verdes': 0, 'grises': 0}, 'UAIBOTA': {'verdes': 0, 'grises': 0}, 'UAIBOTINO': {'verdes': 0, 'grises': 0}, 'UABOTINA': {'verdes': 0, 'grises': 0}}
personajeActualIndex = 0
personajeActual = personajes[personajeActualIndex]

pantalla = damePantalla()
pygame.font.init()
tipografia = pygame.font.SysFont('Arial', 18)
tipografiaGrande = pygame.font.SysFont('Arial', 24)
tipografiaMuyGrande = pygame.font.SysFont('Arial', 64)



colorVerde, colorAzul, colorBlanco, colorNegro, colorNaranja, colorBordeaux = (11, 102, 35), (0, 0, 255), (255, 255, 255), (0, 0, 0), (239, 27, 126), (102, 41, 53)

# Variables de bucle de juego
ticksAlComenzar = pygame.time.get_ticks()
clock = pygame.time.Clock()
juegoEnEjecucion = True


# Nueva variable para controlar el tiempo de cambio de personaje
tiempoCambioPersonaje = 0
intervaloCambio = 50  # Intervalo de 500 ms (0.5 segundos)

# Cargar imágenes
imgFondo = pygame.image.load("fondo.png")
imgUAIBOT = pygame.transform.scale(pygame.image.load("UAIBOT.png").convert_alpha(), (pantalla.get_width() / 12, pantalla.get_height() / 12))
imgUAIBOTA = pygame.transform.scale(pygame.image.load("UAIBOTA.png").convert_alpha(), (pantalla.get_width() / 12, pantalla.get_height() / 12))
imgUAIBOTINO = pygame.transform.scale(pygame.image.load("UAIBOTINO.png").convert_alpha(), (pantalla.get_width() / 12, pantalla.get_height() / 12))
imgUABOTINA = pygame.transform.scale(pygame.image.load("UAIBOTINA.png").convert_alpha(), (pantalla.get_width() / 12, pantalla.get_height() / 12))
imgGanaste = (pygame.image.load("cartel de victoria.png"))
imgPerdiste = (pygame.image.load("cartel perdiste.png"))
# Cargar imágenes de las bolsas
imgBolsaVerde = pygame.transform.scale(pygame.image.load("BolsaVerde.png").convert_alpha(), (pantalla.get_width() / 12, pantalla.get_height() / 12))
imgBolsaGrisOscuro = pygame.transform.scale(pygame.image.load("BolsaGrisOscuro.png").convert_alpha(), (pantalla.get_width() / 12, pantalla.get_height() / 12))
imgCestoNegro = pygame.transform.scale(pygame.image.load("cestonegro.png").convert_alpha(), (pantalla.get_width() / 12, pantalla.get_height() / 12))
imgCestoVerde = pygame.transform.scale(pygame.image.load("cestoverde.png").convert_alpha(), (pantalla.get_width() / 12, pantalla.get_height() / 12))

cesto_negro_rect=imgCestoNegro.get_rect(topleft=(900, 400))
cesto_verde_rect=imgCestoVerde.get_rect(topleft=(900, 200))
# Datos de personaje
avatar = imgUAIBOT
avatar_rect = avatar.get_rect()
avatar_rect.x = 100
avatar_rect.y = 500
rapidezPersonaje =  10

# Crear bolsas
bolsas = []


# Cambiar personaje
def cambiarPersonaje():
    global personajeActual, personajeActualIndex, avatar
    personajeActualIndex = (personajeActualIndex + 1) % len(personajes)
    personajeActual = personajes[personajeActualIndex]
    # Cambiar el avatar según el personaje actual
    if personajeActual == 'UAIBOT':
        avatar = imgUAIBOT
    elif personajeActual == 'UAIBOTA':
        avatar = imgUAIBOTA
    elif personajeActual == 'UAIBOTINO':
        avatar = imgUAIBOTINO
    elif personajeActual == 'UABOTINA':
        avatar = imgUABOTINA

# Movimientos 
def arriba():
    avatar_rect.y -= rapidezPersonaje

def abajo():
    avatar_rect.y += rapidezPersonaje

def derecha():
    avatar_rect.x += rapidezPersonaje

def izquierda():
    avatar_rect.x -= rapidezPersonaje

# Operaciones de renderización
def dibujarFondo():
    pantalla.blit(imgFondo, (0, 0))

def dibujarTexto(texto, tipografia, colorTexto, anchoRecuadro, altoRecuadro, colorRecuadro, posX, posY):
    textoReglas = tipografia.render(texto, False, colorTexto)
    pygame.draw.rect(pantalla, colorRecuadro, (posX, posY, anchoRecuadro, altoRecuadro))
    pantalla.blit(textoReglas, (posX + 5, posY + 5, anchoRecuadro, altoRecuadro))

def dibujarUIyFondo():
    dibujarFondo()
    dibujarTexto('Elige a tu personaje con la tecla C y muévelo con las flechas para recolectar residuos y llevarlos a sus cestos correspondientes.', tipografia, colorBlanco, 820, 30, colorBordeaux, 15, 0)



def contadorDeBolsasEnPantalla():
    bolsas_verdes = sum(1 for bolsa in bolsas if bolsa['tipo'] == 'verde' and not bolsa['cargada'])
    bolsas_grises = sum(1 for bolsa in bolsas if bolsa['tipo'] == 'gris' and not bolsa['cargada'])
    dibujarTexto(f'Bolsas en la pantalla: {bolsas_verdes + bolsas_grises}', tipografia, colorBlanco, 250, 30, colorAzul, 337, 30)
   
    if bolsas_verdes == 0 and bolsas_grises == 0 and (cargaActual[personajeActual]['verdes'] == 0 and cargaActual[personajeActual]['grises'] == 0):
       
        pantalla.blit(imgGanaste, (430, 284))

contadorGanar = 0
objetivoGanar = 5
def ajustar_posicion_bolsa(bolsa):
    if bolsa['rect'].x < limite_izquierdo:
        bolsa['rect'].x = limite_izquierdo - 60
    elif bolsa['rect'].x > limite_derecho:        bolsa['rect'].x = limite_derecho - 60

    if bolsa['rect'].y < limite_superior:
        bolsa['rect'].y = limite_superior - 60
    elif bolsa['rect'].y > limite_inferior:
        bolsa['rect'].y = limite_inferior - 60
    
    if bolsa['rect'] == (900, 400):
        bolsa['rect'] = pygame.Rect(random.randint(960, 1092), random.randint(460, 588))
    elif bolsa['rect'] == (900, 200):
        bolsa['rect'] = pygame.Rect(random.randint(960, 1092), random.randint(260, 588))

def dibujarBasuraYTachos():
    pantalla.blit(imgCestoNegro, (900, 400))
    pantalla.blit(imgCestoVerde, (900, 200))
    for bolsa in bolsas:
        ajustar_posicion_bolsa(bolsa)  # Ajusta la posición de la bolsa
        if not bolsa['cargada']:
            if bolsa['tipo'] == 'verde':
                pantalla.blit(imgBolsaVerde, bolsa['rect'])
            else:  # 'gris'
                pantalla.blit(imgBolsaGrisOscuro, bolsa['rect'])
        
def hay_colision(rect, lista_objetos):
    for objeto in lista_objetos:
        if rect.colliderect(objeto['rect']):
            return True
    return False      

def dibujarJugador():
    pantalla.blit(avatar, avatar_rect)
    
def dibujarCarga():
    carga_texto = f"{personajeActual} Carga: {cargaActual[personajeActual]['verdes']} bolsas verdes y {cargaActual[personajeActual]['grises']} bolsas grises"
    dibujarTexto(carga_texto, tipografia, colorBlanco, 325, 30, colorNegro, 15, 30)

def dibujarTodo():
    dibujarUIyFondo()
    dibujarBasuraYTachos()
    dibujarJugador()
    dibujarCarga()  # Llamar a la función para dibujar la carga
    contadorDeBolsasEnPantalla()


# Bucle de juego
while juegoEnEjecucion:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            juegoEnEjecucion = False
            
    for event in pygame.event.get():
     if keys[pygame.K_r]:
        juegoEnEjecucion = False
            
    clock.tick(60)
    tiempo_actual = 60*1000
    keys = pygame.key.get_pressed()
    tiempo_restante = tiempo_limite - (tiempo_actual - tiempo_inicio)
    
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
            
    if keys[pygame.K_c] :
        
        cambiarPersonaje()
        
       
    tiempo_actual = pygame.time.get_ticks()
    
   

    # Verificar colisiones con bolsas
  # Verificar colisiones con bolsas
# Verificar colisiones con bolsas
    for bolsa in bolsas:
    
      if not bolsa['cargada'] and avatar_rect.colliderect(bolsa['rect']):
        
        if (cargaActual[personajeActual]['verdes'] + cargaActual[personajeActual]['grises']) < capacidades[personajeActual]:
            
            bolsa['cargada'] = True
            
            # Sumar al contador correspondiente según el tipo de bolsa
            if bolsa['tipo'] == 'verde':
                cargaActual[personajeActual]['verdes'] += 1  # VIncrementar carga de bolsas verdes
            elif bolsa['tipo'] == 'gris':
                cargaActual[personajeActual]['grises'] += 1  # Incrementar carga de bolsas grises

# Dejar bolsa en cesto negro
    if avatar_rect.colliderect(cesto_negro_rect) and keys[pygame.K_e]:
     if cargaActual[personajeActual]['grises'] > 0:  # Asegurarse de que hay bolsas grises para dejar
        cargaActual[personajeActual]['grises'] -= 1  # Dejar una bolsa gris
        contadorGanar += 1
# Dejar bolsa en cesto verde
    if avatar_rect.colliderect(cesto_verde_rect) and keys[pygame.K_e]:
     if cargaActual[personajeActual]['verdes'] > 0:  # Asegurarse de que hay bolsas verdes para dejar
        cargaActual[personajeActual]['verdes'] -= 1  # Dejar una bolsa verde
        contadorGanar += 1
    #if cargaActual[personajeActual]['verdes'] ==0 and cargaActual[personajeActual]['grises']==0 and :
        
     # Cambiar la cantidad de bolsas en pantalla
    if keys[pygame.K_1]:
        bolsas = crear_bolsas(5)
        objetivoGanar = 5
        tiempo_limite = 15 * 1000
        tiempo_actual = pygame.time.get_ticks()
        tiempo_restante = tiempo_limite - (tiempo_actual - tiempo_inicio)
        
    elif keys[pygame.K_2]:
        bolsas = crear_bolsas(15)
        objetivoGanar = 15
        tiempo_limite = 20 * 1000
        tiempo_actual = pygame.time.get_ticks()
        tiempo_restante = tiempo_limite - (tiempo_actual - tiempo_inicio)
    elif keys[pygame.K_3]:
        bolsas = crear_bolsas(25)
        objetivoGanar = 25
        tiempo_limite = 30 * 1000
        tiempo_actual = pygame.time.get_ticks()
        tiempo_restante = tiempo_limite - (tiempo_actual - tiempo_inicio)
    
        
        
    if contadorGanar == objetivoGanar :
        pantalla.blit(imgGanaste,(0,0))

  
    if tiempo_restante <= 0:
        # Acción a realizar cuando se agota el tiempo
        print("Tiempo agotado!")
    
   # textoCronometro = tipografiaGrande.render(str(tiempoRestante), True, (255, 255, 255))
   
    
    texto_tiempo = tipografiaGrande.render(str(tiempo_restante // 1000), True, (255, 255, 255))
    pantalla.blit(texto_tiempo, (1100, 10))
    
   # Limpiar la pantalla
  
    pygame.display.flip()
    
    dibujarTodo()
    
    dibujarCarga()
    

 
pygame.quit()