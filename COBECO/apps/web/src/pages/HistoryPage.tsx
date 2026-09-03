import { useEffect, useState } from 'react';
import { ComparisonPanel } from '../components/ComparisonPanel';
import { PriceVariationChart } from '../components/PriceVariationChart';
import { useAuth } from '../context/AuthContext';
import {
  apiService,
  PaginatedQuotationHistory,
  QuotationComparisonResponse,
  QuotationHistorySummary,
  QuotationResponse,
  QuotationResult,
} from '../services/api';

const EMPTY_PAGE: PaginatedQuotationHistory = { items: [], total: 0, page: 1, pageSize: 10, totalPages: 1 };

export function HistoryPage() {
  const { user } = useAuth();
  const [historyPage, setHistoryPage] = useState<PaginatedQuotationHistory>(EMPTY_PAGE);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [quotation, setQuotation] = useState<QuotationResponse | null>(null);
  const [comparison, setComparison] = useState<QuotationComparisonResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadHistory(page: number) {
    setLoading(true);
    try { setHistoryPage(await apiService.getQuotationHistory(page)); }
    catch (requestError) { setError(apiService.getErrorMessage(requestError)); }
    finally { setLoading(false); }
  }

  useEffect(() => { loadHistory(1); }, []);

  async function reopen(id: string) {
    setError('');
    try { setQuotation(await apiService.getQuotation(id)); setComparison(null); }
    catch (requestError) { setError(apiService.getErrorMessage(requestError)); }
  }

  async function compare() {
    if (selectedIds.length !== 2) return;
    setError('');
    try { setComparison(await apiService.compareQuotations(selectedIds[0], selectedIds[1])); setQuotation(null); }
    catch (requestError) { setError(apiService.getErrorMessage(requestError)); }
  }

  async function remove(id: string) {
    if (!window.confirm('Excluir esta cotação do histórico?')) return;
    try {
      await apiService.deleteQuotation(id);
      setSelectedIds((current) => current.filter((selectedId) => selectedId !== id));
      if (quotation?.quotationId === id) setQuotation(null);
      await loadHistory(historyPage.page);
    } catch (requestError) { setError(apiService.getErrorMessage(requestError)); }
  }

  function toggleSelection(id: string) {
    setSelectedIds((current) => current.includes(id) ? current.filter((selectedId) => selectedId !== id) : current.length < 2 ? [...current, id] : [current[1], id]);
  }

  return <div className="min-h-screen bg-gray-50"><div className="page-container">
    <header className="mb-8"><p className="text-sm font-medium text-primary-600">Plataforma</p><h1 className="text-3xl font-bold">Histórico de cotações</h1><p className="text-gray-600">Reabra pesquisas anteriores ou compare o mesmo produto em datas diferentes.</p></header>
    {error && <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700" role="alert">{error}</div>}
    <RecommendationStrip items={historyPage.items} />
    <section className="card" aria-busy={loading}>
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3"><h2 className="text-xl font-bold">Pesquisas anteriores</h2><button className="btn-primary" onClick={compare} disabled={selectedIds.length !== 2}>Comparar selecionadas</button></div>
      {loading ? <p className="text-gray-500">Carregando histórico...</p> : historyPage.items.length === 0 ? <p className="rounded-lg bg-gray-50 p-6 text-center text-gray-500">Nenhuma cotação realizada ainda.</p> : <><div className="divide-y divide-gray-100">{historyPage.items.map((item) => <HistoryRow key={item.id} item={item} selected={selectedIds.includes(item.id)} onToggle={() => toggleSelection(item.id)} onReopen={() => reopen(item.id)} onRemove={() => remove(item.id)} />)}</div><div className="mt-5 flex flex-wrap items-center justify-between gap-3 border-t border-gray-100 pt-4 text-sm"><span>Página {historyPage.page} de {historyPage.totalPages} · {historyPage.total} registro(s)</span><div className="flex gap-2"><button className="btn-secondary" onClick={() => loadHistory(historyPage.page - 1)} disabled={historyPage.page <= 1 || loading}>Anterior</button><button className="btn-secondary" onClick={() => loadHistory(historyPage.page + 1)} disabled={historyPage.page >= historyPage.totalPages || loading}>Próxima</button></div></div></>}
    </section>
    {quotation && <div className="mt-6"><ComparisonPanel quotation={quotation} onClose={() => setQuotation(null)} /></div>}
    {comparison && <ComparisonView comparison={comparison} onClose={() => setComparison(null)} />}
    {user && <TestimonialForm authorName={user.name} />}
  </div></div>;
}

function HistoryRow({ item, selected, onToggle, onReopen, onRemove }: { item: QuotationHistorySummary; selected: boolean; onToggle: () => void; onReopen: () => void; onRemove: () => void }) {
  return <div className="flex flex-wrap items-center gap-4 py-4"><input type="checkbox" checked={selected} onChange={onToggle} aria-label={`Selecionar cotação de ${new Date(item.requestedAt).toLocaleString('pt-BR')}`} /><div className="min-w-0 flex-1"><p className="font-medium">{item.mode === 'list' ? item.listName || 'Lista' : item.descriptions[0] || 'Item isolado'}</p><p className="text-sm text-gray-500">{new Date(item.requestedAt).toLocaleString('pt-BR')} · {item.itemCount} item(ns) · <span className={item.status === 'failed' ? 'text-red-600' : 'text-gray-500'}>{statusLabel(item.status)}</span></p><p className="truncate text-xs text-gray-400">{item.descriptions.join(' · ') || 'Sem resultados persistidos'}</p></div><div className="flex gap-3 text-sm"><button type="button" className="text-primary-700 underline" onClick={onReopen}>Reabrir</button><button type="button" className="text-red-600 underline" onClick={onRemove}>Excluir</button></div></div>;
}

function ComparisonView({ comparison, onClose }: { comparison: QuotationComparisonResponse; onClose: () => void }) {
  return <section className="card mt-6" aria-labelledby="history-comparison-title"><div className="mb-6 flex flex-wrap justify-between gap-3"><div><p className="text-sm font-medium text-primary-600">Comparação histórica</p><h2 id="history-comparison-title" className="text-2xl font-bold">Produtos em comum</h2><p className="text-sm text-gray-500">{formatDate(comparison.first.requestedAt)} × {formatDate(comparison.second.requestedAt)}</p></div><button type="button" className="btn-secondary" onClick={onClose}>Fechar</button></div><div className="space-y-6">{comparison.items.map((item) => <div key={item.description} className="border-t border-gray-100 pt-5"><h3 className="mb-3 font-bold">{item.description}</h3><div className="grid gap-4 md:grid-cols-2"><HistoricalOffers title={`Pesquisa de ${formatDate(item.first.requestedAt)}`} results={item.first.results} /><HistoricalOffers title={`Pesquisa de ${formatDate(item.second.requestedAt)}`} results={item.second.results} /></div><PriceVariationChart first={item.first.results} second={item.second.results} /></div>)}</div></section>;
}

function HistoricalOffers({ title, results }: { title: string; results: QuotationResult[] }) {
  return <div className="rounded-lg bg-gray-50 p-4"><p className="mb-3 text-sm font-medium text-gray-700">{title}</p>{results.length === 0 ? <p className="text-sm text-gray-500">Sem resultados.</p> : <ul className="space-y-2">{results.slice(0, 5).map((result) => <li key={result.id} className="flex justify-between gap-3 text-sm"><span className="truncate">{result.retailerName}</span><span className="font-semibold">{result.price === null ? 'Preço indisponível' : new Intl.NumberFormat('pt-BR', { style: 'currency', currency: result.currency }).format(result.price)}</span></li>)}</ul>}</div>;
}

function formatDate(value: string): string { return new Date(value).toLocaleDateString('pt-BR'); }
function statusLabel(status: QuotationHistorySummary['status']): string { return status === 'completed' ? 'concluída' : status === 'failed' ? 'falhou' : 'em andamento'; }

function RecommendationStrip({ items }: { items: QuotationHistorySummary[] }) {
  const counts = new Map<string, number>();
  items.flatMap((item) => item.descriptions).forEach((description) => counts.set(description, (counts.get(description) || 0) + 1));
  const recommendations = [...counts.entries()].sort((left, right) => right[1] - left[1]).slice(0, 3);
  if (!recommendations.length) return null;
  return <section className="card mb-6 border-primary-100 bg-primary-50/50" aria-labelledby="recommendations-title"><h2 id="recommendations-title" className="mb-2 font-bold">Sugestões para você</h2><p className="mb-3 text-sm text-gray-600">Produtos que aparecem com mais frequência no seu histórico.</p><div className="flex flex-wrap gap-2">{recommendations.map(([description, count]) => <span key={description} className="rounded-full bg-white px-3 py-1 text-sm text-primary-800">{description} · {count} pesquisa(s)</span>)}</div></section>;
}

function TestimonialForm({ authorName }: { authorName: string }) {
  const [content, setContent] = useState('');
  const [sent, setSent] = useState(false);
  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!content.trim()) return;
    await apiService.submitTestimonial(authorName, content);
    setContent(''); setSent(true);
  }
  return <section className="card mt-6" aria-labelledby="testimonial-title"><h2 id="testimonial-title" className="mb-2 text-xl font-bold">Compartilhe sua experiência</h2><p className="mb-4 text-sm text-gray-600">Seu depoimento será revisado antes de aparecer na página pública.</p>{sent && <p className="mb-3 text-sm text-green-700" role="status">Depoimento enviado para moderação.</p>}<form onSubmit={submit} className="flex flex-col gap-3 sm:flex-row"><label className="sr-only" htmlFor="testimonial-content">Seu depoimento</label><textarea id="testimonial-content" className="input-field min-h-20" value={content} onChange={(event) => setContent(event.target.value)} maxLength={500} placeholder="Conte como foi sua experiência..." /><button className="btn-primary self-end sm:self-center" disabled={content.trim().length < 10}>Enviar</button></form></section>;
}
