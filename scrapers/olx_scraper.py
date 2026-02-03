"""
Scraper para OLX
"""

import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from base_scraper import BaseScraper
from utils.helpers import limpar_preco, limpar_area, extrair_numero, logger


class OLXScraper(BaseScraper):
    """
    Scraper específico para OLX
    """
    
    def get_fonte_nome(self) -> str:
        return "olx"
    
    def construir_url(self, tipo_imovel: str, tipo_transacao: str, pagina: int = 1) -> str:
        """
        Constrói URL da OLX
        
        Exemplo: https://sp.olx.com.br/araraquara-e-regiao/araraquara/imoveis
        """
        base = "https://sp.olx.com.br"
        
        # OLX não separa bem por tipo de transação nas categorias
        # Geralmente usa filtros
        
        # Normalizar tipo de imóvel
        imovel_map = {
            'apartamento': 'apartamentos',
            'casa': 'casas',
            'terreno': 'terrenos-sitios-e-fazendas',
            'comercial': 'comercial'
        }
        categoria = imovel_map.get(tipo_imovel.lower(), 'imoveis')
        
        # Construir URL
        cidade_formatada = self.cidade.lower().replace(' ', '-')
        
        url = f"{base}/araraquara-e-regiao/{cidade_formatada}/{categoria}"
        
        if pagina > 1:
            url += f"?o={pagina}"
        
        # Adicionar filtro de transação se for aluguel
        if tipo_transacao.lower() == 'aluguel':
            separador = '&' if '?' in url else '?'
            url += f"{separador}sf=1"  # sf=1 é filtro de aluguel
        
        return url
    
    def extrair_dados_pagina(self, soup: BeautifulSoup, url: str) -> List[Dict[str, Any]]:
        """
        Extrai dados dos anúncios da OLX
        """
        imoveis = []
        
        # OLX usa estrutura diferente - ajustar seletores
        anuncios = soup.find_all('li', {'data-ds-component': 'DS-AdCard'})
        
        if not anuncios:
            # Tentar seletor alternativo
            anuncios = soup.find_all('a', {'class': re.compile(r'.*olx-ad-card.*')})
        
        logger.info(f"Encontrados {len(anuncios)} anúncios na página")
        
        for anuncio in anuncios:
            try:
                imovel = self._extrair_dados_anuncio(anuncio)
                if imovel:
                    imoveis.append(imovel)
            except Exception as e:
                logger.warning(f"Erro ao extrair anúncio: {e}")
                continue
        
        return imoveis
    
    def _extrair_dados_anuncio(self, anuncio) -> Dict[str, Any]:
        """
        Extrai dados de um anúncio específico
        """
        dados = {}
        
        try:
            # Título
            titulo_elem = anuncio.find('h2')
            if not titulo_elem:
                titulo_elem = anuncio.find('span', {'class': re.compile(r'.*title.*')})
            if titulo_elem:
                dados['titulo'] = titulo_elem.get_text(strip=True)
            
            # Preço
            preco_elem = anuncio.find('span', {'class': re.compile(r'.*price.*')})
            if not preco_elem:
                preco_elem = anuncio.find('h3', {'class': re.compile(r'.*price.*')})
            if preco_elem:
                preco_text = preco_elem.get_text(strip=True)
                if 'grátis' not in preco_text.lower():
                    dados['preco'] = limpar_preco(preco_text)
            
            # Localização
            loc_elem = anuncio.find('span', {'class': re.compile(r'.*location.*')})
            if loc_elem:
                localizacao = loc_elem.get_text(strip=True)
                dados['endereco'] = localizacao
                
                # Tentar extrair bairro (geralmente vem antes da cidade)
                if ',' in localizacao:
                    partes = [p.strip() for p in localizacao.split(',')]
                    dados['bairro'] = partes[0] if partes else None
            
            # URL do anúncio
            if anuncio.name == 'a' and anuncio.get('href'):
                href = anuncio['href']
                if href.startswith('http'):
                    dados['url'] = href
                else:
                    dados['url'] = f"https://sp.olx.com.br{href}"
            else:
                link = anuncio.find('a', href=True)
                if link:
                    href = link['href']
                    if href.startswith('http'):
                        dados['url'] = href
                    else:
                        dados['url'] = f"https://sp.olx.com.br{href}"
            
            # Descrição curta (se disponível)
            desc_elem = anuncio.find('p', {'class': re.compile(r'.*description.*')})
            if desc_elem:
                dados['descricao'] = desc_elem.get_text(strip=True)[:500]
            
            # Características (tentar extrair da descrição ou título)
            texto_completo = (dados.get('titulo', '') + ' ' + dados.get('descricao', '')).lower()
            
            # Área
            match_area = re.search(r'(\d+)\s*m[²2]', texto_completo)
            if match_area:
                dados['area'] = float(match_area.group(1))
            
            # Quartos
            match_quartos = re.search(r'(\d+)\s*quarto', texto_completo)
            if match_quartos:
                dados['quartos'] = int(match_quartos.group(1))
            
            # Banheiros
            match_banheiros = re.search(r'(\d+)\s*banheiro', texto_completo)
            if match_banheiros:
                dados['banheiros'] = int(match_banheiros.group(1))
            
            # Vagas
            match_vagas = re.search(r'(\d+)\s*vaga', texto_completo)
            if match_vagas:
                dados['vagas'] = int(match_vagas.group(1))
            
            # Inferir tipo de imóvel
            if 'titulo' in dados:
                dados['tipo_imovel'] = self._inferir_tipo_imovel(dados['titulo'])
            
            return dados if dados.get('preco') else None
            
        except Exception as e:
            logger.warning(f"Erro ao extrair dados do anúncio: {e}")
            return None
    
    def _inferir_tipo_imovel(self, texto: str) -> str:
        """
        Infere tipo de imóvel a partir do texto
        """
        texto_lower = texto.lower()
        
        if 'apartamento' in texto_lower or 'apto' in texto_lower or 'ap ' in texto_lower:
            return 'apartamento'
        elif 'casa' in texto_lower:
            if 'condominio' in texto_lower or 'condomínio' in texto_lower:
                return 'casa_condominio'
            return 'casa'
        elif 'terreno' in texto_lower or 'lote' in texto_lower or 'área' in texto_lower:
            return 'terreno'
        elif any(x in texto_lower for x in ['comercial', 'sala', 'loja', 'ponto comercial', 'galpão']):
            return 'comercial'
        elif any(x in texto_lower for x in ['sítio', 'fazenda', 'chácara', 'rural']):
            return 'rural'
        
        return 'outro'


def main():
    """
    Função principal para teste
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Scraper OLX')
    parser.add_argument('--cidade', default='Araraquara', help='Cidade para busca')
    parser.add_argument('--tipo-imovel', default='apartamento', help='Tipo de imóvel')
    parser.add_argument('--tipo-transacao', default='venda', help='venda ou aluguel')
    parser.add_argument('--max-paginas', type=int, default=5, help='Máximo de páginas')
    
    args = parser.parse_args()
    
    scraper = OLXScraper(cidade=args.cidade)
    scraper.coletar(
        tipo_imovel=args.tipo_imovel,
        tipo_transacao=args.tipo_transacao,
        max_paginas=args.max_paginas
    )
    
    # Salvar dados
    scraper.salvar_dados(formato='csv')
    
    # Exibir resumo
    resumo = scraper.get_resumo()
    print("\n=== RESUMO DA COLETA ===")
    for chave, valor in resumo.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    main()
