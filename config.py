"""
Configurações gerais do Observatório Imobiliário de Araraquara
"""

import os
from pathlib import Path

# Diretórios do projeto
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
SCRAPERS_DIR = BASE_DIR / 'scrapers'
ANALYSIS_DIR = BASE_DIR / 'analysis'

# Criar diretórios se não existirem
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configurações de scraping
CIDADE = "Araraquara"
ESTADO = "SP"
UF = "SP"

# Rate limiting (respeitar servidores)
REQUEST_DELAY = 2  # segundos entre requisições
MAX_RETRIES = 3
TIMEOUT = 30

# Headers para requests (simular navegador)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Sites para scraping
SITES = {
    'vivareal': {
        'base_url': 'https://www.vivareal.com.br',
        'enabled': True
    },
    'zapimoveis': {
        'base_url': 'https://www.zapimoveis.com.br',
        'enabled': True
    },
    'olx': {
        'base_url': 'https://www.olx.com.br',
        'enabled': True
    }
}

# Tipos de imóveis
TIPOS_IMOVEIS = [
    'apartamento',
    'casa',
    'casa-em-condominio',
    'terreno',
    'comercial',
    'rural'
]

# Tipos de transação
TIPOS_TRANSACAO = ['venda', 'aluguel']

# Colunas esperadas nos dados
COLUNAS_PADRAO = [
    'id_anuncio',
    'titulo',
    'tipo_imovel',
    'tipo_transacao',
    'preco',
    'area',
    'quartos',
    'banheiros',
    'vagas',
    'endereco',
    'bairro',
    'cidade',
    'estado',
    'cep',
    'latitude',
    'longitude',
    'descricao',
    'url',
    'fonte',
    'data_coleta',
    'condominio',
    'iptu'
]

# Configurações de análise
BAIRROS_ARARAQUARA = [
    'Centro',
    'Jardim América',
    'Vila Harmonia',
    'Jardim Paulista',
    'Parque Pinheiros',
    'Vila Xavier',
    'Jardim Santa Lúcia',
    'Jardim das Hortênsias',
    'Vale do Sol',
    'Jardim Iguatemi',
    # Adicionar mais conforme necessário
]

# Database
DB_NAME = 'observatorio_araraquara.db'
DB_PATH = DATA_DIR / DB_NAME

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
