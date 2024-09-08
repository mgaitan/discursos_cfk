# Discursos de Cristina Fernandez de Kirchner

Todos los discursos de Cristina Fernandez de Kirchner como Presidenta de la Nación desde el 10 de diciembre de 2007, en formato de texto (markdown)


- Hasta el discurso del 10-12-2015 fueron obtenidos via `screapper.py` desde http://www.casarosada.gob.ar/informacion/discursos/
- Los posteriores fueron obtenidos desde el sitio oficial de CFK https://www.cfkargentina.com/ via `scrapper_cfkargentina.py`


## ¿cómo ejecutar el scrapper?

```
pip install -r requirements.py
python scrapper.py
```

luego agrupé desde ipython

```
In [1]: for a in range(2007, 2016):
   ...:     !mkdir {a}
   ...:     !git mv *{a}*.md {a}
```


### atención

Los siguiente articulos no pudieron ser obtenidos por error 404

```
265. http://www.casarosada.gob.ar/informacion/discursos/20099-blank-80914256
266. http://www.casarosada.gob.ar/informacion/discursos/20101-blank-47559486
267. http://www.casarosada.gob.ar/informacion/discursos/20106-blank-63091205
590. http://www.casarosada.gob.ar/informacion/discursos/21618-blank-84642414
591. http://www.casarosada.gob.ar/informacion/discursos/21621-blank-39411822
593. http://www.casarosada.gob.ar/informacion/discursos/21630-blank-64824131
594. http://www.casarosada.gob.ar/informacion/discursos/21633-blank-30188586
595. http://www.casarosada.gob.ar/informacion/discursos/21636-blank-60437797
596. http://www.casarosada.gob.ar/informacion/discursos/21638-blank-56772362
597. http://www.casarosada.gob.ar/informacion/discursos/21639-blank-43563728
598. http://www.casarosada.gob.ar/informacion/discursos/21642-blank-21984009
599. http://www.casarosada.gob.ar/informacion/discursos/21644-blank-22621977
600. http://www.casarosada.gob.ar/informacion/discursos/21649-blank-17080375
637. http://www.casarosada.gob.ar/informacion/discursos/21813-blank-53373529
638. http://www.casarosada.gob.ar/informacion/discursos/21816-blank-87473672
766. http://www.casarosada.gob.ar/informacion/discursos/22328-blank-8284793
809. http://www.casarosada.gob.ar/informacion/discursos/22477-blank-47254815
1023. http://www.casarosada.gob.ar/informacion/discursos/6185-palabras-de-la-presidenta-en-la-inauguracion-de-la-fabrica-de-computadoras-bangho-en-vicente-lopez
1053. http://www.casarosada.gob.ar/informacion/discursos/6246-lanzamiento-del-plan-federal-de-ganados-y-carnes-discurso-de-la-presidenta-cristina-fernandez
1068. http://www.casarosada.gob.ar/informacion/discursos/23252-blank-87320479
1154. http://www.casarosada.gob.ar/informacion/discursos/25428-acto-de-entrega-del-nuevo-dni-numero-10-millones-e-inauguracion-de-un-nuevo-centro-de-documentacion-palabras-de-la-presidenta-de-la-nacion
1241. http://www.casarosada.gob.ar/informacion/discursos/25815-carta-de-la-sra-presidenta-leida-por-el-canciller-en-el-acto-de-reconocimiento-a-la-politica-de-derechos-humanos-del-presidente-nestor-kirchner-por-parte-de-la-universidad-de-padua
1256. http://www.casarosada.gob.ar/informacion/discursos/25870-presentacion-ante-la-asamblea-legislativa-de-angola-discurso-de-la-presidenta-de-la-nacion
1270. http://www.casarosada.gob.ar/informacion/discursos/25933-argentina-no-va-a-convalidar-el-golpe-en-paraguay-palabras-de-la-presidenta-de-la-nacion
```