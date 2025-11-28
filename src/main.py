import sys
import os
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.assembler import Assembler
from src.hardware import CPU

def main():
    parser = argparse.ArgumentParser(description="Simulador Funcional UFLA-RISC")
    parser.add_argument("arquivo", help="Caminho para o arquivo de entrada (.asm ou .bin)")
    args = parser.parse_args()

    arquivo_entrada = args.arquivo
    arquivo_binario = arquivo_entrada
    
    print(f"=== Simulador UFLA-RISC iniciada ===")
    print(f"Arquivo de entrada: {arquivo_entrada}")

    if arquivo_entrada.endswith('.asm'):
        print("\n[1/3] Detectado arquivo Assembly. Iniciando Montagem...")
        asm = Assembler()
        arquivo_binario = arquivo_entrada.replace('.asm', '.bin')
        
        try:
            asm.montar(arquivo_entrada, arquivo_binario)
            print(f"      Montagem concluída! Binário gerado: {arquivo_binario}")
        except Exception as e:
            print(f"❌ Erro na montagem: {e}")
            sys.exit(1)
    
    print("\n[2/3] Inicializando CPU e Memória...")
    cpu = CPU()
    
    try:
        with open(arquivo_binario, 'r') as f:
            endereco_atual = 0
            instrucoes_carregadas = 0
            
            for linha_num, linha in enumerate(f, 1):
                linha = linha.strip()
                if not linha: continue
                
                if linha.startswith('address'):
                    partes = linha.split()
                    if len(partes) > 1:
                        val_str = partes[1]
                        try:
                            if all(c in '01' for c in val_str) and len(val_str) > 1:
                                endereco_atual = int(val_str, 2)
                            else:
                                endereco_atual = int(val_str)
                        except ValueError:
                            print(f"      Aviso: Endereço inválido na linha {linha_num}")
                    continue
                
                try:
                    valor_instrucao = int(linha, 2)
                    cpu.mem.escrever(endereco_atual, valor_instrucao)
                    endereco_atual += 1
                    instrucoes_carregadas += 1
                except ValueError:
                    pass

        print(f"      {instrucoes_carregadas} instruções carregadas com sucesso.")

    except FileNotFoundError:
        print(f"❌ Erro: Arquivo {arquivo_binario} não encontrado.")
        sys.exit(1)

    print("\n[3/3] Executando Simulação...")
    print("-" * 40)
    
    try:
        while cpu.running:
            cpu.executar_ciclo()

    except KeyboardInterrupt:
        print("\n\n⚠️  Simulação interrompida pelo usuário.")
    
    print("-" * 40)
    print("=== Simulação Finalizada ===")

if __name__ == "__main__":
    main()