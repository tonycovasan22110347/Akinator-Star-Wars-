import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  
import json
import os

# Función para cargar los datos desde el archivo JSON
def cargar_datos(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error al cargar los datos o archivo no encontrado.")
        return {"preguntas": [], "personajes": {}}

# Función para guardar los datos en el archivo JSON
def guardar_datos(archivo, datos):
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        print("Datos guardados correctamente.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

class JuegoStarWars:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Adivina Quién - Star Wars")
        self.ventana.geometry("800x600")
        self.ventana.resizable(False, False)
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Cargar los datos desde el archivo JSON
        self.datos = cargar_datos("Personajes.json")
        
        # Verificar si 'preguntas' existe en los datos
        if "preguntas" in self.datos:
            self.preguntas_random = self.datos["preguntas"][:16]  # Limitar a 16 preguntas
        else:
            print("No se encontró la clave 'preguntas' en los datos.")
            self.preguntas_random = []  # Establecer una lista vacía para evitar errores

        # Inicializar variables
        self.pregunta_actual = 0
        self.respuestas = []
        self.personajes_filtrados = self.datos.get("personajes", {}).copy()

        # Crear un canvas para contener la imagen de fondo y los widgets
        self.canvas = tk.Canvas(self.ventana, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Intentar cargar la imagen de fondo usando Pillow (soporta JPEG)
        try:
            imagen = Image.open("fondo_star_wars.jpg")
            imagen = imagen.resize((800, 600), Image.Resampling.LANCZOS)
            self.fondo_img = ImageTk.PhotoImage(imagen)
            self.canvas.create_image(0, 0, image=self.fondo_img, anchor="nw")
        except Exception as e:
            print("No se pudo cargar la imagen de fondo:", e)
        
        # Crear la pantalla principal
        self.crear_pantalla_inicio()

    def crear_pantalla_inicio(self):
        # Crear la interfaz de inicio con el nombre del juego y un botón para empezar
        self.frame_inicio = tk.Frame(self.canvas, bg="#000000", bd=0)
        self.frame_inicio.place(relx=0.5, rely=0.5, anchor="center")
        
        titulo = tk.Label(
            self.frame_inicio,
            text="¡Adivina Quién - Star Wars!",
            font=("Helvetica", 24, "bold"),
            bg="#000000",
            fg="#FFD700"
        )
        titulo.pack(pady=20)
        
        etiqueta_inicio = tk.Label(
            self.frame_inicio,
            text="Presiona 'Iniciar' para empezar el juego.",
            font=("Helvetica", 16),
            bg="#000000",
            fg="white"
        )
        etiqueta_inicio.pack(pady=10)
        
        boton_iniciar = ttk.Button(self.frame_inicio, text="Iniciar", command=self.iniciar_juego)
        boton_iniciar.pack(pady=20)
    
    def iniciar_juego(self):
        # Destruir la pantalla de inicio y empezar el juego
        self.frame_inicio.destroy()
        self.crear_interfaz_preguntas()

    def crear_interfaz_preguntas(self):
        # Crear la interfaz donde se mostrarán las preguntas
        self.frame_preguntas = tk.Frame(self.canvas, bg="#000000")
        self.frame_preguntas.place(relx=0.5, rely=0.5, anchor="center")
        
        titulo = tk.Label(
            self.frame_preguntas,
            text="¡Responde las preguntas!",
            font=("Helvetica", 20, "bold"),
            bg="#000000",
            fg="#FFD700"
        )
        titulo.pack(pady=10)

        self.etiqueta_pregunta = tk.Label(
            self.frame_preguntas,
            text="",
            font=("Helvetica", 16),
            wraplength=700,
            bg="#000000",
            fg="white"
        )
        self.etiqueta_pregunta.pack(pady=20)

        botones_frame = tk.Frame(self.frame_preguntas, bg="#000000")
        botones_frame.pack(pady=20)

        self.boton_si = ttk.Button(botones_frame, text="Sí", command=lambda: self.responder(1))
        self.boton_no = ttk.Button(botones_frame, text="No", command=lambda: self.responder(0))
        self.boton_si.grid(row=0, column=0, padx=30, ipadx=10, ipady=10)
        self.boton_no.grid(row=0, column=1, padx=30, ipadx=10, ipady=10)

        self.etiqueta_resultado = tk.Label(
            self.frame_preguntas,
            text="",
            font=("Helvetica", 14),
            bg="#000000",
            fg="#FF6347"
        )
        self.etiqueta_resultado.pack(pady=20)

        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        if self.pregunta_actual < len(self.preguntas_random):
            self.etiqueta_pregunta.config(text=self.preguntas_random[self.pregunta_actual])
        else:
            self.finalizar_juego()

    def responder(self, respuesta):
        self.respuestas.append(respuesta)
        self.personajes_filtrados = {
            personaje: respuestas for personaje, respuestas in self.personajes_filtrados.items()
            if respuestas[:len(self.respuestas)] == self.respuestas
        }
        self.pregunta_actual += 1
        self.mostrar_pregunta()

    def finalizar_juego(self):
        # Deshabilitar botones al finalizar
        self.boton_si.config(state="disabled")
        self.boton_no.config(state="disabled")

        if len(self.personajes_filtrados) == 1:
            mensaje = f"¡Tu personaje es: {list(self.personajes_filtrados.keys())[0]}!"
        elif len(self.personajes_filtrados) > 1:
            posibles = ', '.join(self.personajes_filtrados.keys())
            mensaje = f"No se pudo identificar con precisión. Posibles personajes: {posibles}."
        else:
            mensaje = "No se encontró coincidencia. Puedes agregar un nuevo personaje."
            self.pedir_nuevo_personaje()

        self.etiqueta_resultado.config(text=mensaje)
        
        # Agregar un botón de Reiniciar en la pantalla final
        self.boton_reiniciar = ttk.Button(self.frame_preguntas, text="Reiniciar", command=self.reiniciar_juego)
        self.boton_reiniciar.pack(pady=10)

    def pedir_nuevo_personaje(self):
        self.etiqueta_pregunta.config(text="¿Cuál era el personaje?")
        self.entrada_personaje = ttk.Entry(self.frame_preguntas, font=("Helvetica", 14))
        self.entrada_personaje.pack(pady=10)
        self.boton_guardar = ttk.Button(self.frame_preguntas, text="Guardar", command=self.guardar_personaje)
        self.boton_guardar.pack(pady=5)

    def guardar_personaje(self):
        nuevo_personaje = self.entrada_personaje.get().strip()
        if nuevo_personaje:
            self.datos["personajes"][nuevo_personaje] = self.respuestas
            guardar_datos("Personajes.json", self.datos)
            self.etiqueta_resultado.config(text=f"Personaje guardado: {nuevo_personaje}")
        self.entrada_personaje.destroy()
        self.boton_guardar.destroy()
        
    def reiniciar_juego(self):
        # Destruir el frame de preguntas y restablecer variables para reiniciar el juego
        self.frame_preguntas.destroy()
        self.pregunta_actual = 0
        self.respuestas = []
        self.personajes_filtrados = self.datos.get("personajes", {}).copy()
        # Volver a la pantalla de inicio
        self.crear_pantalla_inicio()

def main():
    ventana = tk.Tk()
    app = JuegoStarWars(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()
