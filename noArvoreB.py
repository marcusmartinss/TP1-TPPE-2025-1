import icontract
from typing import List, Optional, Tuple


@icontract.invariant(lambda self: self.chaves == sorted(self.chaves), "As chaves devem estar sempre ordenadas")
class NoArvoreB:
    """
    Cada nó pode ser uma folha ou um nó interno. A classe armazena uma lista ordenada
    de chaves e, se for um nó interno, uma lista de referências para seus nós filhos.

    Atributos:
        folha (bool): Verdadeiro se o nó é uma folha, ou seja, no um nó da "ponta da árvore".
        chaves (List[int]): A lista de chaves (valores inteiros) armazenadas no nó.
        filhos (List['NoArvoreB']): A lista de referências para os nós filhos.
    """
    def __init__(self, folha: bool = False):
        """
        Construtor da classe.

        Argumentos:
            folha (bool): Especifica se o nó a ser criado é uma folha.
                          Por padrão, é inicializado como Falso.
        """
        self.folha = folha
        self.chaves: List[int] = []
        self.filhos: List['NoArvoreB'] = []

    def buscar(self, chaveProcurada: int) -> Optional[Tuple['NoArvoreB', int]]:
        """
        Busca uma chave a partir deste nó, descendo recursivamente se necessário.

        Argumentos:
            chaveProcurada (int): A chave que está sendo buscada.

        REtorna:
            Optional[Tuple['NoArvoreB', int]]: Uma tupla contendo o nó e o índice onde a
                                               chave foi encontrada. Retorna None se a chave
                                               não for encontrada na subárvore a partir deste nó.
        """
        i = 0
        # Enquanto a chave for menor que a procurada, continua procurando
        while i < len(self.chaves) and chaveProcurada > self.chaves[i]:
            i += 1
        
        # Condição de sucesso: Se achou a chave procurada, retorna ela e seu índice.
        if i < len(self.chaves) and chaveProcurada == self.chaves[i]:
            return (self, i)
        
        # Caso base: Se chegou em um nó e não é a chave, não está nessa subárvore
        if self.folha:
            return None
        # Se não é folha, continua buscando dentro dos filhos do nó
        else:
            return self.filhos[i].buscar(chaveProcurada)