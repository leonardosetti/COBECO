import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FormField } from '../components/FormField';
import { apiService } from '../services/api';

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!email.trim()) {
      setError('E-mail é obrigatório');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('/api/auth/request-password-reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error?.message || 'Erro ao processar solicitação');
      }

      setSubmitted(true);
    } catch (err) {
      setError(apiService.getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center py-8">
        <div className="card w-full max-w-md text-center">
          <div className="text-4xl mb-4">✓</div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">E-mail Enviado</h1>
          <p className="text-gray-600 mb-6">
            Se a conta existir, você receberá um e-mail com instruções para redefinir sua senha.
          </p>
          <Link to="/login" className="btn-primary inline-block">
            Voltar ao Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white flex items-center justify-center py-8">
      <div className="card w-full max-w-md">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 text-center">Recuperar Senha</h1>
        <p className="text-center text-gray-600 mb-6">
          Informe o e-mail associado à sua conta para receber instruções de recuperação.
        </p>

        {error && (
          <div
            className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6"
            role="alert"
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate>
          <FormField
            label="E-mail"
            type="email"
            placeholder="seu@email.com"
            value={email}
            onChange={setEmail}
            required
          />

          <button
            type="submit"
            className="btn-primary w-full mb-4 disabled:opacity-50"
            disabled={isLoading}
            aria-label="Enviar e-mail de recuperação"
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                Enviando...
              </span>
            ) : (
              'Enviar E-mail'
            )}
          </button>
        </form>

        <p className="text-center text-gray-600">
          <Link to="/login" className="text-primary-600 hover:text-primary-700 font-semibold">
            Voltar ao Login
          </Link>
        </p>
      </div>
    </div>
  );
}
