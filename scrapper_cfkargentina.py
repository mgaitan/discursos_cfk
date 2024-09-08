import sys
import logging
import pickle
import glob
import requests
from pyquery import PyQuery as pq
import pypandoc
import dateparser
from slugify import slugify
from pathlib import Path

# Configurar logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Configuración de headers y páginas
headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"}
BASE_URL = "https://www.cfkargentina.com/category/cfk/discursos/page/{}"


def get_all_links():
    """
    Obtiene todos los enlaces de los discursos y los almacena en un archivo pickle.
    """
    try:
        # Intenta cargar los links previamente guardados
        with open('.links', 'rb') as f:
            return pickle.load(f)
    except IOError:
        links = []
        page_number = 1
        while True:
            url = BASE_URL.format(page_number)
            logging.info(f'Descargando links desde {url}')
            response = requests.get(url, headers=headers)
            if response.status_code != 200 or page_number > 11:
                logging.error(f"Error al obtener la página {page_number}")
                break
            # Usa PyQuery para parsear la página
            doc = pq(response.text)
            doc.make_links_absolute(base_url=url)
            page_links = [a.attr['href'] for a in doc('a.overdefultlink').items()]

            if not page_links:
                break
            links.extend(page_links)
            page_number += 1
        
        # Guarda los links en un archivo .links utilizando 'with' para cerrarlo correctamente
        with open('.links', 'wb') as f:
            pickle.dump(links, f)

        return links


def faltantes():
    """
    Encuentra los discursos que faltan por descargar comparando los archivos ya bajados.
    """
    bajados = {Path(l).stem.split('.')[0] for l in glob.glob('*.md')}
    links = get_all_links()
    faltan = [i for i, link in enumerate(links) if str(i) not in bajados]
    return [links[i] for i in faltan]


def save_discourse(did, url):
    """
    Descarga y guarda el contenido de un discurso en formato markdown.
    """
    try:
        d = pq(url=url, headers=headers)

        # Realizar limpieza del HTML
        d.remove('ul.actions, #fb-root, script, div[style="clear:both"]')

        # Obtén la fecha del discurso usando el selector correcto
        fecha_texto = d('body > div.box_interna > div.box_interna_lefy > div.box_interna_date').text()
        if not fecha_texto:
            logging.error(f"No se pudo encontrar la fecha en la URL {url}")
            return
        fecha = dateparser.parse(fecha_texto, languages=['es'])
        if not fecha:
            logging.error(f"No se pudo parsear la fecha '{fecha_texto}' en la URL {url}")
            return

        # Obtener el título del discurso usando el selector correcto
        titulo = d('body > div.box_interna > div.box_interna_lefy > div.box_interna_titulo').text()
        if not titulo:
            logging.error(f"No se pudo encontrar el título en la URL {url}")
            return
        titulo_slug = slugify(titulo, lowercase=True)

        # Obtener el subtítulo o bajada
        subtitulo = d('body > div.box_interna > div.box_interna_lefy > div.box_interna_subtitulo').text()

        # Obtener los párrafos del contenido del discurso
        contenido_p = "\n".join([p.text().strip() for p in d('body > div.box_interna > div.box_interna_lefy p').items()])
        if not contenido_p:
            logging.error(f"No se pudo encontrar el contenido en la URL {url}")
            return

        # Crear el nombre del archivo con formato: numero.fecha.titulo.md
        filename = f"{did:04d}.{fecha.strftime('%d-%m-%Y')}.{titulo_slug}.md"
        logging.info(f'Guardando {filename}...')

        # Crear el contenido en Markdown
        markdown_content = f"# {titulo}\n\n{subtitulo}\n[{fecha.strftime('%d-%m-%Y')}]\n{contenido_p}"

        # Guardar el archivo en formato Markdown
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

    except Exception as e:
        logging.exception(f'Error procesando {url}: {str(e)}')



def main():
    # Descargar discursos faltantes
    for did, url in enumerate(faltantes()):
        if url:
            logging.info(f'Procesando discurso {did}: {url}')
            save_discourse(did, url)

if __name__ == "__main__":
    main()
