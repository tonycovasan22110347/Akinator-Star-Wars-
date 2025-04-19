import json
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Cargar base de datos
with open("personajes.json", "r") as f:
    personajes = json.load(f)

# Guardar todos los grafos en un solo PDF
from matplotlib.backends.backend_pdf import PdfPages

# Crear PDF
pdf_path = "grafos_personajes_starwars.pdf"
with PdfPages(pdf_path) as pdf:
    for nombre, caracteristicas in personajes.items():
        # Crear grafo
        G = nx.Graph()
        G.add_node(nombre)
        for caracteristica, valor in caracteristicas.items():
            if valor:
                G.add_node(caracteristica)
                G.add_edge(nombre, caracteristica)

        # Dibujar grafo
        plt.figure(figsize=(6, 6))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=9, font_weight='bold')
        plt.title(nombre)

        # Guardar como página en PDF
        pdf.savefig()
        plt.close()

print(f"✅ PDF generado exitosamente: {pdf_path}")
