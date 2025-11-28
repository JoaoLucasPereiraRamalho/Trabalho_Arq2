import sys
import os

diretorio_testes = os.path.dirname(os.path.abspath(__file__))
diretorio_raiz = os.path.dirname(diretorio_testes)
sys.path.append(diretorio_raiz)

from src.assembler import Assembler

def main():
    print(">>> Iniciando Teste de Montagem...")
    asm = Assembler()
    
    arquivo_entrada = os.path.join(diretorio_testes, "exemplo.asm")
    arquivo_saida = os.path.join(diretorio_testes, "exemplo.bin")
    
    print(f"Lendo arquivo: {arquivo_entrada}")
    
    try:
        asm.montar(arquivo_entrada, arquivo_saida)
        
        if os.path.exists(arquivo_saida):
            print(f"Sucesso! Arquivo criado em: {arquivo_saida}")
            print("\n--- Conteúdo Binário Gerado ---")
            with open(arquivo_saida, 'r') as f:
                print(f.read())
        else:
            print("Erro: O arquivo binário não foi criado.")
            
    except Exception as e:
        print(f"Erro Crítico: {e}")

if __name__ == "__main__":
    main()