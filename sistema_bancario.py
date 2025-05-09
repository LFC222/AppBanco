import textwrap

def menu():
    "====== MENU ======"
    menu = """
    [1] Novo Usuário
    [2] Criar Conta
    [3] Listar Contas
    [4] Depositar
    [5] Sacar
    [6] Extrato
    [0] Sair
    => """
    return (input(textwrap.dedent(menu)))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()
        if opcao == "1":
            criar_usuario(usuarios)
        
        elif opcao == "2":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
                
        elif opcao == "3":
            listar_contas(contas)
                
        elif opcao == "4":
            valor = float(input("Informe o valor do deposito: "))
            saldo,extrato = depositar(saldo, valor, extrato)
        elif opcao == "5":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                limite=limite,
                extrato=extrato,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
        elif opcao == "6":
            extrato_conta(saldo, extrato=extrato)
        elif opcao == "0":
            break
        else:
            print("Operação inválida")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("=====Conta Criada com sucesso!=====")
        return { "agencia": agencia, "numero_conta": numero_conta, "usuario": usuario }
    print("Usuario não encontrado")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agencia: \t{conta['agencia']}
            C/C: \t\t{conta['numero_conta']}
            Titular: \t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))
        

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito: \tR$ {valor:.2f}\n"
        print("=== Deposito realizado com sucesso ===")
    else:
        print("\n@@@ Operação falhou, o valor informado é invalido. @@@")
    print(f"Saldo da conta: {saldo}")
    return saldo, extrato

def criar_usuario(usuarios):
    cpf = input("CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("CPF já existe")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print("=====Usuário criado com sucesso=====")
    
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo:
        print("Saldo insuficiente")
    elif excedeu_limite:
        print("Limite de saque excedido")
    elif excedeu_saques:
        print("Limite de saques diários excedido")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: \tR$ {valor:.2f}\n"
        numero_saques += 1
        print("=== Saque realizado com sucesso ===")
    else:
        print("\n@@@ Operação falhou, o valor informado é invalido. @@@")
        
    return saldo, extrato

def extrato_conta(saldo, /, *, extrato):
    print("===== Extrato da Conta =====")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("================================")

main()