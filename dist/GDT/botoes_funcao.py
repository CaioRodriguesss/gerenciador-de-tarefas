import sqlite3
import datetime
import excessoes as EX

banco = 'gerenciador.db'

# ========== ABA PRINCIPAL ========== #

# ===== GERENTES ===== #

# === BOTAO ADICIONAR GERENTE - TABELA gerente === #

def adicionar_gerente(nome_gerente):
    nome = (str(nome_gerente).strip().upper(),)
    try:
        with sqlite3.connect(banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO gerente(nome_gerente) VALUES(?)""",
                nome
            )
            conexao.commit()
            cursor.close
    except sqlite3.Error as er:
        print(er)

# === BOTAO ALTERAR GERENTE - TABELA gerente === #

def alterar_gerente(id_gerente, nome_gerente):
    dados = (str(nome_gerente).strip().upper(), int(id_gerente))

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """UPDATE gerente SET nome_gerente = ? WHERE id_gerente = ?""",
            dados
        )
        conexao.commit()
        cursor.close

# === BOTAO REMOVER GERENTE - TABELA gerente === #

def remover_gerente(id_gerente):
    id_ger = (int(id_gerente),)

    if consulta_gerente_designado(id_ger) is True:
        raise EX.GerenteDesignadoDepartamento("Não é possível remover um gerente já designado a um departamento.")
    else:
        pass

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """DELETE FROM gerente WHERE id_gerente = ?""",
            id_ger
        )
        if cursor.rowcount == 1:
            conexao.commit()
        else:
            conexao.rollback()
            print("erro")
        cursor.close


# ===== DEPARTAMENTOS ===== #

# === BOTAO ADICIONAR DEPARTAMENTO - TABELA departamento === #

def adicionar_departamento(nome_dpt, id_gerente=None):
    nome = str(nome_dpt).strip().upper()
    id_ger = id_gerente

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """INSERT INTO departamento(nome_departamento, id_gerente) VALUES(?, ?)""", 
            (nome, id_ger)
        )
        conexao.commit()
        cursor.close()

# === BOTAO ALTERAR NOME DEPARTAMENTO - TABELA departamento === # (Será que é bom permitir atualizar o gerente do departamento?)

def alterar_nome_departamento(id_dpt, nome_dpt):
    dados = (str(nome_dpt).strip().upper(), int(id_dpt))

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """UPDATE departamento SET nome_departamento = ? WHERE id_departamento = ?""",
            dados
        )
        if cursor.rowcount == 1:
            conexao.commit()
        else:
            conexao.rollback
            print("erro")
        cursor.close()

# === BOTAO REMOVER DEPARTAMENTO - TABELA departamento === #

def remover_departamento(id_dpt):
    id_departamento = (int(id_dpt),)

    if consulta_departamento_com_gerente(id_departamento) is True:
        raise EX.DepartamentoComGerenteDesignado("Não é possível remover um departamento com gerente designado.")
    else:
        pass

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """DELETE FROM departamento WHERE id_departamento = ?""",
            id_departamento
        )
        if cursor.rowcount == 1:
            conexao.commit()
        else:
            conexao.rollback
            print("erro")
        cursor.close()

# === BOTAO DESIGNAR GERENTE AO DEPARTAMENTO - TABELA departamento === #

def desig_gerente_departamento(id_dpt, id_gerente):
    dados = (int(id_gerente), int(id_dpt))

    if consulta_departamento_com_gerente((int(id_dpt),)) is True:
        raise EX.DepartamentoComGerenteDesignado("Não é possível efetuar a designação, o departamento já possui um gerente.")
    else:
        pass

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """UPDATE departamento SET id_gerente = ? WHERE id_departamento = ?""",
            dados
        )
        if cursor.rowcount == 1:
            conexao.commit()
        else:
            conexao.rollback
            print("erro")
        if consulta_funcionario_com_gerente(id_dpt) is False:
            cursor.execute(
            """UPDATE funcionario SET id_gerente = ? WHERE id_departamento = ?""",
            dados
            )
            conexao.commit()
        cursor.close()

# === BOTAO RETIRAR GERENTE DE UM DEPARTAMENTO - TABELA departamento === #
def desvincular_gerente_departamento(id_dpt):
    dados = (None, int(id_dpt))

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """UPDATE departamento SET id_gerente = ? WHERE id_departamento = ?""",
            dados
        )
        if cursor.rowcount == 1:
            conexao.commit()
        else:
            conexao.rollback
            print("erro")
        if consulta_funcionario_com_gerente(id_dpt) is True:
            cursor.execute(
            """UPDATE funcionario SET id_gerente = ? WHERE id_departamento = ?""",
            dados
            )
            conexao.commit()
        cursor.close()

# ===== FUNCIONARIOS ===== #

# === BOTAO ADICIONAR FUNCIONARIO - TABELA funcionario === # (04122022 Atualizar a função, o gerente deve estar atrelado ao departamento, caso não esteja
# uma excessão deve ser gerada e impedir a inclusão)

def adicionar_funcionario(nome_func, id_dpt):
    nome = str(nome_func).strip().upper()
    id_departamento = int(id_dpt)

    if consulta_departamento_com_gerente((id_departamento,)) is False:
        raise EX.DepartamentoSemGerenteDesignado("Não é possível adicionar um funcionário utilizando um departamento sem gerente.")
    else:
        pass

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """SELECT id_gerente FROM departamento WHERE id_departamento = ?""",
            (id_departamento,)
        )
        valor = cursor.fetchone()[0] # (Tem que existir uma excessão aqui para o tipo None, assim não permitirá cadastrar um funcionário sem gerente)
        if valor is None:
            pass
        cursor.execute(
            """INSERT INTO funcionario(nome_funcionario, id_departamento, id_gerente) VALUES(?, ?, ?)""",
            (nome, id_departamento, valor)
        )
        conexao.commit()
        cursor.close()

# === BOTAO ALTERAR FUNCIONARIO - TABELA funcionario === # (alterar o comportamento ao alterar um departamento, o gerente deve vir junto)

def alterar_funcionario(id_func=None, nome_func=None, id_dpt=None):
    id_funcionario = id_func
    nome_funcionario = nome_func
    departamento = id_dpt

    if consulta_funcionario_possui_tarefa(int(id_func)) is True:
        raise EX.FuncionarioPossuiUmaTarefa("O funcionário não pode ser alterado porque ele possui uma tarefa.")

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        if nome_funcionario is not None and str(nome_funcionario).strip() != "":
            cursor.execute(
                """UPDATE funcionario SET nome_funcionario = ? WHERE id_funcionario = ?""",
                (str(nome_funcionario).strip().upper(), int(id_funcionario))
            )
            if cursor.rowcount == 1:
                conexao.commit()
            else:
                conexao.rollback()
                print("erro")
        if departamento is not None:
            cursor.execute(
            """SELECT id_gerente FROM departamento WHERE id_departamento = ?""",
            (int(departamento),)
            )
            valor = cursor.fetchone()[0]
            cursor.execute(
                """UPDATE funcionario SET id_departamento = ?, id_gerente = ? WHERE id_funcionario = ?""",
                (int(departamento), valor, int(id_funcionario))
            )
            if cursor.rowcount == 1:
                conexao.commit()
            else:
                conexao.rollback()
                print("erro")
        cursor.close()

# === REMOVER FUNCIONARIO - TABELA funcionario === #

def remover_funcionario(id_func):
    id_funcionario = (int(id_func),)

    if consulta_funcionario_possui_tarefa(int(id_func)) is True:
        raise EX.FuncionarioPossuiUmaTarefa("O funcionário não pode ser removido porque ele possui uma tarefa.")

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """DELETE FROM funcionario WHERE id_funcionario = ?""",
            id_funcionario
        )
        if cursor.rowcount == 1:
            conexao.commit()
        else:
            conexao.rollback
            print("erro")
        cursor.close()

# ===== FUNCOES DA ABA PRINCIPAL ===== #


# ========== ABA TAREFAS ========== #

# ===== TAREFAS ===== #

# === BOTAO ADICIONAR TAREFA - TABELA tarefas_mestre === #
#obs: Existe um TRIGGER  para fazer a adição à tabela tarefas_pendetes após o INSERT de uma tarefa na tabela tarefas_mestre

def adicionar_tarefa(titulo, descricao, data_inicio, data_final, id_func, id_nivel, id_relacao_tarefa):
    titulo = str(titulo).strip().upper()
    descricao = str(descricao).strip().upper()
    data_inicio = datetime.datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
    id_funcionario = int(id_func)
    id_nivel = int(id_nivel)
    id_relacao = int(id_relacao_tarefa) if isinstance(id_relacao_tarefa, int) else None

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        # Efetua a busca do id do departamento e do id do gerente com base no cadastro do funcionário.
        cursor.execute(
            """SELECT id_gerente, id_departamento FROM funcionario WHERE id_funcionario = ?""",
            (id_funcionario,)
        )
        id_valores = cursor.fetchone()
        id_ger = int(id_valores[0])
        id_dpt = int(id_valores[1])
        
        dados = (titulo, descricao, data_inicio, data_final, id_ger, id_dpt, id_funcionario, id_nivel, id_relacao)

        cursor.execute(
            """INSERT INTO tarefas_mestre(
                   titulo, descricao, data_inicio, data_final, id_gerente, id_departamento, id_funcionario, id_nivel, id_relacao_tarefa
               )
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);""",
               dados
        )
        conexao.commit()
        cursor.close()

# === BOTAO ADIAR TAREFA - TABELA tarefas_mestre === #
#obs: Existe um TRIGGER  para fazer a adição à tabela tarefas_adiadas_hist após o UPDATE do prazo na tabela tarefas_mestre

def adiar_tarefa(id_tarefa, nova_data):
    dados = (datetime.datetime.strptime(nova_data, "%Y-%m-%d").date(), int(id_tarefa))

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """UPDATE tarefas_mestre SET data_final = ? WHERE id_tarefa = ?""",
            dados
        )
        if cursor.rowcount == 1:
            conexao.commit()
        else:
            conexao.rollback
            print("erro")
        cursor.close()

# === BOTAO ADIAR TAREFA PARA ADICIONAR O MOTIVO DO ADIAMENTO DA TAREFA - TABELA tarefas_mestre === #
def motivo_adiar_tarefa(id_tarefa, motivo):
    id_tar = (int(id_tarefa),)
    motivo_adiam = str(motivo).strip().upper()

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """SELECT MAX(id_tar_adiada) FROM tarefas_adiadas_hist WHERE id_tarefa = ?""",
            id_tar
        )
        max_id_tar = cursor.fetchone()[0]

        cursor.execute(
            """UPDATE tarefas_adiadas_hist SET motivo_adiamento = ? WHERE id_tar_adiada = ?""",
            (motivo_adiam, int(max_id_tar))
        )
        if cursor.rowcount == 1:
            conexao.commit()
        else:
            conexao.rollback
            print("erro")
        cursor.close()

# === BOTAO FINALIZAR TAREFA - TABELA tarefas_mestre === #

def finalizar_tarefa(id_tarefa):
    id_tarefa = (int(id_tarefa),)

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """SELECT id_tarefa, id_departamento, id_funcionario
               FROM tarefas_mestre
               WHERE id_tarefa = ?""", id_tarefa
        )
        lista = list(cursor.fetchone())
        lista.append(datetime.date.today())

        cursor.execute(
            """INSERT INTO tarefas_concl(id_tarefa, id_departamento, id_funcionario, data_concl)
               VALUES(?, ?, ?, ?)
            """, lista
        )
        cursor.execute(
            """DELETE FROM tarefas_pendentes WHERE id_tarefa = ?""",
            id_tarefa
        )
        if cursor.rowcount == 1:
            conexao.commit()
        else:
            conexao.rollback
            print("erro")
        cursor.close()

# === BOTAO REMOVER TAREFA - TABELA tarefas_mestre === #

# Só irá remover tarefas que estão pendentes, porque os valores que vão para o DROPDOWN de remoção de tarefas conta somente com tarefas pendentes.
# As tarefas que já foram finalizadas não poderão ser removidas pela aplicação, somente na marretada.
def remover_tarefa(id_tarefa):
    id_tarefa = (int(id_tarefa),)
    valor_nulo = None

    with sqlite3.connect(banco) as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """DELETE FROM tarefas_mestre WHERE id_tarefa = ?""",
            id_tarefa
        )
        cursor.execute(
            """DELETE FROM tarefas_pendentes WHERE id_tarefa = ?""",
            id_tarefa
        )
        cursor.execute(
            """DELETE FROM tarefas_adiadas_hist WHERE id_tarefa = ?""",
            id_tarefa
        )
        # Remove a relação de uma tarefa que esta sendo excluída de outras tarefas, ou seja, caso a tarefa que está sendo
        # excluída tenha sido relacionada à outras tarefas, ela será excluída do campo de relação destas tarefas.
        cursor.execute(
            """UPDATE tarefas_mestre SET id_relacao_tarefa = ? WHERE id_relacao_tarefa = ?""",
            (valor_nulo, int(id_tarefa[0]))
        )
        conexao.commit()
        cursor.close()

# ===== CONSULTAS PARA EXCESSOES DE INTEGRIDADE ===== #

# Consulta para verificar se o gerente que será removido já está designado a um departamento. Em caso positivo, a função retornará
# True, impedindo que o gerente seja removido, em caso negativo, False, removendo o gerente. 
def consulta_gerente_designado(id_gerente):
    with sqlite3.connect(banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT MIN(id_gerente) FROM departamento WHERE id_gerente = ?""",
                id_gerente
            )
            valor = cursor.fetchone()[0]
            cursor.close()
            if valor is None:
                return False
            if valor:
                return True

# Consulta para verificar se o departamento possui um gerente designado. Em caso positivo, a função retornará True, impedindo que o departamento
# seja removido, em caso negativo, False, removendo o departamento.
def consulta_departamento_com_gerente(id_departamento):
    with sqlite3.connect(banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT id_gerente FROM departamento WHERE id_departamento = ?""",
                id_departamento
            )
            valor = cursor.fetchone()[0]
            cursor.close()
            if valor is None:
                return False
            if valor:
                return True


# Consulta para verificar se um funcionário possui um gerente designado na tabela funcionario, caso possua, ele retorna True,
# caso não, ele retorna False. Serve para saber se o desvincular departamento deve também atualizar a tabela de funcionário.
def consulta_funcionario_com_gerente(id_dpt):
    id_departamento = (int(id_dpt),)

    with sqlite3.connect(banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT MIN(id_gerente) FROM funcionario WHERE id_departamento = ?""",
                id_departamento
            )
            valor = cursor.fetchone()[0]
            cursor.close()
            if valor is None:
                return False
            if valor:
                return True

# Consulta para verificar se o funcionário já foi designado a uma tarefa e gerar uma excessão que não permitirá que ele seja removido.
def consulta_funcionario_possui_tarefa(id_funcionario):
    id_func = (int(id_funcionario),)

    with sqlite3.connect(banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT MIN(id_tarefa), id_funcionario FROM tarefas_mestre WHERE id_funcionario = ?""",
                id_func
            )
            valor = cursor.fetchone()[1]
            cursor.close()
            if valor is None:
                return False
            if valor:
                return True
