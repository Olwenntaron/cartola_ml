#!/usr/bin/python3
# coding: utf-8
from multiprocessing.dummy import Pool as ThreadPool
from collections import OrderedDict
import json
import requests
import csv
import time


def get_json(url):
    try:
        content = requests.get(url).content
        try:
            j = json.loads(str(content, 'utf-8'))
            return j['atleta']
        except ValueError:
            return None
    except requests.ConnectionError:
        return None

    
def decode_json(j):
    d = OrderedDict((
        ('apelido'    , j['apelido']),
        ('posicao'    , j['posicao']['nome']),
        ('clube'      , j['clube']['nome']),
        ('jogos'      , j['jogos']),
        ('status'     , j['status']),
        ('preco'      , j['preco']),
        ('variacao_pr', j['variacao']),
        ('pontos'     , j['pontos']),
        ('media_pts'  , j['media'])
    ))
    
    scout_headers = ['FS', 'PE', 'A', 'FT', 'FD', 'FF', 'G', 'I', 'PP', 'RB', 'FC', 'GC', 'CA', 'CV', 'SG', 'DD', 'DP', 'GS']
    for h in scout_headers:
        for i in j['scout']:
            if h == i['nome']:
                d[h] = i['quantidade']
        if h not in d.keys():
            d[h] = 0
    return d


num_pages = 41
atletas = []
for i in range(num_pages):
    url = "http://cartolafc.globo.com/mercado/filtrar.json?page=%s&order_by=preco" % str(i+1)
    print("Baixando json da url: %s" % url)
    
    j = get_json(url)
    while not j:
        print("Falha na pagina %d. Tentando novamente..." % (i+1))
        j = get_json(url)
        time.sleep(5)
    atletas.extend(j)
    
# salva os dados crus
with open('raw.json', 'w') as f:
    f.writelines(str(i) for i in atletas)

# formata os dados e salva como um arquivo csv
pool = ThreadPool(8)
atletas = pool.map(decode_json, atletas)
with open('jogadores.csv', 'w') as f:
    w = csv.DictWriter(f, atletas[0].keys())
    w.writeheader()
    for row in atletas:
        #print(row)
        w.writerow(row)
