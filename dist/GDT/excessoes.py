# ===== EXCESSOES PARA A PAGINA PRINCIPAL ===== #

# Campo obrigatório não preenchido.
class CampoNaoPreenchido(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)

# Gerente designado a um departamento.
class GerenteDesignadoDepartamento(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)

# Departamento com gerente designado.
class DepartamentoComGerenteDesignado(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)

# Departamento sem gerente designado. Utilizada ao tentar adicionar um funcionário e atrelar um departamento que não possui um gerente.
class DepartamentoSemGerenteDesignado(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)

# ===== EXCESSOES PARA A PARTE DE TAREFAS ===== #

# Excessão para evitar que a data final de uma nova tarefa seja menor que a data inicial.
class DataFinalMenorQueDataInicial(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)

# Excessão para evitar que a nova data de uma tarefa que foi adiada seja menor do que a data atual.
class NovaDataMenorQueaAtual(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)

# Excessão para não permitir remover um funcionário que foi designado a uma tarefa.
class FuncionarioPossuiUmaTarefa(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)