"""
Esse módulo contém testes unitários e
automatizados referente as funções
do módulo operations_utils.py
"""
from src.utils import operations_utils

def test_increment_index() -> None:
    """Testa a função `increment_index`."""
    index = 0
    len_list = 3
    assert index == 0, f"Index: {index}"
    index = operations_utils.increment_index(index, len_list)
    assert index == 1, f"Index: {index}"
    index = operations_utils.increment_index(index, len_list)
    assert index == 2, f"Index: {index}"
    index = operations_utils.increment_index(index, len_list)
    assert index == 0, f"Index: {index}"

    index = 0
    assert index == 0, f"Index: {index}"
    index = operations_utils.increment_index(index, len_list, -1)
    assert index == 2, f"Index: {index}"
    index = operations_utils.increment_index(index, len_list, -1)
    assert index == 1, f"Index: {index}"
    index = operations_utils.increment_index(index, len_list, -1)
    assert index == 0, f"Index: {index}"
