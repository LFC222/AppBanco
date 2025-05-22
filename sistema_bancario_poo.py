from abc import ABC, abstractproperty
from datetime import datetime
import textwrap

class Cliente:
  def __init__(self, endereco):
    self.endereco = endereco
    self.contas = []

  def realizar_transacoes(self, conta, transacao):
    transacao.registrar(conta)

  def adicionar_conta(self, conta):
    self.contas.append(conta)

class PessoaFisica(Cliente):
  def __init__(self, nome, data_nascimento, cpf, endereco):
    super().__init__(endereco)
    self.nome = nome
    self.data_nascimento = data_nascimento
    self.cpf = cpf

class Conta:
  def __init__(self, numero_conta, cliente):
    self._saldo = 0
    self._numero_conta = numero_conta
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()
  
  @classmethod
  def nova_conta(cls, cliente, numero_conta):
    return cls(numero_conta, cliente)

  @property
  def saldo(self):
    return self._saldo
  
  @property
  def numero_conta(self):
    return self._numero_conta
  
  @property
  def agencia(self):
    return self._agencia
  
  @property
  def cliente(self):
    return self._cliente
  
  @property
  def historico(self):
    return self._historico

  def sacar(self, valor):
    saldo = self.saldo
    excedeu_saldo = valor > saldo

    if excedeu_saldo:
      print("Saldo insuficiente")

    elif valor > 0:
      self._saldo -= valor
      print("\n========== Saque realizado ==========")
      return True
    
    else:
      print("Valor inválido")
    
    return False

  def depositar(self, valor):
    if valor > 0:
      self._saldo += valor
      print("\n========== Depósito realizado ==========")
      return True
    else:
      print("Valor inválido")
      return False

class ContaCorrente(Conta):
  def __init__(self, numero_conta, cliente, limite=500, limite_saques=3):
    super().__init__(numero_conta, cliente)
    self._limite = limite
    self._limite_saques = limite_saques
  
  def sacar(self, valor):
    numero_saques = len([
      transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
    )

    excedeu_limite = valor > self._limite
    excedeu_limite_saques = numero_saques >= self._limite_saques

    if excedeu_limite:
      print("Limite de saque excedido")
    elif excedeu_limite_saques:
      print("Limite de saques diários excedido")
    else:
      return super().sacar(valor)
  
    return False
  
  def __str__(self):
    return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero_conta}
        Titular:\t{self.cliente.nome}
    """
  
class Historico:
  def __init__(self):
    self._transacoes = []

  @property
  def transacoes(self):
    return self._transacoes
  
  def adicionar_transacao(self, transacao):
    self._transacoes.append({
      'tipo': type(transacao).__name__,
      'valor': transacao.valor,
      'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    })

class Transacao(ABC):

  @property
  def valor(self):
    pass

  @property
  def registrar(self, conta):
    pass

class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    sucesso_transacao = conta.sacar(self.valor)
    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    sucesso_transacao = conta.depositar(self.valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)


def menu():
    menu = """
    "====== MENU ======"
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
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            criar_cliente(clientes)
        elif opcao == "2":
            numero_conta = len(contas) + 1
            criar_conta( numero_conta, clientes, contas)
        elif opcao == "3":
            listar_contas(contas)
        elif opcao == "4":
            depositar(clientes)
        elif opcao == "5":
            sacar(clientes)
        elif opcao == "6":
            exibir_extrato(clientes)
        elif opcao == "0":
            break
        else:
            print("Operação inválida")

def filtrar_cliente(cpf, clientes):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
  return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
  if not cliente.contas:
    print(" O cliente não tem conta")
    return
  
  return cliente.contas[0]

def depositar(clientes):
  cpf = input(" Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("Cliente não encontrado")
    return
  
  valor = float(input(" Digite o valor a ser depositado: "))
  transacao = Deposito(valor)
  conta = recuperar_conta_cliente( cliente)

  if not conta:
    return
  
  cliente.realizar_transacoes(conta, transacao)

def sacar( clientes):
  cpf = input(" Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("Cliente não encontrado")
    return
  
  valor = float(input(" Digite o valor a ser sacado: "))
  transacao = Saque(valor)

  conta = recuperar_conta_cliente( cliente)
  if not conta:
    return
  
  cliente.realizar_transacoes(conta, transacao)

def exibir_extrato(clientes):
  cpf = input(" Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("Cliente não encontrado")
    return
  
  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return
  
  print("===== Extrato da Conta =====")
  transacoes = conta.historico.transacoes
  
  extrato = ""
  if not transacoes:
    print("Nenhuma transação realizada")
  else:
    for transacao in transacoes:
      extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
  
  print(extrato)
  print( f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
  print("===== Fim do Extrato =====")

def criar_cliente(clientes):
  cpf = input(" Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if cliente:
    print("CPF já existe")
    return
  
  nome = input(" Digite o nome do cliente: ")
  data_nascimento = input(" Digite a data de nascimento do cliente (dd-mm-aaaa): ")
  endereco = input(" Digite o endereço do cliente: ")

  cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)

  clientes.append(cliente)

  print(f"Cliente {nome} criado com sucesso!")

def listar_contas(contas):
  for conta in contas:
    print("=" * 100)
    print(textwrap.dedent(str(conta)))

def criar_conta(numero_conta, clientes, contas):
  cpf = input("Digite o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("Cliente não encontrado")
    return
  
  conta = ContaCorrente.nova_conta(cliente=cliente, numero_conta=numero_conta)
  contas.append(conta)
  cliente.contas.append(conta)

  print( f"Conta criada com sucesso para o cliente {cliente.nome}")

main()