class ALU:
    def __init__(self):
        
        self.zero = False
        self.neg = False
        self.carry = False
        self.overflow = False

    def executar(self, opcode, ra_val, rb_val):

        resultado = 0

        if opcode in [Opcode.AND, Opcode.OR]:
            self.carry = False
            self.overflow = False

        if opcode == Opcode.ADD:
            res_temp = ra_val + rb_val
 
            resultado = res_temp & 0xFFFFFFFF
            
        elif opcode == Opcode.MULT:
            resultado = (ra_val * rb_val) & 0xFFFFFFFF
                 
        self._atualizar_flags_gerais(resultado)
        return resultado

    def _atualizar_flags_gerais(self, resultado):
        # Atualiza Zero e Neg [cite: 38]
        self.zero = (resultado == 0)
        self.neg = (resultado >> 31) == 1