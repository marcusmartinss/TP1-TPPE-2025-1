import icontract
from typing import List, Optional, Tuple
from noArvoreB import NoArvoreB


class ArvoreB:
    """
    Implementação de uma Árvore B.

    Atributos:
        raiz (NoArvoreB): O nó raiz da árvore.
        ordem (int): A ordem da Árvore B (número mínimo de chaves em um nó não raiz).
    """

    def __init__(self, ordem: int):
        """
        Inicializa a Árvore B.

        Argumentos:
            ordem (int): A ordem da árvore B.
        """
        if ordem < 2:
            raise ValueError("A ordem da Árvore B deve ser pelo menos 2.")
        self.ordem = ordem
        self.raiz: NoArvoreB = NoArvoreB(folha=True)

    def buscar(self, chaveProcurada: int) -> Optional[Tuple['NoArvoreB', int]]:
        """
        Busca uma chave na árvore B.

        Argumentos:
            chaveProcurada (int): A chave a ser buscada.

        Retorna:
            Optional[Tuple['NoArvoreB', int]]: Uma tupla contendo o nó e o índice onde a
                                                chave foi encontrada, ou None se a chave não for encontrada.
        """
        return self.raiz.buscar(chaveProcurada)

    def inserir(self, chave: int) -> None:
        """
        Insere uma chave na Árvore B.

        Argumentos:
            chave (int): A chave a ser inserida.
        """
        raiz_atual = self.raiz
        if len(raiz_atual.chaves) == (2 * self.ordem) - 1:
            nova_raiz = NoArvoreB()
            nova_raiz.filhos.append(self.raiz)
            self.raiz = nova_raiz
            self._dividirFilho(nova_raiz, 0)
            self._inserirEmNaoCheio(nova_raiz, chave)
        else:
            self._inserirEmNaoCheio(raiz_atual, chave)

    def _inserirEmNaoCheio(self, no: NoArvoreB, chave: int) -> None:
        """
        Método auxiliar para inserir uma chave em um nó que não está cheio.

        Argumentos:
            no (NoArvoreB): O nó onde a chave será inserida.
            chave (int): A chave a ser inserida.
        """
        i = len(no.chaves) - 1
        if no.folha:
            # Encontra a posição correta para a chave e insere
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            no.chaves.insert(i + 1, chave)
        else:
            # Encontra o filho correto para descer
            while i >= 0 and chave < no.chaves[i]:
                i -= 1
            i += 1
            if len(no.filhos[i].chaves) == (2 * self.ordem) - 1:
                self._dividirFilho(no, i)
                if chave > no.chaves[i]:
                    i += 1
            self._inserirEmNaoCheio(no.filhos[i], chave)

    def _dividirFilho(self, pai: NoArvoreB, indice_filho: int) -> None:
        """
        Divide o filho cheio do nó pai.

        Argumentos:
            pai (NoArvoreB): O nó pai do filho a ser dividido.
            indice_filho (int): O índice do filho a ser dividido na lista de filhos do pai.
        """
        filho_cheio = pai.filhos[indice_filho]
        novo_filho = NoArvoreB(folha=filho_cheio.folha)

        # Move a chave mediana para o pai
        chave_mediana = filho_cheio.chaves[self.ordem - 1]
        pai.chaves.insert(indice_filho, chave_mediana)
        pai.filhos.insert(indice_filho + 1, novo_filho)

        # Move as chaves e filhos para o novo_filho
        novo_filho.chaves = filho_cheio.chaves[self.ordem:]
        filho_cheio.chaves = filho_cheio.chaves[:self.ordem - 1]

        if not filho_cheio.folha:
            novo_filho.filhos = filho_cheio.filhos[self.ordem:]
            filho_cheio.filhos = filho_cheio.filhos[:self.ordem]

    def imprimirArvore(self, no: Optional[NoArvoreB] = None, nivel: int = 0) -> None:
        """
        Imprime a árvore B de forma hierárquica.

        Argumentos:
            no (Optional[NoArvoreB]): O nó a partir do qual a impressão começará.
                                     Por padrão, começa da raiz.
            nivel (int): O nível atual na árvore, usado para indentação.
        """
        if no is None:
            no = self.raiz

        print("  " * nivel + f"Nível {nivel}: {no.chaves}")

        if not no.folha:
            for filho in no.filhos:
                self.imprimirArvore(filho, nivel + 1)

    def _verificarPropriedades(self, no: NoArvoreB) -> bool:
        """
        Verifica as propriedades de uma Árvore B para o nó dado e seus descendentes.

        Argumentos:
            no (NoArvoreB): O nó a ser verificado.

        Retorna:
            bool: True se as propriedades forem satisfeitas, False caso contrário.
        """
        # Propriedade 1: Cada nó tem no máximo 2t-1 chaves
        if len(no.chaves) > (2 * self.ordem) - 1:
            print(f"Erro: Nó {no.chaves} tem mais de {2 * self.ordem - 1} chaves.")
            return False

        # Propriedade 2: Cada nó interno tem exatamente um filho a mais que chaves
        if not no.folha and len(no.filhos) != len(no.chaves) + 1:
            print(f"Erro: Nó interno {no.chaves} não tem o número correto de filhos.")
            return False

        # Propriedade 3: Cada nó, exceto a raiz, tem pelo menos t-1 chaves (se não for a raiz e não for o nó inicial vazio)
        if no is not self.raiz and len(no.chaves) < self.ordem - 1:
            print(f"Erro: Nó {no.chaves} tem menos de {self.ordem - 1} chaves.")
            return False

        # Propriedade 4: Todas as chaves em um nó são ordenadas
        if no.chaves != sorted(no.chaves):
            print(f"Erro: Chaves em {no.chaves} não estão ordenadas.")
            return False

        # Propriedade 5: Propriedade de ordem das chaves e filhos
        if not no.folha:
            for i in range(len(no.chaves)):
                if not all(chave < no.chaves[i] for chave in no.filhos[i].chaves):
                    print(f"Erro: Chaves no filho {no.filhos[i].chaves} não são menores que {no.chaves[i]}.")
                    return False
                if not all(chave > no.chaves[i] for chave in no.filhos[i + 1].chaves):
                    print(f"Erro: Chaves no filho {no.filhos[i+1].chaves} não são maiores que {no.chaves[i]}.")
                    return False

        # Verifica recursivamente os filhos
        if not no.folha:
            for filho in no.filhos:
                if not self._verificarPropriedades(filho):
                    return False
        return True

    def _obterProfundidadesFolhas(self, no: NoArvoreB, nivel: int, profundidades: List[int]) -> None:
        """
        Método auxiliar para obter as profundidades de todas as folhas na árvore.

        Argumentos:
            no (NoArvoreB): O nó atual.
            nivel (int): O nível atual na árvore.
            profundidades (List[int]): Lista para armazenar as profundidades das folhas.
        """
        if no.folha:
            profundidades.append(nivel)
        else:
            for filho in no.filhos:
                self._obterProfundidadesFolhas(filho, nivel + 1, profundidades)

    def _todasFolhasNaMesmaProfundidade(self) -> bool:
        """
        Verifica se todas as folhas da árvore estão na mesma profundidade.

        Retorna:
            bool: True se todas as folhas estiverem na mesma profundidade, False caso contrário.
        """
        profundidades: List[int] = []
        self._obterProfundidadesFolhas(self.raiz, 0, profundidades)
        if not profundidades:
            return True  # Árvore vazia ou apenas a raiz que é folha, considerada consistente
        return all(p == profundidades[0] for p in profundidades)