from src.common.utils import to_unsigned

class Registradores:
    def __init__(self):
        self.regs = [0] * 32

    def ler(self, indice):
        self._validar_indice(indice)
        return self.regs[indice]

    def escrever(self, indice, valor):
        self._validar_indice(indice)
        
        self.regs[indice] = to_unsigned(valor)

    def _validar_indice(self, indice):
        if not (0 <= indice < 32):
            raise ValueError(f"Registrador inválido: r{indice}. Deve ser entre 0 e 31.")

    def dump_formatado(self):
        saida = "Estado dos Registradores:\n"
        for i in range(0, 32, 4):
            line = ""
            for j in range(4):
                reg_idx = i + j
                if reg_idx < 32:
                    line += f"R{reg_idx:02d}: 0x{self.regs[reg_idx]:08X}  "
            saida += line + "\n"
        return saida