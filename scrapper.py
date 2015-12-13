import sys
import logging
import pickle
import glob
from pyquery import PyQuery
import pypandoc
import dateparser
from slugify import slugify


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"}

pages = range(1760, -1, -40)
pages[-1] = 1


def get_all_links():

    try:
        return pickle.load(open('.links'))
    except IOError:
        URL_BASE = "http://www.casarosada.gob.ar/informacion/discursos?start={}"
        links = []
        for start in pages:
            url = URL_BASE.format(start)
            logging.info('Descargando links desde {}'.format(url))
            pq = PyQuery(url=url, headers=headers)
            pq.make_links_absolute()
            page_links = pq('div.category-item-title a')

            links.extend(list(reversed(page_links)))
        links = [pq(a).attr('href') for a in links]
        pickle.dump(links, open('.links', 'w'))
        return links


def faltantes():
    bajados = {int(l.split('.')[0]) - 1 for l in glob.glob('*.md')}
    links = get_all_links()
    faltan = set(range(len(links))) - bajados
    return [links[i] if i in faltan else None for i in range(len(links))]


for did, url in enumerate(faltantes()):
    if not url:
        continue
    try:
        d = PyQuery(url=url, headers=headers)

        # cleanups
        d.remove('ul.actions, #fb-root, script, div[style="clear:both"]')
        for cf in d('.clearfix'):
            if d(cf).text() == "":
                d(cf).remove()

        fecha = d('dd.published').text()
        d('.article-info').before(u'<p>[{}]</p>'.format(fecha))
        d.remove('.article-info')

        # no link in the title
        titulo = d('.item-page h2 a').text().decode('utf8')
        d('.item-page h2').text(titulo)

        # clean html content
        discurso = d('.item-page').html()
        import ipdb;ipdb.set_trace()
        fecha = dateparser.parse(fecha, languages=['es'])
        filename = "{did:0=4d}.{fecha}.{titulo}.md".format(did=did + 1, fecha=fecha.strftime('%d-%m-%Y'), titulo=slugify(titulo))
        logging.info('Guardando {}...'.format(filename))
        output = pypandoc.convert(discurso, 'md', format='html', outputfile=filename)
    except Exception:
        logging.exception('ID: {} |  URL: {}'.format(d, url))