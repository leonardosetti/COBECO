import { useMemo, useState } from 'react';
import { QuotationItem, QuotationResponse, QuotationResult } from '../services/api';
import { exportQuotationCsv, printQuotation } from '../services/export';

type SortMode = 'price' | 'delivery' | 'value';

interface ComparisonPanelProps {
  quotation: QuotationResponse;
  onClose: () => void;
}

export function ComparisonPanel({ quotation, onClose }: ComparisonPanelProps) {
  const [sortMode, setSortMode] = useState<SortMode>('price');

  if (quotation.groups) return <ParityPanel quotation={quotation} onClose={onClose} />;

  return (
    <section className="card" aria-labelledby="comparison-title">
      <div className="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-primary-600">Resultado da cotação</p>
          <h2 id="comparison-title" className="text-2xl font-bold">
            Comparação de ofertas
          </h2>
          <p className="text-sm text-gray-500">
            Pesquisado em {new Date(quotation.requestedAt).toLocaleString('pt-BR')}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            className="btn-secondary"
            onClick={() => exportQuotationCsv(quotation)}
          >
            Exportar CSV
          </button>
          <button type="button" className="btn-secondary" onClick={printQuotation}>
            Imprimir / PDF
          </button>
          <button type="button" className="btn-secondary" onClick={onClose}>
            Fechar
          </button>
        </div>
      </div>

      <div className="mb-6 flex flex-wrap items-center gap-3 border-b border-gray-100 pb-5">
        <label htmlFor="sort-quotation" className="text-sm font-medium text-gray-700">
          Ordenar por
        </label>
        <select
          id="sort-quotation"
          className="input-field max-w-xs"
          value={sortMode}
          onChange={(event) => setSortMode(event.target.value as SortMode)}
        >
          <option value="price">Menor preço</option>
          <option value="delivery">Menor prazo</option>
          <option value="value">Melhor relação preço e prazo</option>
        </select>
      </div>

      <div className="space-y-8">
        {quotation.items.map((item) => (
          <ComparisonItem key={item.itemId || item.description} item={item} sortMode={sortMode} />
        ))}
      </div>
    </section>
  );
}

function ParityPanel({ quotation, onClose }: ComparisonPanelProps) {
  const itemNames = new Map(quotation.items.map((item) => [item.itemId, item.description]));
  const groups = quotation.groups || [];
  return (
    <section className="card" aria-labelledby="comparison-title">
      <div className="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-primary-600">Resultado da cotação</p>
          <h2 id="comparison-title" className="text-2xl font-bold">
            Grupos por paridade
          </h2>
          <p className="text-sm text-gray-500">
            {quotation.meta?.selectedSuppliers} fornecedores · {quotation.meta?.totalItems} itens
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            className="btn-secondary"
            onClick={() => exportQuotationCsv(quotation)}
          >
            Exportar CSV
          </button>
          <button type="button" className="btn-secondary" onClick={printQuotation}>
            Imprimir / PDF
          </button>
          <button type="button" className="btn-secondary" onClick={onClose}>
            Fechar
          </button>
        </div>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        {groups.map((group, index) => {
          const best = group.groupId === quotation.bestGroupId;
          return (
            <article
              key={group.groupId}
              className={`rounded-xl border p-5 ${
                best ? 'border-primary-500 bg-primary-50' : 'border-gray-200'
              }`}
              aria-label={`Grupo ${index + 1}, cobertura ${group.coverage}%`}
            >
              <div className="mb-4 flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-lg font-bold">
                    Grupo {index + 1} · {group.coverage}%
                  </h3>
                  <p className="text-sm text-gray-600">{group.supplierNames.join(', ')}</p>
                </div>
                {best && (
                  <span className="rounded-full bg-primary-600 px-3 py-1 text-xs font-semibold text-white">
                    Melhor orçamento
                  </span>
                )}
              </div>
              <dl className="mb-4 grid grid-cols-2 gap-3">
                <div>
                  <dt className="text-xs text-gray-500">Menor custo consolidado</dt>
                  <dd className="font-bold">{formatPrice(group.total, 'BRL')}</dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-500">Cobertura</dt>
                  <dd className="font-bold">
                    {group.availableItems.length}/{quotation.meta?.totalItems}
                  </dd>
                </div>
              </dl>
              {group.missingItems.length > 0 ? (
                <div className="rounded-lg bg-amber-50 p-3 text-sm text-amber-900">
                  <p className="font-semibold">Itens ausentes</p>
                  <p>{group.missingItems.map((id) => itemNames.get(id) || id).join(', ')}</p>
                </div>
              ) : (
                <p className="rounded-lg bg-green-50 p-3 text-sm font-medium text-green-800">
                  Todos os itens estão disponíveis.
                </p>
              )}
              <div className="mt-4 border-t pt-3">
                <p className="mb-2 text-xs font-semibold uppercase text-gray-500">
                  Totais por fornecedor
                </p>
                {group.supplierBudgets.map((budget) => (
                  <div key={budget.supplierId} className="flex justify-between text-sm">
                    <span>{budget.supplierName}</span>
                    <strong>{formatPrice(budget.total, 'BRL')}</strong>
                  </div>
                ))}
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

function ComparisonItem({ item, sortMode }: { item: QuotationItem; sortMode: SortMode }) {
  const results = useMemo(() => sortResults(item.results, sortMode), [item.results, sortMode]);
  const failedProviders = item.providers.filter((provider) => provider.state !== 'success');

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
        <div>
          <h3 className="text-lg font-bold">{item.description}</h3>
          <p className="text-sm text-gray-500">Quantidade: {item.quantity}</p>
        </div>
        <span className="text-sm text-gray-500">{results.length} oferta(s)</span>
      </div>
      {failedProviders.length > 0 && (
        <div className="mb-4 space-y-2" role="status">
          {failedProviders.map((provider) => (
            <p
              key={provider.providerSlug}
              className="rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-800"
            >
              {provider.providerName}: {provider.message}
            </p>
          ))}
        </div>
      )}
      {results.length === 0 ? (
        <p className="rounded-lg bg-gray-50 p-5 text-center text-sm text-gray-500">
          Nenhuma oferta encontrada para este item.
        </p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {results.map((result) => (
            <OfferCard key={result.id} result={result} item={item} />
          ))}
        </div>
      )}
    </div>
  );
}

function OfferCard({ result, item }: { result: QuotationResult; item: QuotationItem }) {
  const badges = [
    item.highlights.lowestPriceIds.includes(result.id) ? 'Melhor preço' : '',
    item.highlights.fastestDeliveryIds.includes(result.id) ? 'Menor prazo' : '',
    item.highlights.bestValueIds.includes(result.id) ? 'Melhor relação' : '',
  ].filter(Boolean);

  return (
    <article
      className={`rounded-xl border p-4 ${
        badges.length ? 'border-primary-300 bg-primary-50/40' : 'border-gray-200'
      }`}
    >
      <div className="mb-3 flex flex-wrap items-start justify-between gap-2">
        <div>
          <p className="font-semibold">{result.productName}</p>
          <p className="text-sm text-gray-500">{result.retailerName}</p>
        </div>
        {badges.length > 0 && (
          <span className="rounded-full bg-primary-100 px-2 py-1 text-xs font-medium text-primary-800">
            {badges[0]}
          </span>
        )}
      </div>
      <dl className="grid grid-cols-2 gap-3 text-sm">
        <div>
          <dt className="text-gray-500">Preço</dt>
          <dd className="font-semibold">{formatPrice(result.price, result.currency)}</dd>
        </div>
        <div>
          <dt className="text-gray-500">Entrega</dt>
          <dd className="font-semibold">{formatDelivery(result.deliveryDays)}</dd>
        </div>
      </dl>
      {badges.length > 1 && (
        <p className="mt-3 text-xs text-primary-700">{badges.slice(1).join(' · ')}</p>
      )}
      {result.incompleteFields.length > 0 && (
        <p className="mt-3 text-xs text-amber-700">
          Dados incompletos:{' '}
          {result.incompleteFields
            .map((field) => (field === 'price' ? 'preço' : 'prazo'))
            .join(' e ')}
          .
        </p>
      )}
      <a
        className="mt-4 inline-block text-sm font-medium"
        href={result.redirectUrl}
        target="_blank"
        rel="noopener noreferrer"
      >
        Ver no lojista
      </a>
    </article>
  );
}

function sortResults(results: QuotationResult[], mode: SortMode): QuotationResult[] {
  const copy = [...results];
  const scoreMap = mode === 'value' ? createValueScores(results) : null;
  return copy.sort((left, right) => {
    const leftValue =
      mode === 'value' ? scoreMap?.get(left.id) : mode === 'price' ? left.price : left.deliveryDays;
    const rightValue =
      mode === 'value'
        ? scoreMap?.get(right.id)
        : mode === 'price'
        ? right.price
        : right.deliveryDays;
    if (leftValue === null || leftValue === undefined) return 1;
    if (rightValue === null || rightValue === undefined) return -1;
    return leftValue - rightValue;
  });
}

function createValueScores(results: QuotationResult[]): Map<string, number> {
  const complete = results.filter(
    (result) => result.price !== null && result.deliveryDays !== null
  );
  const prices = complete.map((result) => result.price as number);
  const deliveries = complete.map((result) => result.deliveryDays as number);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const minDelivery = Math.min(...deliveries);
  const maxDelivery = Math.max(...deliveries);
  return new Map(
    complete.map((result) => [
      result.id,
      normalize(result.price as number, minPrice, maxPrice) +
        normalize(result.deliveryDays as number, minDelivery, maxDelivery),
    ])
  );
}

function normalize(value: number, minimum: number, maximum: number): number {
  return maximum === minimum ? 0 : (value - minimum) / (maximum - minimum);
}

function formatPrice(price: number | null, currency: string): string {
  if (price === null) return 'Não informado';
  try {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(price);
  } catch {
    return `${currency} ${price.toFixed(2)}`;
  }
}

function formatDelivery(deliveryDays: number | null): string {
  return deliveryDays === null
    ? 'Não informado'
    : `${deliveryDays} ${deliveryDays === 1 ? 'dia' : 'dias'}`;
}
