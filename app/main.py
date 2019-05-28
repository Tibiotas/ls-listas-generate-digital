# -*- coding: utf-8 -*-
import peewee
import threading
from six.moves.urllib.request import urlopen
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup
import SimpleHTTPServer
import SocketServer
import time
from datetime import date
from datetime import timedelta

PORT_API = 5000
PORT_WEB = 5001

def run_app2():
    app = Flask(__name__, static_url_path='')
    CORS(app)

    @app.route('/semanas/<int:qtd>/<int:dia>/<int:mes>/<int:ano>')
    def semanas(qtd, dia, mes, ano):
        semanas = []
        datePrincipal = date(ano, mes, dia)
        data = {}

        for x in range(0, qtd):
            semanas.append([]);
            for y in range(0, 2):
                semanas[x].append([]);
                link = "https://wol.jw.org/bzs/wol/dt/r402/lp-lsb/"+str(datePrincipal.year)+"/"+str(datePrincipal.month)+"/"+str(datePrincipal.day)
                response = urlopen(link)
                content = response.read()
                soup = BeautifulSoup(content, 'html.parser')
                
                data = {
                    'semana': soup.find(id='p1').text ,
                    'biblia_semana': soup.find(id='p2').text,
                    'cantico_inicio': soup.find(id='p3').a.text,
                    'cantico_meio': soup.find(id='section4').findChildren('p')[0].a.text,
                    'cantico_final': soup.find(id='section4').findChildren('p')[-1].a.text,
                    'estudo_biblico_congregacao': soup.find(id='section4').findChildren('p')[-3].text.replace(' E', 'E'),
                    'tesouros_palavra_de_deus_1': soup.find(id='section2').find(id='p6').a.text,
                    'tesouros_palavra_de_deus_2': soup.find(id='section2').find(id='p10').strong.text.replace(': ', ''),
                    'leitura_biblia': soup.find(id='section2').find(id='p15').findChildren('a')[0].text,
                    'leitura_biblia_licao': soup.find(id='section2').find(id='p15').findChildren('a')[1].text,
                    'faca_seu_melhor_1': soup.find(id='section3').findChildren('p')[0].strong.text.replace(': ', '') if len(soup.find(id='section3').findChildren('p')) > 0 else None,
                    'faca_seu_melhor_2': soup.find(id='section3').findChildren('p')[1].strong.text.replace(': ', '') if len(soup.find(id='section3').findChildren('p')) > 1 else None,
                    'faca_seu_melhor_3': soup.find(id='section3').findChildren('p')[2].strong.text.replace(': ', '') if len(soup.find(id='section3').findChildren('p')) > 2 else None,
                    'faca_seu_melhor_4': soup.find(id='section3').findChildren('p')[3].strong.text.replace(': ', '') if len(soup.find(id='section3').findChildren('p')) > 3 else None,
                    'nossa_vida_crista_1': soup.find(id='section4').findChildren('p')[1].strong.text if len(soup.find(id='section4').findChildren('p')[1].findChildren('strong')) < 2 else soup.find(id='section4').findChildren('p')[1].findChildren('strong')[1].text,
                    'nossa_vida_crista_2': (soup.find(id='section4').findChildren('p')[2].strong.text if len(soup.find(id='section4').findChildren('p')[2].findChildren('strong')) < 2 else soup.find(id='section4').findChildren('p')[2].findChildren('strong')[1].text) if len(soup.find(id='section4').findChildren('p')) > 5 else None,
                }
                semanas[x][y] = data
                datePrincipal = datePrincipal + timedelta(days=7)

        return jsonify(semanas);

    @app.route('/semana/<int:dia>/<int:mes>/<int:ano>')
    def semana(dia, mes, ano):
        link = "https://wol.jw.org/bzs/wol/dt/r402/lp-lsb/"+str(ano)+"/"+str(mes)+"/"+str(dia)
        response = urlopen(link)
        content = response.read()
        soup = BeautifulSoup(content, 'html.parser')

        return jsonify({
                'semana': soup.find(id='p1').text ,
                'biblia_semana': soup.find(id='p2').text,
                'cantico_inicio': soup.find(id='p3').a.text,
                'cantico_meio': soup.find(id='section4').findChildren('p')[0].a.text,
                'cantico_final': soup.find(id='section4').findChildren('p')[-1].a.text,
                'estudo_biblico_congregacao': soup.find(id='section4').findChildren('p')[-3].text.replace(' E', 'E'),
                'tesouros_palavra_de_deus_1': soup.find(id='section2').find(id='p6').a.text,
                'tesouros_palavra_de_deus_2': soup.find(id='section2').find(id='p10').strong.text.replace(': ', ''),
                'leitura_biblia': soup.find(id='p15').findChildren('a')[0].text,
                'leitura_biblia_licao': soup.find(id='p15').findChildren('a')[1].text,
                'faca_seu_melhor_1': soup.find(id='section3').findChildren('p')[0].strong.text.replace(': ', '') if len(soup.find(id='section3').findChildren('p')) > 0 else None,
                'faca_seu_melhor_2': soup.find(id='section3').findChildren('p')[1].strong.text.replace(': ', '') if len(soup.find(id='section3').findChildren('p')) > 1 else None,
                'faca_seu_melhor_3': soup.find(id='section3').findChildren('p')[2].strong.text.replace(': ', '') if len(soup.find(id='section3').findChildren('p')) > 2 else None,
                'faca_seu_melhor_4': soup.find(id='section3').findChildren('p')[3].strong.text.replace(': ', '') if len(soup.find(id='section3').findChildren('p')) > 3 else None,
                'nossa_vida_crista_1': soup.find(id='section4').findChildren('p')[1].strong.text.replace(': ', '') if len(soup.find(id='section4').findChildren('p')[1].findChildren('strong')) < 2 else soup.find(id='section4').findChildren('p')[1].findChildren('strong')[1].text,
                'nossa_vida_crista_2': soup.find(id='section4').findChildren('p')[2].strong.text.replace(': ', '') if len(soup.find(id='section4').findChildren('p')) > 5 else None,
                })

    app.config.update(JSON_AS_ASCII=False)
    app.run(debug=True, port=PORT_API, use_reloader=False)

class HTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

def run_app1():
    httpd = SocketServer.TCPServer(("", PORT_WEB), HTTPRequestHandler)
    print "Iniciando gerador de lista no link: http://localhost:", PORT_WEB
    httpd.serve_forever()

t1 = threading.Thread(target=run_app1)
t1.setDaemon(True)
t1.start()
t2 = threading.Thread(target=run_app2)
t2.setDaemon(True)
t2.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    exit(0)