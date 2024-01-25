from flask import Flask, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

    #configuração padrão de DB na 9 linha.
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db_matriculas'  # Substitua pelas suas informações de conexão MySQL

db = SQLAlchemy(app)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    periodo = db.Column(db.String(100), nullable=False)
    comentarios = db.Column(db.Text)
    mensagem_pais = db.Column(db.Text)


class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    disciplina = db.Column(db.String(100), nullable=False)
    nota = db.Column(db.Float, nullable=False)

@app.route('/aluno', methods=['GET', 'POST'])

#CADASTRAR ALUNO

def cria_aluno():
    body = request.get_json()

    #validar se veio os parâmetros.

    try:
        aluno = Aluno(nome= body['nome'], email= body['email'], curso= body['curso'], periodo= body['periodo'], comentarios= body['comentarios'], mensagem_pais= body['mensagem_pais'])
        db.session.add(aluno)
        db.session.commit()
        return gera_response(201, 'aluno', aluno.to_json(), 'criado com sucesso')
    except Exception as e:
        print(e)
        return gera_response(400, 'aluno', {}, 'Erro ao cadastrar')


#ATUALIZAR
#@app.route('/aluno/<id>, methods=['PUT'])
#def atualiza_aluno(id):
    #PEGA O ALUNO
    #aluno = Aluno.query.filter_by(id=id).first()
    #PEGA MODIFICAÇÕES
    #body = request.get_json()

    #try:
        #if('nome' in body):
            #aluno.nome = body['nome']
            #aluno.email = body['email']
            #aluno.curso = body['curso']
            #aluno.periodo = body['periodo']
            #aluno.comentarios = body['comentarios']
            #aluno.mensagem_pais = body['mensagem_pais']



@app.route('/matricula', methods=['GET', 'POST'])
def processar_matricula():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        curso = request.form['curso']
        periodo = request.form['periodo']
        comentarios = request.form['comentarios']
        mensagem_pais = request.form['mensagem_pais']

        novo_aluno = Aluno(nome=nome, email=email, curso=curso, periodo=periodo, comentarios=comentarios, mensagem_pais=mensagem_pais)
        db.session.add(novo_aluno)
        db.session.commit()

        # Após a inserção, redirecione para a página de matrícula
        return redirect('/matricula')

    alunos = Aluno.query.all()
    notas = Nota.query.all()
 

    return render_template('matricula.html', alunos=alunos, notas=notas)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

