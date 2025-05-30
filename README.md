# 📄 Sistema de Faturamento por Cliente

Este é um sistema web simples, desenvolvido com **Python** e **Streamlit**, para automatizar o cálculo de faturamento com base na quantidade de impressões realizadas por clientes. O sistema gera relatórios individuais em Excel para cada cliente, com todos os detalhes da fatura.

---

## 🚀 Funcionalidades

- Autenticação simples por login e senha
- Upload de planilha com os dados de impressão
- Cálculo automático de franquia e excedente (A4 e A3)
- Visualização do relatório resumido na tela
- Geração de relatórios individuais por cliente (formato `.xlsx`)
- Barra de busca para facilitar encontrar o cliente

---

## 📊 Cálculo da Fatura

- **Franquia fixa:** R$ 100,00 para até 1000 créditos
- Impressões A4 valem 1 crédito
- Impressões A3 valem 2 créditos
- Excedente é cobrado:
  - R$ 0,10 por A4
  - R$ 0,20 por A3 (convertido proporcionalmente)

---

## 📁 Exemplo de Planilha de Entrada

| Cliente    | Tipo_Impressao | Quantidade | Data       |
|------------|----------------|------------|------------|
| Cliente 1  | A4             | 800        | 01/05/2025 |
| Cliente 1  | A3             | 150        | 01/05/2025 |
| Cliente 2  | A4             | 1100       | 01/05/2025 |
| Cliente 2  | A3             | 50         | 01/05/2025 |
| Cliente 3  | A4             | 600        | 01/05/2025 |
| Cliente 3  | A3             | 0          | 01/05/2025 |

---

## ▶️ Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sistema-faturamento.git
cd sistema-faturamento

Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Execute o app com o Streamlit:

bash
Copiar
Editar
streamlit run app.py
🔒 Acesso Seguro
O sistema exige login e senha. Os dados de acesso estão definidos no arquivo login.py. Em produção, recomenda-se integrar com autenticação mais robusta ou sistemas externos (ex: GitHub Auth, autenticação por token, etc.).

📦 Empacotar como EXE (opcional)
Para transformar o app em executável .exe:

bash
Copiar
Editar
pip install pyinstaller
pyinstaller --noconfirm --onefile --add-data "templates;templates" app.py
Atenção: Streamlit é pensado para aplicações web. A versão .exe funciona com navegador local.

🛠 Estrutura do Projeto
pgsql
Copiar
Editar
sistema-faturamento/
├── app.py
├── login.py
├── utils/
│   ├── calculos.py
│   └── relatorios.py
├── requirements.txt
└── README.md
📬 Contato
Desenvolvido por Jhonatan de Andrade Pires
LinkedIn | jhonatandeandradepires@gmail.com

