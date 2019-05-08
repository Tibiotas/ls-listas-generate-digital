# -*- coding: utf-8 -*-
import peewee
from six.moves.urllib.request import urlopen
from flask import Flask, jsonify, request, render_template
from bs4 import BeautifulSoup

app = Flask(__name__, static_url_path='')

@app.route('/lista')
def lista():
    return render_template('index.html');

# GET /musicas/
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

if __name__ == '__main__':
    app.config.update(JSON_AS_ASCII=False)
    app.run(debug=True,port=8000)