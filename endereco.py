import socket

# ==== FORNECIMENTO DO HOST E DA PORTA PARA A APLICACAO ==== #

# Define o host para a aplicação, as opções são "rede" e "local". Caso "rede" seja passado como opção, o host da rede (fornecido pelo roteador)
# será retornado. Caso a opção passada seja "local", o host retornado será o "localhost" (127.0.0.1).
def definir_host(rede_ou_local):
    opcao = str(rede_ou_local).strip().lower()
    if opcao == "rede":
        host_name = socket.gethostname()
        host = socket.gethostbyname(host_name)
        return host
    if opcao == "local":
        host_name = "localhost"
        host = socket.gethostbyname(host_name)
        return host

# Verifica se a porta designada para uso já está em uso no host selecionado, em caso positivo, passa para a próxima porta. Por exemplo, caso a 
# porta designada 8050 já esteja em uso, ele passa para a porta 8051.
def verificar_porta(host, porta):
    host_ = host
    porta_ = porta
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    while True:
        if sock.connect_ex((host_, porta_)) == 0:
            porta_ += 1
        else:
            sock.close()
            return porta_

e_host = definir_host("local")

e_porta = verificar_porta(e_host, 8050)