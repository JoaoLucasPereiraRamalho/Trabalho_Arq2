from enum import Enum

class Opcode(Enum):
    
    ADD   = 0x01  # Adição
    SUB   = 0x02  # Subtração
    ZEROS = 0x03  # Zera registrador
    XOR   = 0x04  # Ou exclusivo
    OR    = 0x05  # Ou lógico
    NOT   = 0x06  # Negação
    AND   = 0x07  # E lógico
    ASL   = 0x08  # Shift Aritmético Esquerda
    ASR   = 0x09  # Shift Aritmético Direita
    LSL   = 0x0A  # Shift Lógico Esquerda
    LSR   = 0x0B  # Shift Lógico Direita
    COPY  = 0x0C  # Copia registrador

    # --- Acesso à Memória e Constantes ---
    LCL_HIGH = 0x0E  # Carrega constante alta
    LCL_LOW  = 0x0F  # Carrega constante baixa
    LOAD     = 0x10  # Carrega da memória
    STORE    = 0x11  # Salva na memória

    # --- Controle de Fluxo ---
    JAL   = 0x12  # Jump and Link
    JR    = 0x13  # Jump Register
    BEQ   = 0x14  # Branch Equal
    BNE   = 0x15  # Branch Not Equal
    J     = 0x16  # Jump Incondicional

    # --- Novas Instruções ---
    MULT  = 0x17  # Multiplicação
    DIV   = 0x18  # Divisão Inteira
    MOD   = 0x19  # Resto da Divisão
    POW   = 0x1A  # Potência
    SLT   = 0x1B  # Set on Less Than
    ABS   = 0x1C  # Valor Absoluto
    MAX   = 0x1D  # Máximo entre dois valores
    MIN   = 0x1E  # Mínimo entre dois valores

    # --- Sistema ---
    HALT  = 0xFFFFFFFF

MASK_OPCODE = 0xFF000000
MASK_RA     = 0x00FF0000
MASK_RB     = 0x0000FF00
MASK_RC     = 0x000000FF