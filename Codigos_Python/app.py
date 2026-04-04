from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
import MySQLdb.cursors
from datetime import datetime, timedelta
import re 
from werkzeug.security import generate_password_hash 
import MySQLdb
from functools import wraps
import pandas as pd
from flask import send_file
import io

app = Flask(__name__)

# --- Configurações (sem alterações) ---
app.secret_key = 'sua_chave_secreta_aqui'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'elcionei'
app.config['MYSQL_DB'] = 'gestao_grm'
mysql = MySQL(app)

# --- MATRIZ DE PERMISSÕES (ESTE BLOCO ESTÁ FALTANDO) ---
PERFIS = {
    'DEVELOPER': { 'full_access' },
    'SUPERVISOR': {
        'ver_dashboard', 'ver_menu_cadastros', 'ver_menu_relatorios',
        'conceder_acesso', 'excluir_registro', 'registrar_frequencia',
        'cadastrar_grm', 'registrar_evento', 'registrar_convertido',
        'cadastrar_supervisor', 'cadastrar_lider', 'cadastrar_colider',
        'cadastrar_lider_treinamento', 'cadastrar_membro', 'cadastrar_visitante',
        'analise_frequencia', 'ver_historico_ofertas', 'analise_menu' # Adicionando novas permissões
    },
    'LIDER': {
        'ver_dashboard', 'ver_menu_cadastros', 'ver_menu_relatorios', 'registrar_frequencia',
        'cadastrar_colider', 'cadastrar_lider_treinamento', 'cadastrar_membro',
        'cadastrar_visitante', 'registrar_evento', 'registrar_convertido',
    },
    'COLIDER': {
        'ver_dashboard', 'ver_menu_relatorios',
        'registrar_evento', 'registrar_convertido',
    },
    'MEMBRO': {
        'ver_dashboard', 'ver_menu_relatorios',
        'cadastrar_visitante',
    }
}


# --- Decorator de Autenticação (sem alterações) ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rotas de Autenticação e Navegação (sem alterações) ---
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username_or_email = request.form['username']
        password_from_form = request.form['password']
        
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # A consulta busca por e-mail OU nome de usuário
            cursor.execute('SELECT * FROM usuarios WHERE email = %s OR username = %s', (username_or_email, username_or_email,))
            user = cursor.fetchone()
            cursor.close()

            # Verifica se o usuário existe E se a senha criptografada corresponde
            if user and check_password_hash(user['senha'], password_from_form):
                # Se o login for bem-sucedido, configuramos a sessão
                session['loggedin'] = True
                session['id'] = user['id']
                session['username'] = user['nome']

                # Lógica de acesso especial para o desenvolvedor
                if user['email'] == 'ney@gmail.com':
                    session['perfil'] = 'DEVELOPER'
                else:
                    session['perfil'] = user.get('perfil', 'MEMBRO')

                # --- ADICIONE ESTA LINHA DE TESTE AQUI ---
                print(f"--- DEBUG INFO --- Login para: {session['username']}, Perfil na sessão: {session['perfil']} ---")
                
                # Verifica se o usuário precisa trocar a senha
                if user.get('force_password_change') == 1:
                    return jsonify({'success': True, 'redirect_url': url_for('change_password')})
                else:
                    return jsonify({'success': True, 'redirect_url': url_for('dashboard')})
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Ocorreu um erro no servidor: {e}'}), 500
            
    return jsonify({'success': False, 'message': 'Requisição inválida.'}), 400

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('menu.html', PERFIS=PERFIS, perfil_usuario=session.get('perfil'))


@app.route('/cadastros')
@login_required
def cadastros():
    return render_template('cadastro.html', PERFIS=PERFIS, perfil_usuario=session.get('perfil'))


# --- ROTA DE CADASTRO DE SUPERVISOR (COM A MUDANÇA) ---
@app.route('/cad_supervisor', methods=['GET', 'POST'])
@login_required
def cad_supervisor():
    if request.method == 'POST':
        # ... (código para pegar dados do formulário sem alterações)
        nome = request.form['nome']
        endereco = request.form['endereco']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']
        telefone = request.form['telefone']
        funcao_ministerial = request.form['funcao_ministerial']

        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO supervisores (nome, endereco, email, data_nascimento, telefone, funcao_ministerial) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, endereco, email, data_nascimento, telefone, funcao_ministerial))
            mysql.connection.commit()
            cursor.close()
            
            # --- MUDANÇA PRINCIPAL AQUI ---
            # Em vez de redirecionar para outra página, redireciona para a mesma página
            # com um parâmetro 'success=true' na URL.
            return redirect(url_for('cad_supervisor', success=True))
        
        except Exception as e:
            return f"Erro ao inserir no banco de dados: {e}"

    # Se a requisição for GET, apenas mostra o formulário
    return render_template('cad_supervisor.html')


@app.route('/cad_lider', methods=['GET', 'POST'])
@login_required
def cad_lider():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        endereco = request.form['endereco']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']
        telefone = request.form['telefone']
        funcao_ministerial = request.form['funcao_ministerial']
        
        try:
            # Insere os dados na nova tabela 'lideres'
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO lideres (nome, endereco, email, data_nascimento, telefone, funcao_ministerial) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, endereco, email, data_nascimento, telefone, funcao_ministerial))
            mysql.connection.commit()
            cursor.close()
            # Redireciona com sinal de sucesso
            return redirect(url_for('cad_lider', success=True))
        except Exception as e:
            # Em caso de erro, você pode criar uma página de erro ou mostrar uma mensagem
            return f"Erro ao inserir líder: {e}"

    # Se a requisição for GET, apenas mostra o formulário
    return render_template('cad_lider.html')


@app.route('/cad_colider', methods=['GET', 'POST'])
@login_required
def cad_colider():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        endereco = request.form['endereco']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']
        telefone = request.form['telefone']
        id_lider_imediato = request.form['id_lider_imediato']
        funcao_ministerial = request.form['funcao_ministerial']
        
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO colideres (nome, endereco, email, data_nascimento, telefone, id_lider_imediato, funcao_ministerial) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, endereco, email, data_nascimento, telefone, id_lider_imediato, funcao_ministerial))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('cad_colider', success=True))
        except Exception as e:
            return f"Erro ao inserir co-líder: {e}"

    # Se a requisição for GET, busca os líderes para preencher o dropdown
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, nome FROM lideres ORDER BY nome ASC")
        lideres = cursor.fetchall()
        cursor.close()
        return render_template('cad_colider.html', lideres=lideres)
    except Exception as e:
        return f"Erro ao buscar líderes: {e}"
    

@app.route('/cad_lider_treinamento', methods=['GET', 'POST'])
@login_required
def cad_lider_treinamento():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']
        telefone = request.form['telefone']
        id_lider = request.form['id_lider']
        id_colider = request.form['id_colider']
        funcao_ministerial = request.form['funcao_ministerial']
        
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO lideres_em_treinamento (nome, email, data_nascimento, telefone, id_lider, id_colider, funcao_ministerial) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, email, data_nascimento, telefone, id_lider, id_colider, funcao_ministerial))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('cad_lider_treinamento', success=True))
        except Exception as e:
            return f"Erro ao inserir líder em treinamento: {e}"

    # Se a requisição for GET, busca líderes e co-líderes
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Busca líderes
        cursor.execute("SELECT id, nome FROM lideres ORDER BY nome ASC")
        lideres = cursor.fetchall()
        
        # Busca co-líderes
        cursor.execute("SELECT id, nome FROM colideres ORDER BY nome ASC")
        colideres = cursor.fetchall()
        
        cursor.close()
        return render_template('cad_lider_treinamento.html', lideres=lideres, colideres=colideres)
    except Exception as e:
        return f"Erro ao buscar dados para o formulário: {e}"
    
@app.route('/cad_membro', methods=['GET', 'POST'])
@login_required
def cad_membro():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        endereco = request.form['endereco']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']
        telefone = request.form['telefone']
        # Os valores dos radio buttons virão como strings '1' ou '0'
        novo_convertido = request.form['novo_convertido']
        membro_outro_ministerio = request.form['membro_outro_ministerio']
        outra_religiao = request.form['outra_religiao']
        nao_professa_fe = request.form['nao_professa_fe']
        
        try:
            cursor = mysql.connection.cursor()
            sql = """
                INSERT INTO membros (nome, endereco, email, data_nascimento, telefone, 
                                     novo_convertido, membro_outro_ministerio, outra_religiao, nao_professa_fe) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nome, endereco, email, data_nascimento, telefone, 
                                 novo_convertido, membro_outro_ministerio, outra_religiao, nao_professa_fe))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('cad_membro', success=True))
        except Exception as e:
            return f"Erro ao inserir membro: {e}"

    # Se a requisição for GET, apenas mostra o formulário
    return render_template('cad_membro.html')

@app.route('/cad_visitante', methods=['GET', 'POST'])
@login_required
def cad_visitante():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        endereco = request.form['endereco']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']
        telefone = request.form['telefone']
        membro_outro_ministerio = request.form['membro_outro_ministerio']
        # Usa .get() para o campo condicional. Se não for enviado, salva None (NULL).
        nome_ministerio = request.form.get('nome_ministerio', None)
        outra_religiao = request.form['outra_religiao']
        
        try:
            cursor = mysql.connection.cursor()
            sql = """
                INSERT INTO visitantes (nome, endereco, email, data_nascimento, telefone, 
                                     membro_outro_ministerio, nome_ministerio, outra_religiao) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nome, endereco, email, data_nascimento, telefone, 
                                 membro_outro_ministerio, nome_ministerio, outra_religiao))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('cad_visitante', success=True))
        except Exception as e:
            return f"Erro ao inserir visitante: {e}"

    # Se a requisição for GET, apenas mostra o formulário
    return render_template('cad_visitante.html')

@app.route('/cad_grm', methods=['GET', 'POST'])
@login_required
def cad_grm():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome_grm = request.form['nome_grm']
        regiao = request.form['regiao']
        id_lider = request.form['id_lider']
        id_colider = request.form['id_colider']
        id_lider_treinamento = request.form['id_lider_treinamento']
        
        try:
            cursor = mysql.connection.cursor()
            sql = """
                INSERT INTO grm (nome_grm, regiao, id_lider, id_colider, id_lider_treinamento) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nome_grm, regiao, id_lider, id_colider, id_lider_treinamento))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('cad_grm', success=True))
        except Exception as e:
            return f"Erro ao registrar GRM: {e}"

    # Se a requisição for GET, busca os dados para os dropdowns
    else:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            # Busca todos os líderes
            cursor.execute("SELECT id, nome FROM lideres ORDER BY nome")
            lideres = cursor.fetchall()

            # Busca todos os co-líderes
            cursor.execute("SELECT id, nome FROM colideres ORDER BY nome")
            colideres = cursor.fetchall()

            # Busca todos os líderes em treinamento
            cursor.execute("SELECT id, nome FROM lideres_em_treinamento ORDER BY nome")
            lideres_em_treinamento = cursor.fetchall()

            cursor.close()
            
            return render_template(
                'cad_grm.html', 
                lideres=lideres, 
                colideres=colideres, 
                lideres_em_treinamento=lideres_em_treinamento
            )
        except Exception as e:
            return f"Erro ao carregar dados para o formulário: {e}"
        

@app.route('/relatorios')
@login_required
def relatorios():
    return render_template('menu_relatorios.html')

# --- ROTA PARA O RELATÓRIO DE GRMS ---
@app.route('/relatorio/grms')
@login_required
def relatorio_grms():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # A consulta SQL abaixo junta as tabelas para trazer os nomes em vez de apenas os IDs.
        # NOTA: Assumimos que a tabela 'grm' tem colunas 'id_lider', 'id_colider', etc.
        # Por enquanto, não temos como calcular "membros ativos", deixaremos para um próximo passo.
        sql = """
            SELECT 
                g.id,
                g.nome_grm,
                g.regiao,
                lider.nome AS nome_lider,
                colider.nome AS nome_colider,
                treinamento.nome AS nome_lider_treinamento
            FROM 
                grm AS g
            LEFT JOIN 
                lideres AS lider ON g.id_lider = lider.id
            LEFT JOIN 
                colideres AS colider ON g.id_colider = colider.id
            LEFT JOIN 
                lideres_em_treinamento AS treinamento ON g.id_lider_treinamento = treinamento.id
            ORDER BY
                g.nome_grm ASC;
        """
        
        cursor.execute(sql)
        grms = cursor.fetchall()
        cursor.close()
        
        # Renderiza o novo template com os dados dos GRMs
        return render_template('relatorio_grms.html', grms=grms)

    except Exception as e:
        # Em caso de erro, mostre uma mensagem amigável
        flash(f"Ocorreu um erro ao gerar o relatório: {e}", "danger")
        return redirect(url_for('relatorios'))

@app.route('/exportar/grms_excel')
@login_required
def exportar_grms_excel():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # 1. Usamos a mesma consulta SQL do relatório
        sql = """
            SELECT 
                g.nome_grm AS "Nome do GRM",
                g.regiao AS "Região",
                lider.nome AS "Líder",
                colider.nome AS "Co-líder",
                treinamento.nome AS "Líder em Treinamento"
            FROM 
                grm AS g
            LEFT JOIN 
                lideres AS lider ON g.id_lider = lider.id
            LEFT JOIN 
                colideres AS colider ON g.id_colider = colider.id
            LEFT JOIN 
                lideres_em_treinamento AS treinamento ON g.id_lider_treinamento = treinamento.id
            ORDER BY
                g.nome_grm ASC;
        """
        cursor.execute(sql)
        grms_data = cursor.fetchall()
        cursor.close()

        # 2. Convertemos os dados para um DataFrame do pandas
        df = pd.DataFrame(grms_data)

        # 3. Criamos um "arquivo" Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Relatorio_GRMs', index=False)
        
        # Retorna o buffer para o início
        output.seek(0)
        
        # 4. Enviamos o arquivo em memória para o navegador como um download
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='relatorio_grms.xlsx'
        )

    except Exception as e:
        flash(f"Ocorreu um erro ao exportar para Excel: {e}", "danger")
        return redirect(url_for('relatorio_grms'))

@app.route('/relatorio/membros')
@login_required
def relatorio_membros():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Busca todos os membros ordenados por nome
        cursor.execute("SELECT * FROM membros ORDER BY nome ASC")
        membros = cursor.fetchall()
        cursor.close()
        return render_template('relatorio_membros.html', membros=membros)
    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de membros: {e}", "danger")
        return redirect(url_for('relatorios'))

# --- ROTA PARA EXPORTAR MEMBROS PARA EXCEL ---
@app.route('/exportar/membros_excel')
@login_required
def exportar_membros_excel():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Usamos uma consulta similar, mas com aliases para nomes de coluna amigáveis
        sql = """
            SELECT
                nome AS "Nome Completo",
                endereco AS "Endereço",
                email AS "E-mail",
                data_nascimento AS "Data de Nascimento",
                telefone AS "Telefone",
                novo_convertido AS "Novo Convertido",
                membro_outro_ministerio AS "Veio de Outro Ministério",
                outra_religiao AS "Veio de Outra Religião",
                nao_professa_fe AS "Não Professava Fé"
            FROM membros
            ORDER BY nome ASC;
        """
        cursor.execute(sql)
        membros_data = cursor.fetchall()
        cursor.close()

        if not membros_data:
            flash("Não há dados de membros para exportar.", "warning")
            return redirect(url_for('relatorio_membros'))

        df = pd.DataFrame(membros_data)

        # Converte os valores 0 e 1 para 'Não' e 'Sim' para clareza na planilha
        bool_cols = ["Novo Convertido", "Veio de Outro Ministério", "Veio de Outra Religião", "Não Professava Fé"]
        for col in bool_cols:
            df[col] = df[col].apply(lambda x: 'Sim' if x == 1 else 'Não')

        # Cria o arquivo Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Relatorio_Membros', index=False)
        output.seek(0)

        # Envia o arquivo para o navegador
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='relatorio_membros.xlsx'
        )

    except Exception as e:
        flash(f"Ocorreu um erro ao exportar os dados de membros: {e}", "danger")
        return redirect(url_for('relatorio_membros'))

@app.route('/relatorio/supervisores')
@login_required
def relatorio_supervisores():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, nome, email, telefone, funcao_ministerial FROM supervisores ORDER BY nome ASC")
        supervisores = cursor.fetchall()
        cursor.close()
        return render_template('relatorio_supervisores.html', supervisores=supervisores)
    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de supervisores: {e}", "danger")
        return redirect(url_for('relatorios'))

# --- ROTA PARA EXPORTAR SUPERVISORES PARA EXCEL ---
@app.route('/exportar/supervisores_excel')
@login_required
def exportar_supervisores_excel():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Selecionamos todas as colunas relevantes com nomes amigáveis para o Excel
        sql = """
            SELECT
                nome AS "Nome Completo",
                endereco AS "Endereço",
                email AS "E-mail",
                data_nascimento AS "Data de Nascimento",
                telefone AS "Telefone",
                funcao_ministerial AS "Função Ministerial"
            FROM supervisores
            ORDER BY nome ASC;
        """
        cursor.execute(sql)
        supervisores_data = cursor.fetchall()
        cursor.close()

        if not supervisores_data:
            flash("Não há dados de supervisores para exportar.", "warning")
            return redirect(url_for('relatorio_supervisores'))

        df = pd.DataFrame(supervisores_data)

        # Cria o arquivo Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Relatorio_Supervisores', index=False)
        output.seek(0)

        # Envia o arquivo para o navegador
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='relatorio_supervisores.xlsx'
        )
    except Exception as e:
        flash(f"Ocorreu um erro ao exportar os dados de supervisores: {e}", "danger")
        return redirect(url_for('relatorio_supervisores'))


@app.route('/relatorio/lideres')
@login_required
def relatorio_lideres():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, nome, email, telefone, funcao_ministerial FROM lideres ORDER BY nome ASC")
        lideres = cursor.fetchall()
        cursor.close()
        return render_template('relatorio_lideres.html', lideres=lideres)
    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de líderes: {e}", "danger")
        return redirect(url_for('relatorios'))

# --- ROTA PARA EXPORTAR LÍDERES PARA EXCEL ---
@app.route('/exportar/lideres_excel')
@login_required
def exportar_lideres_excel():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Selecionamos todas as colunas relevantes com nomes amigáveis para o Excel
        sql = """
            SELECT
                nome AS "Nome Completo",
                endereco AS "Endereço",
                email AS "E-mail",
                data_nascimento AS "Data de Nascimento",
                telefone AS "Telefone",
                funcao_ministerial AS "Função Ministerial"
            FROM lideres
            ORDER BY nome ASC;
        """
        cursor.execute(sql)
        lideres_data = cursor.fetchall()
        cursor.close()

        if not lideres_data:
            flash("Não há dados de líderes para exportar.", "warning")
            return redirect(url_for('relatorio_lideres'))

        df = pd.DataFrame(lideres_data)

        # Cria o arquivo Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Relatorio_Lideres', index=False)
        output.seek(0)

        # Envia o arquivo para o navegador
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='relatorio_lideres.xlsx'
        )
    except Exception as e:
        flash(f"Ocorreu um erro ao exportar os dados de líderes: {e}", "danger")
        return redirect(url_for('relatorio_lideres'))
    
@app.route('/relatorio/colideres')
@login_required
def relatorio_colideres():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Usamos LEFT JOIN para buscar o nome do líder imediato
        sql = """
            SELECT
                c.id, c.nome, c.email, c.telefone, c.funcao_ministerial,
                l.nome AS nome_lider_imediato
            FROM
                colideres AS c
            LEFT JOIN
                lideres AS l ON c.id_lider_imediato = l.id
            ORDER BY
                c.nome ASC;
        """
        cursor.execute(sql)
        colideres = cursor.fetchall()
        cursor.close()
        return render_template('relatorio_colideres.html', colideres=colideres)
    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de co-líderes: {e}", "danger")
        return redirect(url_for('relatorios'))

# --- ROTA PARA EXPORTAR CO-LÍDERES PARA EXCEL ---
@app.route('/exportar/colideres_excel')
@login_required
def exportar_colideres_excel():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT
                c.nome AS "Nome Completo",
                c.endereco AS "Endereço",
                c.email AS "E-mail",
                c.data_nascimento AS "Data de Nascimento",
                c.telefone AS "Telefone",
                c.funcao_ministerial AS "Função Ministerial",
                l.nome AS "Líder Imediato"
            FROM
                colideres AS c
            LEFT JOIN
                lideres AS l ON c.id_lider_imediato = l.id
            ORDER BY
                c.nome ASC;
        """
        cursor.execute(sql)
        colideres_data = cursor.fetchall()
        cursor.close()

        if not colideres_data:
            flash("Não há dados de co-líderes para exportar.", "warning")
            return redirect(url_for('relatorio_colideres'))

        df = pd.DataFrame(colideres_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Relatorio_Co-lideres', index=False)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='relatorio_colideres.xlsx'
        )
    except Exception as e:
        flash(f"Ocorreu um erro ao exportar os dados de co-líderes: {e}", "danger")
        return redirect(url_for('relatorio_colideres'))
    

@app.route('/relatorio/lideres_treinamento')
@login_required
def relatorio_lideres_treinamento():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Usamos dois LEFT JOINs para buscar os nomes do líder e co-líder
        sql = """
            SELECT
                lt.id, lt.nome, lt.email, lt.telefone,
                l.nome AS nome_lider,
                c.nome AS nome_colider
            FROM
                lideres_em_treinamento AS lt
            LEFT JOIN
                lideres AS l ON lt.id_lider = l.id
            LEFT JOIN
                colideres AS c ON lt.id_colider = c.id
            ORDER BY
                lt.nome ASC;
        """
        cursor.execute(sql)
        lideres_t = cursor.fetchall()
        cursor.close()
        return render_template('relatorio_lideres_treinamento.html', lideres_t=lideres_t)
    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório: {e}", "danger")
        return redirect(url_for('relatorios'))

# --- ROTA PARA EXPORTAR LÍDERES EM TREINAMENTO PARA EXCEL ---
@app.route('/exportar/lideres_treinamento_excel')
@login_required
def exportar_lideres_treinamento_excel():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT
                lt.nome AS "Nome Completo",
                lt.email AS "E-mail",
                lt.data_nascimento AS "Data de Nascimento",
                lt.telefone AS "Telefone",
                l.nome AS "Líder Direto",
                c.nome AS "Co-líder Direto",
                lt.funcao_ministerial AS "Função Ministerial"
            FROM
                lideres_em_treinamento AS lt
            LEFT JOIN
                lideres AS l ON lt.id_lider = l.id
            LEFT JOIN
                colideres AS c ON lt.id_colider = c.id
            ORDER BY
                lt.nome ASC;
        """
        cursor.execute(sql)
        lideres_t_data = cursor.fetchall()
        cursor.close()

        if not lideres_t_data:
            flash("Não há dados de líderes em treinamento para exportar.", "warning")
            return redirect(url_for('relatorio_lideres_treinamento'))

        df = pd.DataFrame(lideres_t_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Lideres_Treinamento', index=False)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='relatorio_lideres_treinamento.xlsx'
        )
    except Exception as e:
        flash(f"Ocorreu um erro ao exportar os dados: {e}", "danger")
        return redirect(url_for('relatorio_lideres_treinamento'))

@app.route('/relatorio/visitantes')
@login_required
def relatorio_visitantes():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM visitantes ORDER BY nome ASC")
        visitantes = cursor.fetchall()
        cursor.close()
        return render_template('relatorio_visitantes.html', visitantes=visitantes)
    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de visitantes: {e}", "danger")
        return redirect(url_for('relatorios'))

# --- NOVA ROTA PARA EXPORTAR VISITANTES PARA EXCEL ---
@app.route('/exportar/visitantes_excel')
@login_required
def exportar_visitantes_excel():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT
                nome AS "Nome Completo",
                endereco AS "Endereço",
                email AS "E-mail",
                data_nascimento AS "Data de Nascimento",
                telefone AS "Telefone",
                membro_outro_ministerio AS "Membro de Outro Ministério",
                nome_ministerio AS "Nome do Ministério de Origem",
                outra_religiao AS "Veio de Outra Religião"
            FROM visitantes
            ORDER BY nome ASC;
        """
        cursor.execute(sql)
        visitantes_data = cursor.fetchall()
        cursor.close()

        if not visitantes_data:
            flash("Não há dados de visitantes para exportar.", "warning")
            return redirect(url_for('relatorio_visitantes'))

        df = pd.DataFrame(visitantes_data)
        
        # Converte as colunas de 0/1 para 'Não'/'Sim' para melhor leitura
        bool_cols = ["Membro de Outro Ministério", "Veio de Outra Religião"]
        for col in bool_cols:
            df[col] = df[col].apply(lambda x: 'Sim' if x == 1 else 'Não')

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Relatorio_Visitantes', index=False)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='relatorio_visitantes.xlsx'
        )
    except Exception as e:
        flash(f"Ocorreu um erro ao exportar os dados de visitantes: {e}", "danger")
        return redirect(url_for('relatorio_visitantes'))
    

@app.route('/cad_evento', methods=['GET', 'POST'])
@login_required
def cad_evento():
    if request.method == 'POST':
        # Pega os dados do formulário
        id_grm = request.form['id_grm']
        # .get() para campos não obrigatórios, como o co-líder
        id_lider_responsavel = request.form.get('id_lider_responsavel')
        id_colider_responsavel = request.form.get('id_colider_responsavel')
        participantes = request.form['participantes']
        valor_ofertas = request.form['valor_ofertas']
        data_evento = request.form['data_evento']

        # Converte para None se a string estiver vazia, para o banco de dados aceitar NULL
        id_lider_responsavel = id_lider_responsavel if id_lider_responsavel else None
        id_colider_responsavel = id_colider_responsavel if id_colider_responsavel else None

        try:
            cursor = mysql.connection.cursor()
            sql = """
                INSERT INTO eventos (id_grm, id_lider_responsavel, id_colider_responsavel, participantes, valor_ofertas, data_evento) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (id_grm, id_lider_responsavel, id_colider_responsavel, participantes, valor_ofertas, data_evento))
            mysql.connection.commit()
            cursor.close()
            # Redireciona com sinal de sucesso
            return redirect(url_for('cad_evento', success=True))
        except Exception as e:
            return f"Erro ao registrar o evento: {e}"

    # Se a requisição for GET, busca os dados para preencher os dropdowns
    else:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT id, nome_grm, regiao FROM grm ORDER BY nome_grm ASC")
            grms = cursor.fetchall()
            
            cursor.execute("SELECT id, nome FROM lideres ORDER BY nome ASC")
            lideres = cursor.fetchall()
            
            cursor.execute("SELECT id, nome FROM colideres ORDER BY nome ASC")
            colideres = cursor.fetchall()

            cursor.close()
            return render_template('cad_evento.html', grms=grms, lideres=lideres, colideres=colideres)
        except Exception as e:
            return f"Erro ao carregar dados para o formulário: {e}"
        

@app.route('/cad_convertido', methods=['GET', 'POST'])
@login_required
def cad_convertido():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        telefone = request.form['telefone']
        id_evento = request.form['id_evento']
        data_conversao = request.form['data_conversao']
        observacoes = request.form.get('observacoes', '') # .get() para campo opcional

        try:
            cursor = mysql.connection.cursor()
            sql = """
                INSERT INTO convertidos (nome, telefone, id_evento, data_conversao, observacoes) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nome, telefone, id_evento, data_conversao, observacoes))
            mysql.connection.commit()
            cursor.close()
            # Redireciona com sinal de sucesso
            return redirect(url_for('cad_convertido', success=True))
        except Exception as e:
            return f"Erro ao registrar o convertido: {e}"

    # Se a requisição for GET, busca os eventos para preencher o dropdown
    else:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Buscamos os eventos e os GRMs associados para dar mais contexto no dropdown
            sql = """
                SELECT e.id, e.data_evento, g.nome_grm 
                FROM eventos e
                JOIN grm g ON e.id_grm = g.id
                ORDER BY e.data_evento DESC;
            """
            cursor.execute(sql)
            eventos = cursor.fetchall()
            cursor.close()
            return render_template('cad_convertido.html', eventos=eventos)
        except Exception as e:
            return f"Erro ao carregar dados para o formulário: {e}"
        

@app.route('/relatorio/convertidos')
@login_required
def relatorio_convertidos():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Esta consulta junta todas as tabelas para criar um relatório completo
        sql = """
            SELECT
                cv.id,
                cv.nome,
                cv.telefone,
                cv.data_conversao,
                g.nome_grm,
                g.regiao,
                l.nome AS nome_lider,
                c.nome AS nome_colider
            FROM
                convertidos AS cv
            JOIN
                eventos AS ev ON cv.id_evento = ev.id
            JOIN
                grm AS g ON ev.id_grm = g.id
            LEFT JOIN
                lideres AS l ON ev.id_lider_responsavel = l.id
            LEFT JOIN
                colideres AS c ON ev.id_colider_responsavel = c.id
            ORDER BY
                cv.data_conversao DESC;
        """
        cursor.execute(sql)
        convertidos = cursor.fetchall()
        cursor.close()
        return render_template('relatorio_convertidos.html', convertidos=convertidos)
    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de convertidos: {e}", "danger")
        return redirect(url_for('relatorios'))

# --- NOVA ROTA PARA EXPORTAR CONVERTIDOS PARA EXCEL ---
@app.route('/exportar/convertidos_excel')
@login_required
def exportar_convertidos_excel():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT
                cv.nome AS "Nome do Convertido",
                cv.telefone AS "Telefone",
                cv.data_conversao AS "Data da Conversão",
                g.nome_grm AS "GRM do Evento",
                g.regiao AS "Região",
                l.nome AS "Líder Responsável pelo Evento",
                c.nome AS "Co-líder Responsável pelo Evento",
                cv.observacoes AS "Observações"
            FROM
                convertidos AS cv
            JOIN
                eventos AS ev ON cv.id_evento = ev.id
            JOIN
                grm AS g ON ev.id_grm = g.id
            LEFT JOIN
                lideres AS l ON ev.id_lider_responsavel = l.id
            LEFT JOIN
                colideres AS c ON ev.id_colider_responsavel = c.id
            ORDER BY
                cv.data_conversao DESC;
        """
        cursor.execute(sql)
        convertidos_data = cursor.fetchall()
        cursor.close()

        if not convertidos_data:
            flash("Não há dados de convertidos para exportar.", "warning")
            return redirect(url_for('relatorio_convertidos'))

        df = pd.DataFrame(convertidos_data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Relatorio_Convertidos', index=False)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='relatorio_convertidos.xlsx'
        )
    except Exception as e:
        flash(f"Ocorreu um erro ao exportar os dados: {e}", "danger")
        return redirect(url_for('relatorio_convertidos'))


@app.route('/conceder_acesso', methods=['GET', 'POST'])
@login_required
def conceder_acesso():
    # Garante que apenas Supervisores ou Desenvolvedores acessem esta página
    if session['perfil'] not in ['SUPERVISOR', 'DEVELOPER']:
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            # Pega os dados do formulário
            pessoa_selecionada = request.form.get('pessoa')
            perfil = request.form.get('perfil')
            senha = request.form.get('senha')
            login_type = request.form.get('login_type') # Novo campo: 'email' ou 'generate'
            username_gerado = request.form.get('username_gerado') # Novo campo

            if not pessoa_selecionada or not perfil or not senha:
                flash("Todos os campos são obrigatórios.", "danger")
                return redirect(url_for('conceder_acesso'))

            tipo, pessoa_id, nome, email = pessoa_selecionada.split(':', 3)
            
            # Decide qual será o username salvo no banco
            username_final = None
            if login_type == 'generate':
                username_final = username_gerado

            # Criptografa a senha antes de salvar
            senha_hash = generate_password_hash(senha)

            cursor = mysql.connection.cursor()
            # ATUALIZAÇÃO: Inserindo nas novas colunas 'username' e 'force_password_change'
            sql = """
                INSERT INTO usuarios (nome, email, username, senha, perfil, force_password_change) 
                VALUES (%s, %s, %s, %s, %s, 1)
            """
            cursor.execute(sql, (nome, email, username_final, senha_hash, perfil))
            mysql.connection.commit()
            cursor.close()

            flash(f"Acesso concedido para {nome} com o perfil de {perfil}!", "success")
            return redirect(url_for('conceder_acesso'))

        except Exception as e:
            flash(f"Ocorreu um erro: {e}", "danger")
            return redirect(url_for('conceder_acesso'))

    # A parte GET (que busca as pessoas) continua a mesma
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql_supervisores = """
            SELECT s.id, s.nome, s.email, 'supervisor' as tipo
            FROM supervisores s LEFT JOIN usuarios u ON s.email = u.email WHERE u.id IS NULL;
        """
        cursor.execute(sql_supervisores)
        supervisores_sem_acesso = cursor.fetchall()

        sql_lideres = """
            SELECT l.id, l.nome, l.email, 'lider' as tipo
            FROM lideres l LEFT JOIN usuarios u ON l.email = u.email WHERE u.id IS NULL;
        """
        cursor.execute(sql_lideres)
        lideres_sem_acesso = cursor.fetchall()
        
        cursor.close()
        
        pessoas_sem_acesso = supervisores_sem_acesso + lideres_sem_acesso
        
        return render_template('conceder_acesso.html', pessoas=pessoas_sem_acesso)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    # Se a requisição for para salvar a nova senha
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # --- Validação das Regras da Senha ---

        # 1. Verifica se as senhas digitadas são iguais
        if new_password != confirm_password:
            flash('As senhas não coincidem. Tente novamente.', 'danger')
            return redirect(url_for('change_password'))

        # 2. Verifica o comprimento mínimo de 8 caracteres
        if len(new_password) < 8:
            flash('A senha deve ter no mínimo 8 caracteres.', 'danger')
            return redirect(url_for('change_password'))

        # 3. Verifica se há pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', new_password):
            flash('A senha deve conter pelo menos uma letra maiúscula.', 'danger')
            return redirect(url_for('change_password'))

        # 4. Verifica se há pelo menos dois números
        if len(re.findall(r'[0-9]', new_password)) < 2:
            flash('A senha deve conter pelo menos dois números.', 'danger')
            return redirect(url_for('change_password'))

        # Se todas as regras passaram, atualiza o banco de dados
        try:
            # Criptografa a nova senha
            hashed_password = generate_password_hash(new_password)
            user_id = session['id'] # Pega o ID do usuário logado na sessão

            cursor = mysql.connection.cursor()
            # Atualiza a senha e desativa a flag de troca obrigatória
            sql = "UPDATE usuarios SET senha = %s, force_password_change = 0 WHERE id = %s"
            cursor.execute(sql, (hashed_password, user_id))
            mysql.connection.commit()
            cursor.close()

            flash('Senha alterada com sucesso! Você já pode usar o sistema.', 'success')
            return redirect(url_for('dashboard')) # Redireciona para o menu principal

        except Exception as e:
            flash(f'Ocorreu um erro ao atualizar sua senha: {e}', 'danger')
            return redirect(url_for('change_password'))

    # Se a requisição for GET, apenas mostra a página para trocar a senha
    return render_template('change_password.html')


# --- ROTA PARA O HISTÓRICO DE OFERTAS ---
@app.route('/historico_ofertas')
@login_required
def historico_ofertas():
    # Protege a rota, permitindo apenas perfis autorizados
    if session['perfil'] not in ['SUPERVISOR', 'DEVELOPER']: # Adicione outros perfis se necessário
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('dashboard'))

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT
                e.data_evento,
                e.valor_ofertas,
                g.nome_grm,
                g.regiao,
                l.nome AS nome_lider
            FROM
                eventos AS e
            JOIN
                grm AS g ON e.id_grm = g.id
            LEFT JOIN
                lideres AS l ON e.id_lider_responsavel = l.id
            ORDER BY
                e.data_evento DESC;
        """
        cursor.execute(sql)
        ofertas = cursor.fetchall()
        cursor.close()
        return render_template('historico_ofertas.html', ofertas=ofertas)
    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o histórico: {e}", "danger")
        return redirect(url_for('dashboard'))

# ---ROTA PARA EXPORTAR HISTÓRICO DE OFERTAS PARA EXCEL ---
@app.route('/exportar/ofertas_excel')
@login_required
def exportar_ofertas_excel():
    if session['perfil'] not in ['SUPERVISOR', 'DEVELOPER']:
        return redirect(url_for('dashboard'))

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            SELECT
                e.data_evento AS "Data do Evento",
                e.valor_ofertas AS "Valor Arrecadado (R$)",
                g.nome_grm AS "GRM",
                g.regiao AS "Região",
                l.nome AS "Líder Responsável"
            FROM
                eventos AS e
            JOIN
                grm AS g ON e.id_grm = g.id
            LEFT JOIN
                lideres AS l ON e.id_lider_responsavel = l.id
            ORDER BY
                e.data_evento DESC;
        """
        cursor.execute(sql)
        ofertas_data = cursor.fetchall()
        cursor.close()

        df = pd.DataFrame(ofertas_data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Historico_Ofertas', index=False)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='historico_ofertas.xlsx'
        )
    except Exception as e:
        flash(f"Ocorreu um erro ao exportar os dados: {e}", "danger")
        return redirect(url_for('historico_ofertas'))
    
@app.route('/excluir_registro')
@login_required
def excluir_registro():
    # Protege a rota, permitindo apenas perfis com permissão
    if session['perfil'] not in ['SUPERVISOR', 'DEVELOPER']:
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('dashboard'))
        
    return render_template('excluir_registro.html')


@app.route('/api/search/<string:tipo_registro>')
@login_required
def api_search(tipo_registro):
    query = request.args.get('q', '') # Pega o termo de busca (ex: ?q=joao)
    
    if not query:
        return jsonify([]) # Retorna lista vazia se não houver busca

    # Mapeia o tipo recebido para o nome da tabela no banco
    tabelas_permitidas = {
        'supervisor': 'supervisores',
        'lider': 'lideres',
        'colider': 'colideres',
        'membro': 'membros',
        'grm': 'grm'
    }

    tabela = tabelas_permitidas.get(tipo_registro)
    
    # Se o tipo não for válido, retorna erro
    if not tabela:
        return jsonify({'error': 'Tipo de registro inválido'}), 400

    # O nome da coluna pode variar, ajustamos aqui
    coluna_nome = 'nome_grm' if tabela == 'grm' else 'nome'

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Usamos LIKE para buscar nomes que comecem com o termo digitado
        sql = f"SELECT id, {coluna_nome} AS nome FROM {tabela} WHERE {coluna_nome} LIKE %s"
        # O '%' é o coringa do SQL para "qualquer coisa"
        cursor.execute(sql, (f"{query}%",)) 
        
        resultados = cursor.fetchall()
        cursor.close()
        
        return jsonify(resultados) # Retorna a lista de resultados em formato JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/details/<string:tipo_registro>/<int:item_id>')
@login_required
def api_details(tipo_registro, item_id):
    tabelas_permitidas = {
        'supervisor': 'supervisores', 'lider': 'lideres', 'colider': 'colideres',
        'membro': 'membros', 'grm': 'grm'
    }
    tabela = tabelas_permitidas.get(tipo_registro)
    if not tabela:
        return jsonify({'error': 'Tipo de registro inválido'}), 400

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = f"SELECT * FROM {tabela} WHERE id = %s"
        cursor.execute(sql, (item_id,))
        resultado = cursor.fetchone()
        cursor.close()
        
        # Converte a data para string para poder ser enviada via JSON
        if resultado and 'data_nascimento' in resultado and resultado['data_nascimento']:
            resultado['data_nascimento'] = resultado['data_nascimento'].strftime('%d/%m/%Y')
            
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- API PARA DELETAR UM ITEM ---
@app.route('/api/delete/<string:tipo_registro>/<int:item_id>', methods=['DELETE'])
@login_required
def api_delete(tipo_registro, item_id):
    # Apenas Supervisor e Developer podem excluir
    if session['perfil'] not in ['SUPERVISOR', 'DEVELOPER']:
        return jsonify({'error': 'Permissão negada'}), 403

    tabelas_permitidas = {
        'supervisor': 'supervisores', 'lider': 'lideres', 'colider': 'colideres',
        'membro': 'membros', 'grm': 'grm'
    }
    tabela = tabelas_permitidas.get(tipo_registro)
    if not tabela:
        return jsonify({'error': 'Tipo de registro inválido'}), 400

    try:
        cursor = mysql.connection.cursor()
        sql = f"DELETE FROM {tabela} WHERE id = %s"
        cursor.execute(sql, (item_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'success': True, 'message': 'Registro excluído com sucesso!'})
    except MySQLdb.IntegrityError as e:
        # Erro de integridade (chave estrangeira), o mais comum ao tentar excluir
        return jsonify({'success': False, 'message': 'Erro: Este registro não pode ser excluído pois está sendo usado por outro item no sistema.'}), 409
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro desconhecido: {str(e)}'}), 500
    

@app.route('/analise_menu')
@login_required
def analise_menu():
    if session['perfil'] not in ['DEVELOPER', 'SUPERVISOR']:
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('dashboard'))
    # Passa as informações de permissão para o analise_menu.html também
    return render_template('analise_menu.html', PERFIS=PERFIS, perfil_usuario=session.get('perfil'))

        
    

@app.route('/analise/grms') # A URL continua a mesma
@login_required
def analise_grms():
    if session['perfil'] not in ['DEVELOPER', 'SUPERVISOR']:
        flash("Você não tem permissão para gerar este relatório.", "danger")
        return redirect(url_for('analise_menu'))
        
    try:
        # Pega a região da URL (enviada pelo formulário de filtros)
        regiao_filtro = request.args.get('regiao', 'todas')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        hoje = datetime.now()
        data_bimestre = hoje - timedelta(days=60)
        data_semestre = hoje - timedelta(days=180)
        data_ano = hoje - timedelta(days=365)
        
        # --- Modificação principal: As consultas agora são dinâmicas ---
        
        def executar_consulta_filtrada(base_sql, data_limite):
            params = [data_limite]
            query = base_sql
            if regiao_filtro != 'todas':
                query += " AND regiao = %s"
                params.append(regiao_filtro)
            query += " GROUP BY regiao ORDER BY regiao;"
            cursor.execute(query, tuple(params))
            return cursor.fetchall()

        # Consultas base (sem a parte do GROUP BY)
        sql_base_bimestre = "SELECT regiao AS 'Região', COUNT(id) AS 'GRMs Criados (Últimos 60 dias)' FROM grm WHERE data_criacao >= %s"
        sql_base_semestre = "SELECT regiao AS 'Região', COUNT(id) AS 'GRMs Criados (Últimos 180 dias)' FROM grm WHERE data_criacao >= %s"
        sql_base_ano = "SELECT regiao AS 'Região', COUNT(id) AS 'GRMs Criados (Último Ano)' FROM grm WHERE data_criacao >= %s"

        df_bimestre = pd.DataFrame(executar_consulta_filtrada(sql_base_bimestre, data_bimestre))
        df_semestre = pd.DataFrame(executar_consulta_filtrada(sql_base_semestre, data_semestre))
        df_ano = pd.DataFrame(executar_consulta_filtrada(sql_base_ano, data_ano))
        
        cursor.close()

        # O resto do código para gerar o Excel continua igual
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_bimestre.to_excel(writer, sheet_name='Últimos 60 Dias', index=False)
            df_semestre.to_excel(writer, sheet_name='Últimos 180 Dias', index=False)
            df_ano.to_excel(writer, sheet_name='Último Ano', index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'analise_crescimento_grms_{regiao_filtro}.xlsx'
        )

    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de GRMs: {e}", "danger")
        return redirect(url_for('analise_menu'))


@app.route('/analise/grms/filtros')
@login_required
def analise_grms_filtros():
    if session['perfil'] not in ['DEVELOPER', 'SUPERVISOR']:
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('analise_menu'))
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Busca todas as regiões únicas que existem na tabela GRM
        cursor.execute("SELECT DISTINCT regiao FROM grm ORDER BY regiao")
        regioes = cursor.fetchall()
        cursor.close()
        # Renderiza a nova página de filtros, passando a lista de regiões
        return render_template('analise_grms_filtros.html', regioes=regioes)

    except Exception as e:
        flash(f"Ocorreu um erro ao carregar os filtros: {e}", "danger")
        return redirect(url_for('analise_menu'))
    
@app.route('/analise/conversoes')
@login_required
def analise_conversoes():
    # Verificação de permissão
    if session.get('perfil', '').strip() not in ['DEVELOPER', 'SUPERVISOR']:
        flash("Você não tem permissão para gerar este relatório.", "danger")
        return redirect(url_for('analise_menu'))
        
    try:
        # Pega os filtros da URL, enviados pelo formulário
        periodo = request.args.get('periodo', 'geral')
        regiao = request.args.get('regiao', 'todas')
        grm_id = request.args.get('grm_id', 'todos')

        # Lógica para definir os períodos de data
        ano_atual = datetime.now().year
        datas = {
            'bimestre1': (f'{ano_atual}-01-01', f'{ano_atual}-02-28'),
            'semestre1': (f'{ano_atual}-01-01', f'{ano_atual}-06-30'),
            'ano_atual': (f'{ano_atual}-01-01', f'{ano_atual}-12-31'),
            'ano_anterior': (f'{ano_atual-1}-01-01', f'{ano_atual-1}-12-31')
        }

        # --- Montagem da Consulta SQL Dinâmica ---
        # Base da consulta que junta as tabelas necessárias
        sql = """
            SELECT 
                cv.nome AS "Nome do Convertido", 
                cv.data_conversao AS "Data da Conversão", 
                g.nome_grm AS "GRM de Origem", 
                g.regiao AS "Região"
            FROM convertidos cv
            JOIN eventos ev ON cv.id_evento = ev.id
            JOIN grm g ON ev.id_grm = g.id
            WHERE 1=1
        """
        params = []

        # Adiciona os filtros à consulta conforme a seleção do usuário
        if periodo in datas:
            sql += " AND cv.data_conversao BETWEEN %s AND %s"
            params.extend(datas[periodo])
        
        if regiao != 'todas':
            sql += " AND g.regiao = %s"
            params.append(regiao)
            
        if grm_id != 'todos':
            sql += " AND g.id = %s"
            params.append(grm_id)
            
        sql += " ORDER BY cv.data_conversao DESC"

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, tuple(params))
        resultados = cursor.fetchall()
        cursor.close()
        
        df = pd.DataFrame(resultados)

        # --- Geração da Planilha Excel ---
        output = io.BytesIO()
        df.to_excel(output, sheet_name='Analise_de_Conversoes', index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'analise_conversoes.xlsx'
        )

    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de conversões: {e}", "danger")
        return redirect(url_for('analise_conversoes_filtros'))



@app.route('/analise/conversoes/filtros')
@login_required
def analise_conversoes_filtros():
    if session['perfil'] not in ['DEVELOPER', 'SUPERVISOR']:
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('analise_menu'))
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Busca todas as regiões e GRMs para os filtros
        cursor.execute("SELECT DISTINCT regiao FROM grm ORDER BY regiao")
        regioes = cursor.fetchall()
        cursor.execute("SELECT id, nome_grm FROM grm ORDER BY nome_grm")
        grms = cursor.fetchall()
        cursor.close()
        
        return render_template('analise_conversoes_filtros.html', regioes=regioes, grms=grms)

    except Exception as e:
        flash(f"Ocorreu um erro ao carregar os filtros: {e}", "danger")
        return redirect(url_for('analise_menu'))
    
@app.route('/analise/membros/filtros')
@login_required
def analise_membros_filtros():
    if session.get('perfil', '').strip() not in ['DEVELOPER', 'SUPERVISOR']:
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('analise_menu'))
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT DISTINCT regiao FROM grm ORDER BY regiao")
        regioes = cursor.fetchall()
        cursor.execute("SELECT id, nome_grm FROM grm ORDER BY nome_grm")
        grms = cursor.fetchall()
        cursor.close()
        return render_template('analise_membros_filtros.html', regioes=regioes, grms=grms)

    except Exception as e:
        flash(f"Ocorreu um erro ao carregar os filtros: {e}", "danger")
        return redirect(url_for('analise_menu'))
    

@app.route('/analise/membros')
@login_required
def analise_membros():
    if session.get('perfil', '').strip() not in ['DEVELOPER', 'SUPERVISOR']:
        return redirect(url_for('analise_menu'))
        
    try:
        # Pega os filtros da URL
        nome = request.args.get('nome_membro', '')
        periodo = request.args.get('periodo', 'todos')
        regiao = request.args.get('regiao', 'todas')
        grm_id = request.args.get('grm_id', 'todos')

        # --- Lógica de Datas ---
        hoje = datetime.now()
        data_limite = None
        if periodo == 'bimestre': data_limite = hoje - timedelta(days=60)
        elif periodo == 'semestre': data_limite = hoje - timedelta(days=180)
        elif periodo == 'ano': data_limite = hoje - timedelta(days=365)

        # --- Montagem da Consulta para a LISTA de membros ---
        sql_lista = """
            SELECT m.nome, m.email, m.telefone, m.data_cadastro, g.nome_grm, g.regiao
            FROM membros m
            LEFT JOIN grm g ON m.id_grm_principal = g.id
            WHERE 1=1
        """
        params_lista = []
        if nome:
            sql_lista += " AND m.nome LIKE %s"
            params_lista.append(f"%{nome}%")
        if data_limite:
            sql_lista += " AND m.data_cadastro >= %s"
            params_lista.append(data_limite)
        if regiao != 'todas':
            sql_lista += " AND g.regiao = %s"
            params_lista.append(regiao)
        if grm_id != 'todos':
            sql_lista += " AND g.id = %s"
            params_lista.append(grm_id)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql_lista, tuple(params_lista))
        lista_membros = cursor.fetchall()
        df_lista = pd.DataFrame(lista_membros)

        # --- Consulta para os TOTAIS por região ---
        sql_totais = """
            SELECT g.regiao, COUNT(m.id) as total_membros
            FROM membros m
            JOIN grm g ON m.id_grm_principal = g.id
            GROUP BY g.regiao
            ORDER BY g.regiao
        """
        cursor.execute(sql_totais)
        totais_regiao = cursor.fetchall()
        df_totais = pd.DataFrame(totais_regiao)
        cursor.close()

        # --- Geração do Excel com 2 abas ---
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_lista.to_excel(writer, sheet_name='Lista_de_Membros_Filtrada', index=False)
            df_totais.to_excel(writer, sheet_name='Total_Membros_por_Regiao', index=False)
        output.seek(0)
        
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='analise_membros.xlsx')

    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de membros: {e}", "danger")
        return redirect(url_for('analise_membros_filtros'))

@app.route('/analise/lideranca/filtros')
@login_required
def analise_lideranca_filtros():
    if session.get('perfil', '').strip() not in ['DEVELOPER', 'SUPERVISOR']:
        return redirect(url_for('analise_menu'))
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT DISTINCT regiao FROM grm ORDER BY regiao")
        regioes = cursor.fetchall()
        cursor.close()
        return render_template('analise_lideranca_filtros.html', regioes=regioes)
    except Exception as e:
        flash(f"Ocorreu um erro ao carregar os filtros: {e}", "danger")
        return redirect(url_for('analise_menu'))

@app.route('/analise/lideranca')
@login_required
def analise_lideranca():
    if session.get('perfil', '').strip() not in ['DEVELOPER', 'SUPERVISOR']:
        return redirect(url_for('analise_menu'))
        
    try:
        cargo = request.args.get('cargo', 'todos')
        periodo = request.args.get('periodo', 'total')
        regiao = request.args.get('regiao', 'todas')

        ano_atual = datetime.now().year
        datas = {
            'bimestre': (datetime.now() - timedelta(days=60), datetime.now()),
            'semestre': (datetime.now() - timedelta(days=180), datetime.now()),
            'ano_atual': (f'{ano_atual}-01-01', f'{ano_atual}-12-31'),
            'ano_anterior': (f'{ano_atual-1}-01-01', f'{ano_atual-1}-12-31')
        }

        sql_base = """
            (SELECT s.nome, s.email, s.data_cadastro, 'Supervisor' as cargo, NULL as nome_grm, NULL as regiao FROM supervisores s)
            UNION ALL
            (SELECT l.nome, l.email, l.data_cadastro, 'Líder' as cargo, g.nome_grm, g.regiao FROM lideres l LEFT JOIN grm g ON l.id = g.id_lider)
            UNION ALL
            (SELECT c.nome, c.email, c.data_cadastro, 'Co-líder' as cargo, g.nome_grm, g.regiao FROM colideres c LEFT JOIN grm g ON c.id = g.id_colider)
        """
        
        # A consulta final será construída dentro de uma subquery para permitir a filtragem
        sql_final = f"SELECT * FROM ({sql_base}) AS lideranca WHERE 1=1"
        params = []

        if cargo != 'todos':
            sql_final += " AND cargo = %s"
            params.append(cargo[:-1].capitalize()) # Remove o 's' e capitaliza (ex: 'lideres' -> 'Líder')
        
        if periodo in datas:
            sql_final += " AND data_cadastro BETWEEN %s AND %s"
            params.extend(datas[periodo])
            
        if regiao != 'todas':
            sql_final += " AND regiao = %s"
            params.append(regiao)
            
        sql_final += " ORDER BY data_cadastro DESC"
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql_final, tuple(params))
        resultados = cursor.fetchall()
        cursor.close()
        
        df = pd.DataFrame(resultados)

        output = io.BytesIO()
        df.to_excel(output, sheet_name='Analise_de_Lideranca', index=False)
        output.seek(0)
        
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='analise_lideranca.xlsx')

    except Exception as e:
        flash(f"Ocorreu um erro ao gerar o relatório de liderança: {e}", "danger")
        return redirect(url_for('analise_lideranca_filtros'))

if __name__ == '__main__':
    app.run(debug=True)