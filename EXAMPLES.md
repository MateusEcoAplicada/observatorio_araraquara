# Exemplos Práticos de Uso

## 📝 Casos de Uso Reais

### Caso 1: Estudante de Geografia fazendo TCC

**Objetivo**: Analisar como os preços variam entre bairros centrais e periféricos em Araraquara.

**Passos**:

```bash
# 1. Coletar dados
python scrapers/run_all.py --max-paginas 20

# 2. Analisar
python analysis/analise_mercado.py --relatorio-completo
```

**Análise no Python**:
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/raw/seu_arquivo.csv')

# Definir bairros centrais vs periféricos
bairros_centrais = ['Centro', 'Vila Harmonia', 'Jardim América']
bairros_perifericos = ['Parque Pinheiros', 'Jardim Iguatemi', 'Vale do Sol']

df['categoria'] = df['bairro'].apply(
    lambda x: 'Central' if x in bairros_centrais 
    else 'Periférico' if x in bairros_perifericos 
    else 'Outro'
)

# Comparar preços médios
comparacao = df.groupby('categoria')['preco'].agg(['mean', 'median', 'count'])
print(comparacao)

# Visualizar
df.boxplot(column='preco', by='categoria', figsize=(10, 6))
plt.ylabel('Preço (R$)')
plt.title('Comparação: Bairros Centrais vs Periféricos')
plt.savefig('analise_centro_periferia.png')
```

---

### Caso 2: Corretor Imobiliário analisando mercado

**Objetivo**: Identificar bairros em valorização e oportunidades.

```python
import pandas as pd

df = pd.read_csv('data/raw/seu_arquivo.csv')

# Calcular preço por m² por bairro
df['preco_m2'] = df['preco'] / df['area']

analise_bairros = df.groupby('bairro').agg({
    'preco': ['mean', 'count'],
    'preco_m2': 'mean',
    'area': 'mean'
}).round(2)

# Filtrar bairros com volume significativo
analise_bairros = analise_bairros[analise_bairros[('preco', 'count')] >= 10]

# Ordenar por preço/m²
analise_bairros = analise_bairros.sort_values(('preco_m2', 'mean'), ascending=False)

print("Top 10 Bairros - Preço/m²:")
print(analise_bairros.head(10))

# Identificar oportunidades: baixo preço/m² + área grande
oportunidades = df[(df['preco_m2'] < df['preco_m2'].median()) & 
                   (df['area'] > df['area'].median())]

print(f"\nOportunidades encontradas: {len(oportunidades)}")
print(oportunidades[['titulo', 'bairro', 'preco', 'area', 'preco_m2']].head(10))
```

---

### Caso 3: Gestor Público planejando habitação social

**Objetivo**: Identificar áreas com menor custo para programas habitacionais.

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data/raw/seu_arquivo.csv')

# Focar em imóveis de interesse social (2-3 quartos, até 70m²)
df_interesse_social = df[
    (df['quartos'].between(2, 3)) &
    (df['area'] <= 70) &
    (df['tipo_imovel'].isin(['apartamento', 'casa']))
]

# Analisar por bairro
analise_social = df_interesse_social.groupby('bairro').agg({
    'preco': ['mean', 'min', 'count'],
    'area': 'mean'
})

analise_social.columns = ['Preco_Medio', 'Preco_Minimo', 'Quantidade', 'Area_Media']
analise_social = analise_social[analise_social['Quantidade'] >= 5]
analise_social = analise_social.sort_values('Preco_Medio')

print("Bairros mais acessíveis para habitação social:")
print(analise_social.head(10))

# Visualizar
plt.figure(figsize=(12, 8))
top_15 = analise_social.head(15)
plt.barh(range(len(top_15)), top_15['Preco_Medio'])
plt.yticks(range(len(top_15)), top_15.index)
plt.xlabel('Preço Médio (R$)')
plt.title('15 Bairros Mais Acessíveis - Imóveis Interesse Social')
plt.tight_layout()
plt.savefig('bairros_interesse_social.png', dpi=300)
```

---

### Caso 4: Pesquisador comparando com outras cidades médias

**Objetivo**: Comparar Araraquara com outras cidades do interior paulista.

```python
import pandas as pd

# Supondo que você coletou dados de múltiplas cidades
df_araraquara = pd.read_csv('data/raw/araraquara_dados.csv')
df_ribeirao = pd.read_csv('data/raw/ribeirao_preto_dados.csv')  # Exemplo
df_sao_carlos = pd.read_csv('data/raw/sao_carlos_dados.csv')  # Exemplo

# Adicionar coluna de cidade
df_araraquara['cidade_analise'] = 'Araraquara'
df_ribeirao['cidade_analise'] = 'Ribeirão Preto'
df_sao_carlos['cidade_analise'] = 'São Carlos'

# Concatenar
df_total = pd.concat([df_araraquara, df_ribeirao, df_sao_carlos])

# Comparar
comparacao = df_total.groupby('cidade_analise').agg({
    'preco': ['mean', 'median', 'min', 'max'],
    'area': 'mean'
})

comparacao['amplitude'] = comparacao[('preco', 'max')] / comparacao[('preco', 'min')]

print("Comparação entre cidades:")
print(comparacao)

# Boxplot comparativo
df_total.boxplot(column='preco', by='cidade_analise', figsize=(10, 6))
plt.ylabel('Preço (R$)')
plt.title('Comparação de Preços - Cidades Médias Paulistas')
plt.savefig('comparacao_cidades.png')
```

---

### Caso 5: Jornalista escrevendo reportagem

**Objetivo**: Encontrar histórias sobre desigualdade imobiliária.

```python
import pandas as pd

df = pd.read_csv('data/raw/seu_arquivo.csv')

# 1. Encontrar o imóvel mais caro e o mais barato
mais_caro = df.loc[df['preco'].idxmax()]
mais_barato = df.loc[df['preco'].idxmin()]

print("CONTRASTE:")
print(f"\nImóvel mais caro:")
print(f"  Preço: R$ {mais_caro['preco']:,.2f}")
print(f"  Bairro: {mais_caro['bairro']}")
print(f"  Tipo: {mais_caro['tipo_imovel']}")

print(f"\nImóvel mais barato:")
print(f"  Preço: R$ {mais_barato['preco']:,.2f}")
print(f"  Bairro: {mais_barato['bairro']}")
print(f"  Tipo: {mais_barato['tipo_imovel']}")

print(f"\nDiferença: {mais_caro['preco'] / mais_barato['preco']:.1f}x")

# 2. Calcular quantos salários mínimos (R$ 1.412 em 2024)
salario_minimo = 1412

df['salarios_minimos'] = df['preco'] / salario_minimo

print(f"\nImóvel médio custa: {df['salarios_minimos'].mean():.0f} salários mínimos")
print(f"Imóvel mais caro custa: {df['salarios_minimos'].max():.0f} salários mínimos")

# 3. Bairros com maior amplitude
amplitude_bairro = df.groupby('bairro').agg({
    'preco': ['min', 'max', 'count']
})
amplitude_bairro['amplitude'] = amplitude_bairro[('preco', 'max')] / amplitude_bairro[('preco', 'min')]
amplitude_bairro = amplitude_bairro[amplitude_bairro[('preco', 'count')] >= 10]
amplitude_bairro = amplitude_bairro.sort_values('amplitude', ascending=False)

print("\nBairros com maior desigualdade interna:")
print(amplitude_bairro.head(5))
```

---

### Caso 6: Desenvolvedor criando aplicação web

**Objetivo**: Dashboard interativo com Streamlit.

Criar arquivo `dashboard.py`:

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title('🏘️ Observatório Imobiliário de Araraquara')

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv('data/raw/dados_completos.csv')
    df['preco_m2'] = df['preco'] / df['area']
    return df

df = load_data()

# Sidebar - Filtros
st.sidebar.header('Filtros')
tipo_transacao = st.sidebar.multiselect(
    'Tipo de Transação',
    options=df['tipo_transacao'].unique(),
    default=df['tipo_transacao'].unique()
)

tipo_imovel = st.sidebar.multiselect(
    'Tipo de Imóvel',
    options=df['tipo_imovel'].unique(),
    default=df['tipo_imovel'].unique()
)

# Filtrar dados
df_filtrado = df[
    (df['tipo_transacao'].isin(tipo_transacao)) &
    (df['tipo_imovel'].isin(tipo_imovel))
]

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Anúncios", f"{len(df_filtrado):,}")
col2.metric("Preço Médio", f"R$ {df_filtrado['preco'].mean():,.0f}")
col3.metric("Preço/m² Médio", f"R$ {df_filtrado['preco_m2'].mean():,.0f}")

# Gráficos
st.subheader('Distribuição de Preços')
fig = px.histogram(df_filtrado, x='preco', nbins=50)
st.plotly_chart(fig)

st.subheader('Preço Médio por Bairro')
preco_bairro = df_filtrado.groupby('bairro')['preco'].mean().sort_values(ascending=False).head(15)
fig = px.bar(x=preco_bairro.values, y=preco_bairro.index, orientation='h')
st.plotly_chart(fig)

# Tabela
st.subheader('Últimos Anúncios')
st.dataframe(df_filtrado[['titulo', 'preco', 'bairro', 'tipo_imovel']].head(20))
```

Executar:
```bash
streamlit run dashboard.py
```

---

## 🔄 Workflow de Análise Longitudinal

Para acompanhar evolução ao longo do tempo:

```bash
# Configurar cron job (Linux) para executar semanalmente
# Editar crontab:
crontab -e

# Adicionar linha (executa todo domingo às 2h):
0 2 * * 0 cd /path/to/observatorio_araraquara && python scrapers/run_all.py

# Depois de alguns meses, comparar:
```

```python
import pandas as pd
import matplotlib.pyplot as plt

# Carregar múltiplas coletas
df_jan = pd.read_csv('data/raw/coleta_2026_01.csv')
df_fev = pd.read_csv('data/raw/coleta_2026_02.csv')
df_mar = pd.read_csv('data/raw/coleta_2026_03.csv')

df_jan['mes'] = 'Janeiro'
df_fev['mes'] = 'Fevereiro'
df_mar['mes'] = 'Março'

df_total = pd.concat([df_jan, df_fev, df_mar])

# Evolução do preço médio
evolucao = df_total.groupby('mes')['preco'].mean()

plt.figure(figsize=(10, 6))
evolucao.plot(kind='line', marker='o')
plt.ylabel('Preço Médio (R$)')
plt.title('Evolução do Preço Médio - Araraquara')
plt.grid(True)
plt.savefig('evolucao_temporal.png')
```

---

## 💡 Dicas e Truques

### 1. Lidar com dados faltantes
```python
# Verificar dados faltantes
print(df.isnull().sum())

# Imputar valores
df['quartos'].fillna(df['quartos'].median(), inplace=True)
df['bairro'].fillna('Não informado', inplace=True)
```

### 2. Criar categorias de preço
```python
df['faixa_preco'] = pd.cut(
    df['preco'],
    bins=[0, 200000, 400000, 600000, float('inf')],
    labels=['Até 200k', '200k-400k', '400k-600k', 'Acima de 600k']
)
```

### 3. Exportar para Excel formatado
```python
with pd.ExcelWriter('analise_completa.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Dados Brutos', index=False)
    resumo.to_excel(writer, sheet_name='Resumo')
    por_bairro.to_excel(writer, sheet_name='Por Bairro')
```

### 4. Salvar gráficos de alta qualidade
```python
plt.savefig('grafico.png', dpi=300, bbox_inches='tight', transparent=False)
```

---

Estes exemplos cobrem os principais casos de uso do projeto. Adapte-os conforme suas necessidades!
