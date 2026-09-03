import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { apiService, SharedList } from '../services/api';

export function SharedListPage() {
  const { token } = useParams<{ token: string }>();
  const [list, setList] = useState<SharedList | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token) return;
    apiService.getSharedList(token).then(setList).catch((requestError) => setError(apiService.getErrorMessage(requestError)));
  }, [token]);

  if (error) return <div className="page-container"><div className="card text-center text-red-700" role="alert">{error}</div></div>;
  if (!list) return <div className="page-container"><div className="card text-center text-gray-500" aria-busy="true">Carregando lista compartilhada...</div></div>;
  return <main className="page-container"><section className="card mx-auto max-w-2xl"><p className="text-sm font-medium text-primary-600">Lista compartilhada</p><h1 className="mb-6 text-3xl font-bold">{list.name}</h1><ul className="divide-y divide-gray-100">{list.items.map((item) => <li key={item.id} className="flex justify-between gap-4 py-4"><span>{item.description}</span><span className="text-sm text-gray-500">Quantidade: {item.quantity}</span></li>)}</ul><p className="mt-6 text-xs text-gray-500">Esta lista é somente para visualização.</p></section></main>;
}
