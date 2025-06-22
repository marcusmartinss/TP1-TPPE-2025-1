from noArvoreB import NoArvoreB
from arvoreB import ArvoreB
import random

def gerar_e_exibir_arvore_b(ordem: int, num_chaves: int):
    """
    Gera uma Árvore B com chaves aleatórias e a exibe.

    Argumentos:
        ordem (int): A ordem da Árvore B.
        num_chaves (int): O número de chaves aleatórias para inserir na árvore.
    """
    if ordem < 2:
        print("Erro: A ordem da Árvore B deve ser pelo menos 2.")
        return
    if num_chaves <= 0:
        print("Erro: O número de chaves deve ser positivo.")
        return

    arvore = ArvoreB(ordem)
    chaves_para_inserir = random.sample(range(1, 1000), num_chaves) # Gera chaves únicas entre 1 e 999

    print(f"Gerando Árvore B de ordem {ordem} com {num_chaves} chaves aleatórias...")
    print(f"Chaves a serem inseridas: {sorted(chaves_para_inserir)}")
    print("-" * 30)

    for chave in chaves_para_inserir:
        arvore.inserir(chave)

    print("\nEstrutura da Árvore B:")
    arvore.imprimirArvore()
    print("-" * 30)

    # Verificação de propriedades após a geração
    if arvore._verificarPropriedades(arvore.raiz):
        print("Verificação de Propriedades: A árvore B satisfaz suas propriedades.")
    else:
        print("Verificação de Propriedades: A árvore B NÃO satisfaz suas propriedades (HOUVE UM ERRO).")
    
    if arvore._todasFolhasNaMesmaProfundidade():
        print("Verificação de Profundidade das Folhas: Todas as folhas estão na mesma profundidade.")
    else:
        print("Verificação de Profundidade das Folhas: As folhas estão em profundidades diferentes (HOUVE UM ERRO).")


if __name__ == "__main__":
    gerar_e_exibir_arvore_b(ordem=3, num_chaves=20)
    print("\n" + "="*50 + "\n")
    gerar_e_exibir_arvore_b(ordem=2, num_chaves=15)