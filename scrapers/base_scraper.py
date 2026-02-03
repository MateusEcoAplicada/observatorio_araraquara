"""
Classe base abstrata para scrapers de imóveis
"""

import logging
import requests
import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup
import sys
import os

# Adicionar path do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import HEADERS, REQUEST_DELAY, MAX_RETRIES, TIMEOUT
from utils.helpers import (
    delay_request, timestamp_agora, validar_dados_imovel,
    gerar_id_unico, logger
)

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Classe base para todos os scrapers
    """
    
    def __init__(self, cidade: str = "Araraquara", estado: str = "SP"):
        self.cidade = cidade
        self.estado = estado
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.imoveis = []
        
    @abstractmethod
    def construir_url(self, tipo_imovel: str, tipo_transacao: str, pagina: int = 1) -> str:
        """
        Constrói URL de busca
        
        Args:
            tipo_imovel: Tipo do imóvel (casa, apartamento, etc)
            tipo_transacao: venda ou aluguel
            pagina: Número da página
            
        Returns:
            URL completa
        """
        pass
    
    @abstractmethod
    def extrair_dados_pagina(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        """
        Extrai dados dos imóveis de uma página
        
        Args:
            soup: BeautifulSoup da página
            url: URL da página
            
        Returns:
            Lista de dicionários com dados dos imóveis
        """
        pass
    
    @abstractmethod
    def get_fonte_nome(self) -> str:
        """
        Retorna nome da fonte (site)
        """
        pass
    
    def fazer_requisicao(self, url: str, tentativa: int = 1) -> Optional[requests.Response]:
        """
        Faz requisição HTTP com retry
        
        Args:
            url: URL para requisição
            tentativa: Número da tentativa atual
            
        Returns:
            Response ou None se falhar
        """
        try:
            logger.info(f"Requisitando: {url}")
            response = self.session.get(url, timeout=TIMEOUT)
            
            if response.status_code == 200:
                delay_request(REQUEST_DELAY)
                return response
            
            elif response.status_code == 429:  # Too Many Requests
                logger.warning(f"Rate limit atingido. Aguardando...")
                delay_request(REQUEST_DELAY * 3)
                if tentativa < MAX_RETRIES:
                    return self.fazer_requisicao(url, tentativa + 1)
            
            else:
                logger.error(f"Status {response.status_code} para {url}")
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout na requisição: {url}")
            if tentativa < MAX_RETRIES:
                delay_request(REQUEST_DELAY)
                return self.fazer_requisicao(url, tentativa + 1)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            
        return None
    
    def processar_imovel(self, dados_brutos: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Processa e padroniza dados de um imóvel
        
        Args:
            dados_brutos: Dados extraídos do site
            
        Returns:
            Dados processados ou None se inválido
        """
        # Adicionar metadados
        dados_brutos['fonte'] = self.get_fonte_nome()
        dados_brutos['data_coleta'] = timestamp_agora()
        dados_brutos['cidade'] = self.cidade
        dados_brutos['estado'] = self.estado
        
        # Gerar ID único
        if 'url' in dados_brutos:
            dados_brutos['id_anuncio'] = gerar_id_unico(
                dados_brutos['url'], 
                self.get_fonte_nome()
            )
        
        # Validar
        if validar_dados_imovel(dados_brutos):
            return dados_brutos
        
        return None
    
    def coletar(self, tipo_imovel: str, tipo_transacao: str, max_paginas: int = 10) -> List[Dict[str, Any]]:
        """
        Coleta dados de imóveis
        
        Args:
            tipo_imovel: Tipo do imóvel
            tipo_transacao: venda ou aluguel
            max_paginas: Número máximo de páginas a coletar
            
        Returns:
            Lista de imóveis coletados
        """
        logger.info(f"Iniciando coleta: {tipo_imovel} - {tipo_transacao}")
        imoveis_coletados = []
        
        for pagina in range(1, max_paginas + 1):
            try:
                url = self.construir_url(tipo_imovel, tipo_transacao, pagina)
                response = self.fazer_requisicao(url)
                
                if not response:
                    logger.warning(f"Falha na página {pagina}, encerrando coleta")
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                imoveis_pagina = self.extrair_dados_pagina(soup, url)
                
                if not imoveis_pagina:
                    logger.info(f"Nenhum imóvel encontrado na página {pagina}, encerrando")
                    break
                
                # Processar e validar cada imóvel
                for imovel_bruto in imoveis_pagina:
                    imovel_processado = self.processar_imovel(imovel_bruto)
                    if imovel_processado:
                        imoveis_coletados.append(imovel_processado)
                
                logger.info(f"Página {pagina}: {len(imoveis_pagina)} imóveis coletados")
                
            except Exception as e:
                logger.error(f"Erro ao processar página {pagina}: {e}")
                continue
        
        logger.info(f"Coleta finalizada: {len(imoveis_coletados)} imóveis no total")
        self.imoveis.extend(imoveis_coletados)
        return imoveis_coletados
    
    def salvar_dados(self, formato: str = 'csv', nome_arquivo: str = None) -> str:
        """
        Salva dados coletados
        
        Args:
            formato: csv, json ou excel
            nome_arquivo: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not self.imoveis:
            logger.warning("Nenhum dado para salvar")
            return None
        
        df = pd.DataFrame(self.imoveis)
        
        if not nome_arquivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo = f"{self.get_fonte_nome()}_{self.cidade}_{timestamp}"
        
        # Determinar caminho
        from pathlib import Path
        data_dir = Path(__file__).parent.parent / 'data' / 'raw'
        data_dir.mkdir(parents=True, exist_ok=True)
        
        if formato == 'csv':
            filepath = data_dir / f"{nome_arquivo}.csv"
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
        elif formato == 'json':
            filepath = data_dir / f"{nome_arquivo}.json"
            df.to_json(filepath, orient='records', force_ascii=False, indent=2)
        elif formato == 'excel':
            filepath = data_dir / f"{nome_arquivo}.xlsx"
            df.to_excel(filepath, index=False)
        else:
            raise ValueError(f"Formato inválido: {formato}")
        
        logger.info(f"Dados salvos em: {filepath}")
        return str(filepath)
    
    def get_resumo(self) -> Dict[str, Any]:
        """
        Retorna resumo dos dados coletados
        """
        if not self.imoveis:
            return {"total": 0}
        
        df = pd.DataFrame(self.imoveis)
        
        return {
            "total": len(df),
            "fonte": self.get_fonte_nome(),
            "cidade": self.cidade,
            "tipos_imovel": df['tipo_imovel'].value_counts().to_dict() if 'tipo_imovel' in df else {},
            "tipos_transacao": df['tipo_transacao'].value_counts().to_dict() if 'tipo_transacao' in df else {},
            "preco_medio": df['preco'].mean() if 'preco' in df else None,
            "preco_min": df['preco'].min() if 'preco' in df else None,
            "preco_max": df['preco'].max() if 'preco' in df else None,
        }
