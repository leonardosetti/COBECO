import { QuotationResponse } from './api';

export function exportQuotationCsv(quotation: QuotationResponse): void {
  const rows: string[][] = [];
  if (quotation.groups) {
    rows.push([
      'Grupo',
      'Fornecedores',
      'Cobertura (%)',
      'Total consolidado',
      'Itens ausentes',
      'Melhor grupo',
    ]);
    const itemNames = new Map(quotation.items.map((item) => [item.itemId, item.description]));
    quotation.groups.forEach((group, index) =>
      rows.push([
        String(index + 1),
        group.supplierNames.join(', '),
        String(group.coverage),
        String(group.total),
        group.missingItems.map((id) => itemNames.get(id) || id).join(', '),
        group.groupId === quotation.bestGroupId ? 'Sim' : 'Não',
      ])
    );
  } else {
    rows.push([
      'Item',
      'Quantidade',
      'Produto',
      'Lojista',
      'Preço',
      'Moeda',
      'Prazo (dias)',
      'Link',
    ]);
    quotation.items.forEach((item) =>
      item.results.forEach((result) =>
        rows.push([
          item.description,
          String(item.quantity),
          result.productName,
          result.retailerName,
          result.price === null ? '' : String(result.price),
          result.currency,
          result.deliveryDays === null ? '' : String(result.deliveryDays),
          result.redirectUrl,
        ])
      )
    );
  }
  const csv = rows
    .map((row) => row.map((value) => `"${value.replace(/"/g, '""')}"`).join(';'))
    .join('\n');
  const blob = new Blob([`\uFEFF${csv}`], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = `cobeco-cotacao-${new Date(quotation.requestedAt)
    .toISOString()
    .slice(0, 10)}.csv`;
  anchor.click();
  URL.revokeObjectURL(url);
}

export function printQuotation(): void {
  window.print();
}
