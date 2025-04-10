import json
import random

# Cargar los personajes desde el archivo JSON
def cargar_personajes():
    try:
        with open("personajes.json", "r", encoding="utf-8") as archivo:
            personajes = json.load(archivo)
        return personajes
    except FileNotFoundError:
        print("Error: El archivo 'personajes.json' no fue encontrado.")
        return []
    except json.JSONDecodeError:
        print("Error: Hubo un problema al leer el archivo JSON.")
        return []

# Función para hacer preguntas sobre los personajes
def hacer_pregunta(personajes, pregunta):
    print(f"\nPregunta: ¿El personaje {pregunta.replace('_', ' ')}? (Responde 'si' o 'no')")
    respuesta = input().lower()

    if respuesta == "si":
        # Filtrar personajes que cumplen con la característica
        personajes_filtrados = [p for p in personajes if p.get(pregunta, False) == True]
    else:
        # Filtrar personajes que no cumplen con la característica
        personajes_filtrados = [p for p in personajes if p.get(pregunta, False) == False]
    
    return personajes_filtrados

# Función para adivinar el personaje con preguntas dinámicas
def adivinar_personaje(personajes):
    # Lista de características disponibles, alineadas con el JSON
    preguntas_disponibles = [
        'es_droide', 'es_alienigena', 'usa_blaster', 'es_jedi', 'es_sith',
        'es_humano', 'es_mujer', 'usa_fuerza', 'tiene_mascara', 'lado_oscuro',
        'usa_sable_de_luz', 'usa_casco', 'usa_armadura'
    ]
    
    print("¡Bienvenido al juego de Adivina Quién!")
    preguntas_hechas = 0

    # Mientras haya más de un personaje posible
    while len(personajes) > 1:
        # Elegir una pregunta aleatoria de las disponibles
        pregunta = random.choice(preguntas_disponibles)
        
        # Hacer la pregunta y filtrar personajes
        personajes = hacer_pregunta(personajes, pregunta)
        
        # Eliminar la pregunta de la lista de preguntas disponibles
        preguntas_disponibles.remove(pregunta)

        # Incrementar el contador de preguntas
        preguntas_hechas += 1
        
        print(f"\nHan quedado {len(personajes)} personajes posibles.")

    # Si solo queda un personaje, adivinamos
    if len(personajes) == 1:
        print(f"\n¡Adiviné! El personaje es: {personajes[0]['nombre']}")
    else:
        # Si no se adivinó, el jugador tiene que adivinar
        print(f"\nNo pude adivinar el personaje. ¡Te toca a ti!")
        
# Función para reiniciar el juego
def jugar_otra_vez():
    respuesta = input("\n¿Quieres jugar otra vez? (si/no): ").lower()
    return respuesta == "si"

# Programa principal
if __name__ == "__main__":
    while True:
        personajes = cargar_personajes()
        
        # Solo continuar si los personajes se cargaron correctamente
        if not personajes:
            print("No se puede continuar sin los personajes.")
            break
        
        adivinar_personaje(personajes)
        
        # Preguntar si el jugador quiere jugar otra vez
        if not jugar_otra_vez():
            print("¡Gracias por jugar! ¡Hasta la próxima!")
            break
