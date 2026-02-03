"""
Funções utilitárias para o projeto
"""

import re
import time
import logging
from datetime import datetime
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def limpar_preco(preco_str: str) -> Optional[float]:
    """
    Extrai valor numérico de string de preço
    
    Args:
        preco_str: String contendo preço (ex: "R$ 450.000")
        
    Returns:
        Valor float ou None se inválido
    """
    if not preco_str or preco_str == 'Sob consulta':
        return None
    
    try:
        # Remove tudo exceto números, pontos e vírgulas
        preco_limpo = re.sub(r'[^\d,.]', '', str(preco_str))
        
        # Trata formato brasileiro (vírgula como decimal)
        if ',' in preco_limpo and '.' in preco_limpo:
            # Ex: 1.500.000,00
            preco_limpo = preco_limpo.replace('.', '').replace(',', '.')
        elif ',' in preco_limpo:
            # Ex: 1500,00
            preco_limpo = preco_limpo.replace(',', '.')
        
        return float(preco_limpo)
    except (ValueError, AttributeError) as e:
        logger.warning(f"Erro ao limpar preço '{preco_str}': {e}")
        return None


def limpar_area(area_str: str) -> Optional[float]:
    """
    Extrai área em m² de string
    
    Args:
        area_str: String contendo área (ex: "85 m²", "85m2")
        
    Returns:
        Valor float ou None se inválido
    """
    if not area_str:
        return None
    
    try:
        # Extrai números
        area_limpa = re.sub(r'[^\d,.]', '', str(area_str))
        
        if ',' in area_limpa:
            area_limpa = area_limpa.replace(',', '.')
        
        area = float(area_limpa)
        
        # Validação básica (área razoável)
        if 10 <= area <= 10000:
            return area
        return None
    except (ValueError, AttributeError) as e:
        logger.warning(f"Erro ao limpar área '{area_str}': {e}")
        return None


def extrair_numero(texto: str) -> Optional[int]:
    """
    Extrai primeiro número inteiro de uma string
    
    Args:
        texto: String contendo número
        
    Returns:
        Inteiro ou None
    """
    if not texto:
        return None
    
    try:
        numeros = re.findall(r'\d+', str(texto))
        if numeros:
            return int(numeros[0])
        return None
    except (ValueError, AttributeError, IndexError):
        return None


def normalizar_bairro(bairro: str) -> str:
    """
    Normaliza nome de bairro (padroniza)
    
    Args:
        bairro: Nome do bairro
        
    Returns:
        Bairro normalizado
    """
    if not bairro:
        return ""
    
    # Capitaliza palavras
    bairro = bairro.title()
    
    # Remove espaços extras
    bairro = " ".join(bairro.split())
    
    return bairro


def normalizar_tipo_imovel(tipo: str) -> str:
    """
    Normaliza tipo de imóvel
    
    Args:
        tipo: Tipo do imóvel
        
    Returns:
        Tipo normalizado
    """
    if not tipo:
        return "Outro"
    
    tipo = tipo.lower().strip()
    
    # Mapeamento de variações
    mapeamento = {
        'apartamento': ['apartamento', 'apto', 'ap', 'flat', 'studio', 'kitnet'],
        'casa': ['casa', 'sobrado', 'moradia'],
        'casa_condominio': ['casa em condominio', 'casa condominio', 'condominio'],
        'terreno': ['terreno', 'lote', 'area'],
        'comercial': ['comercial', 'loja', 'sala', 'galpao', 'predio'],
        'rural': ['rural', 'fazenda', 'sitio', 'chacara']
    }
    
    for tipo_norm, variantes in mapeamento.items():
        if any(var in tipo for var in variantes):
            return tipo_norm
    
    return "outro"


def calcular_preco_m2(preco: float, area: float) -> Optional[float]:
    """
    Calcula preço por m²
    
    Args:
        preco: Preço total
        area: Área em m²
        
    Returns:
        Preço por m² ou None
    """
    if not preco or not area or area == 0:
        return None
    
    try:
        preco_m2 = preco / area
        # Validação básica
        if 0 < preco_m2 < 100000:
            return round(preco_m2, 2)
        return None
    except (ZeroDivisionError, TypeError):
        return None


def delay_request(seconds: int = 2):
    """
    Adiciona delay entre requests (rate limiting)
    
    Args:
        seconds: Segundos de delay
    """
    time.sleep(seconds)
    

def timestamp_agora() -> str:
    """
    Retorna timestamp atual formatado
    
    Returns:
        String com timestamp
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def validar_dados_imovel(dados: Dict[str, Any]) -> bool:
    """
    Valida se dados do imóvel estão minimamente completos
    
    Args:
        dados: Dicionário com dados do imóvel
        
    Returns:
        True se válido, False caso contrário
    """
    # Campos obrigatórios
    campos_obrigatorios = ['preco', 'tipo_imovel', 'cidade']
    
    for campo in campos_obrigatorios:
        if campo not in dados or not dados[campo]:
            logger.debug(f"Dados inválidos: campo '{campo}' ausente ou vazio")
            return False
    
    # Validações específicas
    if dados.get('preco', 0) <= 0:
        logger.debug("Dados inválidos: preço <= 0")
        return False
    
    return True


def gerar_id_unico(url: str, fonte: str) -> str:
    """
    Gera ID único para um anúncio
    
    Args:
        url: URL do anúncio
        fonte: Nome da fonte (site)
        
    Returns:
        ID único
    """
    import hashlib
    
    # Hash da URL + fonte
    texto = f"{fonte}_{url}"
    return hashlib.md5(texto.encode()).hexdigest()


def limpar_texto(texto: str, max_length: int = None) -> str:
    """
    Limpa e normaliza texto
    
    Args:
        texto: Texto a limpar
        max_length: Comprimento máximo (opcional)
        
    Returns:
        Texto limpo
    """
    if not texto:
        return ""
    
    # Remove espaços extras
    texto = " ".join(str(texto).split())
    
    # Trunca se necessário
    if max_length and len(texto) > max_length:
        texto = texto[:max_length] + "..."
    
    return texto.strip()
