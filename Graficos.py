import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import random
import os

# Cargar personajes desde el archivo JSON
def cargar_personajes():
    with open("personajes.json", "r", encoding="utf-8") as archivo:
        personajes = json.load(archivo)
    return personajes

# Configuración de la ventana de inicio
def iniciar_juego():
    # Inicia el juego
    game_window()

# Mostrar la ventana del juego
def game_window():
    global personajes, pregunta_actual, preguntas_hechas

    pregunta_actual = ""
    preguntas_hechas = 0

    # Eliminar los widgets de la ventana principal
    for widget in main_window.winfo_children():
        widget.destroy()

    # Mostrar la primera pregunta
    mostrar_pregunta()

# Mostrar una pregunta y las opciones
def mostrar_pregunta():
    global personajes, pregunta_actual, preguntas_hechas

    if len(personajes) <= 1:
        mostrar_ganador()
        return

    # Lista de preguntas disponibles
    preguntas_disponibles = [
        'es_droide', 'es_alienigena', 'usa_blaster', 'es_jedi', 'es_sith',
        'es_humano', 'es_mujer', 'usa_fuerza', 'tiene_mascara', 'lado_oscuro',
        'usa_sable_de_luz', 'usa_casco', 'usa_armadura'
    ]

    pregunta_actual = random.choice(preguntas_disponibles)
    
    # Mostrar la pregunta
    pregunta_label.config(text=f"¿El personaje {pregunta_actual.replace('_', ' ')}?")

    # Crear botones de respuesta
    yes_button.config(state=tk.NORMAL)
    no_button.config(state=tk.NORMAL)

# Función para procesar respuesta "Sí"
def responder_si():
    global personajes, pregunta_actual, preguntas_hechas
    personajes = [p for p in personajes if p.get(pregunta_actual, False) == True]
    preguntas_hechas += 1
    mostrar_pregunta()

# Función para procesar respuesta "No"
def responder_no():
    global personajes, pregunta_actual, preguntas_hechas
    personajes = [p for p in personajes if p.get(pregunta_actual, False) == False]
    preguntas_hechas += 1
    mostrar_pregunta()

# Mostrar la imagen del ganador
def mostrar_ganador():
    if len(personajes) == 1:
        ganador = personajes[0]
        messagebox.showinfo("¡Ganador!", f"¡Adiviné! El personaje es: {ganador['nombre']}")
        imagen_ganador = Image.open(f"imagenes_personajes/{ganador['nombre']}.jpg")
        imagen_ganador.thumbnail((250, 250))  # Ajustar tamaño
        img = ImageTk.PhotoImage(imagen_ganador)

        # Mostrar imagen del ganador
        ganador_label.config(image=img)
        ganador_label.image = img
        ganador_label.grid(row=3, column=0, columnspan=2, pady=20)

# Función para cargar las imágenes de los personajes
def cargar_imagenes_personajes():
    imagenes = []
    for filename in os.listdir("imagenes_personajes"):
        if filename.endswith(".jpg"):
            imagenes.append(filename)
    return imagenes

# Función para mostrar las imágenes de todos los personajes
def mostrar_imagenes():
    imagenes = cargar_imagenes_personajes()

    for i, imagen in enumerate(imagenes):
        img = Image.open(f"imagenes_personajes/{imagen}")
        img.thumbnail((100, 100))  # Ajustar tamaño
        img = ImageTk.PhotoImage(img)

        label_imagen = tk.Label(imagenes_frame, image=img)
        label_imagen.image = img  # Para evitar que la imagen se libere
        label_imagen.grid(row=i // 5, column=i % 5, padx=10, pady=10)  # Organizar en la ventana

# Configuración de la ventana principal
main_window = tk.Tk()
main_window.title("Adivina Quién - Star Wars")
main_window.geometry("800x600")

# Frame de las imágenes de los personajes
imagenes_frame = tk.Frame(main_window)
imagenes_frame.pack(pady=20)

# Mostrar las imágenes de todos los personajes
mostrar_imagenes()

# Botón para iniciar el juego
inicio_button = tk.Button(main_window, text="Iniciar Juego", command=iniciar_juego)
inicio_button.pack(pady=20)

# Configuración del juego (ventana de preguntas)
pregunta_label = tk.Label(main_window, text="", font=("Arial", 14))
pregunta_label.pack(pady=10)

# Botones para responder "Sí" o "No"
yes_button = tk.Button(main_window, text="Sí", state=tk.DISABLED, command=responder_si)
yes_button.pack(side=tk.LEFT, padx=20, pady=10)

no_button = tk.Button(main_window, text="No", state=tk.DISABLED, command=responder_no)
no_button.pack(side=tk.LEFT, padx=20, pady=10)

# Label para mostrar la imagen del ganador
ganador_label = tk.Label(main_window)
ganador_label.pack(pady=20)

# Cargar los personajes desde el JSON
personajes = cargar_personajes()

# Ejecutar la ventana principal
main_window.mainloop()
