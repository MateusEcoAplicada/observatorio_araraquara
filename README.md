# Observatório Imobiliário de Araraquara 🏘️

Projeto de web scraping e análise de dados do mercado imobiliário de Araraquara/SP, inspirado no Observatório Nacional da UNESP.

## 📋 Descrição

Este projeto coleta, trata e analisa dados de anúncios imobiliários em Araraquara para:
- Monitorar preços de imóveis (venda e aluguel)
- Identificar tendências de mercado
- Mapear expansão territorial urbana
- Analisar desigualdades intraurbanas
- Apoiar políticas públicas de habitação

## 🛠️ Tecnologias

- **Python 3.8+**
- **Scrapers**: BeautifulSoup4, Selenium, Requests
- **Dados**: Pandas, NumPy
- **Visualização**: Matplotlib, Seaborn, Plotly
- **Geoespacial**: GeoPandas, Folium
- **Armazenamento**: SQLite, CSV

## 📂 Estrutura do Projeto

```
observatorio_araraquara/
├── scrapers/          # Scripts de coleta de dados
├── data/             # Dados coletados (raw e processados)
├── analysis/         # Scripts de análise
├── notebooks/        # Jupyter notebooks exploratórios
├── utils/            # Funções auxiliares
└── requirements.txt  # Dependências
```

## 🚀 Instalação

```bash
# Clone o repositório
git clone [seu-repo]

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente (opcional)
cp .env.example .env
```

## 💻 Uso

### 1. Coletar dados

```bash
# Scraping de todos os sites
python scrapers/run_all.py

# Scraping de site específico
python scrapers/vivareal_scraper.py --cidade araraquara
```

### 2. Processar dados

```bash
python utils/data_cleaner.py
```

### 3. Análise

```bash
# Executar análise completa
python analysis/analise_mercado.py

# Ou usar notebooks interativos
jupyter notebook notebooks/exploracao_dados.ipynb
```

## 📊 Análises Disponíveis

- Distribuição de preços por bairro
- Evolução temporal dos preços
- Análise de amplitude de valores (desigualdade)
- Mapeamento geoespacial dos anúncios
- Tipos de imóveis mais ofertados
- Análise de m² médio por região

## ⚖️ Considerações Éticas

Este projeto:
- Respeita robots.txt dos sites
- Implementa rate limiting
- Não sobrecarrega servidores
- Uso apenas para pesquisa acadêmica
- Dados públicos disponíveis nos portais

## 📝 Licença

MIT License - Uso acadêmico e pesquisa

## 👥 Autor

Inspirado no trabalho do Prof. Everaldo Melazzo (UNESP/Presidente Prudente)

## 🔗 Referências

- [Artigo do Jornal da UNESP](https://jornal.unesp.br/2026/01/28/pesquisadores-da-unesp-investigam-efeitos-da-crescente-influencia-do-capital-financeiro-sobre-a-producao-de-moradias-no-brasil/)
- GAsPERR - Grupo de Pesquisa Produção do Espaço e Redefinições Regionais
