"""
Esse módulo contém funções utilitáras referentes
a cálculos ou operações.
"""

def increment_index(
    index: int,
    len_list: int,
    increment_value: int = 1
) -> int:
    """
    Incrementa em um index mantendo-o no tamanho da lista.
    Valores positivos incrementam, negativos decrementam.
    """
    if increment_value > 0:
        return (index + increment_value) % len_list
    if increment_value < 0:
        return (len_list + increment_value) % len_list
    return index
