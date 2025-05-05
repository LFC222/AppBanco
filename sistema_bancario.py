menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "1":
        print("Depósito")
        deposito = float(input("Digite o valor do depósito: "))
        saldo += deposito
        extrato.append(f"DEPOSITO: + R${deposito:.2f}.")
        print(f"Saldo da conta: {saldo}")

    elif opcao == "2":
        print("Saque")

        if numero_saques < LIMITE_SAQUES:
            if saldo > 0:
                valor_saque = float(input("Digite o valor de saque que deseja: "))
            
                if valor_saque > limite:
                    print("O valor desejado excede o limite, tente um valor menor.")
                else:
                    numero_saques += 1
                    saldo -= valor_saque
                    extrato.append(f"SAQUE: -R${valor_saque:.2f} {numero_saques}/{LIMITE_SAQUES}.")
                    print("Saque realizado com sucesso")
            else:
                print("Não foi possivel realizar saque, saldo insuficiente")

        else: 
            print("Limites de saques diários alcançados, tente novamente amanhã.")

    elif opcao == "3":
        print("Extrato")

        if extrato:
            print("\n ========== EXTRATO =========")
            print('\n'.join(extrato))
            print("\n ============================")
            print(f"Saldo da conta: {saldo}")
        else:
            print("Não foram realizadas movimentações.")

    elif opcao == "0":
        break

    else:
        print("Operação inválida")