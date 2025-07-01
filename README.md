# 📊 Dashboard Online Retail

Este projeto apresenta um dashboard interativo desenvolvido com Streamlit para explorar visualmente os dados de vendas de uma pequena loja online do Reino Unido, através do dataset Online Retail. Através de gráficos e filtros, é possível analisar tendências de receita, comportamento de compra dos clientes, produtos mais vendidos, entre outras informações úteis.

## 🎯 Objetivo

Facilitar a análise exploratória de dados de vendas de um e-commerce do Reino Unidodo usando o dataset "Online Retail", destacando padrões de consumo, desempenho por país, perfil de clientes e variações temporais nas vendas.

## 📁 Estrutura do Projeto

- `main.py`: código principal com o dashboard.
- `Online Retail.xlsx`: base de dados utilizada.
- `requirements.txt`: lista de dependências.

## 🚀 Como Executar

1. **Clone o repositório** ou copie os arquivos para sua máquina.

2. (Opcional) **Crie um ambiente virtual**:
```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Execute o dashboard**:
```bash
streamlit run main.py
```

## 🧭 Navegação e Funcionalidades

- O menu lateral permite navegar por 4 páginas:
  - **Visão Geral**: resumo de indicadores e receita mensal.
  - **Produtos**: análise de produtos mais vendidos e preços.
  - **Clientes e Países**: principais clientes e países que mais compram.
  - **Análises Temporais**: comportamento de vendas por hora e dia da semana.

- Os **filtros de data** afetam todos os gráficos e seções.
- Possibilidade de **baixar os dados filtrados** no formato CSV.

## 📌 Dataset

O conjunto de dados utilizado é o [Online Retail Data Set](https://archive.ics.uci.edu/dataset/352/online+retail), disponibilizado pela UCI Machine Learning Repository.

---

Desenvolvido por Jonathan 😺, aluno do cimol do curso de informatica