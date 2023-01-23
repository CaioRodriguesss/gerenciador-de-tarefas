import sqlite3
import pandas as pd

banco = "gerenciador.db"

# ===== SUPRIMENTOS PÁGINA PRINCIPAL E TAREFAS ===== #

# ==== SUPRIMENTOS DROPDOWN ==== #

# Função para transformar a tabela de gerentes em uma lista de dicionários que irá alimentar os dropdowns da página principal.
def drp_consulta_gerente(banco):
    with sqlite3.connect(banco) as con:
        df_ger_id = pd.read_sql_query("SELECT * FROM gerente", con)
        if df_ger_id.empty:
            return []
        else:
            lista_ger = []
            for row in df_ger_id.itertuples():
                dado = {"label":row[2], "value":row[1]}
                lista_ger.append(dado)
                dado = {}
            return lista_ger


#print(consulta_gerente_id(banco))

# Função para transformar a tabela de departamentos em uma lista de dicionários que irá alimentar os dropdowns da página principal.
def drp_consulta_departamento(banco):
    with sqlite3.connect(banco) as con:
        df_dpt_id = pd.read_sql_query("SELECT id_departamento, nome_departamento FROM departamento", con)
        if df_dpt_id.empty:
            return []
        else:
            lista_dpt = []
            for row in df_dpt_id.itertuples():
                dado = {"label": row[2], "value": row[1]}
                lista_dpt.append(dado)
                dado = {}
            return lista_dpt

#print(consulta_departamento(banco))

# Função para transformar a tabela de funcionários em uma lista de dicionários que irá alimentar os dropdown da página principal.
def drp_consulta_funcionario(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query("SELECT id_funcionario, nome_funcionario FROM funcionario", con)
        if df_func_id.empty:
            return []
        else:
            lista_func = []
            for row in df_func_id.itertuples():
                dado = {"label": row[2], "value": row[1]}
                lista_func.append(dado)
                dado = {}
            return lista_func

# Função para transformar a tabela de níveis em uma lista de dicionários que irá alimentar os dropdown da página de tarefas.
def drp_consulta_nivel(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query("SELECT id_nivel, desc_nivel FROM nivel", con)
        if df_func_id.empty:
            return []
        else:
            lista_func = []
            for row in df_func_id.itertuples():
                dado = {"label": row[2], "value": row[1]}
                lista_func.append(dado)
                dado = {}
            return lista_func

# Função para transformar a tabela de tarefas pendentes em uma lista de dicionários que irá alimentar os dropdown da página de tarefas.
def drp_consulta_tarefa_relacionada(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query("SELECT id_tarefa FROM tarefas_pendentes", con)
        if df_func_id.empty:
            return []
        else:
            lista_func = []
            for row in df_func_id.itertuples():
                dado = {"label": row[1], "value": row[1]}
                lista_func.append(dado)
                dado = {}
            return lista_func

# ==== SUPRIMENTOS TABELAS ==== #

# Função que retorna um DataFrame com os dados dos gerentes da tabela gerente.
def tab_consulta_gerente(banco):
    with sqlite3.connect(banco) as con:
        df_ger_id = pd.read_sql_query("SELECT * FROM gerente", con)
        if df_ger_id.empty:
            return pd.DataFrame()
        else:
            return df_ger_id

# Função que retorna um DataFrame com os dados dos departamentos da tabela departamento.
def tab_consulta_departamento(banco):
    with sqlite3.connect(banco) as con:
        df_dpt_id = pd.read_sql_query(
            """SELECT dpt.id_departamento, dpt.nome_departamento, ger.nome_gerente
               FROM departamento dpt
               LEFT JOIN gerente ger ON (dpt.id_gerente = ger.id_gerente)""",
             con
        )
        if df_dpt_id.empty:
            return pd.DataFrame()
        else:
            return df_dpt_id

# Função que retorna um DataFrame com dados dos funcionarios da tabela funcionario
def tab_consulta_funcionario(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query(
            """SELECT func.id_funcionario, func.nome_funcionario, dpt.nome_departamento, ger.nome_gerente
               FROM funcionario func
               LEFT JOIN departamento dpt ON (func.id_departamento = dpt.id_departamento)
               LEFT JOIN gerente ger ON (func.id_gerente = ger.id_gerente)""", 
            con
        )
        if df_func_id.empty:
            return pd.DataFrame()
        else:
            return df_func_id

# Função que retorna um DataFrame com dados das tabela de tarefas_mestre
def tab_consulta_tarefas_mestre(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query(
            """
                SELECT 
                    tm.id_tarefa, 
                    tm.titulo, 
                    tm.descricao, 
                    tm.data_inicio, 
                    tm.data_final, 
                    ger.nome_gerente, 
                    dpt.nome_departamento, 
                    func.nome_funcionario,
                    niv.desc_nivel,
                    id_relacao_tarefa
                FROM tarefas_mestre tm
                INNER JOIN gerente ger ON (
                    tm.id_gerente = ger.id_gerente
                )
                INNER JOIN departamento dpt ON (
                    tm.id_departamento = dpt.id_departamento
                )
                INNER JOIN funcionario func ON (
                    tm.id_funcionario = func.id_funcionario
                )
                INNER JOIN nivel niv ON (
                    tm.id_nivel = niv.id_nivel
                );
            """,
            con
        )
        if df_func_id.empty:
            return pd.DataFrame()
        else:
            return df_func_id

# Função que retorna um DataFrame com dados para suprir o  tipo de visualização "CONCLUÍDAS".
def tab_consulta_concluidas(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query(
            """
                SELECT 
                    tm.id_tarefa, 
                    tm.titulo, 
                    tm.descricao, 
                    ger.nome_gerente, 
                    dpt.nome_departamento, 
                    func.nome_funcionario, 
                    niv.desc_nivel,
                    tm.data_inicio, 
                    tm.data_final,
                    tcon.data_concl, 
                    id_relacao_tarefa
                FROM tarefas_mestre tm
                INNER JOIN tarefas_concl tcon ON (
                    tm.id_tarefa = tcon.id_tarefa
                )
                INNER JOIN gerente ger ON (
                    tm.id_gerente = ger.id_gerente
                )
                INNER JOIN departamento dpt ON (
                    tm.id_departamento = dpt.id_departamento
                )
                INNER JOIN funcionario func ON (
                    tm.id_funcionario = func.id_funcionario
                )
                INNER JOIN nivel niv ON (
                    tm.id_nivel = niv.id_nivel
                );
            """,
            con
        )
        if df_func_id.empty:
            return pd.DataFrame()
        else:
            return df_func_id

# Função que retorna um DataFrame com dados para suprir o  tipo de visualização "CONCLUÍDAS ANALÍTICO".
def tab_consulta_concluidas_analitico(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query(
            """
                SELECT 
                    tm.id_tarefa, 
                    tm.titulo, 
                    tm.descricao, 
                    ger.nome_gerente, 
                    dpt.nome_departamento, 
                    func.nome_funcionario, 
                    niv.desc_nivel,
                    julianday(tcon.data_concl) - julianday(tm.data_inicio) AS dias_necessarios,
                    CASE
                        WHEN julianday(tcon.data_concl) <= julianday(tm.data_final)
                            THEN "NO PRAZO"
                        ELSE
                            "COM ATRASO"
                    END AS "finalizacao", 
                    id_relacao_tarefa
                FROM tarefas_mestre tm
                INNER JOIN tarefas_concl tcon ON (
                    tm.id_tarefa = tcon.id_tarefa
                )
                INNER JOIN gerente ger ON (
                    tm.id_gerente = ger.id_gerente
                )
                INNER JOIN departamento dpt ON (
                    tm.id_departamento = dpt.id_departamento
                )
                INNER JOIN funcionario func ON (
                    tm.id_funcionario = func.id_funcionario
                )
                INNER JOIN nivel niv ON (
                    tm.id_nivel = niv.id_nivel
                );
            """,
            con
        )
        if df_func_id.empty:
            return pd.DataFrame()
        else:
            return df_func_id

# Função que retorna um DataFrame com dados para suprir o  tipo de visualização "PENDENTES".
def tab_consulta_pendentes(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query(
            """
                SELECT 
                    tm.id_tarefa, 
                    tm.titulo, 
                    tm.descricao, 
                    ger.nome_gerente, 
                    dpt.nome_departamento, 
                    func.nome_funcionario, 
                    niv.desc_nivel,
                    tm.data_inicio, 
                    tm.data_final, 
                    id_relacao_tarefa
                FROM tarefas_mestre tm
                INNER JOIN tarefas_pendentes tpend ON (
                    tm.id_tarefa = tpend.id_tarefa
                )
                INNER JOIN gerente ger ON (
                    tm.id_gerente = ger.id_gerente
                )
                INNER JOIN departamento dpt ON (
                    tm.id_departamento = dpt.id_departamento
                )
                INNER JOIN funcionario func ON (
                    tm.id_funcionario = func.id_funcionario
                )
                INNER JOIN nivel niv ON (
                    tm.id_nivel = niv.id_nivel
                )
                ORDER BY
                    tm.data_final ASC, 
                    tm.id_nivel DESC;
            """,
            con
        )
        if df_func_id.empty:
            return pd.DataFrame()
        else:
            return df_func_id

# Função que retorna um DataFrame com dados para suprir o  tipo de visualização "PENDENTES ANALITICO".
def tab_consulta_pendentes_analitico(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query(
            """
                SELECT 
                    tm.id_tarefa, 
                    tm.titulo, 
                    tm.descricao, 
                    ger.nome_gerente, 
                    dpt.nome_departamento, 
                    func.nome_funcionario, 
                    niv.desc_nivel,
                    tm.data_inicio, 
                    tm.data_final,
                    CASE
                        WHEN julianday(tm.data_final) >= julianday(DATE('now'))
                            THEN 'FALTAM ' || (julianday(tm.data_final) - julianday(DATE('now'))) ||' DIAS'
                        ELSE 
                            'ATRASADA ' || ABS((julianday(tm.data_final) - julianday(DATE('now')))) || ' DIAS'
                    END AS progresso, 
                    id_relacao_tarefa
                FROM tarefas_mestre tm
                INNER JOIN tarefas_pendentes tpend ON (
                    tm.id_tarefa = tpend.id_tarefa
                )
                INNER JOIN gerente ger ON (
                    tm.id_gerente = ger.id_gerente
                )
                INNER JOIN departamento dpt ON (
                    tm.id_departamento = dpt.id_departamento
                )
                INNER JOIN funcionario func ON (
                    tm.id_funcionario = func.id_funcionario
                )
                INNER JOIN nivel niv ON (
                    tm.id_nivel = niv.id_nivel
                )
                ORDER BY
                    tm.data_final ASC, 
                    tm.id_nivel DESC;
            """,
            con
        )
        if df_func_id.empty:
            return pd.DataFrame()
        else:
            return df_func_id

# Função que retorna um DataFrame com dados para suprir o  tipo de visualização "RELACIONADAS".
def tab_consulta_relacionada(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query(
            """
                SELECT 
                    tm.id_tarefa, 
                    tm.titulo, 
                    tm.descricao,  
                    ger.nome_gerente, 
                    dpt.nome_departamento, 
                    func.nome_funcionario,
                    niv.desc_nivel, 
                    tm2.id_tarefa AS id_tarefa2,
                    tm2.titulo AS titulo2,
                    tm2.descricao AS descricao2,
                    ger2.nome_gerente AS nome_gerente2,
                    dpt2.nome_departamento AS departamento2,
                    func2.nome_funcionario AS funcionario2,
                    niv2.desc_nivel AS desc_nivel2
                FROM tarefas_mestre tm
                INNER JOIN tarefas_mestre tm2 ON (
                    tm.id_tarefa = tm2.id_relacao_tarefa
                )
                INNER JOIN gerente ger ON (
                    tm.id_gerente = ger.id_gerente
                )
                INNER JOIN gerente ger2 ON (
                    ger2.id_gerente = tm2.id_gerente
                )
                INNER JOIN departamento dpt ON (
                    tm.id_departamento = dpt.id_departamento
                )
                INNER JOIN departamento dpt2 ON (
                    tm2.id_departamento = dpt2.id_departamento
                )
                INNER JOIN funcionario func ON (
                    tm.id_funcionario = func.id_funcionario
                )
                INNER JOIN funcionario func2 ON (
                    tm2.id_funcionario = func2.id_funcionario
                )
                INNER JOIN nivel niv ON (
                    tm.id_nivel = niv.id_nivel
                )
                INNER JOIN nivel niv2 ON (
                    tm2.id_nivel = niv2.id_nivel
                );
            """,
            con
        )
        if df_func_id.empty:
            return pd.DataFrame()
        else:
            return df_func_id

# Função que retorna um DataFrame com dados para suprir o  tipo de visualização "ADIADAS HISTORICO".
def tab_consulta_adiadas_hist(banco):
    with sqlite3.connect(banco) as con:
        df_func_id = pd.read_sql_query(
            """
                SELECT 
                    tah.id_tar_adiada,
                    tah.id_tarefa,
                    tm.titulo,
                    dpt.nome_departamento,
                    func.nome_funcionario,
                    tah.data_adiamento,
                    tah.prazo_anterior,
                    tah.novo_prazo,
                    (julianday(tah.novo_prazo) - julianday(tah.prazo_anterior)) AS dias_concedidos,
                    tah.motivo_adiamento
                FROM tarefas_adiadas_hist tah
                INNER JOIN tarefas_mestre tm ON (
                    tah.id_tarefa = tm.id_tarefa
                )
                INNER JOIN departamento dpt ON (
                    tah.id_departamento = dpt.id_departamento
                )
                INNER JOIN funcionario func ON (
                    tah.id_funcionario = func.id_funcionario
                );
            """,
            con
        )
        if df_func_id.empty:
            return pd.DataFrame()
        else:
            return df_func_id

# Dicionário contendo dados com opções visualização das tarefas na tabela.
tipo_visualizacao = [
    {"label": "TAREFAS CONCLUÍDAS", "value": "t-concluidas"},
    {"label": "TAREFAS CONCLUÍDAS ANALÍTICO", "value": "t-concluidas-anl"},
    {"label": "TAREFAS PENDENTES", "value": "t-pendentes"},
    {"label": "TAREFAS PENDENTES ANALÍTICO", "value": "t-pendentes-anl"},
    {"label": "TAREFAS RELACIONADAS", "value": "t-relacionadas"},
    {"label": "TAREFAS ADIADAS HISTORICO", "value": "t-adiadas-hist"}
]

# ==== CONSULTAS PARA AUXILIAR NO LANÇAMENTO DE EXCESSÕES ==== #
def verificar_id_adiar_tarefa(id_tarefa):
    id_tar = (int(id_tarefa),)
    with sqlite3.connect(banco) as con:
        cursor = con.cursor()
        cursor.execute(
            """SELECT tm.data_final 
               FROM tarefas_mestre tm
               INNER JOIN tarefas_pendentes tpend ON (
                   tm.id_tarefa = tpend.id_tarefa
               ) 
               WHERE tm.id_tarefa = ?""",
            id_tar
        )
        data = cursor.fetchone()[0]
        cursor.close()
        return str(data)
