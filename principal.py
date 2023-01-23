from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import suprimento_dados as supD
import locale
from datetime import date

locale.setlocale(locale.LC_ALL, "pt_BR.utf-8")

# Banco de dados do gerenciador de tarefas.
banco = "gerenciador.db"

# ===== SUPRIMENTO DE DADOS PARA OS DROPDOWNS DA ABA PRINCIPAL ===== #

# Suprimento de dados para os dropdowns de gerente.
drp_dados_gerente = supD.drp_consulta_gerente(banco)

# Suprimento de dados para os dropdowns de departamento.
drp_dados_departamento = supD.drp_consulta_departamento(banco)

# Suprimento de dados para os dropdowns de funcionarios.
drp_dados_funcionario = supD.drp_consulta_funcionario(banco)

# Suprimento de dados para os dropdowns de nível das tarefas.
drp_dados_nivel = supD.drp_consulta_nivel(banco)

# Suprimento de dados para os dropdowns de tarefa relacionada das tarefas (utiliza a tabela tarefas_pendentes).
drp_dados_tarefa_relacionada = supD.drp_consulta_tarefa_relacionada(banco)

# ===== SUPRIMENTO DE DADOS PARA AS TABELAS ===== #

# Suprimento de dados para a tabela de gerentes
tab_dados_gerente = supD.tab_consulta_gerente(banco)

# Suprimento de dados para a tabela de departamento
tab_dados_departamento = supD.tab_consulta_departamento(banco)

# Suprimento de dados para a tabela de funcionarios
tab_dados_funcionario = supD.tab_consulta_funcionario(banco)

# Suprimento de dados para a tabela de tarefas com dados da tabela tarefas_mestre. Excluir depois 08 01 2023
tab_dados_tabela_mestre = supD.tab_consulta_tarefas_mestre(banco)

# Suprimento de dados para a tabela de tarefas com dados de acordo com o tipo de visualização selecionado no dropdown.
# Inicia com a consulta de tarefas pendetes 08 01 2023
tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes(banco)

# ===== ESTILIZAÇÃO DAS TABELAS DA ABA PRINCIPAL ===== #

# Estilo do cabeçalho das tabelas.
table_header_style = {
    "background-color": "rgb(30, 30, 30)",
    "overflow": "hidden",
    "textOverflow": "clip",
    "maxWidth": 0,
    "textAlign": "left",
}

# Estilo do corpo (celulas) das tabelas.
table_cell_style = {
    "background-color": "rgb(50, 50, 50)",
    "overflow": "hidden",
    "textOverflow": "clip",
    "maxWidth": 0,
    "textAlign": "left"
}

# Estilo do filtro das tabelas.
table_filter_style = {
    "backgroundColor": "rgb(50, 50, 50)",
    "color": "white"
}

    # ===== LAYOUT PRINCIPAL ===== #

# Layout da aba principal que irá alimentar o id "main" ao app.py.
principal_layout = dbc.Row(
    [
        # Modal para comportar as excessoes da parte principal.
        dbc.Modal(
            [
                dbc.ModalHeader([], id="mod-head-excessao", class_name="modal-header modal-excessao"),
                dbc.ModalBody([], id="mod-body-excessao")
            ],
            id="modal-excessao",
            is_open=False
        ),

        # Modal para comportar as excessoes da parte de tarefas.
        dbc.Modal(
            [
                dbc.ModalHeader([], id="mod-head-excessao-tarefas", class_name="modal-header modal-excessao"),
                dbc.ModalBody([], id="mod-body-excessao-tarefas")
            ],
            id="modal-excessao-tarefas",
            is_open=False
        ),

        # Titulo da parte de Cadastros.
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(["CADASTROS"], id="titulo-cadastros", className="h2-titulo-secao")
                    ],
                    class_name="col-titulo",
                    width=12,
                    md=4
                )
            ],
            align="center",
            justify="center",
            style={"height": "10vh"},
            class_name="row-titulos"
        ),

        # Conteúdo de manipulação
        dbc.Row(
            [
                # Coluna da tabela de gerentes
                dbc.Col(
                    [
                        # Modal para adicionar um gerente
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Adicionar Gerente"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["Nome:"]), 
                                        dcc.Input(
                                            id="mod-in-add-ger", 
                                            type="text", 
                                            maxLength=50, 
                                            debounce=True, 
                                            className="input-medio",
                                            placeholder="Nome do gerente que será adicionado..."
                                        )
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Adicionar", id="mod-btn-add-ger"), dbc.Button("Cancelar", id="mod-btn-add-ger-cancel")])
                            ],
                            id="modal-add-ger",
                            is_open=False
                        ),

                        # Modal para alterar um gerente
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Alterar Gerente"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["ID:"]), 
                                        dcc.Dropdown(
                                            options=drp_dados_gerente,
                                            id="mod-drp-alt-ger-id",
                                            placeholder="Selecione um gerente...",
                                            searchable=False,
                                            clearable=False
                                        ),
                                        html.H4(["Nome:"]), 
                                        dcc.Input(
                                            id="mod-in-alt-ger-nom", 
                                            type="text", 
                                            maxLength=50, 
                                            debounce=True, 
                                            className="input-medio",
                                            placeholder="Novo nome para o gerente selecionado..."
                                        )
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Alterar", id="mod-btn-alt-ger"), dbc.Button("Cancelar", id="mod-btn-alt-ger-cancel")])
                            ],
                            id="modal-alt-ger",
                            is_open=False
                        ),

                        # Modal para remover um gerente
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Remover Gerente"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["ID:"]), 
                                        dcc.Dropdown(
                                            options=drp_dados_gerente,
                                            id="mod-drp-rem-ger-id",
                                            placeholder="Selecione um gerente...",
                                            searchable=False,
                                            clearable=False
                                        )
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Remover", id="mod-btn-rem-ger"), dbc.Button("Cancelar", id="mod-btn-rem-ger-cancel")])
                            ],
                            id="modal-rem-ger",
                            is_open=False
                        ),


                        # Tabela com dados dos gerentes e botões com funções
                        html.Div([html.H2(["Tabela de Gerentes"], className="h2-texto-tabela")], className="div-texto-tabela"),
                        html.Div(
                            [
                                dbc.Button("Adicionar Gerente", id="btn-add-ger", n_clicks=0),
                                dbc.Button("Alterar Gerente", id="btn-alt-ger", n_clicks=0),
                                dbc.Button("Remover Gerente", id="btn-rem-ger", n_clicks=0)
                            ],
                            className="div-botoes"
                        ),

                        # Div da tabela de gerentes
                        html.Div(
                            [
                                dash_table.DataTable(
                                    data=tab_dados_gerente.to_dict("records"),
                                    columns=[{"name": col, "id": col} for col in tab_dados_gerente.columns],
                                    id="tabela-gerente",
                                    style_header=table_header_style,
                                    style_data=table_cell_style,
                                    page_size=5,
                                    filter_action="native",
                                    filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                    style_filter=table_filter_style,
                                    tooltip_data=[
                                        {
                                            column: {"value": str(value), "type": "markdown"}
                                            for column, value in row.items()
                                        } for row in tab_dados_gerente.to_dict("records")
                                    ],
                                    tooltip_duration=None
                                )
                            ],
                            id="div-tabela-gerente"
                        ),  
                    ],
                    md=4,
                    sm=12,
                    class_name="col col-tabelas"
                ),

                # Coluna da tabela de departamentos
                dbc.Col(
                    [
                        # Modal para adicionar um departamento
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Adicionar Departamento"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["Nome:"]), 
                                        dcc.Input(
                                            id="mod-in-add-dpt", 
                                            type="text", 
                                            maxLength=50, 
                                            debounce=True,
                                            className="input-medio",
                                            placeholder="Nome do departamento que será adicionado..."
                                        )
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Adicionar", id="mod-btn-add-dpt"), dbc.Button("Cancelar", id="mod-btn-add-dpt-cancel")])
                            ],
                            id="modal-add-dpt",
                            is_open=False
                        ),
                        
                        # Modal para alterar um departamento
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Alterar Departamento"),
                                dbc.ModalBody(
                                    [
                                        html.H4(["ID:"]), 
                                        dcc.Dropdown(
                                            options=drp_dados_departamento ,
                                            id="mod-drp-alt-dpt-id",
                                            placeholder="Selecione um departamento...",
                                            searchable=False,
                                            clearable=False
                                        ),
                                        html.H4(["Nome:"]), 
                                        dcc.Input(
                                            id="mod-in-alt-dpt-nom", 
                                            type="text", 
                                            maxLength=50, 
                                            debounce=True, 
                                            className="input-medio",
                                            placeholder="Novo nome para o departamento selecionado..."
                                        )
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Alterar", id="mod-btn-alt-dpt"), dbc.Button("Cancelar", id="mod-btn-alt-dpt-cancel")])
                            ],
                            id="modal-alt-dpt",
                            is_open=False
                        ),

                        # Modal para remover um departamento
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Remover Departamento"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["ID:"]), 
                                        dcc.Dropdown(
                                            options=drp_dados_departamento ,
                                            id="mod-drp-rem-dpt-id",
                                            placeholder="Selecione um departamento...",
                                            searchable=False,
                                            clearable=False
                                        )
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Remover", id="mod-btn-rem-dpt"), dbc.Button("Cancelar", id="mod-btn-rem-dpt-cancel")])
                            ],
                            id="modal-rem-dpt",
                            is_open=False
                        ),

                        # Modal para designar um gerente a um departamento
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Designar gerente a um departamento"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["ID Gerente:"]), 
                                        dcc.Dropdown(
                                            options=drp_dados_gerente,
                                            id="mod-drp-desig-ger-id",
                                            placeholder="Selecione um gerente...",
                                            searchable=False,
                                            clearable=False
                                        ),
                                        html.H4(["ID Departamento:"]), 
                                        dcc.Dropdown(
                                            options=drp_dados_departamento ,
                                            id="mod-drp-desig-dpt-id",
                                            placeholder="Selecione um departamento...",
                                            searchable=False,
                                            clearable=False
                                        )
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Designar", id="mod-btn-desig-ger-dpt"), dbc.Button("Cancelar", id="mod-btn-desig-ger-dpt-cancel")])
                            ],
                            id="modal-desig-ger-dpt",
                            is_open=False
                        ),

                        # Modal para desvincular um gerente de um departamento
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Desvincular gerente de um departamento"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["ID Departamento:"]), 
                                        dcc.Dropdown(
                                            options=drp_dados_departamento,
                                            id="mod-drp-desv-dpt-id",
                                            placeholder="Selecione um departamento...",
                                            searchable=False,
                                            clearable=False
                                        )
                                    ]
                                ),
                                dbc.ModalFooter(
                                    [dbc.Button("Desvincular", id="mod-btn-desv-ger-dpt"), dbc.Button("Cancelar", id="mod-btn-desv-ger-dpt-cancel")]
                                )
                            ],
                            id="modal-desv-ger-dpt",
                            is_open=False
                        ),

                        html.Div([html.H2(["Tabela de Departamentos"], className="h2-texto-tabela")], className="div-texto-tabela"),
                        html.Div(
                            [
                                dbc.Button("Adicionar Departamento", id="btn-add-dpt", n_clicks=0),
                                dbc.Button("Alterar Departamento", id="btn-alt-dpt", n_clicks=0),
                                dbc.Button("Remover Departamento", id="btn-rem-dpt", n_clicks=0),
                                dbc.Button("Designar Gerente", id="btn-desig-ger-dpt", n_clicks=0),
                                dbc.Button("Desvincular Gerente", id="btn-desv-ger-dpt", n_clicks=0)
                            ],
                            className="div-botoes"
                        ),

                        # Div da tabela de departamentos
                        html.Div(
                            [
                                dash_table.DataTable(
                                    data=tab_dados_departamento.to_dict("records"),
                                    columns=[{"name": col, "id": col} for col in tab_dados_departamento.columns],
                                    id="tabela-departamento",
                                    style_header=table_header_style,
                                    style_data=table_cell_style,
                                    page_size=5,
                                    filter_action="native",
                                    filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                    style_filter=table_filter_style,
                                    tooltip_data=[
                                        {
                                            column: {"value": str(value), "type": "markdown"}
                                            for column, value in row.items()
                                        } for row in tab_dados_departamento.to_dict("records")
                                    ],
                                    tooltip_duration=None
                                )
                            ],
                            id="div-tabela-departamento"
                        )
                    ],
                    md=4,
                    sm=12,
                    class_name="col col-tabelas"
                ),

                # Coluna da tabela de funcionários
                dbc.Col(
                    [
                        # Modal para adicionar um funcionário
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Adicionar Funcionário"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["Nome:"]), 
                                        dcc.Input(
                                            id="mod-in-add-func", 
                                            type="text", 
                                            maxLength=50, 
                                            debounce=True, 
                                            className="input-medio",
                                            placeholder="Nome do funcionário que será adicionado..."
                                        ),
                                        html.H4(["ID Departamento:"]), 
                                        dcc.Dropdown(
                                            options=drp_dados_departamento,
                                            id="mod-drp-add-func-dpt-id",
                                            placeholder="Selecione um departamento...",
                                            searchable=False,
                                            clearable=False
                                        ),
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Adicionar", id="mod-btn-add-func"), dbc.Button("Cancelar", id="mod-btn-add-func-cancel")])
                            ],
                            id="modal-add-func",
                            is_open=False
                        ),

                        # Modal para alterar dados de um funcionário já cadastrado
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Alterar dados Funcionário"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["ID Funcionário:"]),
                                        dcc.Dropdown(
                                            options=drp_dados_funcionario,
                                            id="mod-drp-alt-func-func-id",
                                            placeholder="Selecione um funcionário...",
                                            searchable=False,
                                            clearable=False
                                        ),
                                        html.H4(["Nome:"]), 
                                        dcc.Input(
                                            id="mod-in-alt-func", 
                                            type="text", 
                                            maxLength=50, 
                                            debounce=True, 
                                            className="input-medio",
                                            placeholder="Novo nome para o funcionário selecionado..."
                                        ),
                                        html.H4(["ID Departamento:"]),
                                        dcc.Dropdown(
                                            options=drp_dados_departamento,
                                            id="mod-drp-alt-func-dpt-id",
                                            placeholder="Selecione um departamento...",
                                            searchable=False
                                        ),
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Alterar", id="mod-btn-alt-func"), dbc.Button("Cancelar", id="mod-btn-alt-func-cancel")])
                            ],
                            id="modal-alt-func",
                            is_open=False
                        ),

                        # Modal para remover um funcionário
                        dbc.Modal(
                            [
                                dbc.ModalHeader(["Remover Funcionário"]),
                                dbc.ModalBody(
                                    [
                                        html.H4(["ID Funcionário:"]),
                                        dcc.Dropdown(
                                            options=drp_dados_funcionario,
                                            id="mod-drp-rem-func-func-id",
                                            placeholder="Selecione um funcionário...",
                                            searchable=False,
                                            clearable=False
                                        ),
                                    ]
                                ),
                                dbc.ModalFooter([dbc.Button("Remover", id="mod-btn-rem-func"), dbc.Button("Cancelar", id="mod-btn-rem-func-cancel")])
                            ],
                            id="modal-rem-func",
                            is_open=False
                        ),

                        html.Div([html.H2(["Tabela de Funcionários"], className="h2-texto-tabela")], className="div-texto-tabela"),
                        html.Div(
                            [
                                dbc.Button("Adicionar Funcionário", id="btn-add-func", n_clicks=0),
                                dbc.Button("Alterar Funcionário", id="btn-alt-func", n_clicks=0),
                                dbc.Button("Remover Funcionário", id="btn-rem-func", n_clicks=0)
                            ],
                            className="div-botoes"
                        ),

                        # Div da tabela de funcionários.
                        html.Div(
                            [
                                dash_table.DataTable(
                                    data=tab_dados_funcionario.to_dict("records"),
                                    columns=[{"name": col, "id": col} for col in tab_dados_funcionario.columns],
                                    id="tabela-funcionario",
                                    style_header=table_header_style,
                                    style_data=table_cell_style,
                                    page_size=5,
                                    filter_action="native",
                                    filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                    style_filter=table_filter_style,
                                    tooltip_data=[
                                        {
                                            column: {"value": str(value), "type": "markdown"}
                                            for column, value in row.items()
                                        } for row in tab_dados_funcionario.to_dict("records")
                                    ],
                                    tooltip_duration=None
                                )
                            ],
                            id="div-tabela-funcionario"
                        )
                    ],
                    md=4,
                    sm=12,
                    class_name="col col-tabelas"
                ),
            ],
            justify="between",
            style={"height": "84vh"},
            class_name="row-tabelas-principal"
        ),

        # Titulo da parte de Tarefas.
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(["TAREFAS"], id="titulo-tarefas", className="h2-titulo-secao")
                    ],
                    class_name="col-titulo",
                    width=12
                )
            ],
            align="center",
            justify="center",
            style={"height": "10vh"},
            class_name="row-titulos",
        ),

        # Linha com dados das tarefas 17/12/2022 - (problema de alternação e atualização de páginas)
        dbc.Row(
            [
                # Linha contendo os botões de suprimento de dados.
                dbc.Row(
                    [
                        html.Div(
                            [
                                # Modal para adicionar uma tarefa.
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Adicionar tarefa"),
                                        dbc.ModalBody(
                                            [
                                                html.H4("Título"),
                                                dcc.Input(
                                                    id="mod-in-add-tar-tit", 
                                                    type="text", 
                                                    maxLength=50, 
                                                    debounce=True, 
                                                    className="input-medio",
                                                    placeholder="Título da tarefa que será adicionada..."
                                                ),
                                                html.H4("Descrição"),
                                                dcc.Textarea(
                                                    id="mod-textarea-add-tar-desc", 
                                                    maxLength=1000, 
                                                    className="area-texto", 
                                                    rows=3,
                                                    placeholder="Descrição da tarefa que será adicionada..."
                                                ),
                                                html.H4("Data de Início"),
                                                dcc.DatePickerSingle(
                                                    id="mod-date-add-tar-inicio",
                                                    min_date_allowed=date(2022, 12, 1),
                                                    month_format="DD/MM/YYYY",
                                                    display_format="DD/MM/YYYY",
                                                    date=date.today()
                                                ),
                                                html.H4("Data Final"),
                                                dcc.DatePickerSingle(
                                                    id="mod-date-add-tar-final",
                                                    min_date_allowed=date(2022, 12, 1),
                                                    month_format="DD/MM/YYYY",
                                                    display_format="DD/MM/YYYY",
                                                    date=date.today()
                                                ),
                                                html.H4("Funcionário"),
                                                dcc.Dropdown(
                                                    options=drp_dados_funcionario,
                                                    id="mod-drp-add-tar-func-id",
                                                    placeholder="Selecione um funcionário...",
                                                    searchable=False,
                                                    clearable=False
                                                ),
                                                html.H4("Nível da Tarefa"),
                                                dcc.Dropdown(
                                                    options=drp_dados_nivel,
                                                    id="mod-drp-add-tar-nivel",
                                                    placeholder="Selecione um nível...",
                                                    searchable=False,
                                                    clearable=False
                                                ),
                                                html.H4("Tarefa Relacionada"),
                                                dcc.Dropdown(
                                                    options=drp_dados_tarefa_relacionada,
                                                    id="mod-drp-add-tar-relacionada",
                                                    placeholder="Selecione uma tarefa relacionada...",
                                                    searchable=False
                                                )
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Adicionar", id="mod-btn-add-tar"), 
                                                dbc.Button("Cancelar", id="mod-btn-add-tar-cancel")
                                            ]
                                        )
                                    ],
                                    id="modal-add-tar",
                                    is_open=False
                                ),
                                
                                # Modal para adiar um tarefa.
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Adiar tarefa"),
                                        dbc.ModalBody(
                                            [
                                                html.H4("ID Tarefa"),
                                                dcc.Dropdown(
                                                    options=drp_dados_tarefa_relacionada,
                                                    id="mod-drp-adiar-tar-tar-id",
                                                    placeholder="Selecione uma tarefa para adiar...",
                                                    searchable=False,
                                                    clearable=False
                                                ),
                                                html.H4("Nova Data"),
                                                dcc.DatePickerSingle(
                                                    id="mod-date-adiar-tar-nova-data",
                                                    min_date_allowed=date(2022, 12, 1),
                                                    month_format="DD/MM/YYYY",
                                                    display_format="DD/MM/YYYY",
                                                    date=date.today()
                                                ),
                                                html.H4("Motivo do Adiamento"),
                                                dcc.Textarea(
                                                    id="mod-textarea-adiar-tar-mot", 
                                                    maxLength=1000,
                                                    className="area-texto", 
                                                    rows=3,
                                                    placeholder="Motivo da tarefa ser adiada..."
                                                )
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Adiar", id="mod-btn-adiar-tar"), 
                                                dbc.Button("Cancelar", id="mod-btn-adiar-tar-cancel")
                                            ]
                                        )
                                    ],
                                    id="modal-adiar-tar",
                                    is_open=False
                                ),

                                # Modal para finalizar uma tarefa.
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Finalizar tarefa"),
                                        dbc.ModalBody(
                                            [
                                                html.H4("ID Tarefa"),
                                                dcc.Dropdown(
                                                    options=drp_dados_tarefa_relacionada,
                                                    id="mod-drp-finalizar-tar-tar-id",
                                                    placeholder="Selecione uma tarefa para finalizar...",
                                                    searchable=False,
                                                    clearable=False
                                                ),
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Finalizar", id="mod-btn-finalizar-tar"), 
                                                dbc.Button("Cancelar", id="mod-btn-finalizar-tar-cancel")
                                            ]
                                        )
                                    ],
                                    id="modal-finalizar-tar",
                                    is_open=False
                                ),

                                # Modal para remover uma tarefa
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Remover Tarefa"),
                                        dbc.ModalBody(
                                            [
                                                html.H4("ID Tarefa"),
                                                dcc.Dropdown(
                                                    options=drp_dados_tarefa_relacionada,
                                                    id="mod-drp-rem-tar-tar-id",
                                                    placeholder="Selecione uma tarefa para remover...",
                                                    searchable=False,
                                                    clearable=False
                                                ),
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Remover", id="mod-btn-rem-tar"),
                                                dbc.Button("Cancelar", id="mod-btn-rem-tar-cancel")
                                            ]
                                        )
                                    ],
                                    id="modal-rem-tar",
                                    is_open=False
                                ),

                                dbc.Button("Adicionar Tarefa", id="btn-add-tar", n_clicks=0, class_name="botoes-tarefas-temporario"),
                                dbc.Button("Adiar Tarefa", id="btn-adiar-tar", n_clicks=0, class_name="botoes-tarefas-temporario"),
                                dbc.Button("Finalizar Tarefa", id="btn-finalizar-tar", n_clicks=0, class_name="botoes-tarefas-temporario"),
                                dbc.Button("Remover Tarefa", id="btn-rem-tar", n_clicks=0, class_name="botoes-tarefas-temporario") 
                            ],
                            className="div-botoes-tarefas"
                        )
                    ],
                    class_name="row-tabela-botoes"
                ),

                # Linha contendo os dropdowns de filtros
                dbc.Row(
                    [
                        html.Div(
                            [
                                html.H4(["Selecione o tipo de visualização desejada: "], className="texto-tipo-visualizacao"),
                                dcc.Dropdown(
                                    options=supD.tipo_visualizacao,
                                    id="drp-tipo-visualizacao",
                                    value="t-pendentes",
                                    searchable=False,
                                    clearable=False,
                                    className="tamanho-dropdown"
                                ),
                            ],
                            className="div-tipo-visualizacao"
                        )
                    ],
                    class_name="row-tabela-dropdown-tipo-visualizacao"
                ),
                
                # Linha contendo a dica de uso das funcionalidades da tabela.
                dbc.Row(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        html.P(
                                            [
                                                """Visualizar dados: Os dados podem ser melhor visualizados posicionando
                                                   o cursor do mouse sobre a célula da tabela na qual está contido o dado."""
                                            ]
                                        ),
                                        html.P(
                                            [
                                                """Filtrar dados do tipo texto: Os dados são interpretados pela tabela como dados
                                                   do tipo texto após pressionar a tecla "Enter". A forma padrão de filtro está em
                                                   buscar correspondências nas células da coluna para o conjunto de caracteres
                                                   digitado. Por exemplo, digitar ba possibilita encontrar barco, balsa e abacate."""
                                            ]
                                        ),
                                        html.P(
                                            [
                                                """Filtrar dados do tipo data: Dados do tipo data podem ser filtrados utilizando
                                                   os caracteres que compõe a data, em busca de datas correspondentes,
                                                   como acontece com o filtro de dados do tipo texto. Além disso, é possível
                                                   utilizar os operadores maior (>), menor (<), igual (=), maior ou igual (>=) e 
                                                   menor ou igual (<=). Por exemplo, 2022-01 trará dados de janeiro de 2022, 
                                                   mas > 2022-01 trará dados a partir de janeiro de 2022."""
                                            ]
                                        ),
                                        html.P(
                                            [
                                                """Filtrar dados do tipo numérico: Os dados númericos devem ser postos entre aspas
                                                   para efetuar as buscas e encontrar correspondências exatas. Além disso, é possível
                                                   utilizar os operadores maior (>), menor (<), igual (=), maior ou igual (>=) e 
                                                   menor ou igual (<=). No entanto, ao utilizar esses operadores, deve-se comparar
                                                   com um dado existente na tabela (melhorias futuras podem corrigir o comportamento). """
                                            ]
                                        )
                                    ],
                                    title="Dicas de uso relacionadas às funcionalidades da tabela",
                                    class_name="definicao-accordionitem"
                                ),
                            ],
                            flush=True,
                            class_name="definicao-accordion",
                            start_collapsed=True
                        )
                    ]
                ),

                # Linha contendo a tabela.
                dbc.Row(
                    [
                        dash_table.DataTable(
                            data=tab_dados_tipo_visualizacao.to_dict("records"),
                            columns=[{"name": col, "id": col} for col in tab_dados_tipo_visualizacao.columns],
                            id="tabela-tarefas-mestre",
                            style_header=table_header_style,
                            style_data=table_cell_style,
                            page_size=10,
                            filter_action="native",
                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                            style_filter=table_filter_style,
                            tooltip_data=[
                                {
                                    column: {"value": str(value), "type": "markdown"}
                                    for column, value in row.items()
                                } for row in tab_dados_tipo_visualizacao.to_dict("records")
                            ],
                            tooltip_duration=None,
                            style_data_conditional = [
                                {
                                    "if": {
                                        "filter_query": f"{{data_final}} < {date.today()}"
                                    },
                                    "backgroundColor": "rgba(254, 38, 68, 0.6)"
                                }
                            ]
                        ),
                    ],
                    id="row-tab-mestre",
                    class_name="row-tabela-tarefas"
                )
            ],
            class_name="row-tarefas"
        ),

        # Titulo da parte de Dados.
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(["DADOS"], id="titulo-dados", className="h2-titulo-secao")
                    ],
                    class_name="col-titulo",
                    width=12,
                    md=4
                )
            ],
            align="center",
            justify="center",
            style={"height": "10vh"},
            class_name="row-titulos"
        ),

    ],
    class_name="row-tabelas-principal"
)