import peewee
from flask import Flask, jsonify, request

app = Flask(__name__)
# GET /musicas/
@app.route('/semana')
def musicas():
    return jsonify([musica.to_dict() for musica in Musica.select()])

# GET /musica/1
@app.route('/semana/<int:codigo>')
def musica(codigo):
    try:
        musica = Musica.get(codigo=codigo)
        return jsonify(musica.to_dict())
    except Musica.DoesNotExist:
        return jsonify({'status': 404, 'mensagem': 'Musica não encontrada'})

# POST /musica/
@app.route('/semana', methods=['POST'])
def nova_musica():
    try:
        print(request.json)
        dados = request.json
        musica = Musica(titulo=dados['titulo'], artista=dados['artista'], ano=dados['ano'])
        musica.save()
        return jsonify({'status': 200, 'mensagem': 'Musica salva com sucesso!'})
    except Exception as e:
        print(e)
        return jsonify({'status': 500, 'mensagem': 'Erro interno do servidor. Algum erro aconteceu!'})

# PUT/PATCH /postagens/1
@app.route('/semana/<int:codigo>', methods=['PUT', 'PATCH'])
def editar_musica(codigo):
    dados = request.json

    try:
        musica = Musica.get(codigo=codigo)
    except Musica.DoesNotExist as e:
        return jsonify({'status': 404, 'mensagem': 'Musica não encontrada'})

    musica.titulo = dados['titulo']
    musica.artista = dados['artista']
    musica.ano = dados['ano']
    musica.save()
    return jsonify({'status': 200, 'mensagem': 'Musica atualizada com sucesso'})

# DELETE /postagens/1
@app.route('/semana/<int:codigo>', methods=['DELETE'])
def apagar_musica(codigo):
    try:
        musica = Musica.get(codigo=codigo)
        musica.delete_instance()
        return jsonify({'status': 200, 'mensagem': 'Musica excluída com sucesso'})
    except Musica.DoesNotExist:
        return jsonify({'status': 404, 'mensagem': 'Musica não encontrada'})

if __name__ == '__main__':
    app.run(debug=True,port=8000)
