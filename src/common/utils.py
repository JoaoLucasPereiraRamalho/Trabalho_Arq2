def to_unsigned(valor):
    return valor & 0xFFFFFFFF

def to_signed(valor):
    valor = valor & 0xFFFFFFFF
    if valor & 0x80000000:
        return valor - 0x100000000
    return valor

def get_bit(valor, posicao):
    return (valor >> posicao) & 1