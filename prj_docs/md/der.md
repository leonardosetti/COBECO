# Diagrama Entidade-Relacionamento

```mermaid
erDiagram
  USER ||--o{ PRODUCT_LIST : possui
  USER ||--o{ QUOTATION : realiza
  CATEGORY ||--o{ PRODUCT_LIST : classifica
  CATEGORY ||--o{ PRODUCT : contem
  CATEGORY ||--o{ SUPPLIER : agrega
  PRODUCT_LIST ||--o{ LIST_ITEM : contem
  PRODUCT o|--o{ LIST_ITEM : normaliza
  SUPPLIER ||--o{ SUPPLIER_PRODUCT : oferece
  PRODUCT ||--o{ SUPPLIER_PRODUCT : precificado_em
  PRODUCT_LIST o|--o{ QUOTATION : origina
  QUOTATION ||--o{ QUOTATION_RESULT : detalha
  RETAILER ||--o{ QUOTATION_RESULT : publica
  PRODUCT_LIST ||--o{ LIST_SHARE : compartilha
  USER ||--o{ PASSWORD_RESET_TOKEN : solicita
  USER o|--o{ TESTIMONIAL : escreve
```

O resultado de paridade (`parityGroups`, `parityMeta` e `bestGroupId`) é armazenado na cotação como snapshot JSON para preservar o histórico mesmo que preços ou catálogo mudem.
