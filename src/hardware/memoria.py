class Memoria:
    def __init__(self, tamanho=65536):

        self.dados = [0] * tamanho 

    def ler(self, endereco):
        if 0 <= endereco < len(self.dados):
            return self.dados[endereco]
        raise IndexError(f"Acesso inválido à memória: {endereco}")

    def escrever(self, endereco, valor):
        if 0 <= endereco < len(self.dados):
            self.dados[endereco] = valor & 0xFFFFFFFF