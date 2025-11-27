from src.common.constantes import Opcode
from src.common.utils import to_signed, to_unsigned, get_bit

class ALU:
    def __init__(self):
        self.zero = False     
        self.neg = False       
        self.carry = False     
        self.overflow = False  

    def executar(self, opcode, val_ra, val_rb):

        s_ra = to_signed(val_ra)
        s_rb = to_signed(val_rb)
        
        resultado = 0
        
        op = None
        try:
            op = Opcode(opcode)
        except ValueError:
            return 0

        if op == Opcode.ADD:
            res_temp = s_ra + s_rb
            resultado = to_unsigned(res_temp)
            self._update_arithmetic_flags(s_ra, s_rb, res_temp, is_sub=False)

        elif op == Opcode.SUB:
            res_temp = s_ra - s_rb
            resultado = to_unsigned(res_temp)
            self._update_arithmetic_flags(s_ra, s_rb, res_temp, is_sub=True)

        elif op == Opcode.ZEROS:
            resultado = 0
            self._reset_flags(zero=True)

        elif op == Opcode.AND:
            resultado = to_unsigned(s_ra & s_rb)
            self._update_logic_flags(resultado)

        elif op == Opcode.OR:
            resultado = to_unsigned(s_ra | s_rb)
            self._update_logic_flags(resultado)

        elif op == Opcode.XOR: # [cite: 146]
            resultado = to_unsigned(s_ra ^ s_rb)
            self._update_logic_flags(resultado)

        elif op == Opcode.NOT:
            resultado = to_unsigned(~s_ra)
            self._update_logic_flags(resultado)
            
        elif op == Opcode.COPY:
            resultado = to_unsigned(s_ra)
            self._update_logic_flags(resultado)

        elif op == Opcode.ASL:
            shift = s_rb & 0x1F
            resultado = to_unsigned(s_ra << shift)
            self._update_logic_flags(resultado)
            
        elif op == Opcode.ASR:
            shift = s_rb & 0x1F
            resultado = to_unsigned(s_ra >> shift)
            self._update_logic_flags(resultado)
            
        elif op == Opcode.LSL:
            shift = s_rb & 0x1F
            resultado = to_unsigned(s_ra << shift)
            self._update_logic_flags(resultado)
            
        elif op == Opcode.LSR:
            shift = s_rb & 0x1F
            resultado = (to_unsigned(s_ra) >> shift)
            self._update_logic_flags(resultado)

        elif op == Opcode.MULT:
            res_temp = s_ra * s_rb
            resultado = to_unsigned(res_temp)
            self._update_logic_flags(resultado)
            
        elif op == Opcode.DIV:
            if s_rb == 0:
                resultado = 0
                self.overflow = True
            else:
                resultado = int(s_ra / s_rb)
                resultado = to_unsigned(resultado)
                self._update_logic_flags(resultado)

        elif op == Opcode.MOD:
             if s_rb == 0:
                resultado = 0
             else:
                resultado = to_unsigned(s_ra % s_rb)
                self._update_logic_flags(resultado)
        
        elif op == Opcode.POW:
            exp = s_rb if s_rb >= 0 else 0
            resultado = to_unsigned(pow(s_ra, exp))
            self._update_logic_flags(resultado)
            
        elif op == Opcode.SLT:
            resultado = 1 if s_ra < s_rb else 0
            self._update_logic_flags(resultado)
            
        elif op == Opcode.ABS:
            resultado = to_unsigned(abs(s_ra))
            self._update_logic_flags(resultado)
            
        elif op == Opcode.MAX:
            resultado = to_unsigned(max(s_ra, s_rb))
            self._update_logic_flags(resultado)
            
        elif op == Opcode.MIN:
            resultado = to_unsigned(min(s_ra, s_rb))
            self._update_logic_flags(resultado)

        return resultado

    def _update_logic_flags(self, resultado):
        self.carry = False
        self.overflow = False
        self.zero = (resultado == 0)
        self.neg = (get_bit(resultado, 31) == 1)

    def _reset_flags(self, zero=False, neg=False, carry=False, ov=False):
        self.zero = zero
        self.neg = neg
        self.carry = carry
        self.overflow = ov

    def _update_arithmetic_flags(self, a, b, res, is_sub=False):
        res_32 = to_unsigned(res)
        
        self.zero = (res_32 == 0)
        
        self.neg = (get_bit(res_32, 31) == 1)
        
        if not is_sub:
            self.carry = (res > 0xFFFFFFFF)
            self.overflow = ((a >= 0 and b >= 0 and self.neg) or 
                             (a < 0 and b < 0 and not self.neg))
        else:
            u_a = to_unsigned(a)
            u_b = to_unsigned(b)
            self.carry = (u_b > u_a)
            
            self.overflow = ((a >= 0 and b < 0 and self.neg) or 
                             (a < 0 and b >= 0 and not self.neg))