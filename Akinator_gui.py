import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

class AkinatorStarWars:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator Star Wars")
        self.root.geometry("600x400")
        self.root.configure(bg="black")

        self.frame_inicio = tk.Frame(root, bg="black")
        self.frame_inicio.pack(expand=True)

        self.titulo = tk.Label(self.frame_inicio, text="Akinator Star Wars", font=("Arial", 28), bg="black", fg="yellow")
        self.titulo.pack(pady=40)

        self.boton_jugar = tk.Button(self.frame_inicio, text="Iniciar", font=("Arial", 16), command=self.iniciar_juego, bg="yellow", fg="black")
        self.boton_jugar.pack()

        self.pregunta_actual = 0
        self.respuestas = {}
        self.cargar_datos()

    def cargar_datos(self):
        with open("Personajes.json", "r") as f:
            self.personajes_completos = json.load(f)

        self.personajes = self.personajes_completos.copy()

        self.preguntas = [
            ("¿Es un Jedi?", "es_jedi"),
            ("¿Es un Sith?", "es_sith"),
            ("¿Es un droide?", "es_droide"),
            ("¿Es humano?", "es_humano"),
            ("¿Es un alienígena?", "es_alienigena"),
            ("¿Usa un blaster?", "usa_blaster"),
            ("¿Tiene un sable de luz?", "tiene_sable_luz"),
            ("¿Usa casco?", "usa_casco"),
            ("¿Usa armadura?", "usa_armadura"),
            ("¿Es extraterrestre?", "es_extraterrestre"),
            ("¿Está cubierto de pelo?", "esta_cubierto_de_pelo"),
            ("¿Sale en la primera trilogía? (episodios I-III)", "sale_en_ep_1_3"),
            ("¿Sale en la trilogía clásica? (episodios IV-VI)", "sale_en_ep_4_6"),
            ("¿Sale en la trilogía de secuelas? (episodios VII-IX)", "sale_en_ep_7_9"),
            ("¿Sale en algún spin-off?", "sale_en_spin_off")
        ]

        random.shuffle(self.preguntas)  # Aleatoriza las preguntas
        self.preguntas_random = self.preguntas[:16]  # Limita a 16

    def iniciar_juego(self):
        self.frame_inicio.destroy()
        self.frame_pregunta = tk.Frame(self.root, bg="black")
        self.frame_pregunta.pack(expand=True, fill="both")

        self.etiqueta_pregunta = tk.Label(self.frame_pregunta, text="", font=("Arial", 16), bg="black", fg="white", wraplength=500)
        self.etiqueta_pregunta.pack(pady=30)

        self.boton_si = tk.Button(self.frame_pregunta, text="Sí", font=("Arial", 14), command=lambda: self.responder(True), bg="green", fg="white", width=10)
        self.boton_si.pack(pady=10)

        self.boton_no = tk.Button(self.frame_pregunta, text="No", font=("Arial", 14), command=lambda: self.responder(False), bg="red", fg="white", width=10)
        self.boton_no.pack()

        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        if self.pregunta_actual < len(self.preguntas_random):
            texto, _ = self.preguntas_random[self.pregunta_actual]
            self.etiqueta_pregunta.config(text=texto)
        else:
            self.adivinar_personaje()

    def responder(self, respuesta):
        atributo = self.preguntas_random[self.pregunta_actual][1]
        self.respuestas[atributo] = respuesta
        self.pregunta_actual += 1
        self.filtrar_personajes()
        self.mostrar_pregunta()

    def filtrar_personajes(self):
        for atributo, valor in self.respuestas.items():
            self.personajes = {
                nombre: datos for nombre, datos in self.personajes.items()
                if datos.get(atributo, False) == valor
            }

    def adivinar_personaje(self):
        self.frame_pregunta.destroy()
        frame_resultado = tk.Frame(self.root, bg="black")
        frame_resultado.pack(expand=True)

        if len(self.personajes) == 1:
            personaje = list(self.personajes.keys())[0]
            tk.Label(frame_resultado, text=f"🎯 ¡Adiviné! El personaje es: {personaje}", font=("Arial", 18), bg="black", fg="yellow").pack(pady=20)

            # Mostrar imagen
            ruta_imagen = os.path.join("imagenes", f"{personaje}.png")
            print(f"Buscando imagen en: {ruta_imagen}")
            if os.path.exists(ruta_imagen):
                img = Image.open(ruta_imagen)
                img = img.resize((300, 400), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)

                etiqueta_imagen = tk.Label(frame_resultado, image=photo, bg="black")
                etiqueta_imagen.image = photo  # Mantener referencia
                etiqueta_imagen.pack(pady=10)
            else:
                tk.Label(frame_resultado, text="(Imagen no encontrada)", font=("Arial", 12), bg="black", fg="white").pack(pady=10)

        elif len(self.personajes) > 1:
            tk.Label(frame_resultado, text="🤔 Hay varios personajes posibles:", font=("Arial", 16), bg="black", fg="yellow").pack(pady=20)
            for p in self.personajes:
                tk.Label(frame_resultado, text=f"- {p}", font=("Arial", 14), bg="black", fg="white").pack()
        else:
            tk.Label(frame_resultado, text="❌ No pude adivinar el personaje. Intenta con otro.", font=("Arial", 16), bg="black", fg="red").pack(pady=20)

        tk.Button(frame_resultado, text="Volver a jugar", command=self.reiniciar, font=("Arial", 14), bg="blue", fg="white").pack(pady=20)

    def reiniciar(self):
        self.pregunta_actual = 0
        self.respuestas = {}
        self.cargar_datos()
        self.iniciar_juego()

# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AkinatorStarWars(root)
    root.mainloop()
