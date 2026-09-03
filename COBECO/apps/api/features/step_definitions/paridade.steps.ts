import { Given, Then, When } from '@cucumber/cucumber';
import assert from 'node:assert/strict';
import {
  calculateAvailability,
  CatalogOffer,
  RequestedItem,
} from '../../src/domain/availability.ts';
import { CoverageGroup, groupByCoverageProfile } from '../../src/domain/grouping.ts';

let items: RequestedItem[] = [];
let offers: CatalogOffer[] = [];
let groups: CoverageGroup[] = [];

Given(/^uma lista com os produtos de 1 a 9$/, function () {
  items = Array.from({ length: 9 }, (_, index) => ({
    id: String(index + 1),
    productId: String(index + 1),
    description: `Produto ${index + 1}`,
    quantity: 1,
  }));
});

Given('os fornecedores A a H com as coberturas especificadas', function () {
  const coverage: Record<string, number[]> = {
    A: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    B: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    C: [1, 2, 3, 4, 5, 6, 8, 9],
    D: [1, 2, 4, 5, 8, 9],
    E: [1, 2, 3, 4, 5, 6, 8, 9],
    F: [1, 2, 3, 4, 5, 6, 8, 9],
    G: [1, 3, 4, 5, 8, 9],
    H: [1, 2, 3, 4, 5, 6, 8, 9],
  };
  offers = Object.entries(coverage).flatMap(([supplierId, productIds]) =>
    productIds.map((productId) => ({
      supplierId,
      productId: String(productId),
      price: 10,
      active: true,
    }))
  );
});

When('o motor calcular os grupos de paridade', function () {
  const suppliers = 'ABCDEFGH'.split('').map((id) => ({ id, name: id }));
  groups = groupByCoverageProfile(calculateAvailability(items, suppliers, offers), items.length);
});

Then('serão gerados {int} grupos', function (amount: number) {
  assert.equal(groups.length, amount);
});

Then('os grupos serão {string}', function (expected: string) {
  assert.equal(
    groups.map((group) => group.suppliers.map((entry) => entry.supplier.id).join(',')).join(';'),
    expected
  );
});
