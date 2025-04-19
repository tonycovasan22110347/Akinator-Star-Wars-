import json
import os

class Akinator:
    def __init__(self):
        self.archivo = 'Personajes.json'
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
        self.cargar_personajes()

    def cargar_personajes(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as file:
                self.personajes_completos = json.load(file)
        else:
            self.personajes_completos = {}
        self.personajes = self.personajes_completos.copy()

    def guardar_personajes(self):
        with open(self.archivo, 'w') as file:
            json.dump(self.personajes_completos, file, indent=4)

    def mostrar_personajes(self):
        print("🧑‍🚀 Personajes disponibles:")
        for nombre in self.personajes_completos:
            print(f"- {nombre}")
        print()

    def hacer_pregunta(self, texto):
        respuesta = input(texto + " (Si/No): ").strip().lower()
        while respuesta not in ['si', 'no']:
            print("Por favor, responde con 'Si' o 'No'.")
            respuesta = input(texto + " (Si/No): ").strip().lower()
        return respuesta == 'si'

    def filtrar_personajes(self, atributo, respuesta):
        self.personajes = {
            nombre: datos for nombre, datos in self.personajes.items()
            if datos.get(atributo, False) == respuesta
        }

    def aprender_personaje(self):
        nombre = input("\n😓 No pude adivinar. ¿Cuál era tu personaje?: ").strip()
        print("Vamos a registrar al personaje. Responde las siguientes preguntas:\n")
        nuevo_personaje = {}
        for texto, atributo in self.preguntas:
            nuevo_personaje[atributo] = self.hacer_pregunta(texto)
        self.personajes_completos[nombre] = nuevo_personaje
        self.guardar_personajes()
        print(f"\n✅ ¡Gracias! He aprendido el personaje '{nombre}' para la próxima vez.")

    def jugar(self):
        self.cargar_personajes()
        self.mostrar_personajes()
        print("🔍 Responde las siguientes preguntas para adivinar al personaje:\n")

        for texto, atributo in self.preguntas:
            if len(self.personajes) <= 1:
                break
            respuesta = self.hacer_pregunta(texto)
            self.filtrar_personajes(atributo, respuesta)

        if len(self.personajes) == 1:
            personaje = list(self.personajes.keys())[0]
            print(f"\n🎯 ¡Adiviné! El personaje es: {personaje}")
        elif len(self.personajes) > 1:
            print("\n🤔 Hay varios personajes posibles:")
            for p in self.personajes:
                print(f"- {p}")
        else:
            print("\n❌ No pude adivinar el personaje.")
            self.aprender_personaje()

    def iniciar(self):
        jugar_de_nuevo = True
        while jugar_de_nuevo:
            self.jugar()
            jugar_de_nuevo = self.hacer_pregunta("\n¿Quieres volver a jugar?")

# Ejecutar el juego
if __name__ == "__main__":
    juego = Akinator()
    juego.iniciar()
