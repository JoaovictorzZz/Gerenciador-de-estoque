from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Cria a aplicação Flask
app = Flask(__name__, template_folder="templates")

# Configuração do banco SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Modelo que o SQLAlchemy vai usar pra criar o code SQL 
class Produto(db.Model):
    __tablename__ = "produtos"   # nome da tabela no banco
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

# Rota principal
@app.route("/")
def index():
    produtos = Produto.query.all()
    total = sum([p.quantidade for p in produtos])
    top = max(produtos, key=lambda p: p.quantidade) if produtos else None
    return render_template("index.html", produtos=produtos, total=total, top=top)

# Adicionar produto
@app.route("/adicionar", methods=["POST"])
def adicionar():
   try:
    nome = request.form["nome"]
    quantidade = int(request.form["quantidade"])
    novo = Produto(nome=nome, quantidade=quantidade)
    if not nome:
        return """
            <script>
                alert("Erro: O nome do produto não pode estar vazio!");
                window.location.replace = "/";
            </script>
            """
    elif not quantidade:
       return """
            <script>
                alert("Erro: A quantidade do produto não pode estar vazia!");
                window.location.replace = "/";
            </script>
            """
    db.session.add(novo)
    db.session.commit()
    return redirect("/")
   #tratando erros e respondendo com alerts em JS
   except KeyError:
     return """
        <script>
        alert("Erro: campos obrigatorios nao enviados!")
        window.location.href = "/";
        <script/>
        """
   except ValueError:
    return """
            <script>
                alert("Erro: quantidade inválida! Digite um número.");
                window.location.href = "/";
            </script>
        """

# Remover quantidade
@app.route("/remover", methods=["POST"])
def remover():
    nome = request.form["nome"]
    quantidade = int(request.form["quantidade"])
    produto = Produto.query.filter_by(nome=nome).first()
    if produto and produto.quantidade > 0:
        produto.quantidade -= quantidade
        db.session.commit()
    if not quantidade:
        return
    '''
    <script>alert("Erro campos obrigatorios não enviados")
        '''
    return redirect("/")

# Apagar produto
@app.route("/apagar", methods=["POST"])
def apagar():
    nome = request.form["nome"]
    produto = Produto.query.filter_by(nome=nome).first()
    if produto:
        db.session.delete(produto)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
