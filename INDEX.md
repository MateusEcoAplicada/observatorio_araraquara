# 📚 Índice do Projeto - Observatório Imobiliário de Araraquara

## 📖 Documentação Principal

### 1️⃣ **README.md** - Primeiro contato
- Visão geral do projeto
- Tecnologias utilizadas
- Estrutura básica
- Como citar o projeto

### 2️⃣ **QUICKSTART.md** - Começando rapidamente
- Instalação passo a passo
- Primeiros comandos
- Estrutura dos dados
- Solução de problemas comuns
- **👉 Recomendado para iniciantes**

### 3️⃣ **OVERVIEW.md** - Visão detalhada
- Contexto e inspiração (pesquisa UNESP)
- Objetivos do projeto
- Arquitetura completa
- Metodologia de coleta e análise
- Roadmap futuro
- **👉 Recomendado para entender o projeto em profundidade**

### 4️⃣ **EXAMPLES.md** - Casos práticos de uso
- 6 casos de uso reais
- Código pronto para usar
- Dicas e truques
- **👉 Recomendado para ver o projeto em ação**

## 🗂️ Estrutura de Arquivos

```
observatorio_araraquara/
│
├── 📄 README.md              # Visão geral
├── 📄 QUICKSTART.md          # Guia de início rápido
├── 📄 OVERVIEW.md            # Documentação detalhada
├── 📄 EXAMPLES.md            # Exemplos práticos
├── 📄 INDEX.md               # Este arquivo
│
├── ⚙️ config.py              # Configurações globais
├── 📦 requirements.txt       # Dependências Python
├── 🧪 test_setup.py          # Script de teste
│
├── 🔧 .env.example           # Exemplo de variáveis de ambiente
├── 🚫 .gitignore            # Arquivos ignorados pelo Git
│
├── 📁 scrapers/              # Módulo de coleta de dados
│   ├── __init__.py
│   ├── base_scraper.py      # Classe abstrata base
│   ├── vivareal_scraper.py  # Scraper VivaReal
│   ├── olx_scraper.py       # Scraper OLX
│   └── run_all.py           # Executor principal
│
├── 📁 utils/                 # Utilitários
│   ├── __init__.py
│   └── helpers.py           # Funções auxiliares
│
├── 📁 analysis/              # Módulo de análise
│   ├── __init__.py
│   └── analise_mercado.py   # Análises e visualizações
│
├── 📁 notebooks/             # Notebooks Jupyter
│   └── exploracao_dados.ipynb
│
└── 📁 data/                  # Armazenamento de dados
    ├── raw/                 # Dados brutos (CSVs coletados)
    └── processed/           # Dados processados e análises
```

## 🎯 Por onde começar?

### Se você quer...

#### 🚀 **Usar o projeto rapidamente**
1. Leia **QUICKSTART.md**
2. Execute `python test_setup.py`
3. Execute `python scrapers/run_all.py`
4. Execute `python analysis/analise_mercado.py --relatorio-completo`

#### 📚 **Entender o projeto profundamente**
1. Leia **README.md**
2. Leia **OVERVIEW.md**
3. Explore os códigos em `scrapers/` e `analysis/`
4. Experimente com **EXAMPLES.md**

#### 💻 **Aprender web scraping**
1. Estude `scrapers/base_scraper.py`
2. Compare com `scrapers/vivareal_scraper.py` e `scrapers/olx_scraper.py`
3. Leia os comentários no código
4. Tente criar seu próprio scraper

#### 📊 **Fazer análise de dados**
1. Abra `notebooks/exploracao_dados.ipynb` no Jupyter
2. Estude `analysis/analise_mercado.py`
3. Veja exemplos em **EXAMPLES.md**
4. Adapte para suas necessidades

#### 🎓 **Usar em TCC/Pesquisa**
1. Leia **OVERVIEW.md** para contexto teórico
2. Use **EXAMPLES.md** caso 1 (Estudante de Geografia)
3. Cite o projeto e a pesquisa original da UNESP
4. Adapte as análises para sua cidade/região

## 📋 Arquivos de Código Principais

### Scrapers (Coleta)
| Arquivo | Descrição | Quando usar |
|---------|-----------|-------------|
| `base_scraper.py` | Classe abstrata com lógica comum | Para criar novos scrapers |
| `vivareal_scraper.py` | Scraper do VivaReal | Executado automaticamente |
| `olx_scraper.py` | Scraper da OLX | Executado automaticamente |
| `run_all.py` | Executa todos os scrapers | **Comando principal de coleta** |

### Utilitários
| Arquivo | Descrição | Funções principais |
|---------|-----------|-------------------|
| `helpers.py` | Funções auxiliares | `limpar_preco()`, `limpar_area()`, `calcular_preco_m2()` |
| `config.py` | Configurações globais | CIDADE, HEADERS, REQUEST_DELAY |

### Análise
| Arquivo | Descrição | Quando usar |
|---------|-----------|-------------|
| `analise_mercado.py` | Análise completa | **Comando principal de análise** |
| `exploracao_dados.ipynb` | Notebook interativo | Para exploração visual |

## 🎨 Arquivos de Configuração

| Arquivo | Propósito | Obrigatório? |
|---------|-----------|--------------|
| `.env.example` | Template de variáveis de ambiente | Não (copiar para `.env` se necessário) |
| `.gitignore` | Arquivos a ignorar no Git | Sim (se usar Git) |
| `requirements.txt` | Dependências Python | **Sim** |

## 🔄 Fluxo de Trabalho Típico

```
1. INSTALAÇÃO
   pip install -r requirements.txt
   ↓
2. VERIFICAÇÃO
   python test_setup.py
   ↓
3. COLETA
   python scrapers/run_all.py
   ↓
   Dados salvos em: data/raw/
   ↓
4. ANÁLISE
   python analysis/analise_mercado.py --relatorio-completo
   ↓
   Resultados em: data/processed/
   ↓
5. EXPLORAÇÃO
   jupyter notebook notebooks/exploracao_dados.ipynb
```

## 📞 Ajuda e Suporte

### Problemas Comuns

| Problema | Solução |
|----------|---------|
| Módulos não encontrados | `pip install -r requirements.txt` |
| Nenhum dado coletado | Sites mudaram estrutura - veja QUICKSTART.md |
| Timeout nas requisições | Aumente TIMEOUT em config.py |
| Erro de permissão | `chmod -R 755 data/` (Linux/Mac) |

### Recursos Adicionais

- 📄 **QUICKSTART.md** → Seção "Solução de Problemas"
- 🐛 GitHub Issues (se aplicável)
- 📧 Contato do desenvolvedor

## 🔗 Links Importantes

- [Artigo Original - Jornal UNESP](https://jornal.unesp.br/2026/01/28/pesquisadores-da-unesp-investigam-efeitos-da-crescente-influencia-do-capital-financeiro-sobre-a-producao-de-moradias-no-brasil/)
- [Beautiful Soup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas Docs](https://pandas.pydata.org/docs/)

## 🏆 Créditos

**Inspirado pela pesquisa do Prof. Everaldo Melazzo**  
GAsPERR - Grupo de Pesquisa Produção do Espaço e Redefinições Regionais  
UNESP - Universidade Estadual Paulista  
Câmpus de Presidente Prudente

---

## ✅ Checklist de Primeiro Uso

- [ ] Li README.md
- [ ] Li QUICKSTART.md  
- [ ] Instalei dependências: `pip install -r requirements.txt`
- [ ] Testei setup: `python test_setup.py`
- [ ] Executei primeira coleta: `python scrapers/run_all.py`
- [ ] Gerei análises: `python analysis/analise_mercado.py --relatorio-completo`
- [ ] Explorei notebook: `jupyter notebook notebooks/exploracao_dados.ipynb`
- [ ] Li EXAMPLES.md para casos de uso avançados

---

**Versão**: 0.1.0  
**Última atualização**: Janeiro 2026
