import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FormField } from '../components/FormField';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/api';

export function LoginPage() {
  // RF02: aceita e-mail ou nome de usuário.
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [generalError, setGeneralError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setGeneralError('');
    setErrors({});

    if (!identifier.trim()) {
      setErrors((prev) => ({
        ...prev,
        identifier: 'Informe seu e-mail ou nome de usuário',
      }));
      return;
    }
    if (!password.trim()) {
      setErrors((prev) => ({ ...prev, password: 'Senha é obrigatória' }));
      return;
    }

    setIsLoading(true);
    try {
      await login(identifier.trim(), password);
      navigate('/platform');
    } catch (error) {
      setGeneralError(apiService.getErrorMessage(error));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center py-8">
      <div className="card w-full max-w-md">
        <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">Login</h1>

        {generalError && (
          <div
            className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6"
            role="alert"
          >
            {generalError}
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate>
          <FormField
            label="E-mail ou nome de usuário"
            placeholder="seu@email.com ou joao_silva"
            value={identifier}
            onChange={setIdentifier}
            error={errors.identifier}
            required
          />

          <FormField
            label="Senha"
            type="password"
            placeholder="Sua senha"
            value={password}
            onChange={setPassword}
            error={errors.password}
            required
          />

          <button
            type="submit"
            className="btn-primary w-full mb-4 disabled:opacity-50"
            disabled={isLoading}
            aria-label="Fazer login"
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                Entrando...
              </span>
            ) : (
              'Login'
            )}
          </button>
        </form>

        <div className="space-y-3 text-center text-sm">
          <Link to="/forgot-password" className="block text-primary-600 hover:text-primary-700">
            Esqueci minha senha
          </Link>
          <p className="text-gray-600">
            Não tem conta?{' '}
            <Link to="/sign-up" className="text-primary-600 hover:text-primary-700 font-semibold">
              Cadastre-se
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
