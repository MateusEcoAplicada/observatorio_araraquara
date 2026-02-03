# Guia de Início Rápido 🚀

## Instalação

### 1. Clone o repositório
```bash
git clone [seu-repositorio]
cd observatorio_araraquara
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## Uso Básico

### Coleta de Dados

#### Opção 1: Coleta completa (todos os sites e tipos)
```bash
python scrapers/run_all.py
```

#### Opção 2: Coleta personalizada
```bash
# Apenas apartamentos à venda no VivaReal
python scrapers/run_all.py --tipos-imovel apartamento --tipos-transacao venda --sites vivareal --max-paginas 5

# Casas e apartamentos para venda e aluguel
python scrapers/run_all.py --tipos-imovel apartamento casa --tipos-transacao venda aluguel --max-paginas 10
```

#### Opção 3: Site específico
```bash
# Apenas VivaReal
python scrapers/vivareal_scraper.py --tipo-imovel apartamento --tipo-transacao venda --max-paginas 5

# Apenas OLX
python scrapers/olx_scraper.py --tipo-imovel casa --tipo-transacao aluguel --max-paginas 3
```

### Análise de Dados

#### Análise rápida
```bash
# Usa o arquivo mais recente automaticamente
python analysis/analise_mercado.py
```

#### Relatório completo com visualizações
```bash
python analysis/analise_mercado.py --relatorio-completo
```

#### Análise de arquivo específico
```bash
python analysis/analise_mercado.py --arquivo data/raw/vivareal_Araraquara_20260130.csv --relatorio-completo
```

### Análise Interativa (Jupyter)

```bash
# Iniciar Jupyter
jupyter notebook

# Abrir o notebook
# notebooks/exploracao_dados.ipynb
```

## Estrutura dos Dados

### Colunas principais coletadas:
- `id_anuncio`: ID único do anúncio
- `titulo`: Título do anúncio
- `tipo_imovel`: apartamento, casa, terreno, etc.
- `tipo_transacao`: venda ou aluguel
- `preco`: Preço em R$
- `area`: Área em m²
- `quartos`: Número de quartos
- `banheiros`: Número de banheiros
- `vagas`: Vagas de garagem
- `endereco`: Endereço completo
- `bairro`: Nome do bairro
- `cidade`: Araraquara
- `estado`: SP
- `url`: URL do anúncio original
- `fonte`: Site de origem (vivareal, olx, etc.)
- `data_coleta`: Data e hora da coleta

## Exemplos de Análises

### 1. Comparar preços por bairro
```python
import pandas as pd

df = pd.read_csv('data/raw/seu_arquivo.csv')
preco_por_bairro = df.groupby('bairro')['preco'].mean().sort_values(ascending=False)
print(preco_por_bairro.head(10))
```

### 2. Encontrar imóveis mais caros vs. mais baratos
```python
# Mais caros
print(df.nlargest(10, 'preco')[['titulo', 'preco', 'bairro', 'tipo_imovel']])

# Mais baratos
print(df.nsmallest(10, 'preco')[['titulo', 'preco', 'bairro', 'tipo_imovel']])
```

### 3. Calcular amplitude de preços (desigualdade)
```python
amplitude = df['preco'].max() / df['preco'].min()
print(f"Amplitude: {amplitude:.2f}x")
```

### 4. Analisar preço por m²
```python
df['preco_m2'] = df['preco'] / df['area']
print(df.groupby('bairro')['preco_m2'].mean().sort_values(ascending=False))
```

## Boas Práticas

### 1. Rate Limiting
Os scrapers já implementam delays entre requisições. Para ajustar:
```python
# Em config.py
REQUEST_DELAY = 3  # segundos entre requisições
```

### 2. Limpeza de Dados
Sempre limpe os dados antes de análises:
```python
from analysis.analise_mercado import AnalisadorMercadoImobiliario

analisador = AnalisadorMercadoImobiliario('data/raw/arquivo.csv')
df_limpo = analisador.limpar_dados()
```

### 3. Coleta Incremental
Para coletar dados ao longo do tempo:
```bash
# Adicione ao cron (Linux) ou Task Scheduler (Windows)
# Executar semanalmente
0 2 * * 0 cd /path/to/observatorio_araraquara && python scrapers/run_all.py
```

## Solução de Problemas

### Erro: "No module named 'requests'"
```bash
pip install -r requirements.txt
```

### Erro: Timeout nas requisições
- Aumente o valor em `config.py`: `TIMEOUT = 60`
- Reduza `max_paginas` nas coletas

### Dados vazios ou incompletos
- Sites mudaram estrutura HTML (comum!)
- Atualize os seletores CSS em `scrapers/`
- Use ferramentas de desenvolvedor do navegador para inspecionar

### "Permission denied" ao salvar
```bash
# Linux/Mac
chmod -R 755 data/

# Ou execute com sudo (não recomendado)
```

## Próximos Passos

1. **Geocodificação**: Adicionar coordenadas lat/lon para mapeamento
2. **Análise temporal**: Coletar dados periodicamente e acompanhar evolução
3. **Machine Learning**: Prever preços com base em características
4. **Dashboard**: Criar painel interativo com Streamlit ou Dash
5. **API**: Disponibilizar dados via REST API

## Contribuindo

Este é um projeto educacional inspirado na pesquisa da UNESP. Sinta-se livre para:
- Adicionar novos scrapers (ZapImóveis, Imovelweb, etc.)
- Melhorar análises existentes
- Corrigir bugs
- Documentar melhor

## Recursos Adicionais

- [Tutorial de Web Scraping com BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Artigo Original - Jornal UNESP](https://jornal.unesp.br/2026/01/28/pesquisadores-da-unesp-investigam-efeitos-da-crescente-influencia-do-capital-financeiro-sobre-a-producao-de-moradias-no-brasil/)

## Suporte

Para dúvidas ou problemas:
1. Verifique a documentação acima
2. Consulte os logs de erro
3. Abra uma issue no GitHub
