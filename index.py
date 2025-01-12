from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Criação da instância da aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados (SQLite, por exemplo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilitar o rastreamento de modificações

# Inicializando o banco de dados
db = SQLAlchemy(app)

# Definindo o modelo Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome}>'

# Criando as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Rota inicial
@app.route('/')
def hello_world():
    return 'Olá, Mundo! Bem-vindo ao Controle de Estoque!'

# Rota para adicionar um produto
@app.route('/produto', methods=['POST'])
def adicionar_produto():
    data = request.get_json()
    if 'nome' not in data or 'quantidade' not in data or 'preco' not in data:
        return jsonify({'error': 'Dados insuficientes!'}), 400
    
    novo_produto = Produto(
        nome=data['nome'],
        quantidade=data['quantidade'],
        preco=data['preco']
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({'message': 'Produto adicionado com sucesso!'}), 201

# Rota para listar os produtos
@app.route('/estoque', methods=['GET'])
def obter_estoque():
    produtos = Produto.query.all()
    return jsonify([{'id': produto.id, 'nome': produto.nome, 'quantidade': produto.quantidade, 'preco': produto.preco} for produto in produtos]), 200

if __name__ == '__main__':
    app.run(debug=True)

