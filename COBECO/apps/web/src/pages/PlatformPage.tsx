import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export function PlatformPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleDeleteAccount = async () => {
    try {
      const response = await fetch('/api/platform/account', {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Erro ao deletar conta');
      }

      logout();
      navigate('/');
    } catch (error) {
      alert('Erro ao deletar conta. Tente novamente.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar (futuro) */}
      <div className="flex">
        <aside className="w-64 bg-white shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Menu</h2>
          <nav className="space-y-2">
            <div className="px-4 py-2 text-gray-600">Minhas Listas (em breve)</div>
            <div className="px-4 py-2 text-gray-600">Histórico (em breve)</div>
          </nav>

          <hr className="my-6" />

          <div className="space-y-2">
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 rounded"
              aria-label="Delete account"
            >
              Deletar Conta
            </button>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          <div className="max-w-4xl">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Bem-vindo, {user?.name}!</h1>
            <p className="text-gray-600 mb-8">E-mail: {user?.email}</p>

            <div className="card">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Suas Listas</h2>
              <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                <div className="text-center">
                  <svg
                    className="mx-auto h-12 w-12 text-gray-400 mb-4"
                    stroke="currentColor"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <p className="text-gray-500 font-medium">Suas listas — em breve</p>
                  <p className="text-gray-400 text-sm mt-2">
                    Essa funcionalidade estará disponível em breve
                  </p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          role="dialog"
          aria-modal="true"
          aria-labelledby="delete-dialog-title"
        >
          <div className="bg-white rounded-lg p-6 max-w-sm mx-4">
            <h2 id="delete-dialog-title" className="text-xl font-bold text-gray-900 mb-4">
              Deletar Conta
            </h2>
            <p className="text-gray-600 mb-6">
              Esta ação é irreversível. Todos os seus dados serão permanentemente excluídos.
            </p>
            <div className="flex gap-4">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="btn-secondary flex-1"
                aria-label="Cancel"
              >
                Cancelar
              </button>
              <button
                onClick={handleDeleteAccount}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors"
                aria-label="Confirm delete"
              >
                Deletar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
