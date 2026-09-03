import { QuotationResult } from '../services/api';

export function PriceVariationChart({ first, second }: { first: QuotationResult[]; second: QuotationResult[] }) {
  const firstPrice = lowestPrice(first);
  const secondPrice = lowestPrice(second);
  if (firstPrice === null && secondPrice === null) return <p className="text-xs text-gray-500">Sem preços comparáveis para gerar o gráfico.</p>;
  const maximum = Math.max(firstPrice || 0, secondPrice || 0, 1);
  const change = firstPrice && secondPrice ? ((secondPrice - firstPrice) / firstPrice) * 100 : null;
  return <div className="mt-4" role="img" aria-label="Gráfico de variação do menor preço entre as duas pesquisas"><div className="mb-2 flex items-center justify-between text-xs text-gray-500"><span>Variação do menor preço</span><span>{change === null ? 'Dados parciais' : `${change > 0 ? '+' : ''}${change.toFixed(1)}%`}</span></div><div className="flex h-24 items-end gap-6 border-b border-gray-300 px-4"><Bar label="Data 1" price={firstPrice} height={firstPrice === null ? 0 : (firstPrice / maximum) * 100} /><Bar label="Data 2" price={secondPrice} height={secondPrice === null ? 0 : (secondPrice / maximum) * 100} /></div></div>;
}

function Bar({ label, price, height }: { label: string; price: number | null; height: number }) {
  return <div className="flex h-full flex-1 flex-col items-center justify-end gap-1"><span className="text-xs font-medium">{price === null ? '—' : price.toFixed(2)}</span><div className="w-full max-w-16 rounded-t bg-primary-500" style={{ height: `${Math.max(height, price === null ? 0 : 4)}%` }} /><span className="text-xs text-gray-500">{label}</span></div>;
}

function lowestPrice(results: QuotationResult[]): number | null {
  const prices = results.filter((result) => result.price !== null).map((result) => result.price as number);
  return prices.length ? Math.min(...prices) : null;
}
