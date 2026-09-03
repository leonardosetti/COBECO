import { FormEvent, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Theme, useTheme } from '../context/ThemeContext';
import { ComparisonPanel } from '../components/ComparisonPanel';
import {
  apiService,
  CatalogProduct,
  Category,
  ListItem,
  ProductList,
  QuotationResponse,
  Supplier,
  SupplierAvailability,
} from '../services/api';

/** RF11: limites da sessão de comparação. */
const MIN_SUPPLIERS = 2;
const MAX_SUPPLIERS = 10;

export function ListsPage() {
  const { user, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const navigate = useNavigate();
  const [lists, setLists] = useState<ProductList[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [newName, setNewName] = useState('');
  const [itemName, setItemName] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [bulk, setBulk] = useState('');
  const [editingList, setEditingList] = useState<string | null>(null);
  const [editingName, setEditingName] = useState('');
  const [editingItem, setEditingItem] = useState<ListItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [quoting, setQuoting] = useState(false);
  const [quotation, setQuotation] = useState<QuotationResponse | null>(null);
  const [shareLink, setShareLink] = useState('');
  const [error, setError] = useState('');
  const [categories, setCategories] = useState<Category[]>([]);
  const [newCategoryId, setNewCategoryId] = useState('');
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [products, setProducts] = useState<CatalogProduct[]>([]);
  const [supplierIds, setSupplierIds] = useState<string[]>([]);
  const [supplierStats, setSupplierStats] = useState<SupplierAvailability[]>([]);
  // RF12: piso de disponibilidade exigido dos fornecedores exibidos.
  const [minAvailability, setMinAvailability] = useState(0);

  const selected = lists.find((list) => list.id === selectedId) || null;
  const replace = (list: ProductList) =>
    setLists((current) => current.map((item) => (item.id === list.id ? list : item)));
  const message = (requestError: unknown) => setError(apiService.getErrorMessage(requestError));

  useEffect(() => {
    apiService
      .getLists()
      .then((loaded) => {
        setLists(loaded);
        setSelectedId(loaded[0]?.id || null);
      })
      .catch(message)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    apiService
      .getCategories()
      .then((loaded) => {
        setCategories(loaded);
        setNewCategoryId((current) => current || loaded[0]?.id || '');
      })
      .catch(message);
  }, []);

  useEffect(() => {
    const categoryId = selected?.categoryId || categories[0]?.id;
    if (!categoryId) return;
    Promise.all([apiService.getSuppliers(categoryId), apiService.getCatalogProducts(categoryId)])
      .then(([loadedSuppliers, loadedProducts]) => {
        setSuppliers(loadedSuppliers);
        setProducts(loadedProducts);
        // RF11: a seleção começa cheia, respeitando o teto de fornecedores.
        setSupplierIds(loadedSuppliers.slice(0, MAX_SUPPLIERS).map((supplier) => supplier.id));
      })
      .catch(message);
  }, [selected?.categoryId, categories]);

  // RF12: a disponibilidade depende dos itens da lista, então recarrega quando
  // a lista muda ou ganha/perde itens.
  useEffect(() => {
    if (!selected || selected.items.length === 0) {
      setSupplierStats([]);
      return;
    }
    apiService.getListSupplierAvailability(selected.id).then(setSupplierStats).catch(message);
  }, [selected?.id, selected?.items.length]);

  // E3 do Fluxo 3: mexer no filtro não pode desmarcar quem continua elegível,
  // mas quem saiu da lista precisa sair da seleção.
  useEffect(() => {
    setSupplierIds((current) =>
      current.filter((id) => {
        const stat = supplierStats.find((candidate) => candidate.id === id);
        return !stat || stat.availability >= minAvailability;
      })
    );
  }, [minAvailability, supplierStats]);

  useEffect(() => {
    setQuotation(null);
    setShareLink('');
    setMinAvailability(0);
  }, [selectedId]);

  async function createList(event: FormEvent) {
    event.preventDefault();
    if (!newName.trim()) return;
    setSaving(true);
    try {
      const list = await apiService.createList(newName, newCategoryId || undefined);
      setLists((current) => [list, ...current]);
      setSelectedId(list.id);
      setNewName('');
    } catch (requestError) {
      message(requestError);
    } finally {
      setSaving(false);
    }
  }

  async function renameList(event: FormEvent, id: string) {
    event.preventDefault();
    if (!editingName.trim()) return;
    setSaving(true);
    try {
      replace(await apiService.updateList(id, editingName));
      setEditingList(null);
    } catch (requestError) {
      message(requestError);
    } finally {
      setSaving(false);
    }
  }

  async function deleteList(list: ProductList) {
    if (!window.confirm(`Excluir a lista "${list.name}"?`)) return;
    try {
      await apiService.deleteList(list.id);
      const remaining = lists.filter((item) => item.id !== list.id);
      setLists(remaining);
      setSelectedId(remaining[0]?.id || null);
    } catch (requestError) {
      message(requestError);
    }
  }

  async function duplicateList(list: ProductList) {
    try {
      const copy = await apiService.duplicateList(list.id);
      setLists((current) => [copy, ...current]);
      setSelectedId(copy.id);
    } catch (requestError) {
      message(requestError);
    }
  }

  async function addItem(event: FormEvent) {
    event.preventDefault();
    if (!selected || !itemName.trim()) return;
    setSaving(true);
    try {
      const productId = products.find((product) => product.name === itemName)?.id || null;
      replace(await apiService.addListItem(selected.id, itemName, quantity, productId));
      setItemName('');
      setQuantity(1);
    } catch (requestError) {
      message(requestError);
    } finally {
      setSaving(false);
    }
  }

  async function addBulk(event: FormEvent) {
    event.preventDefault();
    if (!selected || !bulk.trim()) return;
    setSaving(true);
    try {
      replace(await apiService.addBulkListItems(selected.id, bulk));
      setBulk('');
    } catch (requestError) {
      message(requestError);
    } finally {
      setSaving(false);
    }
  }

  async function updateItem(event: FormEvent) {
    event.preventDefault();
    if (!selected || !editingItem?.description.trim()) return;
    setSaving(true);
    try {
      replace(
        await apiService.updateListItem(
          selected.id,
          editingItem.id,
          editingItem.description,
          editingItem.quantity
        )
      );
      setEditingItem(null);
    } catch (requestError) {
      message(requestError);
    } finally {
      setSaving(false);
    }
  }

  async function deleteItem(item: ListItem) {
    if (!selected || !window.confirm(`Remover "${item.description}"?`)) return;
    try {
      replace(await apiService.deleteListItem(selected.id, item.id));
    } catch (requestError) {
      message(requestError);
    }
  }

  async function quoteItem(description: string) {
    setError('');
    setQuoting(true);
    try {
      setQuotation(await apiService.quoteItem(description));
    } catch (requestError) {
      message(requestError);
    } finally {
      setQuoting(false);
    }
  }

  async function quoteSelectedList() {
    if (!selected) return;
    setError('');
    setQuoting(true);
    try {
      setQuotation(await apiService.quoteList(selected.id, supplierIds));
    } catch (requestError) {
      message(requestError);
    } finally {
      setQuoting(false);
    }
  }

  async function shareSelectedList() {
    if (!selected) return;
    setError('');
    try {
      const share = await apiService.shareList(selected.id);
      setShareLink(`${window.location.origin}${share.urlPath}`);
    } catch (requestError) {
      message(requestError);
    }
  }

  async function deleteAccount() {
    if (!window.confirm('Excluir sua conta e todos os dados?')) return;
    try {
      await apiService.deleteAccount();
      logout();
      navigate('/');
    } catch (requestError) {
      message(requestError);
    }
  }

  const statById = new Map(supplierStats.map((stat) => [stat.id, stat]));
  const visibleSuppliers = suppliers.filter((supplier) => {
    const stat = statById.get(supplier.id);
    return !stat || stat.availability >= minAvailability;
  });
  const selectionError =
    supplierIds.length < MIN_SUPPLIERS
      ? `Selecione ao menos ${MIN_SUPPLIERS} fornecedores para comparar`
      : supplierIds.length > MAX_SUPPLIERS
        ? `Selecione no máximo ${MAX_SUPPLIERS} fornecedores por comparação`
        : '';

  function toggleSupplier(id: string, checked: boolean) {
    setSupplierIds((current) =>
      checked ? [...new Set([...current, id])] : current.filter((entry) => entry !== id)
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="page-container">
        <header className="mb-8">
          <p className="text-sm font-medium text-primary-600">Área da plataforma</p>
          <h1 className="text-3xl font-bold">Olá, {user?.name}!</h1>
          <p className="text-gray-600">Organize os produtos que você quer cotar.</p>
        </header>
        {error && (
          <div
            className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700"
            role="alert"
          >
            {error}{' '}
            <button className="ml-3 underline" onClick={() => setError('')}>
              Fechar
            </button>
          </div>
        )}
        <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
          <aside className="card h-fit">
            <section aria-labelledby="account-settings">
              <h2 id="account-settings" className="text-sm font-semibold text-gray-500">
                Configurações da conta
              </h2>
              <p className="truncate text-sm" title={user?.email}>
                {user?.email}
              </p>

              <div className="mt-4">
                <label className="form-label" htmlFor="theme">
                  Tema
                </label>
                <select
                  id="theme"
                  className="input-field"
                  value={theme}
                  onChange={(event) => setTheme(event.target.value as Theme)}
                >
                  <option value="light">Claro</option>
                  <option value="dark">Escuro</option>
                </select>
              </div>

              <button className="mt-4 text-sm text-red-600 underline" onClick={deleteAccount}>
                Excluir minha conta
              </button>
            </section>
            <hr className="my-6" />
            <div className="mb-4 flex justify-between">
              <h2 className="text-lg font-bold">Minhas listas</h2>
              <span className="rounded-full bg-primary-50 px-2 py-1 text-xs text-primary-700">
                {lists.length}
              </span>
            </div>
            <form onSubmit={createList} className="mb-5 space-y-2">
              <label className="sr-only" htmlFor="new-list">
                Nome da nova lista
              </label>
              <div className="flex gap-2">
                <input
                  id="new-list"
                  className="input-field min-w-0"
                  placeholder="Nova lista"
                  value={newName}
                  onChange={(event) => setNewName(event.target.value)}
                  maxLength={80}
                />
                <button className="btn-primary px-3" disabled={saving} aria-label="Criar lista">
                  +
                </button>
              </div>
              <label className="sr-only" htmlFor="new-list-category">
                Categoria
              </label>
              <select
                id="new-list-category"
                className="input-field"
                value={newCategoryId}
                onChange={(event) => setNewCategoryId(event.target.value)}
              >
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </form>
            {loading ? (
              <p className="text-sm text-gray-500">Carregando listas...</p>
            ) : lists.length === 0 ? (
              <p className="text-sm text-gray-500">Você ainda não tem listas.</p>
            ) : (
              <div className="space-y-2">
                {lists.map((list) => (
                  <div
                    key={list.id}
                    className={`rounded-lg border p-3 ${
                      selectedId === list.id
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-200'
                    }`}
                  >
                    {editingList === list.id ? (
                      <form onSubmit={(event) => renameList(event, list.id)} className="space-y-2">
                        <input
                          className="input-field"
                          value={editingName}
                          onChange={(event) => setEditingName(event.target.value)}
                          autoFocus
                        />
                        <div className="flex gap-2">
                          <button className="btn-primary text-xs" disabled={saving}>
                            Salvar
                          </button>
                          <button
                            type="button"
                            className="btn-secondary text-xs"
                            onClick={() => setEditingList(null)}
                          >
                            Cancelar
                          </button>
                        </div>
                      </form>
                    ) : (
                      <>
                        <button className="w-full text-left" onClick={() => setSelectedId(list.id)}>
                          <span className="block font-semibold">{list.name}</span>
                          <span className="text-xs text-gray-500">
                            {list.items.length} {list.items.length === 1 ? 'item' : 'itens'}
                          </span>
                        </button>
                        <div className="mt-2 flex gap-3 text-xs">
                          <button
                            className="text-primary-700 underline"
                            onClick={() => {
                              setEditingList(list.id);
                              setEditingName(list.name);
                            }}
                          >
                            Renomear
                          </button>
                          <button
                            className="text-primary-700 underline"
                            onClick={() => duplicateList(list)}
                          >
                            Duplicar
                          </button>
                          <button
                            className="text-red-600 underline"
                            onClick={() => deleteList(list)}
                          >
                            Excluir
                          </button>
                        </div>
                      </>
                    )}
                  </div>
                ))}
              </div>
            )}
          </aside>
          <main className="space-y-6">
            {!selected ? (
              <section className="card py-16 text-center">
                <h2 className="mb-2 text-xl font-bold">Comece criando uma lista</h2>
                <p className="text-gray-600">Depois, adicione os produtos que deseja comparar.</p>
              </section>
            ) : (
              <>
                <section className="card">
                  <div className="mb-4">
                    <label className="form-label" htmlFor="min-availability">
                      Disponibilidade mínima: {minAvailability}%
                    </label>
                    <input
                      id="min-availability"
                      type="range"
                      min={0}
                      max={100}
                      step={5}
                      value={minAvailability}
                      onChange={(event) => setMinAvailability(Number(event.target.value))}
                      className="w-full max-w-sm accent-primary-600"
                      title="Mostra apenas fornecedores que atendem ao menos este percentual dos itens da lista"
                      disabled={supplierStats.length === 0}
                    />
                    <p className="text-xs text-gray-500">
                      {supplierStats.length === 0
                        ? 'Adicione itens à lista para ver a disponibilidade de cada fornecedor.'
                        : `${visibleSuppliers.length} de ${suppliers.length} fornecedores atendem ao filtro.`}
                    </p>
                  </div>
                  <fieldset>
                    <legend className="mb-3 font-semibold">
                      Fornecedores da comparação
                      <span className="ml-2 text-sm font-normal text-gray-600">
                        {supplierIds.length} selecionados
                      </span>
                    </legend>
                    {visibleSuppliers.length === 0 ? (
                      <p className="rounded-lg bg-gray-50 p-4 text-sm text-gray-600">
                        Nenhum fornecedor atende ao filtro. Reduza a disponibilidade mínima.
                      </p>
                    ) : (
                      <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
                        {visibleSuppliers.map((supplier) => {
                          const stat = statById.get(supplier.id);
                          return (
                            <label
                              key={supplier.id}
                              className="flex items-center gap-2 rounded-lg border p-2 text-sm"
                            >
                              <input
                                type="checkbox"
                                checked={supplierIds.includes(supplier.id)}
                                onChange={(event) =>
                                  toggleSupplier(supplier.id, event.target.checked)
                                }
                              />
                              <span className="min-w-0">
                                <span className="block truncate">{supplier.name}</span>
                                {stat && (
                                  <span className="text-xs text-gray-500">
                                    {stat.availableItems}/{stat.totalItems} itens (
                                    {stat.availability}%)
                                  </span>
                                )}
                              </span>
                            </label>
                          );
                        })}
                      </div>
                    )}
                    <div className="mt-3 flex gap-4 text-sm">
                      <button
                        type="button"
                        className="text-primary-700 underline"
                        onClick={() =>
                          setSupplierIds(
                            visibleSuppliers
                              .slice(0, MAX_SUPPLIERS)
                              .map((supplier) => supplier.id)
                          )
                        }
                      >
                        Selecionar todos
                      </button>
                      <button
                        type="button"
                        className="text-primary-700 underline"
                        onClick={() => setSupplierIds([])}
                      >
                        Limpar seleção
                      </button>
                    </div>
                  </fieldset>
                  <div className="mt-4 flex flex-wrap items-center justify-between gap-2">
                    <p className="text-sm text-red-600" role="status">
                      {selectionError}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <button
                        type="button"
                        className="btn-secondary"
                        onClick={shareSelectedList}
                        disabled={selected.items.length === 0}
                      >
                        Compartilhar lista
                      </button>
                      <button
                        className="btn-primary"
                        onClick={quoteSelectedList}
                        disabled={
                          quoting || selected.items.length === 0 || Boolean(selectionError)
                        }
                      >
                        {quoting ? 'Cotando...' : 'Cotar lista completa'}
                      </button>
                    </div>
                  </div>
                </section>
                <section className="card">
                  <div className="mb-6 flex flex-wrap justify-between gap-3">
                    <div>
                      <h2 className="text-2xl font-bold">{selected.name}</h2>
                      <p className="text-sm text-gray-500">
                        Adicione os produtos para preparar sua cotação.
                      </p>
                    </div>
                    <span className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-600">
                      {selected.items.length} itens
                    </span>
                  </div>
                  <form
                    onSubmit={addItem}
                    className="grid gap-3 sm:grid-cols-[1fr_120px_auto_auto]"
                  >
                    <div>
                      <label className="form-label" htmlFor="item-name">
                        Produto
                      </label>
                      <input
                        id="item-name"
                        className="input-field"
                        list="catalog-products"
                        placeholder="Selecione ou descreva um produto"
                        value={itemName}
                        onChange={(event) => setItemName(event.target.value)}
                        maxLength={160}
                      />
                      <datalist id="catalog-products">
                        {products.map((product) => (
                          <option key={product.id} value={product.name}>
                            {product.unit}
                          </option>
                        ))}
                      </datalist>
                    </div>
                    <div>
                      <label className="form-label" htmlFor="quantity">
                        Quantidade
                      </label>
                      <input
                        id="quantity"
                        className="input-field"
                        type="number"
                        min={1}
                        max={999}
                        value={quantity}
                        onChange={(event) => setQuantity(Number(event.target.value))}
                      />
                    </div>
                    <button
                      type="button"
                      className="btn-secondary self-end"
                      onClick={() => quoteItem(itemName)}
                      disabled={quoting || !itemName.trim()}
                    >
                      Cotar item
                    </button>
                    <button className="btn-primary self-end" disabled={saving}>
                      Adicionar
                    </button>
                  </form>
                  <form onSubmit={addBulk} className="mt-6 border-t border-gray-100 pt-5">
                    <label className="form-label" htmlFor="bulk">
                      Adicionar em lote
                    </label>
                    <textarea
                      id="bulk"
                      className="input-field min-h-24"
                      placeholder={'Cole um produto por linha:\nCafé 500 g\nLeite integral 1 L'}
                      value={bulk}
                      onChange={(event) => setBulk(event.target.value)}
                    />
                    <div className="mt-2 flex justify-between gap-3">
                      <p className="text-xs text-gray-500">
                        Cada linha vira um item com quantidade 1.
                      </p>
                      <button className="btn-secondary" disabled={saving}>
                        Adicionar linhas
                      </button>
                    </div>
                  </form>
                </section>
                {shareLink && (
                  <div className="rounded-lg border border-primary-100 bg-primary-50 p-4 text-sm">
                    <p className="font-medium text-primary-900">Link de compartilhamento</p>
                    <div className="mt-2 flex flex-wrap items-center gap-2">
                      <input
                        className="input-field min-w-0 flex-1 bg-white"
                        value={shareLink}
                        readOnly
                        aria-label="Link de compartilhamento"
                      />
                      <button
                        type="button"
                        className="btn-secondary"
                        onClick={() => navigator.clipboard?.writeText(shareLink)}
                      >
                        Copiar
                      </button>
                      <button
                        type="button"
                        className="text-red-700 underline"
                        onClick={async () => {
                          await apiService.revokeListShare(selected.id);
                          setShareLink('');
                        }}
                      >
                        Revogar
                      </button>
                    </div>
                  </div>
                )}
                <section className="card">
                  <h2 className="mb-4 text-xl font-bold">Itens da lista</h2>
                  {selected.items.length === 0 ? (
                    <p className="rounded-lg bg-gray-50 p-6 text-center text-gray-500">
                      Nenhum item adicionado ainda.
                    </p>
                  ) : (
                    <div className="divide-y divide-gray-100">
                      {selected.items.map((item) => (
                        <div
                          key={item.id}
                          className="flex flex-wrap items-center justify-between gap-3 py-4 first:pt-0 last:pb-0"
                        >
                          {editingItem?.id === item.id ? (
                            <form onSubmit={updateItem} className="flex flex-1 flex-wrap gap-2">
                              <input
                                className="input-field min-w-48 flex-1"
                                value={editingItem.description}
                                onChange={(event) =>
                                  setEditingItem({
                                    ...editingItem,
                                    description: event.target.value,
                                  })
                                }
                                autoFocus
                              />
                              <input
                                className="input-field w-24"
                                type="number"
                                min={1}
                                max={999}
                                value={editingItem.quantity}
                                onChange={(event) =>
                                  setEditingItem({
                                    ...editingItem,
                                    quantity: Number(event.target.value),
                                  })
                                }
                              />
                              <button className="btn-primary" disabled={saving}>
                                Salvar
                              </button>
                              <button
                                type="button"
                                className="btn-secondary"
                                onClick={() => setEditingItem(null)}
                              >
                                Cancelar
                              </button>
                            </form>
                          ) : (
                            <>
                              <div>
                                <p className="font-medium">{item.description}</p>
                                <p className="text-sm text-gray-500">Quantidade: {item.quantity}</p>
                              </div>
                              <div className="flex gap-3 text-sm">
                                <button
                                  className="text-primary-700 underline"
                                  onClick={() => setEditingItem(item)}
                                >
                                  Editar
                                </button>
                                <button
                                  className="text-red-600 underline"
                                  onClick={() => deleteItem(item)}
                                >
                                  Remover
                                </button>
                              </div>
                            </>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </section>
                {quotation && (
                  <ComparisonPanel quotation={quotation} onClose={() => setQuotation(null)} />
                )}
              </>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
