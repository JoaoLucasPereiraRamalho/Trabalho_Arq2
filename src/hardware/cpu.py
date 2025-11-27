class CPU:
    def __init__(self):
        self.pc = 0
        self.ir = 0
        self.reg = Registradores()
        self.mem = Memoria()
        self.alu = ALU()
        self.running = True

    def _fetch(self):
        """Estágio IF"""
        self.ir = self.mem.ler(self.pc)
        self.pc += 1

    def _decode(self):
        """Estágio ID"""
        self.opcode = (self.ir & MASK_OPCODE) >> 24
        self.ra_idx = (self.ir & MASK_RA) >> 16
        self.rb_idx = (self.ir & MASK_RB) >> 8
        self.rc_idx = (self.ir & MASK_RC)
        
        self.val_ra = self.reg.ler(self.ra_idx)
        self.val_rb = self.reg.ler(self.rb_idx)

    def _execute(self):
        if self.ir == 0xFFFFFFFF:
            self.running = False
            return

        if self.opcode == Opcode.BEQ.value:
            if self.val_ra == self.val_rb:
                self.pc = self.mem.ler(self.ir & 0xFFFF)

        
        else:
            self.resultado_alu = self.alu.executar(self.opcode, self.val_ra, self.val_rb)

    def _write_back(self):

        if precisa_escrever(self.opcode):
            self.reg.escrever(self.rc_idx, self.resultado_alu)

    def executar_ciclo(self):
        self._fetch()
        self._decode()
        self._execute()
        self._write_back()
        self.imprimir_estado()