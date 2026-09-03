import { describe, expect, it } from 'vitest';
import { calculateAvailability, CatalogOffer } from './availability';
import { groupByCoverageProfile } from './grouping';
import { calculateGroupBudgets, selectBestGroup } from './budget';

describe('motor de paridade', () => {
  const items = Array.from({ length: 9 }, (_, index) => ({
    id: String(index + 1),
    productId: String(index + 1),
    description: `Produto ${index + 1}`,
    quantity: 1,
  }));
  const profiles: Record<string, number[]> = {
    A: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    B: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    C: [1, 2, 3, 4, 5, 6, 8, 9],
    D: [1, 2, 4, 5, 8, 9],
    E: [1, 2, 3, 4, 5, 6, 8, 9],
    F: [1, 2, 3, 4, 5, 6, 8, 9],
    G: [1, 3, 4, 5, 8, 9],
    H: [1, 2, 3, 4, 5, 6, 8, 9],
  };
  const suppliers = Object.keys(profiles).map((id) => ({ id, name: `Fornecedor ${id}` }));
  const offers: CatalogOffer[] = Object.entries(profiles).flatMap(
    ([supplierId, productIds], supplierIndex) =>
      productIds.map((productId) => ({
        supplierId,
        productId: String(productId),
        price: 10 + supplierIndex + productId,
        active: true,
      }))
  );

  it('reproduz os quatro perfis especificados para A-H', () => {
    const groups = groupByCoverageProfile(
      calculateAvailability(items, suppliers, offers),
      items.length
    );
    expect(groups.map((group) => group.suppliers.map((entry) => entry.supplier.id))).toEqual([
      ['A', 'B'],
      ['C', 'E', 'F', 'H'],
      ['D'],
      ['G'],
    ]);
    expect(groups.map((group) => group.coverage)).toEqual([100, 88.89, 66.67, 66.67]);
  });

  it('calcula totais consolidados e escolhe primeiro a maior cobertura', () => {
    const groups = groupByCoverageProfile(
      calculateAvailability(items, suppliers, offers),
      items.length
    );
    const budgets = calculateGroupBudgets(groups);
    expect(budgets[0].total).toBe(135);
    expect(selectBestGroup(budgets)).toBe('group-1');
  });

  it('trata item sem produto normalizado como ausente para todos', () => {
    const unknown = { id: '10', productId: null, description: 'Não cadastrado', quantity: 1 };
    const availability = calculateAvailability([...items, unknown], suppliers, offers);
    expect(availability.every((entry) => entry.missingItems.some((item) => item.id === '10'))).toBe(
      true
    );
  });
});
