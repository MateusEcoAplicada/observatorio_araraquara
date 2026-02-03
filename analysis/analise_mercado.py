"""
Módulo de análise de dados imobiliários
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import os

# Adicionar path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATA_DIR, PROCESSED_DATA_DIR
from utils.helpers import calcular_preco_m2

# Configurar visualizações
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class AnalisadorMercadoImobiliario:
    """
    Classe para análise de dados do mercado imobiliário
    """
    
    def __init__(self, dados_path: str = None):
        """
        Inicializa analisador
        
        Args:
            dados_path: Caminho para arquivo CSV com dados
        """
        self.df = None
        self.df_limpo = None
        
        if dados_path:
            self.carregar_dados(dados_path)
    
    def carregar_dados(self, path: str):
        """
        Carrega dados de arquivo
        """
        print(f"Carregando dados de: {path}")
        self.df = pd.read_csv(path)
        print(f"Total de registros: {len(self.df)}")
        print(f"Colunas: {list(self.df.columns)}")
        
        return self.df
    
    def limpar_dados(self):
        """
        Limpa e prepara dados para análise
        """
        print("\nLimpando dados...")
        df = self.df.copy()
        
        # Remover duplicatas
        registros_antes = len(df)
        df = df.drop_duplicates(subset=['id_anuncio'], keep='first')
        print(f"Duplicatas removidas: {registros_antes - len(df)}")
        
        # Remover valores nulos em colunas críticas
        df = df.dropna(subset=['preco'])
        
        # Converter tipos
        if 'preco' in df.columns:
            df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
        if 'area' in df.columns:
            df['area'] = pd.to_numeric(df['area'], errors='coerce')
        
        # Calcular preço por m²
        if 'preco' in df.columns and 'area' in df.columns:
            df['preco_m2'] = df.apply(
                lambda row: calcular_preco_m2(row['preco'], row['area']),
                axis=1
            )
        
        # Remover outliers extremos (opcional)
        if 'preco' in df.columns:
            Q1 = df['preco'].quantile(0.01)
            Q3 = df['preco'].quantile(0.99)
            antes = len(df)
            df = df[(df['preco'] >= Q1) & (df['preco'] <= Q3)]
            print(f"Outliers removidos: {antes - len(df)}")
        
        self.df_limpo = df
        print(f"Registros após limpeza: {len(df)}")
        
        return df
    
    def estatisticas_descritivas(self):
        """
        Gera estatísticas descritivas
        """
        if self.df_limpo is None:
            print("Execute limpar_dados() primeiro")
            return
        
        df = self.df_limpo
        
        print("\n" + "="*60)
        print("ESTATÍSTICAS DESCRITIVAS")
        print("="*60)
        
        # Estatísticas de preço
        if 'preco' in df.columns:
            print("\nPreços:")
            print(f"  Média: R$ {df['preco'].mean():,.2f}")
            print(f"  Mediana: R$ {df['preco'].median():,.2f}")
            print(f"  Mínimo: R$ {df['preco'].min():,.2f}")
            print(f"  Máximo: R$ {df['preco'].max():,.2f}")
            print(f"  Desvio padrão: R$ {df['preco'].std():,.2f}")
            
            # Amplitude (desigualdade)
            amplitude = df['preco'].max() / df['preco'].min()
            print(f"  Amplitude (max/min): {amplitude:.2f}x")
        
        # Estatísticas por tipo de imóvel
        if 'tipo_imovel' in df.columns:
            print("\nDistribuição por tipo de imóvel:")
            contagem = df['tipo_imovel'].value_counts()
            for tipo, qtd in contagem.items():
                pct = (qtd / len(df)) * 100
                print(f"  {tipo}: {qtd} ({pct:.1f}%)")
        
        # Estatísticas por tipo de transação
        if 'tipo_transacao' in df.columns:
            print("\nDistribuição por tipo de transação:")
            contagem = df['tipo_transacao'].value_counts()
            for tipo, qtd in contagem.items():
                pct = (qtd / len(df)) * 100
                print(f"  {tipo}: {qtd} ({pct:.1f}%)")
        
        # Top 10 bairros
        if 'bairro' in df.columns:
            print("\nTop 10 bairros com mais anúncios:")
            top_bairros = df['bairro'].value_counts().head(10)
            for bairro, qtd in top_bairros.items():
                if pd.notna(bairro):
                    print(f"  {bairro}: {qtd}")
        
        return df.describe()
    
    def analisar_por_bairro(self):
        """
        Analisa preços por bairro
        """
        if self.df_limpo is None:
            print("Execute limpar_dados() primeiro")
            return
        
        df = self.df_limpo
        
        if 'bairro' not in df.columns or 'preco' not in df.columns:
            print("Dados insuficientes para análise por bairro")
            return
        
        # Agrupar por bairro
        analise_bairro = df.groupby('bairro').agg({
            'preco': ['count', 'mean', 'median', 'min', 'max'],
            'area': 'mean',
            'preco_m2': 'mean'
        }).round(2)
        
        analise_bairro.columns = [
            'Qtd_Anuncios', 'Preco_Medio', 'Preco_Mediano',
            'Preco_Min', 'Preco_Max', 'Area_Media', 'Preco_M2_Medio'
        ]
        
        # Ordenar por quantidade de anúncios
        analise_bairro = analise_bairro.sort_values('Qtd_Anuncios', ascending=False)
        
        # Calcular amplitude por bairro
        analise_bairro['Amplitude'] = (
            analise_bairro['Preco_Max'] / analise_bairro['Preco_Min']
        ).round(2)
        
        print("\n" + "="*60)
        print("ANÁLISE POR BAIRRO (Top 15)")
        print("="*60)
        print(analise_bairro.head(15))
        
        # Salvar
        output_path = PROCESSED_DATA_DIR / 'analise_por_bairro.csv'
        analise_bairro.to_csv(output_path)
        print(f"\nAnálise salva em: {output_path}")
        
        return analise_bairro
    
    def visualizar_distribuicao_precos(self, salvar: bool = True):
        """
        Cria visualização da distribuição de preços
        """
        if self.df_limpo is None:
            print("Execute limpar_dados() primeiro")
            return
        
        df = self.df_limpo
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Distribuição de Preços - Araraquara', fontsize=16, fontweight='bold')
        
        # Histograma
        axes[0, 0].hist(df['preco'], bins=50, edgecolor='black', alpha=0.7)
        axes[0, 0].set_xlabel('Preço (R$)')
        axes[0, 0].set_ylabel('Frequência')
        axes[0, 0].set_title('Histograma de Preços')
        axes[0, 0].ticklabel_format(style='plain', axis='x')
        
        # Boxplot
        axes[0, 1].boxplot(df['preco'].dropna())
        axes[0, 1].set_ylabel('Preço (R$)')
        axes[0, 1].set_title('Boxplot de Preços')
        axes[0, 1].ticklabel_format(style='plain', axis='y')
        
        # Distribuição por tipo de imóvel
        if 'tipo_imovel' in df.columns:
            tipo_counts = df['tipo_imovel'].value_counts()
            axes[1, 0].bar(range(len(tipo_counts)), tipo_counts.values)
            axes[1, 0].set_xticks(range(len(tipo_counts)))
            axes[1, 0].set_xticklabels(tipo_counts.index, rotation=45, ha='right')
            axes[1, 0].set_ylabel('Quantidade')
            axes[1, 0].set_title('Distribuição por Tipo de Imóvel')
        
        # Preço médio por tipo de imóvel
        if 'tipo_imovel' in df.columns:
            preco_por_tipo = df.groupby('tipo_imovel')['preco'].mean().sort_values()
            axes[1, 1].barh(range(len(preco_por_tipo)), preco_por_tipo.values)
            axes[1, 1].set_yticks(range(len(preco_por_tipo)))
            axes[1, 1].set_yticklabels(preco_por_tipo.index)
            axes[1, 1].set_xlabel('Preço Médio (R$)')
            axes[1, 1].set_title('Preço Médio por Tipo de Imóvel')
            axes[1, 1].ticklabel_format(style='plain', axis='x')
        
        plt.tight_layout()
        
        if salvar:
            output_path = PROCESSED_DATA_DIR / 'distribuicao_precos.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Visualização salva em: {output_path}")
        
        plt.show()
    
    def visualizar_precos_por_bairro(self, top_n: int = 15, salvar: bool = True):
        """
        Visualiza preços por bairro
        """
        if self.df_limpo is None:
            print("Execute limpar_dados() primeiro")
            return
        
        df = self.df_limpo
        
        if 'bairro' not in df.columns:
            print("Coluna 'bairro' não encontrada")
            return
        
        # Top N bairros por quantidade de anúncios
        top_bairros = df['bairro'].value_counts().head(top_n).index
        df_top = df[df['bairro'].isin(top_bairros)]
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle(f'Preços por Bairro - Top {top_n} Bairros', fontsize=16, fontweight='bold')
        
        # Boxplot
        df_top.boxplot(column='preco', by='bairro', ax=axes[0], rot=90)
        axes[0].set_xlabel('Bairro')
        axes[0].set_ylabel('Preço (R$)')
        axes[0].set_title('Distribuição de Preços por Bairro')
        axes[0].get_figure().suptitle('')  # Remove título duplicado
        
        # Preço médio por bairro
        preco_medio_bairro = df_top.groupby('bairro')['preco'].mean().sort_values()
        axes[1].barh(range(len(preco_medio_bairro)), preco_medio_bairro.values)
        axes[1].set_yticks(range(len(preco_medio_bairro)))
        axes[1].set_yticklabels(preco_medio_bairro.index)
        axes[1].set_xlabel('Preço Médio (R$)')
        axes[1].set_title('Preço Médio por Bairro')
        axes[1].ticklabel_format(style='plain', axis='x')
        
        plt.tight_layout()
        
        if salvar:
            output_path = PROCESSED_DATA_DIR / 'precos_por_bairro.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Visualização salva em: {output_path}")
        
        plt.show()
    
    def gerar_relatorio_completo(self, salvar_figuras: bool = True):
        """
        Gera relatório completo de análise
        """
        print("\n" + "="*60)
        print("GERANDO RELATÓRIO COMPLETO")
        print("="*60)
        
        # 1. Limpar dados
        self.limpar_dados()
        
        # 2. Estatísticas descritivas
        self.estatisticas_descritivas()
        
        # 3. Análise por bairro
        self.analisar_por_bairro()
        
        # 4. Visualizações
        self.visualizar_distribuicao_precos(salvar=salvar_figuras)
        self.visualizar_precos_por_bairro(salvar=salvar_figuras)
        
        print("\n" + "="*60)
        print("RELATÓRIO COMPLETO GERADO")
        print("="*60)


def main():
    """
    Executa análise dos dados coletados
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Análise de dados imobiliários')
    parser.add_argument('--arquivo', help='Caminho para arquivo CSV')
    parser.add_argument('--relatorio-completo', action='store_true', help='Gerar relatório completo')
    
    args = parser.parse_args()
    
    # Verificar se há arquivo
    if args.arquivo:
        dados_path = args.arquivo
    else:
        # Buscar arquivo mais recente na pasta data/raw
        raw_dir = Path(__file__).parent.parent / 'data' / 'raw'
        arquivos_csv = list(raw_dir.glob('*.csv'))
        
        if not arquivos_csv:
            print("Nenhum arquivo CSV encontrado em data/raw/")
            print("Execute primeiro: python scrapers/run_all.py")
            return
        
        # Pegar arquivo mais recente
        dados_path = max(arquivos_csv, key=lambda p: p.stat().st_mtime)
        print(f"Usando arquivo mais recente: {dados_path.name}")
    
    # Criar analisador
    analisador = AnalisadorMercadoImobiliario(dados_path)
    
    if args.relatorio_completo:
        analisador.gerar_relatorio_completo()
    else:
        analisador.limpar_dados()
        analisador.estatisticas_descritivas()


if __name__ == "__main__":
    main()
