import { CoverageGroup } from './grouping';

export interface SupplierBudget {
  supplierId: string;
  supplierName: string;
  total: number;
}

export interface GroupBudget {
  groupId: string;
  supplierIds: string[];
  supplierNames: string[];
  availableItems: string[];
  missingItems: string[];
  coverage: number;
  total: number;
  supplierBudgets: SupplierBudget[];
}

/** Calcula o menor custo consolidado por item entre fornecedores do mesmo perfil. */
export function calculateGroupBudgets(groups: CoverageGroup[]): GroupBudget[] {
  return groups.map((group) => {
    const supplierBudgets = group.suppliers.map((entry) => ({
      supplierId: entry.supplier.id,
      supplierName: entry.supplier.name,
      total: money(entry.availableItems.reduce((sum, item) => sum + item.subtotal, 0)),
    }));
    const availableItems = group.suppliers[0]?.availableItems || [];
    const total = availableItems.reduce((sum, item) => {
      const candidates = group.suppliers
        .map(
          (entry) => entry.availableItems.find((candidate) => candidate.id === item.id)?.subtotal
        )
        .filter((value): value is number => value !== undefined);
      return sum + (candidates.length ? Math.min(...candidates) : 0);
    }, 0);

    return {
      groupId: group.groupId,
      supplierIds: group.suppliers.map((entry) => entry.supplier.id),
      supplierNames: group.suppliers.map((entry) => entry.supplier.name),
      availableItems: group.availableItemIds,
      missingItems: group.missingItemIds,
      coverage: group.coverage,
      total: money(total),
      supplierBudgets,
    };
  });
}

export function selectBestGroup(groups: GroupBudget[]): string | null {
  if (!groups.length) return null;
  return [...groups].sort(
    (left, right) => right.coverage - left.coverage || left.total - right.total
  )[0].groupId;
}

function money(value: number): number {
  return Math.round((value + Number.EPSILON) * 100) / 100;
}
