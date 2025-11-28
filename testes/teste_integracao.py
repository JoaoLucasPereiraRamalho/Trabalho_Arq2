import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware import CPU
from src.common.constantes import Opcode

def criar_instrucao_alu(opcode, rc, ra, rb):
    return (opcode.value << 24) | (ra << 16) | (rb << 8) | (rc)

def criar_instrucao_lcl(opcode, rc, constante):
    return (opcode.value << 24) | (constante << 8) | (rc)

def main():
    print("=== Teste de Integração (Ciclo de Hardware) ===\n")
    cpu = CPU()
    

    programa = [
        criar_instrucao_lcl(Opcode.LCL_LOW, 1, 10),
        criar_instrucao_lcl(Opcode.LCL_LOW, 2, 20),
        criar_instrucao_alu(Opcode.ADD, 3, 1, 2),
        0xFFFFFFFF 
    ]
    
    cpu.carregar_programa(programa)
    
    while cpu.running:
        cpu.executar_ciclo()

    valor_r3 = cpu.reg.ler(3)
    print(f"\nResultado R3: {valor_r3} (Esperado: 30)")
    
    if valor_r3 == 30:
        print("✅ Integração Hardware: SUCESSO")
    else:
        print("❌ Integração Hardware: FALHA")

if __name__ == "__main__":
    main()