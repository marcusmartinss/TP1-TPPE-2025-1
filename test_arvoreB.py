import pytest
import icontract
from arvoreB import ArvoreB

# --- Fixtures dos estado base dos testes ---

@pytest.fixture
def arvore_vazia_ordem_3():
    """
    Retorna uma árvore B de ordem 3 vazia.
    """
    return ArvoreB(ordem=3)

@pytest.fixture
def arvore_preenchida_ordem_3():
    """
    Retorna uma árvore B de ordem 3 com várias chaves inseridas.
    """
    arvore = ArvoreB(ordem=3)
    chaves = [10, 20, 5, 6, 12, 30, 7, 17, 3, 1, 40, 50, 60, 70, 80]
    
    for chave in chaves:
        arvore.inserir(chave)
    
    return arvore

# --- Testes para as Invariantes ---

def test_invariante_folhas_mesmo_nivel(arvore_preenchida_ordem_3):
    """
    Verifica se todas as folhas permanecem no mesmo nível após operações.
    """
    assert arvore_preenchida_ordem_3._todasFolhasNaMesmaProfundidade() == True, \
        "Falha na invariante: Nem todas as folhas estão na mesma profundidade."

def test_invariantes_de_propriedades_dos_nos(arvore_preenchida_ordem_3):
    """
    Verifica o cumprimento de todas as propriedades estruturais da Árvore B.
    """
    assert arvore_preenchida_ordem_3._verificarPropriedades(arvore_preenchida_ordem_3.raiz) == True, \
        "Falha em uma ou mais invariantes/pós-condições estruturais da árvore."

# --- Testes para as Pré-condições ---

def test_precondicao_inserir_chave_inexistente(arvore_preenchida_ordem_3):
    """
    Garante que inserção de chave existente viola o contrato.
    """
    chave_existente = 20
    
    # Garante que a chave realmente existe antes de tentar a inserção duplicada
    assert arvore_preenchida_ordem_3.buscar(chave_existente) is not None, \
        "Setup do teste falhou: a chave 20 deveria existir."
    
    # Usa pytest.raises para verificar se o bloco de código levanta a exceção esperada.
    # O teste PASSA se a exceção for levantada.
    # O teste FALHA se nenhuma exceção (ou a exceção errada) for levantada.
    with pytest.raises(icontract.errors.ViolationError) as e:
        arvore_preenchida_ordem_3.inserir(chave_existente)

    # Opcional: Verifica se a mensagem de erro do contrato está correta
    assert "A chave a ser inserida não deve existir na árvore" in str(e.value)


def test_precondicao_remover_chave_existente(arvore_preenchida_ordem_3):
    """
    Testa a Pré-condição: "Chave a ser removida existe na árvore".
    """
    chave_inexistente = 999
    
    # Garante que a chave realmente não existe
    assert arvore_preenchida_ordem_3.buscar(chave_inexistente) is None

    # O teste PASSA se a exceção de violação de contrato for levantada
    with pytest.raises(icontract.errors.ViolationError) as e:
        arvore_preenchida_ordem_3.remover(chave_inexistente)
    
    assert "A chave a ser removida deve existir na árvore" in str(e.value)


# --- Testes para as Pós-condições ---

def test_poscondicao_divisao_aumenta_altura():
    """
    Verifica se a divisão da raiz aumenta a altura da árvore.
    """
    arvore = ArvoreB(ordem=2)
    
    # Preenche raiz até capacidade máxima
    for chave in [10, 20, 30]:
        arvore.inserir(chave)
    
    # Insere chave extra para forçar divisão
    arvore.inserir(15)
    
    # Verifica aumento de altura
    profundidades = []
    arvore._obterProfundidadesFolhas(arvore.raiz, 0, profundidades)
    assert len(set(profundidades)) == 1 and profundidades[0] == 1, "A altura da árvore não aumentou em 1 após a divisão da raiz."

def test_poscondicao_fusao_diminui_altura():
    """
    Verifica se fusão de nós reduz a altura da árvore.
    """
    arvore = ArvoreB(ordem=2)
    
    # Cria estrutura com altura 2
    for chave in [10, 20, 30, 5, 15, 25, 35]:
        arvore.inserir(chave)
    
    # Remove chaves para forçar fusão
    arvore.remover(5)
    arvore.remover(15)
    arvore.remover(10)
    
    # Verificar redução de altura
    profundidades = []
    arvore._obterProfundidadesFolhas(arvore.raiz, 0, profundidades)
    assert all(d == profundidades[0] for d in profundidades)