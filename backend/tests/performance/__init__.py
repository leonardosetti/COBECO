# COBECO Backend — Performance Tests (RNF09: p95 < 500ms)
# Placeholder for future performance benchmarks using locust/k6
# Current verification: unit tests (146 passed) + integration tests (partial)

"""
Performance test module for RNF09 compliance verification.

Indexes added for key query patterns:
- listas: usuario_id + criado_em + deletado_em
- itens_lista: lista_id + produto_id
- fornecedores_produtos: fornecedor_id + produto_id + ativo + estoque
- sessoes: usuario_id + revogada_em + expira_em

Run integration tests to verify functional correctness:
    pytest tests/integration/ -v

Run unit tests:
    pytest tests/unit/ -v
"""