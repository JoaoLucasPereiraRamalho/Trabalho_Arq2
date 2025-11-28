from src.hardware import CPU
from src.common.constantes import Opcode

def criar_instrucao_alu(opcode, rc, ra, rb):
    instrucao = (opcode.value << 24) | (ra << 16) | (rb << 8) | (rc)
    return instrucao

def criar_instrucao_lcl(opcode, rc, constante):
    instrucao = (opcode.value << 24) | (constante << 8) | (rc)
    return instrucao

def main():
    print("=== Iniciando Teste Manual do UFLA-RISC ===\n")
    
    cpu = CPU()
    
    programa = [
        criar_instrucao_lcl(Opcode.LCL_LOW, rc=1, constante=10),
        
        criar_instrucao_lcl(Opcode.LCL_LOW, rc=2, constante=20),
        
        criar_instrucao_alu(Opcode.ADD, rc=3, ra=1, rb=2),
        
        0xFFFFFFFF
    ]
    
    print(f"Programa Binário Gerado: {[hex(x) for x in programa]}")
    
    cpu.carregar_programa(programa)
    
    print("\n--- Execução ---")
    while cpu.running:
        cpu.executar_ciclo()

    valor_r3 = cpu.reg.ler(3)
    print("\n--- Resultado Final ---")
    print(f"Valor em R3: {valor_r3} (Esperado: 30)")
    
    if valor_r3 == 30:
        print("✅ SUCESSO: O hardware básico está funcionando!")
    else:
        print("❌ FALHA: O resultado não bateu.")

if __name__ == "__main__":
    main()