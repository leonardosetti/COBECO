import React, { useState } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { FormField } from '../components/FormField';
import { apiService } from '../services/api';

export function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [generalError, setGeneralError] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const token = searchParams.get('token');

  if (!token) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center py-8">
        <div className="card w-full max-w-md text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-4">Link Inválido</h1>
          <p className="text-gray-600 mb-6">
            O link de recuperação de senha é inválido ou expirou.
          </p>
          <Link to="/forgot-password" className="btn-primary inline-block">
            Solicitar Novo Link
          </Link>
        </div>
      </div>
    );
  }

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (newPassword.length < 8) {
      newErrors.newPassword = 'Senha deve ter no mínimo 8 caracteres';
    }
    if (!/[A-Z]/.test(newPassword)) {
      newErrors.newPassword = 'Senha deve conter ao menos uma letra maiúscula';
    }
    if (!/[a-z]/.test(newPassword)) {
      newErrors.newPassword = 'Senha deve conter ao menos uma letra minúscula';
    }
    if (!/\d/.test(newPassword)) {
      newErrors.newPassword = 'Senha deve conter ao menos um número';
    }
    if (newPassword !== confirmPassword) {
      newErrors.confirmPassword = 'Senhas não correspondem';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setGeneralError('');

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, newPassword }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error?.message || 'Erro ao redefinir senha');
      }

      setSuccess(true);
    } catch (error) {
      setGeneralError(apiService.getErrorMessage(error));
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center py-8">
        <div className="card w-full max-w-md text-center">
          <div className="text-4xl mb-4">✓</div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Senha Redefinida</h1>
          <p className="text-gray-600 mb-6">Sua senha foi redefinida com sucesso.</p>
          <button
            onClick={() => navigate('/login')}
            className="btn-primary inline-block"
            aria-label="Ir para login"
          >
            Fazer Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center py-8">
      <div className="card w-full max-w-md">
        <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">Redefinir Senha</h1>

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
            label="Nova Senha"
            type="password"
            placeholder="Mínimo 8 caracteres"
            value={newPassword}
            onChange={setNewPassword}
            error={errors.newPassword}
            required
          />

          <FormField
            label="Confirmar Senha"
            type="password"
            placeholder="Repita sua senha"
            value={confirmPassword}
            onChange={setConfirmPassword}
            error={errors.confirmPassword}
            required
          />

          <button
            type="submit"
            className="btn-primary w-full disabled:opacity-50"
            disabled={isLoading}
            aria-label="Redefinir senha"
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                Redefinindo...
              </span>
            ) : (
              'Redefinir Senha'
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
