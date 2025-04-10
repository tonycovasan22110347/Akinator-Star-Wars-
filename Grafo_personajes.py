import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import json

# Cargar personajes desde el archivo JSON
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

# Crear grafo de un solo personaje con solo las características verdaderas
def crear_grafo_personaje(personaje):
    G = nx.Graph()

    # Nodo principal (personaje)
    G.add_node(personaje["nombre"], tipo="personaje")
    
    # Características con valor True
    caracteristicas = {
        "Es Droide": personaje["es_droide"],
        "Es Alienígena": personaje["es_alienigena"],
        "Usa Blaster": personaje["usa_blaster"],
        "Es Jedi": personaje["es_jedi"],
        "Es Sith": personaje["es_sith"],
        "Es Humano": personaje["es_humano"],
        "Es Mujer": personaje["es_mujer"],
        "Usa Fuerza": personaje["usa_fuerza"],
        "Tiene Máscara": personaje["tiene_mascara"],
        "Lado Oscuro": personaje["lado_oscuro"],
        "Usa Sable de Luz": personaje["usa_sable_de_luz"],
        "Usa Casco": personaje["usa_casco"],
        "Usa Armadura": personaje["usa_armadura"]
    }

    # Solo añadir características verdaderas
    for caracteristica, valor in caracteristicas.items():
        if valor:
            G.add_node(caracteristica, tipo="caracteristica")
            G.add_edge(personaje["nombre"], caracteristica)
    
    return G

# Guardar todos los grafos en un PDF
def guardar_grafos_en_pdf(personajes):
    with PdfPages("grafos_personajes_limpios.pdf") as pdf:
        for personaje in personajes:
            grafo = crear_grafo_personaje(personaje)

            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(grafo, seed=42, k=0.8)

            # Dibujar nodos
            nx.draw_networkx_nodes(grafo, pos, node_size=1000, node_color="lightblue", edgecolors="black")

            # Dibujar aristas
            nx.draw_networkx_edges(grafo, pos, width=2, alpha=0.5)

            # Dibujar solo las etiquetas dentro del nodo
            nx.draw_networkx_labels(grafo, pos, font_size=10, font_weight="bold", font_color="black")

            plt.title(f"{personaje['nombre']} - Características verdaderas")
            plt.axis("off")
            pdf.savefig()
            plt.close()

# Ejecutar
if __name__ == "__main__":
    personajes = cargar_personajes()
    
    if personajes:
        guardar_grafos_en_pdf(personajes)
        print("✅ ¡PDF generado sin textos superpuestos! Solo se muestran las etiquetas en los nodos.")
    else:
        print("No se pudo generar el PDF debido a un error con el archivo de personajes.")

