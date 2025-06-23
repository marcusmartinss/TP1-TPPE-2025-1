import icontract
from typing import List, Optional, Tuple
from noArvoreB import NoArvoreB


class ArvoreB:
    """
    Implementação de uma Árvore B.

    Atributos:
        raiz (NoArvoreB): O nó raiz da árvore, inicia com None.
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
        self.raiz: Optional[NoArvoreB] = None

    def buscar(self, chaveProcurada: int) -> Optional[Tuple['NoArvoreB', int]]:
        """
        Busca uma chave na árvore B.

        Argumentos:
            chaveProcurada (int): A chave a ser buscada.

        Retorna:
            Optional[Tuple['NoArvoreB', int]]: Uma tupla contendo o nó e o índice onde a
                                               chave foi encontrada, ou None se a chave não for encontrada.
        """
        if self.raiz is None:
            return None
        
        return self.raiz.buscar(chaveProcurada)


    @icontract.require(lambda self, chave: self.buscar(chave) is None, "A chave a ser inserida não deve existir na árvore (pré-condição violada).")
    def inserir(self, chave: int) -> None:
        """
        Insere uma chave na Árvore B.

        Argumentos:
            chave (int): A chave a ser inserida.
        """
        if self.raiz is None:
            self.raiz = NoArvoreB(folha=True)
            self.raiz.chaves.append(chave)
            return

        raiz_atual = self.raiz

        if len(raiz_atual.chaves) == (2 * self.ordem) - 1:
            nova_raiz = NoArvoreB(folha=False)
            nova_raiz.filhos.append(raiz_atual)
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

    @icontract.require(lambda self, chave: self.buscar(chave) is not None, "A chave a ser removida deve existir na árvore (pré-condição violada).")
    def remover(self, chave: int) -> None:
        """
        Remove uma chave da Árvore B.

        Argumentos:
            chave (int): A chave a ser removida.
        """
        if not self.raiz:
            print("Erro: Árvore está vazia.")
            return

        self._removerRecursivo(self.raiz, chave)

        # Se a remoção esvaziou a raiz e ela não é uma folha,
        # o primeiro filho se torna a nova raiz, diminuindo a altura da árvore.
        if len(self.raiz.chaves) == 0 and not self.raiz.folha:
            self.raiz = self.raiz.filhos[0]

    def _removerRecursivo(self, no: NoArvoreB, chave: int) -> None:
        """
        Método recursivo para percorrer a árvore e remover a chave.
        """
        # Encontra a posição da chave ou a subárvore onde ela pode estar.
        i = 0
        while i < len(no.chaves) and chave > no.chaves[i]:
            i += 1

        # Caso 1: A chave está neste nó.
        if i < len(no.chaves) and no.chaves[i] == chave:
            if no.folha:
                # Caso 1a: Se o nó for uma folha, simplesmente remove a chave.
                no.chaves.pop(i)
            else:
                # Caso 1b: Se o nó for interno, a lógica é mais complexa.
                self._removerDeNoInterno(no, i)
        
        # Caso 2: A chave não está neste nó.
        else:
            # Se o nó é uma folha, a chave não está na árvore.
            if no.folha:
                print(f"Erro: Chave {chave} não encontrada na árvore.")
                return

            # Antes de descer para o filho, garante que ele tenha chaves suficientes.
            # Esta é a lógica de rebalanceamento preventivo.
            filho_tem_chaves_minimas = (len(no.filhos[i].chaves) >= self.ordem)
            
            if not filho_tem_chaves_minimas:
                self._preencherFilho(no, i)
            
            # Após o possível rebalanceamento, a recursão continua.
            # Se a fusão ocorreu, a chave pode ter se movido.
            if i > len(no.chaves):
                self._removerRecursivo(no.filhos[i-1], chave)
            else:
                self._removerRecursivo(no.filhos[i], chave)

    def _removerDeNoInterno(self, no: NoArvoreB, indice: int) -> None:
        """
        Lida com a remoção de uma chave que está em um nó interno.
        """
        chave = no.chaves[indice]
        filho_anterior = no.filhos[indice]
        filho_seguinte = no.filhos[indice + 1]

        # Caso 2a: Se o filho à esquerda (anterior) tem chaves suficientes,
        # encontramos o predecessor da chave, o substituímos e removemos o predecessor.
        if len(filho_anterior.chaves) >= self.ordem:
            predecessor = self._encontrarPredecessor(filho_anterior)
            no.chaves[indice] = predecessor
            self._removerRecursivo(filho_anterior, predecessor)
        # Caso 2b: Se o filho à direita (seguinte) tem chaves suficientes,
        # fazemos o mesmo com o sucessor.
        elif len(filho_seguinte.chaves) >= self.ordem:
            sucessor = self._encontrarSucessor(filho_seguinte)
            no.chaves[indice] = sucessor
            self._removerRecursivo(filho_seguinte, sucessor)
        # Caso 2c: Se ambos os filhos têm o mínimo de chaves, os fundimos.
        else:
            self._fundir(no, indice)
            self._removerRecursivo(filho_anterior, chave)

    def _encontrarPredecessor(self, no: NoArvoreB) -> int:
        """
        Encontra a maior chave na subárvore (predecessor).
        """
        while not no.folha:
            no = no.filhos[-1]

        return no.chaves[-1]

    def _encontrarSucessor(self, no: NoArvoreB) -> int:
        """
        Encontra a menor chave na subárvore (sucessor).
        """
        while not no.folha:
            no = no.filhos[0]
        
        return no.chaves[0]

    def _preencherFilho(self, no: NoArvoreB, indice: int) -> None:
        """
        Garante que o filho `no.filhos[indice]` tenha pelo menos `ordem` chaves
        antes de descermos para ele.
        """
        # Tenta pegar emprestado do irmão da esquerda.
        if indice != 0 and len(no.filhos[indice - 1].chaves) >= self.ordem:
            self._pegarEmprestadoDoAnterior(no, indice)
        # Tenta pegar emprestado do irmão da direita.
        elif indice != len(no.chaves) and len(no.filhos[indice + 1].chaves) >= self.ordem:
            self._pegarEmprestadoDoProximo(no, indice)
        # Se não for possível emprestar, funde os nós.
        else:
            if indice != len(no.chaves):
                self._fundir(no, indice)
            else:
                self._fundir(no, indice - 1)

    def _pegarEmprestadoDoAnterior(self, no: NoArvoreB, indice: int) -> None:
        """
        Pega uma chave do irmão anterior.
        """
        filho = no.filhos[indice]
        irmao = no.filhos[indice - 1]

        filho.chaves.insert(0, no.chaves[indice - 1])
        no.chaves[indice - 1] = irmao.chaves.pop()

        if not irmao.folha:
            filho.filhos.insert(0, irmao.filhos.pop())

    def _pegarEmprestadoDoProximo(self, no: NoArvoreB, indice: int) -> None:
        """
        Pega uma chave do irmão seguinte.
        """
        filho = no.filhos[indice]
        irmao = no.filhos[indice + 1]

        filho.chaves.append(no.chaves[indice])
        no.chaves[indice] = irmao.chaves.pop(0)

        if not irmao.folha:
            filho.filhos.append(irmao.filhos.pop(0))

    def _fundir(self, no: NoArvoreB, indice: int) -> None:
        """
        Funde o filho `no.filhos[indice]` com `no.filhos[indice+1]`.
        """
        filho_a_fundir = no.filhos[indice]
        irmao = no.filhos[indice + 1]

        # Puxa uma chave do nó pai para o filho.
        filho_a_fundir.chaves.append(no.chaves.pop(indice))
        
        # Move todas as chaves e filhos do irmão para o filho.
        filho_a_fundir.chaves.extend(irmao.chaves)
        if not irmao.folha:
            filho_a_fundir.filhos.extend(irmao.filhos)
        
        # Remove o irmão da lista de filhos do pai.
        no.filhos.pop(indice + 1)

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
        elif no.filhos:
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