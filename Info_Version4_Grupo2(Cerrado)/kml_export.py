# kml_export.py

# Esta función obtiene la longitud y latitud de un nodo (preferentemente NavPoint)
def get_lon_lat(node):
    if hasattr(node, 'lon') and hasattr(node, 'lat'):
        return node.lon, node.lat  # esto ocurre cuando el nodo es un NavPoint con coordenadas geográficas reales
    elif hasattr(node, 'x') and hasattr(node, 'y'):
        return node.x, node.y  # esto ocurre si el nodo es un Node con coordenadas "planas" (menos preciso)
    else:
        return 0, 0  # fallback si no hay coordenadas (no recomendable)

# Exporta el grafo (y opcionalmente un camino) a un archivo KML estándar
def export_to_kml(graph, path=None, filename="export.kml", color="ff0000ff", node_icon_url=None):
    # Define el encabezado XML del archivo KML
    def kml_header():
        return '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'

    # Cierra correctamente el archivo KML
    def kml_footer():
        return '</Document>\n</kml>'

    # Cambia la opacidad de un color KML (formato AABBGGRR)
    def change_opacity(color, alpha_hex):
        return alpha_hex + color[2:]  # esto ocurre para generar transparencia en segmentos no principales

    # Crea un marcador para un nodo
    def point_placemark(node, name_override=None, icon_href=None, icon_color="ffffffff"):
        lon, lat = get_lon_lat(node)  # obtiene coordenadas geográficas
        icon = icon_href or "http://maps.google.com/mapfiles/kml/paddle/red-circle.png"  # ícono por defecto
        name = name_override if name_override else node.name  # nombre del nodo en el KML
        return f"""<Placemark>
  <name>{name}</name>
  <Style>
    <IconStyle>
      <color>{icon_color}</color>
      <Icon><href>{icon}</href></Icon>
    </IconStyle>
  </Style>
  <Point><coordinates>{lon},{lat},0</coordinates></Point>
</Placemark>
"""

    # Dibuja una línea (segmento o ruta) en el KML
    def path_placemark(nodes, color, name="Ruta", width=2):
        coords = "\n".join(f"{get_lon_lat(n)[0]},{get_lon_lat(n)[1]},0" for n in nodes)
        return f"""<Placemark>
  <name>{name}</name>
  <Style>
    <LineStyle><color>{color}</color><width>{width}</width></LineStyle>
  </Style>
  <LineString><coordinates>{coords}</coordinates></LineString>
</Placemark>
"""

    # Almacena los nodos que forman parte del camino principal
    path_nodes = set(path) if path else set()
    path_segments = set()

    # Extrae solo los segmentos que forman parte del camino (para resaltarlos)
    if path:
        for i in range(len(path) - 1):
            for seg in graph.segments:
                if (seg.origin == path[i] and seg.destination == path[i+1]) or (seg.origin == path[i+1] and seg.destination == path[i]):
                    path_segments.add(seg)
                    break  # solo se necesita un segmento por par de nodos

    # Empieza a escribir el archivo KML
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(kml_header())

        # Exporta todos los segmentos, resaltando los del camino principal
        for segment in graph.segments:
            if segment in path_segments:
                seg_color = color        # color completo para segmentos del camino
                width = 4
            else:
                seg_color = change_opacity(color, "66")  # semitransparente para el resto
                width = 2
            f.write(path_placemark([segment.origin, segment.destination], seg_color, name=segment.name, width=width))

        # Exporta todos los nodos, usando color diferente si están en la ruta
        for node in graph.nodes:
            if node in path_nodes:
                icon_color = "ffffffff"  # color blanco opaco para nodos del camino
            else:
                icon_color = "66ffffff"  # color blanco semitransparente para el resto
            f.write(point_placemark(node, icon_href=node_icon_url, icon_color=icon_color))

        # Vuelve a exportar la ruta principal encima (línea gruesa)
        if path and len(path) > 1:
            f.write(path_placemark(path, color, name="Ruta principal", width=6))

        # Cierra el archivo
        f.write(kml_footer())


# Exporta una animación de avión usando gx:Track para Google Earth
def export_track_kml(path, filename="animated_plane.kml", start_time="2025-01-01T00:00:00Z", duration_seconds=60):
    # Encabezado especial que incluye soporte para gx (Google Earth Extensions)
    def kml_header():
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2"\n'
            '     xmlns:gx="http://www.google.com/kml/ext/2.2">\n'
            '<Document>\n'
        )

    # Cierre estándar
    def kml_footer():
        return '</Document>\n</kml>'

    # Crea un <gx:Track> con coordenadas y tiempos interpolados
    def gx_track(path, start_time, duration_seconds):
        from datetime import datetime, timedelta
        base_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")  # inicio de animación
        step = timedelta(seconds=duration_seconds // max(1, len(path.path)-1))  # tiempo entre puntos

        track = """<Placemark>
  <name>Avión animado</name>
  <Style>
    <IconStyle>
      <scale>1.2</scale>
      <Icon>
        <href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>
      </Icon>
    </IconStyle>
  </Style>
  <gx:Track>\n"""

        # Añade una entrada de tiempo y coordenadas por nodo del camino
        for i, node in enumerate(path.path):
            time_str = (base_time + i * step).strftime("%Y-%m-%dT%H:%M:%SZ")
            lon, lat = get_lon_lat(node)
            track += f"    <when>{time_str}</when>\n"
            track += f"    <gx:coord>{lon} {lat} 0</gx:coord>\n"

        track += "  </gx:Track>\n</Placemark>\n"
        return track

    # Genera el archivo KML animado
    with open(filename, "w", encoding='utf-8') as f:
        f.write(kml_header())
        f.write(gx_track(path, start_time, duration_seconds))
        f.write(kml_footer())
