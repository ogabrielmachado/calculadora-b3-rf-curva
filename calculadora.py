import pandas as pd
import requests
import datetime as dt

def obter_token_b3():
    url = "https://api.calculadorarendafixa.com.br/login"
    payload = {"token": "seu-token"}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    data = response.json()
    token = data["Authorization"]
    return token

def consulta_preco_na_curva(codigo, taxa):
    data_hoje = dt.datetime.today().strftime('%Y-%m-%d')
    token = obter_token_b3()
    url = f"https://api.calculadorarendafixa.com.br/calcPU/{codigo}/{data_hoje}/{taxa}"
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    data = response.json()
    emissor = data["issuer"]
    preco_na_curva = data["PU"]
    preco_na_curva_formatado = f"{preco_na_curva:.2f}"
    tipo_ativo = data["tipoIF"]["codigoAsString"]  
    
    # Retorna preço, emissor e tipo do ativo
    return preco_na_curva_formatado, emissor, tipo_ativo

def consulta_taxa_por_preco(codigo, data_compra, preco_compra):
    """Consulta a taxa com base no código, data e preço de compra."""
    token = obter_token_b3()
    url = f"https://api.calculadorarendafixa.com.br/calcYield/{codigo}/{data_compra}/{preco_compra}"
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    data = response.json()
    taxa = data["yield"]
    return str(taxa)

def calcular_preco_na_curva_manual():
    """Calcula o preço na curva para códigos e taxas inseridos manualmente."""
    
    print("=== Calculadora de Preço na Curva ===")
    print("Digite os códigos e escolha entre informar a taxa ou o preço de compra.")
    print("Para finalizar a inserção, deixe o campo de código em branco e pressione Enter.")
    
    resultados = []
    
    while True:
        codigo = input("\nDigite o código do título (ou Enter para finalizar): ").strip().upper()
        if not codigo:
            break
        
        metodo = input(f"Escolha o método de cálculo para {codigo} (1 - Taxa, 2 - Preço+Data): ").strip()
        
        taxa = None
        
        if metodo == "1":
            # Usuário informa a taxa diretamente
            taxa = input(f"Digite a taxa para {codigo} (ex: 7.5): ").strip().replace(',', '.')
        
        elif metodo == "2":
            # Usuário informa preço de compra e data
            preco_compra = input(f"Digite o preço de compra para {codigo}: ").strip().replace(',', '.')
            data_compra_input = input(f"Digite a data de compra (DD/MM/AAAA): ").strip()
            
            try:
                # Validar formato da data
                data_obj = dt.datetime.strptime(data_compra_input, '%d/%m/%Y')
                # Converter para o formato YYYY-MM-DD para a API
                data_compra = data_obj.strftime('%Y-%m-%d')
                
                # Consultar a taxa com base no preço e data
                print(f"Consultando taxa para {codigo} com preço {preco_compra} em {data_compra_input}...")
                taxa = consulta_taxa_por_preco(codigo, data_compra, preco_compra)
                print(f"Taxa calculada: {taxa}%")
                
            except ValueError:
                print("Erro: Formato de data inválido. Use o formato DD/MM/AAAA.")
                continue
            except Exception as e:
                print(f"Erro ao consultar taxa: {str(e)}")
                continue
        
        else:
            print("Opção inválida. Tente novamente.")
            continue
        
        if not taxa:
            print("Erro: Taxa não informada ou não calculada.")
            continue
        
        try:
            # Agora recebemos preço, emissor e tipo do ativo
            preco_curva, emissor, tipo_ativo = consulta_preco_na_curva(codigo, taxa)
            quantidade = input(f"Digite a quantidade de {codigo}: ").strip()
            quantidade = int(quantidade) if quantidade else 1
            
            valor_total = float(preco_curva) * quantidade
            
            resultados.append({
                "Código": codigo,
                "Emissor": emissor,
                "Ativo": tipo_ativo, 
                "Taxa": taxa,
                "Quantidade": quantidade,
                "PU na Curva": float(preco_curva),
                "Valor Total": valor_total
            })
            
            print(f"\nCódigo: {codigo}")
            print(f"Emissor: {emissor}")
            print(f"Tipo: {tipo_ativo}")  # Exibimos o tipo do ativo
            print(f"Taxa: {taxa}%")
            print(f"PU na Curva: R$ {preco_curva}")
            print(f"Quantidade: {quantidade}")
            print(f"Valor Total: R$ {valor_total:.2f}")
            
        except Exception as e:
            print(f"Erro ao consultar {codigo}: {str(e)}")
    
    if resultados:
        # Criar DataFrame com os resultados
        df_resultados = pd.DataFrame(resultados)
        
        # Exibir resultados consolidados
        print("\n=== Resumo dos Cálculos ===")
        print(df_resultados)
        
        # Calcular valor total
        valor_total = df_resultados["Valor Total"].sum()
        print(f"\nValor Total na Curva: R$ {valor_total:.2f}")
        
        # Opção para salvar em Excel
        salvar = input("\nDeseja salvar os resultados em Excel? (s/n): ").strip().lower()
        if salvar == 's':
            try:
                caminho = f"Precos_Na_Curva_{dt.datetime.today().strftime('%Y%m%d')}.xlsx"
                df_resultados.to_excel(caminho, index=False)
                print(f"Resultados salvos em: {caminho}")
            except Exception as e:
                print(f"Erro ao salvar arquivo: {str(e)}")

if __name__ == "__main__":
    calcular_preco_na_curva_manual()