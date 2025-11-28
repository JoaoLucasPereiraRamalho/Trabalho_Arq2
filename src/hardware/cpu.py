from src.hardware.memoria import Memoria
from src.hardware.registradores import Registradores
from src.hardware.alu import ALU
from src.common.constantes import Opcode, MASK_OPCODE, MASK_RA, MASK_RB, MASK_RC
from src.common.utils import to_unsigned

class CPU:
    def __init__(self):
        self.mem = Memoria()
        self.reg = Registradores()
        self.alu = ALU()

        self.pc = 0
        self.ir = 0 
        
        self.running = True
        
        self.opcode = 0
        self.ra_idx = 0
        self.rb_idx = 0
        self.rc_idx = 0
        self.const16 = 0
        self.imm24 = 0
        
        self.val_ra = 0
        self.val_rb = 0
        
        self.alu_out = 0
        self.mem_out = 0
        self.write_enable = False

    def carregar_programa(self, programa_binario):
        self.mem.carregar_programa(programa_binario)
        self.pc = 0
        self.running = True

    def executar_ciclo(self):
        if not self.running:
            return

        print(f"\n--- Ciclo PC: {self.pc} ---")
        
        self._fetch()
        self._decode()
        self._execute()
        self._write_back()
        
        self.imprimir_estado()

    def _fetch(self):
        """Estágio IF"""
        try:
            self.ir = self.mem.ler(self.pc)
            if self.ir == 0xFFFFFFFF:
                self.running = False
                print("HALT encontrado. Parando CPU.")
                return
            
            self.pc += 1
        except IndexError:
            print("Erro: PC fora dos limites da memória.")
            self.running = False

    def _decode(self):
        """Estágio ID"""
        if not self.running: return

        self.opcode = (self.ir & MASK_OPCODE) >> 24
        self.ra_idx = (self.ir & MASK_RA) >> 16
        self.rb_idx = (self.ir & MASK_RB) >> 8
        self.rc_idx = (self.ir & MASK_RC)
        
        self.const16 = (self.ir >> 8) & 0xFFFF
        
        self.imm24 = (self.ir & 0x00FFFFFF)

        self.val_ra = self.reg.ler(self.ra_idx)
        self.val_rb = self.reg.ler(self.rb_idx)
        
        self.write_enable = False

    def _execute(self):
        """Estágio EXE"""
        if not self.running: return

        try:
            op = Opcode(self.opcode)
        except ValueError:
            print(f"Opcode Desconhecido: {self.opcode}")
            return

        if op.value <= Opcode.COPY.value or op.value >= Opcode.MULT.value:
            self.alu_out = self.alu.executar(self.opcode, self.val_ra, self.val_rb)
            self.write_enable = True

        elif op == Opcode.LOAD:
            endereco = self.val_ra
            self.mem_out = self.mem.ler(endereco)
            self.write_enable = True
            
        elif op == Opcode.STORE:
            endereco = self.reg.ler(self.rc_idx)
            valor = self.val_ra
            self.mem.escrever(endereco, valor)
            self.write_enable = False

        elif op == Opcode.LCL_HIGH:
            val_rc_atual = self.reg.ler(self.rc_idx)
            self.alu_out = (self.const16 << 16) | (val_rc_atual & 0xFFFF)
            self.write_enable = True

        elif op == Opcode.LCL_LOW:
            val_rc_atual = self.reg.ler(self.rc_idx)
            self.alu_out = (val_rc_atual & 0xFFFF0000) | self.const16
            self.write_enable = True

        elif op == Opcode.JAL:
            self.reg.escrever(31, self.pc)
            self.pc = self.imm24
            
        elif op == Opcode.JR:
            val_rc = self.reg.ler(self.rc_idx)
            self.pc = val_rc
            
        elif op == Opcode.BEQ:
            dest = self.rc_idx 
            if self.val_ra == self.val_rb:
                self.pc = dest
                
        elif op == Opcode.BNE:
            dest = self.rc_idx
            if self.val_ra != self.val_rb:
                self.pc = dest
                
        elif op == Opcode.J:
            self.pc = self.imm24

    def _write_back(self):
        """Estágio WB"""
        if not self.running or not self.write_enable:
            return

        op = Opcode(self.opcode)

        if op == Opcode.LOAD:
            self.reg.escrever(self.rc_idx, self.mem_out)
            
        else:
            self.reg.escrever(self.rc_idx, self.alu_out)

    def imprimir_estado(self):
        print(f"Flags ULA: Z={int(self.alu.zero)} N={int(self.alu.neg)} "
              f"C={int(self.alu.carry)} V={int(self.alu.overflow)}")
        print(self.reg.dump_formatado())