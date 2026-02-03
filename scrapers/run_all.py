"""
Script para executar todos os scrapers
"""

import sys
import os
import argparse
import logging
from datetime import datetime

# Adicionar path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TIPOS_IMOVEIS, TIPOS_TRANSACAO
from scrapers.vivareal_scraper import VivaRealScraper
from scrapers.olx_scraper import OLXScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def executar_coleta_completa(
    cidade: str = "Araraquara",
    tipos_imovel: list = None,
    tipos_transacao: list = None,
    max_paginas: int = 10,
    sites: list = None
):
    """
    Executa coleta completa de dados
    
    Args:
        cidade: Cidade para busca
        tipos_imovel: Lista de tipos de imóvel
        tipos_transacao: Lista de tipos de transação
        max_paginas: Máximo de páginas por busca
        sites: Lista de sites a coletar
    """
    
    # Valores padrão
    if tipos_imovel is None:
        tipos_imovel = ['apartamento', 'casa']
    if tipos_transacao is None:
        tipos_transacao = ['venda', 'aluguel']
    if sites is None:
        sites = ['vivareal', 'olx']
    
    # Mapear scrapers
    scrapers_disponiveis = {
        'vivareal': VivaRealScraper,
        'olx': OLXScraper,
        # Adicionar mais conforme implementados
    }
    
    resultados = []
    timestamp_inicio = datetime.now()
    
    logger.info("="*60)
    logger.info("INICIANDO COLETA COMPLETA")
    logger.info(f"Cidade: {cidade}")
    logger.info(f"Sites: {', '.join(sites)}")
    logger.info(f"Tipos de imóvel: {', '.join(tipos_imovel)}")
    logger.info(f"Tipos de transação: {', '.join(tipos_transacao)}")
    logger.info("="*60)
    
    # Iterar sobre cada combinação
    for site_nome in sites:
        if site_nome not in scrapers_disponiveis:
            logger.warning(f"Scraper '{site_nome}' não disponível")
            continue
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Site: {site_nome.upper()}")
        logger.info(f"{'='*60}")
        
        ScraperClass = scrapers_disponiveis[site_nome]
        scraper = ScraperClass(cidade=cidade)
        
        for tipo_imovel in tipos_imovel:
            for tipo_transacao in tipos_transacao:
                logger.info(f"\nColetando: {tipo_imovel} - {tipo_transacao}")
                
                try:
                    imoveis = scraper.coletar(
                        tipo_imovel=tipo_imovel,
                        tipo_transacao=tipo_transacao,
                        max_paginas=max_paginas
                    )
                    
                    logger.info(f"✓ {len(imoveis)} imóveis coletados")
                    
                except Exception as e:
                    logger.error(f"✗ Erro na coleta: {e}")
                    continue
        
        # Salvar dados do site
        try:
            arquivo = scraper.salvar_dados(formato='csv')
            logger.info(f"Dados salvos: {arquivo}")
            
            resumo = scraper.get_resumo()
            resultados.append({
                'site': site_nome,
                'total': resumo.get('total', 0),
                'arquivo': arquivo
            })
            
        except Exception as e:
            logger.error(f"Erro ao salvar dados: {e}")
    
    # Resumo final
    timestamp_fim = datetime.now()
    duracao = timestamp_fim - timestamp_inicio
    
    logger.info("\n" + "="*60)
    logger.info("COLETA FINALIZADA")
    logger.info("="*60)
    logger.info(f"Duração: {duracao}")
    logger.info(f"\nResumo por site:")
    
    total_geral = 0
    for resultado in resultados:
        logger.info(f"  {resultado['site']}: {resultado['total']} imóveis")
        total_geral += resultado['total']
    
    logger.info(f"\nTotal geral: {total_geral} imóveis")
    logger.info("="*60)
    
    return resultados


def main():
    parser = argparse.ArgumentParser(
        description='Executa coleta de dados imobiliários'
    )
    
    parser.add_argument(
        '--cidade',
        default='Araraquara',
        help='Cidade para busca'
    )
    
    parser.add_argument(
        '--tipos-imovel',
        nargs='+',
        default=['apartamento', 'casa'],
        choices=['apartamento', 'casa', 'casa_condominio', 'terreno', 'comercial'],
        help='Tipos de imóvel para coletar'
    )
    
    parser.add_argument(
        '--tipos-transacao',
        nargs='+',
        default=['venda', 'aluguel'],
        choices=['venda', 'aluguel'],
        help='Tipos de transação'
    )
    
    parser.add_argument(
        '--max-paginas',
        type=int,
        default=10,
        help='Máximo de páginas por busca'
    )
    
    parser.add_argument(
        '--sites',
        nargs='+',
        default=['vivareal', 'olx'],
        choices=['vivareal', 'olx', 'zapimoveis'],
        help='Sites para coletar'
    )
    
    args = parser.parse_args()
    
    executar_coleta_completa(
        cidade=args.cidade,
        tipos_imovel=args.tipos_imovel,
        tipos_transacao=args.tipos_transacao,
        max_paginas=args.max_paginas,
        sites=args.sites
    )


if __name__ == "__main__":
    main()
