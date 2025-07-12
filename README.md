# 📈 Calculadora de Preço na Curva - Renda Fixa

Após a mudança nas regras de visualização de investimentos, a maioria dos bancos e corretoras limitou a visualização do preço dos títulos de renda fixa na curva, o que pode levar a erros no cálculo da rentabilidade para aqueles investidores que não desejam se desfazer de seus títulos antes do vencimento. 

Este projeto em Python permite calcular o **PU na curva** de títulos de renda fixa e estimar **taxas equivalentes** com base em preço e data de compra, utilizando a API pública da B3 [Calculadora Renda Fixa](https://api.calculadorarendafixa.com.br/).

---

## 🧮 Funcionalidades

- Consultar o **preço na curva (PU)** de um título a partir de seu código e taxa.
- Calcular a **taxa de retorno** com base em preço e data de compra.
- Inserir múltiplos títulos manualmente via terminal.
- Exibir um **resumo consolidado** com emissor, tipo do ativo, taxa, PU e valor total.
- Exportar os resultados para uma planilha Excel (`.xlsx`).

---

## 🔧 Requisitos

- Python 3.8 ou superior
- Bibliotecas:
  - `pandas`
  - `requests`

Instale os requisitos com:

```bash
pip install pandas requests
```

---

## 🔑 Como obter seu token de acesso

Para utilizar a API, é necessário obter um token de autenticação pessoal. Siga os passos abaixo:

1. Acesse o site [https://calculadorarendafixa.com.br/](https://calculadorarendafixa.com.br/).
2. Clique em **Minha Conta** (no canto superior direito) e faça login.
3. Acesse a aba **Meus Dados**.
4. Role a página até a seção **Token de Acesso**.
5. Clique em **Gerar novo token**.
6. Copie o token gerado e cole no seu código Python, substituindo `"seu-token"`:

```python
payload = {"token": "seu-token"}
```

> ⚠️ Guarde seu token com segurança. Ele é pessoal e intransferível.

---

## 🚀 Como usar

1. Clone este repositório:

```bash
git clone https://github.com/ogabrielmachado/calculadora-b3-rf-curva.git
cd calculadora-b3-rf-curva
```

2. Abra o arquivo `.py` e insira seu token pessoal no campo indicado.

3. Execute o script:

```bash
python calculadora.py
```

4. Siga as instruções no terminal:
   - Digite o código do ativo
   - Escolha entre informar a **taxa** ou o **preço + data**
   - Insira a **quantidade**
   - Consulte os dados consolidados
   - Opte por **salvar em Excel**

---

## 💻 Exemplo de uso

```
=== Calculadora de Preço na Curva ===
Digite o código do título (ou Enter para finalizar): ABCA01
Escolha o método de cálculo (1 - Taxa, 2 - Preço+Data): 2
Digite o preço de compra: 985
Digite a data de compra (DD/MM/AAAA): 01/07/2025
Consultando taxa...
Taxa calculada: 10.73%
PU na Curva: R$ 1023.40
Quantidade: 5
Valor Total: R$ 5.117,00
```

---

## 📂 Exportação

Ao final do processo, você pode salvar os resultados em um arquivo `.xlsx`:

```
Resultados salvos em: Precos_Na_Curva_20250712.xlsx
```

---

## 🔒 Observações

- O projeto **não compartilha nem armazena** seu token.
- A API utilizada pode possuir limites de acesso ou políticas de uso definidas pela B3.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
