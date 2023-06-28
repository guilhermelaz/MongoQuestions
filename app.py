import random

from flask import (
    Flask, render_template, request, redirect, url_for, current_app, send_file
)
from database import db_provas
from bson import ObjectId

from docx import Document
from docxtpl import DocxTemplate

import os


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'secret'


#########
# ROTAS #
#########


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/provas/questoes', methods=['GET', 'POST'])
def questoes():
    if request.method == 'GET':
        questoes_list = list(db_provas.questoes.find())
        options = list(db_provas.options.find())
        return render_template('lista_de_questoes.html', questoes=questoes_list, options=options)
    if request.method == 'POST':
        option = request.form.get("selectedOption")
        palavra_chave = request.form.get("chave")
        options = list(db_provas.options.find())

        if option == 'titulo':
            option = 'enunciado'  # No banco o titulo é enunciado

        print("Opção de pesquisa: " + option)

        questoes_list = list(db_provas.questoes.find(
            {
                option: {'$regex': palavra_chave, '$options': 'i'}
            }
        )
        )

        return render_template('lista_de_questoes.html', questoes=questoes_list, options=options)


@app.route('/provas/questoes/nova', methods=['GET', 'POST'])
def nova_questao():
    if request.method == 'GET':
        return render_template('nova_questao.html', action="nova")
    elif request.method == 'POST':
        numero = request.form.get('numero')
        enunciado = request.form.get('enunciado')
        categoria = request.form.get('categoria')

        alternativa1 = request.form.get('alternativa1')
        correta1 = request.form.get('correta1') == 'True'
        alternativa2 = request.form.get('alternativa2')
        correta2 = request.form.get('correta2') == 'True'
        alternativa3 = request.form.get('alternativa3')
        correta3 = request.form.get('correta3') == 'True'
        alternativa4 = request.form.get('alternativa4')
        correta4 = request.form.get('correta4') == 'True'
        alternativa5 = request.form.get('alternativa5')
        correta5 = request.form.get('correta5') == 'True'

        new_question = {
            "numero": numero,
            "enunciado": enunciado,
            "categoria": categoria,
            "alternativas": [
                {"alt": alternativa1, "ver": correta1},
                {"alt": alternativa2, "ver": correta2},
                {"alt": alternativa3, "ver": correta3},
                {"alt": alternativa4, "ver": correta4},
                {"alt": alternativa5, "ver": correta5}
            ]
        }

        db_provas.questoes.insert_one(new_question)

        return redirect(url_for('questoes'))


@app.route('/provas/questoes/excluir/<q_id>', methods=['GET'])
def excluir_questao(q_id):
    db_provas.questoes.delete_one({"_id": ObjectId(q_id)})
    return redirect(url_for('questoes'))


@app.route('/provas/questoes/<q_id>', methods=['GET', 'POST'])
def questao(q_id):
    if request.method == 'GET':
        q = db_provas.questoes.find_one({"_id": ObjectId(q_id)})
        return render_template('view_questao.html', questao=q)
    elif request.method == 'POST':
        numero = request.form.get('numero')
        enunciado = request.form.get('enunciado')
        categoria = request.form.get('categoria')

        alternativa1 = request.form.get('alternativa1')
        correta1 = request.form.get('correta1') == 'True'
        alternativa2 = request.form.get('alternativa2')
        correta2 = request.form.get('correta2') == 'True'
        alternativa3 = request.form.get('alternativa3')
        correta3 = request.form.get('correta3') == 'True'
        alternativa4 = request.form.get('alternativa4')
        correta4 = request.form.get('correta4') == 'True'
        alternativa5 = request.form.get('alternativa5')
        correta5 = request.form.get('correta5') == 'True'

        updated_question = {
            "numero": numero,
            "enunciado": enunciado,
            "categoria": categoria,
            "alternativas": [
                {"alt": alternativa1, "ver": correta1},
                {"alt": alternativa2, "ver": correta2},
                {"alt": alternativa3, "ver": correta3},
                {"alt": alternativa4, "ver": correta4},
                {"alt": alternativa5, "ver": correta5}
            ]
        }

        db_provas.questoes.update_one({"_id": ObjectId(q_id)}, {"$set": updated_question})

        return redirect(url_for('questoes'))


@app.route('/provas/gerar', methods=['GET', 'POST'])
def gerar_prova():
    if request.method == 'GET':

        questoes = list(db_provas.questoes.find())
        random.shuffle(questoes)
        questoes = questoes[:5]

        template_path = os.path.join(current_app.root_path, 'templates', 'prova.docx')
        template = DocxTemplate(template_path)

        context = {
            'questoes': questoes
        }

        template.render(context)

        document_path = os.path.join(current_app.root_path, 'static', 'prova.docx')
        template.save(document_path)
        return send_file(document_path, as_attachment=True)
        # return render_template('gerar_prova.html', questoes=questoes)


if __name__ == '__main__':
    app.run(debug=True)
