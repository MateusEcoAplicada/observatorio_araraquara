"""
Script de teste rápido para verificar se tudo está funcionando
"""

import sys
import os

# Adicionar path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.helpers import (
    limpar_preco, 
    limpar_area, 
    extrair_numero,
    normalizar_bairro,
    calcular_preco_m2
)


def testar_funcoes_auxiliares():
    """
    Testa funções auxiliares
    """
    print("="*60)
    print("TESTANDO FUNÇÕES AUXILIARES")
    print("="*60)
    
    # Teste 1: Limpeza de preço
    print("\n1. Teste de limpeza de preço:")
    testes_preco = [
        "R$ 450.000",
        "R$ 1.500.000,00",
        "450000",
        "450.000,00",
        "Sob consulta"
    ]
    
    for teste in testes_preco:
        resultado = limpar_preco(teste)
        print(f"  '{teste}' → {resultado}")
    
    # Teste 2: Limpeza de área
    print("\n2. Teste de limpeza de área:")
    testes_area = [
        "85 m²",
        "85m2",
        "120 metros quadrados",
        "65.5 m²"
    ]
    
    for teste in testes_area:
        resultado = limpar_area(teste)
        print(f"  '{teste}' → {resultado}")
    
    # Teste 3: Extração de número
    print("\n3. Teste de extração de número:")
    testes_numero = [
        "3 quartos",
        "2 banheiros",
        "1 vaga"
    ]
    
    for teste in testes_numero:
        resultado = extrair_numero(teste)
        print(f"  '{teste}' → {resultado}")
    
    # Teste 4: Normalização de bairro
    print("\n4. Teste de normalização de bairro:")
    testes_bairro = [
        "jardim américa",
        "CENTRO",
        "Vila  Harmonia  "
    ]
    
    for teste in testes_bairro:
        resultado = normalizar_bairro(teste)
        print(f"  '{teste}' → '{resultado}'")
    
    # Teste 5: Cálculo de preço/m²
    print("\n5. Teste de cálculo de preço/m²:")
    print(f"  R$ 450.000 / 85 m² → R$ {calcular_preco_m2(450000, 85)}/m²")
    print(f"  R$ 1.200.000 / 150 m² → R$ {calcular_preco_m2(1200000, 150)}/m²")
    
    print("\n" + "="*60)
    print("TODOS OS TESTES CONCLUÍDOS!")
    print("="*60)


def verificar_estrutura():
    """
    Verifica se a estrutura de diretórios está correta
    """
    print("\n" + "="*60)
    print("VERIFICANDO ESTRUTURA DO PROJETO")
    print("="*60)
    
    from pathlib import Path
    
    base_dir = Path(__file__).parent
    diretorios_esperados = [
        'scrapers',
        'data',
        'data/raw',
        'data/processed',
        'analysis',
        'notebooks',
        'utils'
    ]
    
    print("\nDiretórios:")
    for dir_name in diretorios_esperados:
        dir_path = base_dir / dir_name
        existe = "✓" if dir_path.exists() else "✗"
        print(f"  {existe} {dir_name}")
    
    arquivos_esperados = [
        'README.md',
        'requirements.txt',
        'config.py',
        'QUICKSTART.md'
    ]
    
    print("\nArquivos principais:")
    for file_name in arquivos_esperados:
        file_path = base_dir / file_name
        existe = "✓" if file_path.exists() else "✗"
        print(f"  {existe} {file_name}")
    
    print("\n" + "="*60)


def main():
    """
    Executa todos os testes
    """
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "OBSERVATÓRIO ARARAQUARA" + " "*20 + "║")
    print("║" + " "*20 + "Teste Rápido" + " "*25 + "║")
    print("╚" + "="*58 + "╝")
    
    verificar_estrutura()
    testar_funcoes_auxiliares()
    
    print("\n")
    print("Próximos passos:")
    print("  1. Instalar dependências: pip install -r requirements.txt")
    print("  2. Coletar dados: python scrapers/run_all.py")
    print("  3. Analisar dados: python analysis/analise_mercado.py --relatorio-completo")
    print("  4. Ver QUICKSTART.md para mais informações")
    print("\n")


if __name__ == "__main__":
    main()
