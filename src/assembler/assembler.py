import sys
from src.common.constantes import Opcode

class Assembler:
    def __init__(self):
        self.labels = {}
        self.instrucoes = []
        self.endereco_atual = 0

    def montar(self, arquivo_entrada, arquivo_saida):

        try:
            with open(arquivo_entrada, 'r') as f:
                linhas = f.readlines()
        except FileNotFoundError:
            print(f"Erro: Arquivo {arquivo_entrada} não encontrado.")
            return

        self._primeira_passada(linhas)

        codigo_binario = self._segunda_passada(linhas)

        with open(arquivo_saida, 'w') as f:
            for linha in codigo_binario:
                f.write(linha + '\n')
        
        print(f"Montagem concluída! Arquivo gerado: {arquivo_saida}")

    def _primeira_passada(self, linhas):
        self.endereco_atual = 0
        self.labels = {}

        for linha in linhas:
            linha = linha.split('#')[0].strip()
            if not linha:
                continue

            if linha.startswith('address'):
                partes = linha.split()
                if len(partes) > 1:
                    try:
                        val = partes[1]
                        self.endereco_atual = int(val, 2) if all(c in '01' for c in val) and len(val) > 1 else int(val)
                    except ValueError:
                        print(f"Aviso: Endereço inválido na linha: {linha}")
                continue

            if linha.endswith(':'):
                label_nome = linha[:-1].strip()
                self.labels[label_nome] = self.endereco_atual
                continue

            self.endereco_atual += 1

    def _segunda_passada(self, linhas):
        saida = []
        self.endereco_atual = 0

        for linha_orig in linhas:
            linha = linha_orig.split('#')[0].strip()
            if not linha or linha.endswith(':'):
                continue

            if linha.startswith('address'):
                partes = linha.split()
                if len(partes) > 1:
                    val_str = partes[1]
                    try:
                        val_int = int(val_str, 2) if all(c in '01' for c in val_str) and len(val_str) > 1 else int(val_str)
                        self.endereco_atual = val_int
                        addr_bin = bin(val_int)[2:]
                        saida.append(f"address {addr_bin}")
                    except ValueError:
                        pass
                continue

            binario_instrucao = self._processar_instrucao(linha)
            if binario_instrucao:
                saida.append(binario_instrucao)
                self.endereco_atual += 1
            else:
                print(f"Erro de sintaxe na linha: {linha_orig}")

        return saida

    def _processar_instrucao(self, linha):
        if linha.upper() == 'HALT':
            return '1' * 32

        partes = linha.replace(',', ' ').split()
        mnemonico = partes[0].upper()
        
        try:
            opcode = Opcode[mnemonico] 
        except KeyError:
            mapa_extra = {
                'PASSNOTA': Opcode.NOT,
                'PASSA': Opcode.COPY,
                'ZERO': Opcode.ZEROS
            }
            if mnemonico in mapa_extra:
                opcode = mapa_extra[mnemonico]
            else:
                print(f"Instrução desconhecida: {mnemonico}")
                return None

        # Valores padrão
        ra, rb, rc = 0, 0, 0
        const16 = 0
        imm24 = 0


        if opcode in [Opcode.ADD, Opcode.SUB, Opcode.AND, Opcode.OR, Opcode.XOR, 
                      Opcode.SLT, Opcode.MULT, Opcode.DIV, Opcode.MOD, Opcode.POW, 
                      Opcode.MAX, Opcode.MIN, Opcode.ASL, Opcode.ASR, Opcode.LSL, Opcode.LSR]:
            try:
                rc = self._parse_reg(partes[1])
                ra = self._parse_reg(partes[2])
                rb = self._parse_reg(partes[3])
            except IndexError: return None

        elif opcode in [Opcode.NOT, Opcode.COPY, Opcode.ABS]:
            rc = self._parse_reg(partes[1])
            ra = self._parse_reg(partes[2])
        
        elif opcode == Opcode.ZEROS:
            rc = self._parse_reg(partes[1])

        elif opcode in [Opcode.LOAD, Opcode.STORE]:
            rc = self._parse_reg(partes[1])
            ra = self._parse_reg(partes[2])

        elif opcode in [Opcode.LCL_HIGH, Opcode.LCL_LOW]:
            rc = self._parse_reg(partes[1])
            const16 = self._parse_int(partes[2]) & 0xFFFF

        elif opcode in [Opcode.BEQ, Opcode.BNE]:
            ra = self._parse_reg(partes[1])
            rb = self._parse_reg(partes[2])
            destino = partes[3]
            
            if destino in self.labels:
                rc = self.labels[destino]
            else:
                rc = self._parse_int(destino)
            
            rc = rc & 0xFF 

        elif opcode in [Opcode.JAL, Opcode.J]:
            destino = partes[1]
            if destino in self.labels:
                imm24 = self.labels[destino]
            else:
                imm24 = self._parse_int(destino)
            imm24 = imm24 & 0xFFFFFF

        elif opcode == Opcode.JR:
            rc = self._parse_reg(partes[1])

        instrucao_int = 0

        instrucao_int = (opcode.value << 24)
        
        if opcode in [Opcode.LCL_HIGH, Opcode.LCL_LOW]:
            instrucao_int |= (const16 << 8)
            instrucao_int |= rc
        
        elif opcode in [Opcode.J, Opcode.JAL]:
            instrucao_int |= imm24
            
        else:
            instrucao_int |= (ra << 16)
            instrucao_int |= (rb << 8)
            instrucao_int |= rc

        return f"{instrucao_int:032b}"

    def _parse_reg(self, token):
        token = token.lower().replace(',', '')
        if token.startswith('r'):
            try:
                return int(token[1:])
            except ValueError:
                pass
        return 0

    def _parse_int(self, token):
        token = token.replace(',', '')
        try:
            if token.startswith('0x'):
                return int(token, 16)
            elif token.startswith('0b'):
                return int(token, 2)
            else:
                return int(token)
        except ValueError:
            return 0