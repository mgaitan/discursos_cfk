from pyquery import PyQuery
import pypandoc
import dateparser
from slugify import slugify



URL_BASE = "http://www.casarosada.gob.ar/informacion/discursos?start={}"
headers = {'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"}
pages = range(1760, -1, -40)
pages[-1] = 1
did = 1

for start in pages:
    pq = PyQuery(url=URL_BASE.format(start), headers=headers)
    pq.make_links_absolute()
    links = pq('div.category-item-title a')
    for a in reversed(links):
        url = pq(a).attr('href')
        d = PyQuery(url=url, headers=headers)

        # cleanups
        d.remove('ul.actions, #fb-root, script, .clearfix, div[style="clear:both"]')

        # no link in the title
        titulo = d('.item-page h2 a').text()
        d('.item-page h2').text(titulo)

        # clean html content
        discurso = d('.item-page').html()

        fecha = dateparser.parse(d('dd.published').text(), languages=['es'])
        filename = "{did:0=4d}.{fecha}.{titulo}.md".format(did=did, fecha=fecha.strftime('%d-%m-%Y'), titulo=slugify(titulo))

        print('Descargando {}...'.format(filename))
        output = pypandoc.convert(discurso, 'md', format='html', outputfile=filename)
        did += 1