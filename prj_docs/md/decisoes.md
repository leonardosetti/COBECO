# Registro de decisões — 30/08/2026

Participantes: Leonardo Setti, Fabrício Cabral, Nicholas Anthony, Eduardo Passarelli e Nicolas Mallouk.

- D1 — `objetivos.md` é a fonte normativa do MVP. Materiais anteriores ficam apenas como histórico de concepção.
- D2 — fornecedores são agrupados por perfil idêntico de cobertura. O percentual é um rótulo calculado, não o critério de agrupamento.
- D3 — React 18 é mantido e o RNF20 foi corrigido. O sistema não utiliza jQuery.
- D4 — o catálogo seedado no PostgreSQL é a fonte padrão. Integrações externas permanecem como `PriceProvider` pós-MVP e só são ativadas por `ENABLE_EXTERNAL_PRICE_PROVIDERS=true` ou `PRICE_PROVIDERS` explícito.

Estas decisões eliminam as divergências entre os documentos e orientam schema, API, interface e testes.
