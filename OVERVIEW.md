# Observatório Imobiliário de Araraquara - Visão Geral

## 📊 Contexto e Inspiração

Este projeto foi inspirado pela pesquisa do **Prof. Everaldo Melazzo** da UNESP Presidente Prudente, apresentada no artigo do Jornal da UNESP sobre os efeitos da financeirização do mercado imobiliário nas cidades médias brasileiras.

### Problema Identificado

O artigo destaca que:
- Cidades médias (100-500 mil habitantes) concentram o crescimento populacional brasileiro
- Há déficit de dados sobre mercado imobiliário nessas cidades
- A política habitacional baseada apenas em crédito aumenta preços sem atender à população de baixa renda
- A diferença entre imóveis mais caros e mais baratos está aumentando
- A habitação está sendo tratada como ativo financeiro, não como direito

## 🎯 Objetivos do Projeto

### Objetivos Primários

- Identificar desigualdades intraurbanas (amplitude de preços)
- Mapear expansão territorial urbana
- Analisar tipos de imóveis mais ofertados
- Calcular preços médios por m² por bairro

### Objetivos Futuros
- Análise temporal (comparar dados ao longo dos meses/anos)
- Geocodificação (mapas interativos)
- Predição de preços com Machine Learning
- Dashboard web público
- API para acesso aos dados

## 🏗️ Arquitetura do Projeto

```
observatorio_araraquara/
│
├── scrapers/              # Módulo de coleta de dados
│   ├── base_scraper.py    # Classe abstrata base
│   ├── vivareal_scraper.py
│   ├── olx_scraper.py
│   └── run_all.py         # Executa todos os scrapers
│
├── utils/                 # Funções utilitárias
│   └── helpers.py         # Limpeza e normalização de dados
│
├── analysis/              # Módulo de análise
│   └── analise_mercado.py # Análises estatísticas e visualizações
│
├── data/                  # Armazenamento de dados
│   ├── raw/              # Dados brutos coletados
│   └── processed/        # Dados processados e análises
│
├── notebooks/             # Jupyter notebooks exploratórios
│   └── exploracao_dados.ipynb
│
└── config.py             # Configurações globais
```

## 🔬 Metodologia

### 1. Coleta de Dados (Web Scraping)

**Sites alvos:**
- VivaReal
- OLX
- (Futuro: ZapImóveis, Imovelweb)

**Dados coletados:**
- Preço (venda/aluguel)
- Tipo de imóvel (casa, apartamento, terreno, etc.)
- Localização (endereço, bairro)
- Características (área, quartos, banheiros, vagas)
- URL original e data de coleta

**Boas práticas implementadas:**
- Rate limiting (delays entre requisições)
- Retry logic (tentativas em caso de falha)
- Respeito ao robots.txt
- User-Agent realista
- Logs detalhados

### 2. Processamento de Dados

**Limpeza:**
- Remoção de duplicatas
- Tratamento de valores nulos
- Normalização de textos (bairros, tipos)
- Conversão de tipos de dados
- Remoção de outliers extremos

**Enriquecimento:**
- Cálculo de preço por m²
- Classificação de tipos de imóvel
- Padronização de endereços

### 3. Análise

**Estatísticas descritivas:**
- Média, mediana, min, max de preços
- Distribuição por tipo de imóvel
- Distribuição por tipo de transação
- Top bairros com mais anúncios

**Análises específicas:**
- Preços médios por bairro
- Amplitude de preços (medida de desigualdade)
- Correlações entre variáveis
- Preço por m² por região

**Visualizações:**
- Histogramas de distribuição
- Boxplots de preços
- Gráficos de barras por categoria
- Mapas de calor (correlação)

## 📈 Principais Métricas

### 1. Amplitude de Preços
```
Amplitude = Preço Máximo / Preço Mínimo
```
Mede a desigualdade: quanto maior, maior a diferença entre imóveis caros e baratos.

### 2. Preço por m²
```
Preço/m² = Preço Total / Área
```
Permite comparação justa entre imóveis de tamanhos diferentes.

### 3. Distribuição Espacial
Quantidade e preço médio de anúncios por bairro.

### 4. Composição do Mercado
Percentual de cada tipo de imóvel e transação.

## 🔄 Fluxo de Trabalho Típico

```
1. COLETA
   python scrapers/run_all.py
   ↓
   Dados salvos em: data/raw/

2. ANÁLISE
   python analysis/analise_mercado.py --relatorio-completo
   ↓
   Resultados salvos em: data/processed/
   
3. EXPLORAÇÃO INTERATIVA
   jupyter notebook
   ↓
   Abrir: notebooks/exploracao_dados.ipynb
```

## 🎓 Aplicações Educacionais

Este projeto serve como:
1. **Caso de estudo** em web scraping ético
2. **Exemplo prático** de análise de dados urbanos
3. **Base para TCC** em Geografia, Economia, Ciência da Computação
4. **Ferramenta** para urbanistas e gestores públicos
5. **Laboratório** para aprender Pandas, visualização de dados, etc.

## ⚖️ Considerações Éticas e Legais

### ✅ Boas Práticas
- Dados públicos disponíveis nos portais
- Rate limiting para não sobrecarregar servidores
- Respeito aos termos de serviço
- Uso estritamente acadêmico/pesquisa
- Sem revenda ou uso comercial dos dados

### ⚠️ Limitações
- Sites podem mudar estrutura HTML (manutenção necessária)
- Dados refletem apenas anúncios online (viés)
- Não captura transações efetivadas (apenas ofertas)
- Necessário atualização periódica dos seletores CSS

## 🚀 Expansões Futuras Possíveis

### Curto Prazo
- [ ] Adicionar scraper do ZapImóveis
- [ ] Implementar geocodificação (lat/lon)
- [ ] Criar banco de dados SQLite
- [ ] Adicionar testes unitários

### Médio Prazo
- [ ] Dashboard interativo (Streamlit/Dash)
- [ ] Análise temporal (séries temporais)
- [ ] Comparação com outras cidades médias
- [ ] Integração com dados IBGE

### Longo Prazo
- [ ] Machine Learning para previsão de preços
- [ ] API REST para acesso aos dados
- [ ] Mapa interativo (Folium/Plotly)
- [ ] Análise de sentimento em descrições
- [ ] Detecção de anomalias (preços suspeitos)

## 📚 Referências e Links Úteis

1. **Artigo Original**: [Jornal UNESP](https://jornal.unesp.br/2026/01/28/pesquisadores-da-unesp-investigam-efeitos-da-crescente-influencia-do-capital-financeiro-sobre-a-producao-de-moradias-no-brasil/)

2. **Documentação Técnica**:
   - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
   - [Pandas](https://pandas.pydata.org/docs/)
   - [Matplotlib](https://matplotlib.org/)
   - [Seaborn](https://seaborn.pydata.org/)

3. **Conceitos Relacionados**:
   - Financeirização do mercado imobiliário
   - Déficit habitacional
   - Expansão urbana
   - Desigualdades intraurbanas

## 👥 Contribuindo

Este é um projeto educacional de código aberto. Contribuições são bem-vindas:

- 🐛 Reportar bugs
- 💡 Sugerir melhorias
- 🔧 Corrigir código
- 📖 Melhorar documentação
- 🎨 Adicionar visualizações
- 🌐 Adicionar novos scrapers

## 📄 Licença

MIT License - Livre para uso educacional e pesquisa.

---

**Desenvolvido com base na pesquisa do Prof. Everaldo Melazzo (UNESP)**

*"A depender da dinâmica imobiliária que se estabelece numa cidade, ela pode se tornar uma matriz geradora de um processo de desigualdade que acaba rebatendo em todas as outras políticas públicas."*
