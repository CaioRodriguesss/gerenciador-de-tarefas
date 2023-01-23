from dash import Dash, html, Input, Output, dash_table, ctx, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import principal
import botoes_funcao as BF
import suprimento_dados as supD
import excessoes as EX
import datetime
from endereco import e_host, e_porta

# Banco de dados utilizado.
banco = "gerenciador.db"

# Definção do host
host = e_host

# Verificação da utilização da porta designada.
porta = e_porta


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

app = Dash(__name__, external_stylesheets=[__name__], title="GDT 5N")

app.layout = dbc.Container(
    [
        # Barra de Navegação
        dbc.Row(
            [
                dbc.Col(
                    [html.Img([], src="assets/logopenta.svg", alt="logo não carregado")], width=1
                ),
                dbc.Col(
                    [
                        html.H1("Gerenciador De Tarefas", className="h1-titulo-app")
                    ],
                    width=5,
                    align="center"
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.A(["Cadastros"], href="#titulo-cadastros", className="texto-link"),
                                html.A(["Tarefas"], href="#titulo-tarefas", className="texto-link"),
                                html.A(["Dados"], href="#titulo-dados", className="texto-link")
                            ],
                            className="div-ancoras"
                        )
                    ],
                    width=4,
                    align="end"
                    
                )
            ],
            style={"background-color":"grey", "height":"13vh"},
            justify="between",
        ),
        # Conteúdo de manipulação
        principal.principal_layout
    ],
    fluid=True
)

# Retorno de chamada para abrir e fechar o modais de adicionar gerente, alterar gerente e remover gerente 
# (Falta excessão de popup de valor vazio), (Tem que validar coisas como não ser possível excluir um gerente designado a um departamento)
@app.callback(
    [
        Output("modal-add-ger", "is_open"),
        Output("mod-in-add-ger", "value"),
        Output("mod-drp-alt-ger-id", "options"),
        Output("mod-drp-rem-ger-id", "options"),
        Output("mod-drp-desig-ger-id", "options"),
        Output("div-tabela-gerente", "children"),
        Output("modal-alt-ger", "is_open"),
        Output("mod-in-alt-ger-nom", "value"), #8
        Output("div-tabela-departamento", "children"),
        Output("div-tabela-funcionario", "children"),
        Output("modal-rem-ger", "is_open"),
        Output("modal-add-dpt", "is_open"),
        Output("mod-in-add-dpt", "value"),
        Output("mod-drp-alt-dpt-id", "options"),
        Output("mod-drp-rem-dpt-id", "options"),
        Output("mod-drp-desig-dpt-id", "options"),
        Output("mod-drp-desv-dpt-id", "options"),
        Output("mod-drp-add-func-dpt-id", "options"),
        Output("mod-drp-alt-func-dpt-id", "options"),
        Output("modal-alt-dpt", "is_open"),
        Output("mod-in-alt-dpt-nom", "value"),
        Output("modal-rem-dpt", "is_open"),
        Output("modal-desig-ger-dpt", "is_open"),
        Output("modal-desv-ger-dpt", "is_open"),
        Output("modal-add-func", "is_open"),
        Output("mod-drp-alt-func-func-id", "options"),
        Output("mod-drp-rem-func-func-id", "options"),
        Output("mod-drp-add-tar-func-id", "options"),
        Output("mod-in-add-func", "value"),
        Output("modal-alt-func", "is_open"),
        Output("mod-in-alt-func", "value"),
        Output("modal-rem-func", "is_open"),
        Output("modal-excessao", "is_open"),
        Output("mod-head-excessao", "children"),
        Output("mod-body-excessao", "children"), #35
    ],
    [
        Input("btn-add-ger", "n_clicks"), 
        Input("mod-btn-add-ger-cancel", "n_clicks"), 
        Input("mod-btn-add-ger", "n_clicks"), 
        Input("mod-in-add-ger", "value"),
        Input("btn-alt-ger", "n_clicks"),
        Input("mod-btn-alt-ger-cancel", "n_clicks"),
        Input("mod-btn-alt-ger", "n_clicks"),
        Input("mod-drp-alt-ger-id", "value"),
        Input("mod-in-alt-ger-nom", "value"),
        Input("btn-rem-ger", "n_clicks"),
        Input("mod-btn-rem-ger-cancel", "n_clicks"),
        Input("mod-btn-rem-ger", "n_clicks"),
        Input("mod-drp-rem-ger-id", "value"),
        Input("btn-add-dpt", "n_clicks"),
        Input("mod-btn-add-dpt-cancel", "n_clicks"),
        Input("mod-btn-add-dpt", "n_clicks"),
        Input("mod-in-add-dpt", "value"),
        Input("btn-alt-dpt", "n_clicks"),
        Input("mod-btn-alt-dpt-cancel", "n_clicks"),
        Input("mod-btn-alt-dpt", "n_clicks"),
        Input("mod-drp-alt-dpt-id", "value"),
        Input("mod-in-alt-dpt-nom", "value"),
        Input("btn-rem-dpt", "n_clicks"),
        Input("mod-btn-rem-dpt-cancel", "n_clicks"),
        Input("mod-btn-rem-dpt", "n_clicks"),
        Input("mod-drp-rem-dpt-id", "value"),
        Input("btn-desig-ger-dpt", "n_clicks"),
        Input("mod-btn-desig-ger-dpt-cancel", "n_clicks"),
        Input("mod-btn-desig-ger-dpt", "n_clicks"),
        Input("mod-drp-desig-ger-id", "value"),
        Input("mod-drp-desig-dpt-id", "value"),
        Input("btn-desv-ger-dpt", "n_clicks"),
        Input("mod-btn-desv-ger-dpt-cancel", "n_clicks"),
        Input("mod-btn-desv-ger-dpt", "n_clicks"),
        Input("mod-drp-desv-dpt-id", "value"),
        Input("btn-add-func", "n_clicks"),
        Input("mod-btn-add-func-cancel", "n_clicks"),
        Input("mod-btn-add-func", "n_clicks"),
        Input("mod-in-add-func", "value"),
        Input("mod-drp-add-func-dpt-id", "value"),
        Input("btn-alt-func", "n_clicks"),
        Input("mod-btn-alt-func-cancel", "n_clicks"),
        Input("mod-btn-alt-func", "n_clicks"),
        Input("mod-drp-alt-func-func-id", "value"),
        Input("mod-in-alt-func", "value"),
        Input("mod-drp-alt-func-dpt-id", "value"),
        Input("btn-rem-func", "n_clicks"),
        Input("mod-btn-rem-func-cancel", "n_clicks"),
        Input("mod-btn-rem-func", "n_clicks"),
        Input("mod-drp-rem-func-func-id", "value") # 50

    ]
)
def gerente_modais(
    b1, b2, b3, value, b4, b5, b6, drop, input, b7, b8, b9, drop2, b10, b11, b12, value2, b13, b14, b15, drop3, value3, b16, b17,
    b18, drop4, b19, b20, b21, drop5, drop6, b22, b23, b24, drop7, b25, b26, b27, value4, drop8, b28, b29, b30, drop9, value5, 
    drop10, b31, b32, b33, drop11
    ):
    # Botões para adicionar gerente, alterar gerente e remover gerente.
    # b1
    if "btn-add-ger" == ctx.triggered_id:
        return (
            True, 
            "",
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b2
    if "mod-btn-add-ger-cancel" == ctx.triggered_id:
        return (
            False,
            "", 
            no_update, 
            no_update, 
            no_update, 
            no_update, 
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b3
    if "mod-btn-add-ger" == ctx.triggered_id:
        try:
            if value.strip() == "":
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido!")
            if value:
                try:
                    BF.adicionar_gerente(value)
                    principal.drp_dados_gerente = supD.drp_consulta_gerente(banco)
                    principal.tab_dados_gerente = supD.tab_consulta_gerente(banco)
                    tabela = dash_table.DataTable(
                                data=principal.tab_dados_gerente.to_dict("records"),
                                columns=[{"name": col, "id": col} for col in principal.tab_dados_gerente.columns],
                                id="tabela-gerente",
                                style_header=table_header_style,
                                style_data=table_cell_style,
                                page_size=5,
                                filter_action="native",
                                filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                style_filter=principal.table_filter_style,
                                tooltip_data=[
                                    {
                                        column: {"value": str(value), "type": "markdown"}
                                        for column, value in row.items()
                                    } for row in principal.tab_dados_gerente.to_dict("records")
                                ],
                                tooltip_duration=None
                            )
                    return (
                        False,
                        "", 
                        principal.drp_dados_gerente, 
                        principal.drp_dados_gerente, 
                        principal.drp_dados_gerente,
                        tabela,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update
                    )
                except Exception:
                    print("deu erro")
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("O campo NOME deve ser preenchido para efetuar a inclusão de um gerente.")
            )
    # Botões para alterar um gerente
    # b4
    if "btn-alt-ger" == ctx.triggered_id:
        return (
            no_update,
            no_update, 
            no_update, 
            no_update, 
            no_update, 
            no_update, 
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b5
    if "mod-btn-alt-ger-cancel" == ctx.triggered_id:
        return (
            no_update, 
            no_update, 
            no_update, 
            no_update, 
            no_update, 
            no_update, 
            False,
            "",
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )    
    # b6
    if "mod-btn-alt-ger" == ctx.triggered_id:
        try:
            if drop is None or input is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido!")
            if drop is None or input.strip() == "":
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido!")
            if drop and input:
                try:
                    BF.alterar_gerente(drop, input)
                    principal.drp_dados_gerente = supD.drp_consulta_gerente(banco)
                    principal.tab_dados_gerente = supD.tab_consulta_gerente(banco)
                    tabela_gerente = dash_table.DataTable(
                                data=principal.tab_dados_gerente.to_dict("records"),
                                columns=[{"name": col, "id": col} for col in principal.tab_dados_gerente.columns],
                                id="tabela-gerente",
                                style_header=table_header_style,
                                style_data=table_cell_style,
                                page_size=5,
                                filter_action="native",
                                filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                style_filter=principal.table_filter_style,
                                tooltip_data=[
                                    {
                                        column: {"value": str(value), "type": "markdown"}
                                        for column, value in row.items()
                                    } for row in principal.tab_dados_gerente.to_dict("records")
                                ],
                                tooltip_duration=None
                            )
                    principal.tab_dados_departamento = supD.tab_consulta_departamento(banco)
                    tabela_departamento = dash_table.DataTable(
                                            data=principal.tab_dados_departamento.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_departamento.columns],
                                            id="tabela-departamento",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_departamento.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                    principal.tab_dados_funcionario = supD.tab_consulta_funcionario(banco)
                    tabela_funcionario = dash_table.DataTable(
                                            data=principal.tab_dados_funcionario.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_funcionario.columns],
                                            id="tabela-funcionario",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_funcionario.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                    return (
                        no_update,
                        no_update,
                        principal.drp_dados_gerente, 
                        principal.drp_dados_gerente, 
                        principal.drp_dados_gerente,
                        tabela_gerente,
                        False,
                        "",
                        tabela_departamento,
                        tabela_funcionario,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update
                        
                    )
                except Exception as er:
                    print("deu erro")
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("Os campos ID e NOME devem ser preenchidos em conjunto para efetuar a alteração nos dados de um gerente.")
            )
    # b7
    if "btn-rem-ger" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update, 
            no_update, 
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b8
    if "mod-btn-rem-ger-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update, 
            no_update, 
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b9
    if "mod-btn-rem-ger" == ctx.triggered_id:
        try:
            if drop2 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop2:
                try:
                    BF.remover_gerente(drop2)
                    principal.drp_dados_gerente = supD.drp_consulta_gerente(banco)
                    principal.tab_dados_gerente = supD.tab_consulta_gerente(banco)
                    tabela_gerente = dash_table.DataTable(
                                data=principal.tab_dados_gerente.to_dict("records"),
                                columns=[{"name": col, "id": col} for col in principal.tab_dados_gerente.columns],
                                id="tabela-gerente",
                                style_header=table_header_style,
                                style_data=table_cell_style,
                                page_size=5,
                                filter_action="native",
                                filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                style_filter=principal.table_filter_style,
                                tooltip_data=[
                                    {
                                        column: {"value": str(value), "type": "markdown"}
                                        for column, value in row.items()
                                    } for row in principal.tab_dados_gerente.to_dict("records")
                                ],
                                tooltip_duration=None
                            )
                    principal.tab_dados_departamento = supD.tab_consulta_departamento(banco)
                    tabela_departamento = dash_table.DataTable(
                                            data=principal.tab_dados_departamento.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_departamento.columns],
                                            id="tabela-departamento",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_departamento.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                    return (
                        no_update,
                        no_update,
                        principal.drp_dados_gerente, 
                        principal.drp_dados_gerente, 
                        principal.drp_dados_gerente,
                        tabela_gerente,
                        no_update,
                        no_update,
                        tabela_departamento,
                        no_update,
                        False,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update
                    )
                except EX.GerenteDesignadoDepartamento:
                    return (
                        no_update,
                        no_update, 
                        no_update, 
                        no_update, 
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        True,
                        str("Gerente designado a um departamento."),
                        str("Não é possível remover um gerente já designado a um departamento.")
                    )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("O campo ID deve ser preenchido para efetuar a remoção de um gerente.")
            )
        
    # Botões para adiconar, alterar e remover um departamento e um botão para designar um gerente a um departamento.
    # b10
    if "btn-add-dpt" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update, 
            no_update, 
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b11
    if "mod-btn-add-dpt-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update, 
            no_update, 
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            "",
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b12
    if "mod-btn-add-dpt" == ctx.triggered_id:
        try:
            if value2 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if value2.strip() == "":
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if value2:
                BF.adicionar_departamento(value2)
                principal.drp_dados_departamento = supD.drp_consulta_departamento(banco)
                principal.tab_dados_departamento = supD.tab_consulta_departamento(banco)
                tabela_departamento = dash_table.DataTable(
                                            data=principal.tab_dados_departamento.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_departamento.columns],
                                            id="tabela-departamento",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_departamento.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                principal.tab_dados_funcionario = supD.tab_consulta_funcionario(banco)
                tabela_funcionario = dash_table.DataTable(
                                            data=principal.tab_dados_funcionario.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_funcionario.columns],
                                            id="tabela-funcionario",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_funcionario.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                return (
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    tabela_departamento,
                    tabela_funcionario,
                    no_update,
                    False,
                    "",
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update
                )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("O campo NOME deve ser preenchido para efetuar a inclusão de um departamento.")
            ) 
    # b13
    if "btn-alt-dpt" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b14
    if "mod-btn-alt-dpt-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            "",
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b15
    if "mod-btn-alt-dpt" == ctx.triggered_id:
        try:
            if drop3 is None or value3 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop3 is None or value3.strip() == "":
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop3 and value3:
                BF.alterar_nome_departamento(drop3, value3)
                principal.drp_dados_departamento = supD.drp_consulta_departamento(banco)
                principal.tab_dados_departamento = supD.tab_consulta_departamento(banco)
                tabela_departamento = dash_table.DataTable(
                                            data=principal.tab_dados_departamento.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_departamento.columns],
                                            id="tabela-departamento",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_departamento.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                principal.tab_dados_funcionario = supD.tab_consulta_funcionario(banco)
                tabela_funcionario = dash_table.DataTable(
                                            data=principal.tab_dados_funcionario.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_funcionario.columns],
                                            id="tabela-funcionario",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_funcionario.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                return (
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    tabela_departamento,
                    tabela_funcionario,
                    no_update,
                    no_update,
                    no_update,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    False,
                    "",
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update
                )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("Os campos ID e NOME devem ser preenchidos em conjunto para efetuar a alteração nos dados de um departamento.")
            )
    # b16
    if "btn-rem-dpt" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b17
    if "mod-btn-rem-dpt-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b18
    if "mod-btn-rem-dpt" == ctx.triggered_id:
        try:
            if drop4 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop4:
                try:
                    BF.remover_departamento(drop4)
                    principal.drp_dados_departamento = supD.drp_consulta_departamento(banco)
                    principal.tab_dados_departamento = supD.tab_consulta_departamento(banco)
                    tabela_departamento = dash_table.DataTable(
                                            data=principal.tab_dados_departamento.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_departamento.columns],
                                            id="tabela-departamento",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_departamento.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                    principal.tab_dados_funcionario = supD.tab_consulta_funcionario(banco)
                    tabela_funcionario = dash_table.DataTable(
                                            data=principal.tab_dados_funcionario.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_funcionario.columns],
                                            id="tabela-funcionario",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_funcionario.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                    return (
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        tabela_departamento,
                        tabela_funcionario,
                        no_update,
                        no_update,
                        no_update,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        no_update,
                        no_update,
                        False,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update
                    )
                except EX.DepartamentoComGerenteDesignado:
                    return (
                        no_update,
                        no_update, 
                        no_update,
                        no_update, 
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        True,
                        str("Departamento com gerente designado."),
                        str("Não é possível remover um departamento com um gerente designado.")
                    )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("O campo ID deve ser preenchido para efetuar a remoção de um departamento.")
            )
    # b19
    if "btn-desig-ger-dpt" == ctx.triggered_id:
        return(
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b20
    if "mod-btn-desig-ger-dpt-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b21
    if "mod-btn-desig-ger-dpt" == ctx.triggered_id:
        try:
            if drop5 is None or drop6 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop5 and drop6:
                try:
                    BF.desig_gerente_departamento(drop6, drop5)
                    principal.drp_dados_departamento = supD.drp_consulta_departamento(banco)
                    principal.tab_dados_departamento = supD.tab_consulta_departamento(banco)
                    tabela_departamento = dash_table.DataTable(
                                            data=principal.tab_dados_departamento.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_departamento.columns],
                                            id="tabela-departamento",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_departamento.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                    principal.tab_dados_funcionario = supD.tab_consulta_funcionario(banco)
                    tabela_funcionario = dash_table.DataTable(
                                            data=principal.tab_dados_funcionario.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_funcionario.columns],
                                            id="tabela-funcionario",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_funcionario.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                    return (
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        tabela_departamento,
                        tabela_funcionario,
                        no_update,
                        no_update,
                        no_update,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        principal.drp_dados_departamento,
                        no_update,
                        no_update,
                        no_update,
                        False,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update
                    )
                except EX.DepartamentoComGerenteDesignado:
                    return (
                        no_update,
                        no_update, 
                        no_update,
                        no_update, 
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        True,
                        str("Departamento com gerente designado."),
                        str("Não é possível efetuar a designação, o departamento já possui um gerente.")
                    )

        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("Os campos ID GERENTE e ID DEPARTAMENTO devem ser preenchidos em conjunto para designar um gerente a um departamento.")
            )
    # b22
    if "btn-desv-ger-dpt" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b23
    if "mod-btn-desv-ger-dpt-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b24
    if "mod-btn-desv-ger-dpt" == ctx.triggered_id:
        try:
            if drop7 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop7:
                BF.desvincular_gerente_departamento(drop7)
                principal.drp_dados_departamento = supD.drp_consulta_departamento(banco)
                principal.tab_dados_departamento = supD.tab_consulta_departamento(banco)
                tabela_departamento = dash_table.DataTable(
                                            data=principal.tab_dados_departamento.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_departamento.columns],
                                            id="tabela-departamento",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_departamento.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                principal.tab_dados_funcionario = supD.tab_consulta_funcionario(banco)
                tabela_funcionario = dash_table.DataTable(
                                            data=principal.tab_dados_funcionario.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_funcionario.columns],
                                            id="tabela-funcionario",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_funcionario.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                return (
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    tabela_departamento,
                    tabela_funcionario,
                    no_update,
                    no_update,
                    no_update,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    principal.drp_dados_departamento,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    False,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update
                )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("O campo ID DEPARTAMENTO deve ser preenchido para desvincular um gerente de um departamento.")
            )
    # b25
    if "btn-add-func" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b26
    if "mod-btn-add-func-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            no_update,
            no_update,
            no_update,
            "",
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b27
    if "mod-btn-add-func" == ctx.triggered_id:
        try:
            if drop8 is None or value4 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop8 is None or value4.strip() == "":
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop8 and value4:
                try:
                    BF.adicionar_funcionario(value4, drop8)
                    principal.drp_dados_funcionario = supD.drp_consulta_funcionario(banco)
                    principal.tab_dados_funcionario = supD.tab_consulta_funcionario(banco)
                    tabela_funcionario = dash_table.DataTable(
                                            data=principal.tab_dados_funcionario.to_dict("records"),
                                            columns=[{"name": col, "id": col} for col in principal.tab_dados_funcionario.columns],
                                            id="tabela-funcionario",
                                            style_header=table_header_style,
                                            style_data=table_cell_style,
                                            page_size=5,
                                            filter_action="native",
                                            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                            style_filter=principal.table_filter_style,
                                            tooltip_data=[
                                                {
                                                    column: {"value": str(value), "type": "markdown"}
                                                    for column, value in row.items()
                                                } for row in principal.tab_dados_funcionario.to_dict("records")
                                            ],
                                            tooltip_duration=None
                                        )
                    return(
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        tabela_funcionario,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        False,
                        principal.drp_dados_funcionario,
                        principal.drp_dados_funcionario,
                        principal.drp_dados_funcionario,
                        "",
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update
                    )
                except EX.DepartamentoSemGerenteDesignado:
                    return (
                        no_update,
                        no_update, 
                        no_update,
                        no_update, 
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        True,
                        str("Departamento sem gerente."),
                        str("Não é possível adicionar um funcionário utilizando um departamento sem gerente.")
                    )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("Os campos NOME e ID DEPARTAMENTO devem ser preenchidos em conjunto para efetuar a inclusão de um funcionário.")
            )
    # b28
    if "btn-alt-func" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update, 
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b29
    if "mod-btn-alt-func-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update, 
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            "",
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b30
    if "mod-btn-alt-func" == ctx.triggered_id:
        try:
            if drop9 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop9:
                try:
                    BF.alterar_funcionario(id_func=drop9, nome_func=value5, id_dpt=drop10)
                    principal.drp_dados_funcionario = supD.drp_consulta_funcionario(banco)
                    principal.tab_dados_funcionario = supD.tab_consulta_funcionario(banco)
                    tabela_funcionario = dash_table.DataTable(
                                                data=principal.tab_dados_funcionario.to_dict("records"),
                                                columns=[{"name": col, "id": col} for col in principal.tab_dados_funcionario.columns],
                                                id="tabela-funcionario",
                                                style_header=table_header_style,
                                                style_data=table_cell_style,
                                                page_size=5,
                                                filter_action="native",
                                                filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                                style_filter=principal.table_filter_style,
                                                tooltip_data=[
                                                    {
                                                        column: {"value": str(value), "type": "markdown"}
                                                        for column, value in row.items()
                                                    } for row in principal.tab_dados_funcionario.to_dict("records")
                                                ],
                                                tooltip_duration=None
                                            )
                    return (
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        tabela_funcionario,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        principal.drp_dados_funcionario,
                        principal.drp_dados_funcionario,
                        principal.drp_dados_funcionario,
                        no_update,
                        False,
                        "",
                        no_update,
                        no_update,
                        no_update,
                        no_update
                    )
                except EX.FuncionarioPossuiUmaTarefa:
                    return (
                        no_update,
                        no_update, 
                        no_update, 
                        no_update, 
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        True,
                        str("Funcionário não pode ser alterado."),
                        str("O funcionário não pode ser alterado porque ele já possui tarefa.")
                    )

        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("O campo ID FUNCIONARIO deve ser preenchido para efetuar a alteração nos dados de um funcionário.")
            )
    # b31
    if "btn-rem-func" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update
        )
    # b32
    if "mod-btn-rem-func-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            no_update,
            no_update,
            no_update
        )
    # b33
    if "mod-btn-rem-func" == ctx.triggered_id: #Não permitir remover um funcionário que já possui uma tarefa.
        try:
            if drop11 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if drop11:
                try:
                    BF.remover_funcionario(drop11)
                    principal.drp_dados_funcionario = supD.drp_consulta_funcionario(banco)
                    principal.tab_dados_funcionario = supD.tab_consulta_funcionario(banco)
                    tabela_funcionario = dash_table.DataTable(
                                                data=principal.tab_dados_funcionario.to_dict("records"),
                                                columns=[{"name": col, "id": col} for col in principal.tab_dados_funcionario.columns],
                                                id="tabela-funcionario",
                                                style_header=table_header_style,
                                                style_data=table_cell_style,
                                                page_size=5,
                                                filter_action="native",
                                                filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                                                style_filter=principal.table_filter_style,
                                                tooltip_data=[
                                                    {
                                                        column: {"value": str(value), "type": "markdown"}
                                                        for column, value in row.items()
                                                    } for row in principal.tab_dados_funcionario.to_dict("records")
                                                ],
                                                tooltip_duration=None
                                            )
                    return (
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        tabela_funcionario,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        principal.drp_dados_funcionario,
                        principal.drp_dados_funcionario,
                        principal.drp_dados_funcionario,
                        no_update,
                        no_update,
                        no_update,
                        False,
                        no_update,
                        no_update,
                        no_update
                    )
                except EX.FuncionarioPossuiUmaTarefa:
                    return (
                        no_update,
                        no_update, 
                        no_update, 
                        no_update, 
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        no_update,
                        True,
                        str("Funcionário não pode ser removido."),
                        str("O funcionário não pode ser removido porque ele já possui tarefa.") 
                    )

        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update, 
                no_update, 
                no_update, 
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("O campo ID FUNCIONARIO deve ser preenchido para remover um funcionário.")
            )

    else:
        raise PreventUpdate


# Funcionalidades da parte de tarefas.
@app.callback(
    [
        Output("modal-add-tar", "is_open"),
        Output("row-tab-mestre", "children"),
        Output("mod-in-add-tar-tit", "value"),
        Output("mod-textarea-add-tar-desc", "value"),
        Output("mod-drp-add-tar-relacionada", "options"),
        Output("modal-adiar-tar", "is_open"), #6
        Output("mod-textarea-adiar-tar-mot", "value"),
        Output("modal-finalizar-tar", "is_open"),
        Output("mod-drp-adiar-tar-tar-id", "options"),
        Output("mod-drp-finalizar-tar-tar-id", "options"),
        Output("modal-rem-tar", "is_open"),
        Output("mod-drp-rem-tar-tar-id", "options"),
        Output("modal-excessao-tarefas", "is_open"),
        Output("mod-head-excessao-tarefas", "children"),
        Output("mod-body-excessao-tarefas", "children") #15
    ],
    [
        Input("btn-add-tar", "n_clicks"),
        Input("mod-btn-add-tar-cancel", "n_clicks"),
        Input("mod-btn-add-tar", "n_clicks"),
        Input("mod-in-add-tar-tit", "value"), #titulo
        Input("mod-textarea-add-tar-desc", "value"), #descricao
        Input("mod-date-add-tar-inicio", "date"), #data inicio
        Input("mod-date-add-tar-final", "date"), #data final
        Input("mod-drp-add-tar-func-id", "value"), #funcionario
        Input("mod-drp-add-tar-nivel", "value"), #nivel
        Input("mod-drp-add-tar-relacionada", "value"), #tar_relacionada
        Input("btn-adiar-tar", "n_clicks"),
        Input("mod-btn-adiar-tar-cancel", "n_clicks"),
        Input("mod-btn-adiar-tar", "n_clicks"),
        Input("mod-drp-adiar-tar-tar-id", "value"),
        Input("mod-date-adiar-tar-nova-data", "date"),
        Input("mod-textarea-adiar-tar-mot", "value"),
        Input("btn-finalizar-tar", "n_clicks"),
        Input("mod-btn-finalizar-tar-cancel", "n_clicks"),
        Input("mod-btn-finalizar-tar", "n_clicks"),
        Input("mod-drp-finalizar-tar-tar-id", "value"),
        Input("btn-rem-tar", "n_clicks"),
        Input("mod-btn-rem-tar-cancel", "n_clicks"),
        Input("mod-btn-rem-tar", "n_clicks"),
        Input("mod-drp-rem-tar-tar-id", "value"),
        Input("drp-tipo-visualizacao", "value")
    ]
)
def tarefas_funcionalidades(
    b1, b2, b3, value, value2, data, data2, value3, value4, value5, b4, b5, b6, value6, 
    data3, value7, b7, b8, b9, value8, b10, b11, b12, value9, value10
):
    #b1
    if "btn-add-tar" == ctx.triggered_id:
        return (
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    #b2
    if "mod-btn-add-tar-cancel" == ctx.triggered_id:
        return (
            False,
            no_update,
            "",
            "",
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    #b3
    if "mod-btn-add-tar" == ctx.triggered_id:
        try:
            if value is None or \
               value2 is None or \
               data is None or \
               data2 is None or \
               value3 is None or \
               value4 is None:
                raise EX.CampoNaoPreenchido("Campos obrigatórios não preenchidos.")
            if value.strip() == "" or \
               value2.strip() == "" or \
               data is None or \
               data2 is None or \
               value3 is None or \
               value4 is None:
                raise EX.CampoNaoPreenchido("Campos obrigatórios não preenchidos.")
            if datetime.datetime.strptime(data2, "%Y-%m-%d").date() < datetime.datetime.strptime(data, "%Y-%m-%d").date():
                raise EX.DataFinalMenorQueDataInicial("Data final menor do que a data inicial.")
            if value and value2 and data and data2 and value3 and value4:
                BF.adicionar_tarefa(value, value2, data, data2, value3, value4, value5)
                if value10 == "t-concluidas":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas(banco)
                if value10 == "t-concluidas-anl":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas_analitico(banco)
                if value10 == "t-pendentes":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes(banco)
                if value10 == "t-pendentes-anl":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes_analitico(banco)
                if value10 == "t-relacionadas":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_relacionada(banco)
                if value10 == "t-adiadas-hist":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_adiadas_hist(banco)
                # ATENCAO 19/12/2022: precisei carregar uma nova tabela aqui porque não estava carregando os dados após a inclusão
                # em uma tabela sem dados (vazia). Para não ficar sem dados após rodar o app, tive que deixar a mesma tabela
                # na aba principal2. Terei que atualizar as tabelas de gerente, departamento e funcionário para executar da mesma forma.
                tabela = dash_table.DataTable(
                    data=principal.tab_dados_tipo_visualizacao.to_dict("records"),
                    columns=[{"name": col, "id": col} for col in principal.tab_dados_tipo_visualizacao.columns],
                    id="tabela-tarefas-mestre",
                    style_header=table_header_style,
                    style_data=table_cell_style,
                    page_size=10,
                    filter_action="native",
                    filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                    style_filter=principal.table_filter_style,
                    tooltip_data=[
                        {
                            column: {"value": str(value), "type": "text"}
                            for column, value in row.items()
                        } for row in principal.tab_dados_tipo_visualizacao.to_dict("records")
                    ],
                    tooltip_duration=None
                )
                # Formatação condicional dos tipos de visualização das tabelas. (Estou passando os valores diretamente na propriedade da Classe)
                if value10 == "t-concluidas":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{data_concl} <= {data_final}"
                            },
                            "backgroundColor": "rgba(138, 254, 11, 0.50)"
                        },
                        {
                            "if": {
                                "filter_query": "{data_concl} > {data_final}"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-concluidas-anl":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{finalizacao} contains 'NO PRAZO'",
                                "column_id": "finalizacao"
                            },
                            "backgroundColor": "rgba(138, 254, 11, 0.50)"
                        },
                        {
                            "if": {
                                "filter_query": "{finalizacao} contains 'COM ATRASO'",
                                "column_id": "finalizacao"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-pendentes":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": f"{{data_final}} < {datetime.date.today()}"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-pendentes-anl":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{progresso} contains 'ATRASADA'",
                                "column_id": "progresso"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                principal.drp_dados_tarefa_relacionada = supD.drp_consulta_tarefa_relacionada(banco)
                return (
                    False,
                    tabela,
                    "",
                    "",
                    principal.drp_dados_tarefa_relacionada,
                    no_update,
                    no_update,
                    no_update,
                    principal.drp_dados_tarefa_relacionada,
                    principal.drp_dados_tarefa_relacionada,
                    no_update,
                    principal.drp_dados_tarefa_relacionada,
                    no_update,
                    no_update,
                    no_update
                )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campos obrigatórios não preenchidos."),
                str("""Os campos TITULO, DESCRICAO, DATA DE INICIO, DATA FINAL, FUNCIONARIO e NIVEL DA TAREFA
                       devem ser preenchidos em conjunto para efetuar a inclusão de uma tarefa.""")
            )
        except EX.DataFinalMenorQueDataInicial:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Data final menor que a data inicial."),
                str("""A DATA FINAL precisa ser maior ou igual a DATA DE INICIO.""")
            )

    # b4
    if "btn-adiar-tar" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b5
    if "mod-btn-adiar-tar-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            "",
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b6
    if "mod-btn-adiar-tar" == ctx.triggered_id:
        try:
            if value6 is None or data3 is None or value7 is None:
                raise EX.CampoNaoPreenchido("Campos obrigatórios não preenchidos.")
            if value6 is None or data3 is None or value7.strip() == "":
                raise EX.CampoNaoPreenchido("Campos obrigatórios não preenchidos.")
            if datetime.datetime.strptime(data3, "%Y-%m-%d").date() <= datetime.datetime.strptime(supD.verificar_id_adiar_tarefa(value6), "%Y-%m-%d").date():
                raise EX.NovaDataMenorQueaAtual("Nova data menor ou igual a data final atual.")
            if value6 and data3 and value7:
                BF.adiar_tarefa(value6, data3)
                BF.motivo_adiar_tarefa(value6, value7)
                if value10 == "t-concluidas":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas(banco)
                if value10 == "t-concluidas-anl":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas_analitico(banco)
                if value10 == "t-pendentes":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes(banco)
                if value10 == "t-pendentes-anl":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes_analitico(banco)
                if value10 == "t-relacionadas":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_relacionada(banco)
                if value10 == "t-adiadas-hist":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_adiadas_hist(banco)
                tabela = dash_table.DataTable(
                    data=principal.tab_dados_tipo_visualizacao.to_dict("records"),
                    columns=[{"name": col, "id": col} for col in principal.tab_dados_tipo_visualizacao.columns],
                    id="tabela-tarefas-mestre",
                    style_header=table_header_style,
                    style_data=table_cell_style,
                    page_size=10,
                    filter_action="native",
                    filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                    style_filter=principal.table_filter_style,
                    tooltip_data=[
                        {
                            column: {"value": str(value), "type": "text"}
                            for column, value in row.items()
                        } for row in principal.tab_dados_tipo_visualizacao.to_dict("records")
                    ],
                    tooltip_duration=None
                )
                # Formatação condicional dos tipos de visualização das tabelas. (Estou passando os valores diretamente na propriedade da Classe)
                if value10 == "t-concluidas":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{data_concl} <= {data_final}"
                            },
                            "backgroundColor": "rgba(138, 254, 11, 0.50)"
                        },
                        {
                            "if": {
                                "filter_query": "{data_concl} > {data_final}"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-concluidas-anl":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{finalizacao} contains 'NO PRAZO'",
                                "column_id": "finalizacao"
                            },
                            "backgroundColor": "rgba(138, 254, 11, 0.50)"
                        },
                        {
                            "if": {
                                "filter_query": "{finalizacao} contains 'COM ATRASO'",
                                "column_id": "finalizacao"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-pendentes":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": f"{{data_final}} < {datetime.date.today()}"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-pendentes-anl":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{progresso} contains 'ATRASADA'",
                                "column_id": "progresso"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                return (
                    no_update,
                    tabela,
                    no_update,
                    no_update,
                    no_update,
                    False,
                    "",
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                    no_update
                )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campos obrigatórios não preenchidos."),
                str("""Os campos ID TAREFA, NOVA DATA e MOTIVO DO ADIAMENTO devem ser preenchidos em conjunto para adiar uma tarefa.""")
            )
        except EX.NovaDataMenorQueaAtual:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Nova data menor ou igual a data final atual."),
                str("""A NOVA DATA precisa ser maior do que a data final estipulada atual.""")
            )

    # b7
    if "btn-finalizar-tar" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b8
    if "mod-btn-finalizar-tar-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b9
    if "mod-btn-finalizar-tar" == ctx.triggered_id:
        try:
            if value8 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if value8:
                BF.finalizar_tarefa(value8)
                if value10 == "t-concluidas":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas(banco)
                if value10 == "t-concluidas-anl":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas_analitico(banco)
                if value10 == "t-pendentes":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes(banco)
                if value10 == "t-pendentes-anl":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes_analitico(banco)
                if value10 == "t-relacionadas":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_relacionada(banco)
                if value10 == "t-adiadas-hist":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_adiadas_hist(banco)
                tabela = dash_table.DataTable(
                    data=principal.tab_dados_tipo_visualizacao.to_dict("records"),
                    columns=[{"name": col, "id": col} for col in principal.tab_dados_tipo_visualizacao.columns],
                    id="tabela-tarefas-mestre",
                    style_header=table_header_style,
                    style_data=table_cell_style,
                    page_size=10,
                    filter_action="native",
                    filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                    style_filter=principal.table_filter_style,
                    tooltip_data=[
                        {
                            column: {"value": str(value), "type": "text"}
                            for column, value in row.items()
                        } for row in principal.tab_dados_tipo_visualizacao.to_dict("records")
                    ],
                    tooltip_duration=None
                )
                # Formatação condicional dos tipos de visualização das tabelas. (Estou passando os valores diretamente na propriedade da Classe)
                if value10 == "t-concluidas":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{data_concl} <= {data_final}"
                            },
                            "backgroundColor": "rgba(138, 254, 11, 0.50)"
                        },
                        {
                            "if": {
                                "filter_query": "{data_concl} > {data_final}"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-concluidas-anl":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{finalizacao} contains 'NO PRAZO'",
                                "column_id": "finalizacao"
                            },
                            "backgroundColor": "rgba(138, 254, 11, 0.50)"
                        },
                        {
                            "if": {
                                "filter_query": "{finalizacao} contains 'COM ATRASO'",
                                "column_id": "finalizacao"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-pendentes":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": f"{{data_final}} < {datetime.date.today()}"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-pendentes-anl":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{progresso} contains 'ATRASADA'",
                                "column_id": "progresso"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                principal.drp_dados_tarefa_relacionada = supD.drp_consulta_tarefa_relacionada(banco)
                return(
                    no_update,
                    tabela,
                    no_update,
                    no_update,
                    principal.drp_dados_tarefa_relacionada,
                    no_update,
                    no_update,
                    False,
                    principal.drp_dados_tarefa_relacionada,
                    principal.drp_dados_tarefa_relacionada,
                    no_update,
                    principal.drp_dados_tarefa_relacionada,
                    no_update,
                    no_update,
                    no_update
                )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("""O campo ID TAREFA deve ser preenchido para finalizar uma tarefa.""")
            )

    # b10
    if "btn-rem-tar" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            True,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b11
    if "mod-btn-rem-tar-cancel" == ctx.triggered_id:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            False,
            no_update,
            no_update,
            no_update,
            no_update
        )
    # b12
    if "mod-btn-rem-tar" == ctx.triggered_id:
        try:
            if value9 is None:
                raise EX.CampoNaoPreenchido("Campo obrigatório não preenchido.")
            if value9:
                BF.remover_tarefa(value9)
                if value10 == "t-concluidas":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas(banco)
                if value10 == "t-concluidas-anl":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas_analitico(banco)
                if value10 == "t-pendentes":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes(banco)
                if value10 == "t-pendentes-anl":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes_analitico(banco)
                if value10 == "t-relacionadas":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_relacionada(banco)
                if value10 == "t-adiadas-hist":
                    principal.tab_dados_tipo_visualizacao = supD.tab_consulta_adiadas_hist(banco)
                tabela = dash_table.DataTable(
                    data=principal.tab_dados_tipo_visualizacao.to_dict("records"),
                    columns=[{"name": col, "id": col} for col in principal.tab_dados_tipo_visualizacao.columns],
                    id="tabela-tarefas-mestre",
                    style_header=table_header_style,
                    style_data=table_cell_style,
                    page_size=10,
                    filter_action="native",
                    filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
                    style_filter=principal.table_filter_style,
                    tooltip_data=[
                        {
                            column: {"value": str(value), "type": "text"}
                            for column, value in row.items()
                        } for row in principal.tab_dados_tipo_visualizacao.to_dict("records")
                    ],
                    tooltip_duration=None
                )
                # Formatação condicional dos tipos de visualização das tabelas. (Estou passando os valores diretamente na propriedade da Classe)
                if value10 == "t-concluidas":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{data_concl} <= {data_final}"
                            },
                            "backgroundColor": "rgba(138, 254, 11, 0.50)"
                        },
                        {
                            "if": {
                                "filter_query": "{data_concl} > {data_final}"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-concluidas-anl":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{finalizacao} contains 'NO PRAZO'",
                                "column_id": "finalizacao"
                            },
                            "backgroundColor": "rgba(138, 254, 11, 0.50)"
                        },
                        {
                            "if": {
                                "filter_query": "{finalizacao} contains 'COM ATRASO'",
                                "column_id": "finalizacao"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-pendentes":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": f"{{data_final}} < {datetime.date.today()}"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                if value10 == "t-pendentes-anl":
                    tabela.style_data_conditional = [
                        {
                            "if": {
                                "filter_query": "{progresso} contains 'ATRASADA'",
                                "column_id": "progresso"
                            },
                            "backgroundColor": "rgba(254, 38, 68, 0.6)"
                        }
                    ]
                principal.drp_dados_tarefa_relacionada = supD.drp_consulta_tarefa_relacionada(banco)
                return (
                    no_update,
                    tabela,
                    no_update,
                    no_update,
                    principal.drp_dados_tarefa_relacionada,
                    no_update,
                    no_update,
                    no_update,
                    principal.drp_dados_tarefa_relacionada,
                    principal.drp_dados_tarefa_relacionada,
                    False,
                    principal.drp_dados_tarefa_relacionada,
                    no_update,
                    no_update,
                    no_update
                )
        except EX.CampoNaoPreenchido:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                True,
                str("Campo obrigatório não preenchido."),
                str("""O campo ID TAREFA deve ser preenchido para remover uma tarefa.""")
            )

    #value10
    if "drp-tipo-visualizacao" == ctx.triggered_id:
        if value10 == "t-concluidas":
            principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas(banco)
        if value10 == "t-concluidas-anl":
            principal.tab_dados_tipo_visualizacao = supD.tab_consulta_concluidas_analitico(banco)
        if value10 == "t-pendentes":
            principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes(banco)
        if value10 == "t-pendentes-anl":
            principal.tab_dados_tipo_visualizacao = supD.tab_consulta_pendentes_analitico(banco)
        if value10 == "t-relacionadas":
            principal.tab_dados_tipo_visualizacao = supD.tab_consulta_relacionada(banco)
        if value10 == "t-adiadas-hist":
            principal.tab_dados_tipo_visualizacao = supD.tab_consulta_adiadas_hist(banco)
        tabela = dash_table.DataTable(
            data=principal.tab_dados_tipo_visualizacao.to_dict("records"),
            columns=[{"name": col, "id": col} for col in principal.tab_dados_tipo_visualizacao.columns],
            id="tabela-tarefas-mestre",
            style_header=table_header_style,
            style_data=table_cell_style,
            page_size=10,
            filter_action="native",
            filter_options={"placeholder_text": "Filtrar dados...", "case": "insensitive"},
            style_filter=principal.table_filter_style,
            tooltip_data=[
                {
                    column: {"value": str(value), "type": "text"}
                    for column, value in row.items()
                } for row in principal.tab_dados_tipo_visualizacao.to_dict("records")
            ],
            tooltip_duration=None
        )
        # Formatação condicional dos tipos de visualização das tabelas. (Estou passando os valores diretamente na propriedade da Classe)
        if value10 == "t-concluidas":
            tabela.style_data_conditional = [
                {
                    "if": {
                        "filter_query": "{data_concl} <= {data_final}"
                    },
                    "backgroundColor": "rgba(138, 254, 11, 0.50)"
                },
                {
                    "if": {
                        "filter_query": "{data_concl} > {data_final}"
                    },
                    "backgroundColor": "rgba(254, 38, 68, 0.6)"
                }
            ]
        if value10 == "t-concluidas-anl":
            tabela.style_data_conditional = [
                {
                    "if": {
                        "filter_query": "{finalizacao} contains 'NO PRAZO'",
                        "column_id": "finalizacao"
                    },
                    "backgroundColor": "rgba(138, 254, 11, 0.50)"
                },
                {
                    "if": {
                        "filter_query": "{finalizacao} contains 'COM ATRASO'",
                        "column_id": "finalizacao"
                    },
                    "backgroundColor": "rgba(254, 38, 68, 0.6)"
                }
            ]
        if value10 == "t-pendentes":
            tabela.style_data_conditional = [
                {
                    "if": {
                        "filter_query": f"{{data_final}} < {datetime.date.today()}"
                    },
                    "backgroundColor": "rgba(254, 38, 68, 0.6)"
                }
            ]
        if value10 == "t-pendentes-anl":
            tabela.style_data_conditional = [
                {
                    "if": {
                        "filter_query": "{progresso} contains 'ATRASADA'",
                        "column_id": "progresso"
                    },
                    "backgroundColor": "rgba(254, 38, 68, 0.6)"
                }
            ]
        return (
            no_update,
            tabela,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update
        )

    else:
        raise PreventUpdate

# Rododando o app
if __name__ == "__main__":
    app.run(host=host, port=porta, debug=False)
