from flask import Flask, render_template, session, request, jsonify, url_for, redirect
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL UNIQUE, 
            data_aniversario TEXT NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Nova Coluna
        )
    ''')

    # TABELA: Avaliações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            comentario TEXT NOT NULL,
            estrelas INTEGER NOT NULL,
            data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


app = Flask(__name__)
app.secret_key = 'chave_secreta_para_tcc' # Necessário para usar session

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Busca as últimas 3 avaliações enviadas
    cursor.execute('SELECT * FROM avaliacoes ORDER BY data_avaliacao DESC LIMIT 3')
    lista_avaliacoes = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', avaliacoes=lista_avaliacoes)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        # Defina aqui seu usuário e senha de administrador
        if usuario == 'admin' and senha == 'pizza123':
            session['admin_logado'] = True
            return redirect(url_for('listar_clientes'))
        else:
            return "<script>alert('Acesso Negado!'); window.history.back();</script>"
            
    return render_template('login.html')

@app.route('/admin/excluir_cliente/<int:id>')
def excluir_cliente(id):
    if not session.get('admin_logado'):
        return redirect(url_for('admin_login'))
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return """
        <script>
            alert('Cliente removido com sucesso!');
            window.location.href = '/admin/clientes';
        </script>
    """

@app.route('/enviar_avaliacao', methods=['POST'])
def enviar_avaliacao():
    nome = request.form.get('nome')
    comentario = request.form.get('comentario')
    estrelas = request.form.get('estrelas')

    if nome and comentario and estrelas:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO avaliacoes (nome, comentario, estrelas) VALUES (?, ?, ?)', 
                       (nome, comentario, estrelas))
        conn.commit()
        conn.close()
        return """
            <script>
                alert('Obrigado pela sua avaliação! ⭐');
                window.location.href = '/#review';
            </script>
        """
    return "Erro ao enviar avaliação.", 400

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logado', None)
    return redirect(url_for('index'))

@app.route('/cadastrar_fidelidade', methods=['POST'])
def cadastrar_fidelidade():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    aniversario = request.form.get('aniversario')

    if nome and telefone and aniversario:
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO clientes (nome, telefone, data_aniversario) VALUES (?, ?, ?)', 
                           (nome, telefone, aniversario))
            conn.commit()
            conn.close()
            # Retornamos um script simples para limpar o formulário e avisar o usuário
            return """
                <script>
                    alert('Cadastro realizado com sucesso! 🎉');
                    window.location.href = '/';
                </script>
            """
        except sqlite3.IntegrityError:
            return """
                <script>
                    alert('Erro: Este número de telefone já está cadastrado no Plano Fidelidade.');
                    window.history.back();
                </script>
            """
    
    return "Erro ao cadastrar. Verifique os campos.", 400

@app.route('/admin/clientes')
def listar_clientes():
    # Verifica se o administrador está logado
    if not session.get('admin_logado'):
        return redirect(url_for('admin_login'))
        
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 1. Buscar todos os clientes para a lista geral
    cursor.execute('SELECT * FROM clientes ORDER BY nome ASC')
    todos_clientes = cursor.fetchall()
    
    # 2. Lógica para Aniversariantes do Dia
    hoje = datetime.now().strftime('%m-%d') # Pega apenas Mês e Dia (ex: 04-02)
    aniversariantes_hoje = []
    
    for cliente in todos_clientes:
        # Ajusta a data do banco (AAAA-MM-DD) para comparar apenas Mês-Dia
        data_nasc = cliente['data_aniversario'] # Ex: 1990-04-02
        if data_nasc[5:] == hoje: 
            aniversariantes_hoje.append(cliente)
            
    conn.close()
    return render_template('lista_clientes.html', 
                           clientes=todos_clientes, 
                           aniversariantes=aniversariantes_hoje)

@app.route('/carrinho')
def view_cart():
    cart_raw = session.get('cart', [])
    items_agrupados = {}

    # Agrupa itens para mostrar quantidade e subtotal por linha
    for item in cart_raw:
        nome = item['nome']
        if nome in items_agrupados:
            items_agrupados[nome]['quantidade'] += 1
            items_agrupados[nome]['preco_total'] += item['preco']
        else:
            items_agrupados[nome] = {
                'nome': nome,
                'preco_unitario': item['preco'],
                'quantidade': 1,
                'preco_total': item['preco']
            }

    lista_final = list(items_agrupados.values())
    total_geral = sum(item['preco'] for item in cart_raw)
    
    return render_template('carrinho.html', items=lista_final, total=total_geral)

@app.route('/update_cart_session', methods=['POST'])
def update_cart_session():
    data = request.get_json()
    session['cart'] = data.get('items', [])
    session.modified = True 
    return jsonify({"status": "success"})

@app.route('/admin/notificar_empresa')
def notificar_empresa():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    hoje = datetime.now().strftime('%m-%d')
    cursor.execute('SELECT nome, telefone FROM clientes')
    todos = cursor.fetchall()
    
    aniversariantes = [c['nome'] for c in todos if c['data_aniversario'][5:] == hoje]
    conn.close()

    if not aniversariantes:
        return "<script>alert('Nenhum aniversariante hoje!'); window.history.back();</script>"

    # Monta a mensagem para a empresa
    lista_nomes = ", ".join(aniversariantes)
    mensagem_empresa = f"📢 *Aviso Pizza Amiga*\nHoje temos {len(aniversariantes)} aniversariante(s):\n\n🎂 {lista_nomes}\n\nNão esqueça de enviar os cupons!"
    
    # Redireciona para o WhatsApp da Empresa (seu número)
    numero_empresa = "5561981953090" 
    url = f"https://wa.me/{numero_empresa}?text={mensagem_empresa}"
    return redirect(url)

@app.route('/get_cart')
def get_cart():
    # Retorna o que está na sessão do servidor
    return jsonify({"items": session.get('cart', [])})

@app.route('/limpar')
def clear_cart():
    session.pop('cart', None)
    session.modified = True # Força o Flask a salvar a sessão vazia
    return redirect(url_for('index'))

@app.context_processor
def inject_aniversariantes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Pega o mês atual (ex: '04')
    mes_atual = datetime.now().strftime('%m')
    
    # Conta quantos clientes fazem aniversário neste mês
    # Usamos o LIKE '%-MM-%' para filtrar o mês na string AAAA-MM-DD
    cursor.execute("SELECT COUNT(*) FROM clientes WHERE data_aniversario LIKE ?", (f'%-{mes_atual}-%',))
    total_mes = cursor.fetchone()[0]
    
    conn.close()
    return dict(total_aniversariantes_mes=total_mes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)