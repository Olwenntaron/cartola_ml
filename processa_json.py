#!/usr/bin/python
# encoding: utf-8
from multiprocessing.dummy import Pool as ThreadPool
from collections import OrderedDict
import csv
import json

with open("raw.json", 'r') as f:
    atletas = eval(f.read())

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

    if d['clube'] == j['partida_clube_visitante']['nome']:
        d['proximo_adversario'] = j['partida_clube_casa']['nome']
        d['proxima_em_casa'] = False
    else:
        d['proximo_adversario'] = j['partida_clube_visitante']['nome']
        d['proxima_em_casa'] = True
        
    return d

pool = ThreadPool(8)
atletas = [decode_json(i) for i in atletas]

with open('jogadores.csv', 'w') as f:
    w = csv.DictWriter(f, atletas[0].keys())
    w.writeheader()
    for row in atletas:
        #print(row)
        w.writerow(row)
