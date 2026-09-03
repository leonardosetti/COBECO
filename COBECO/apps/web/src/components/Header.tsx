import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export function Header() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="bg-white shadow sticky top-0 z-50">
      <nav className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-primary-600 no-underline">
          COBECO
        </Link>

        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <Link to="/platform" className="text-sm text-primary-600 no-underline">Listas</Link>
              <Link to="/platform/history" className="text-sm text-primary-600 no-underline">Histórico</Link>
              <span className="text-sm text-gray-600">{user?.name}</span>
              <button
                onClick={handleLogout}
                className="btn-secondary text-sm"
                aria-label="Logout"
              >
                Sair
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-outline text-sm">
                Login
              </Link>
              <Link to="/sign-up" className="btn-outline text-sm">
                Cadastro
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
