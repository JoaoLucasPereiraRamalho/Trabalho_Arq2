from src.common.utils import to_unsigned

class Memoria:
    def __init__(self, tamanho=65536):

        self.tamanho = tamanho
        self.dados = [0] * self.tamanho

    def ler(self, endereco):
        if 0 <= endereco < self.tamanho:
            return self.dados[endereco]
        else:
            raise IndexError(f"Erro de Segmentação: Tentativa de ler endereço inválido {endereco}")

    def escrever(self, endereco, valor):
        if 0 <= endereco < self.tamanho:
            self.dados[endereco] = to_unsigned(valor)
        else:
            raise IndexError(f"Erro de Segmentação: Tentativa de escrever em endereço inválido {endereco}")
        
    def carregar_programa(self, programa, endereco_base=0):
        for i, instrucao in enumerate(programa):
            if endereco_base + i < self.tamanho:
                self.dados[endereco_base + i] = to_unsigned(instrucao)
            else:
                raise MemoryError("Programa excede o tamanho da memória.")

    def dump(self, inicio=0, fim=10):
        return self.dados[inicio:fim]