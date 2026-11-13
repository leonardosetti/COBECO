# Tech Debt Log — COBECO MVP

**Versão:** 1.0  
**Status:** Ativo  
**Data:** DD/MM/AAAA  
**Autor:** <Nome>

---

## Débitos técnicos identificados

| ID | Local (arquivo:linha) | Tipo (TODO / FIXME / Tech Debt) | Descrição | Data | Autor | Issue vinculada | Prioridade |
|---|---|---|---|---|---|---|---|
| TD-01 |  | TODO |  |  |  |  | P0/P1/P2 |
| TD-02 |  | FIXME |  |  |  |  | P0/P1/P2 |

---

## Regras

- Todo TODO/FIXME no código deve ter data, autor e link para issue.
- Tech Debt revisado a cada sprint; itens P0 são bloqueantes para merge.
- Nenhum "para depois" sem issue vinculada (YAGNI, Art. 3.7).

---

## Exemplo de marcação no código

```python
# TODO(TD-01, 13/11/2026, @dev): refatorar uso de asyncmy para aiomysql quando estabilizar (issue #XX)
pass
```

---

**Fim do Tech Debt Log**
