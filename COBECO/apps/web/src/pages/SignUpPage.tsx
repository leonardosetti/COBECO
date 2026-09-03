import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FormField } from '../components/FormField';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/api';

export function SignUpPage() {
  const [name, setName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [consent, setConsent] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [generalError, setGeneralError] = useState('');
  const { signUp } = useAuth();
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!name.trim()) {
      newErrors.name = 'Nome é obrigatório';
    }
    // RF01: 3 a 30 caracteres, alfanuméricos e underscore.
    if (username.trim().length < 3 || username.trim().length > 30) {
      newErrors.username = 'Nome de usuário deve ter de 3 a 30 caracteres';
    }
    if (!/^[A-Za-z0-9_]*$/.test(username.trim())) {
      newErrors.username = 'Use apenas letras, números e underscore';
    }
    if (!email.trim()) {
      newErrors.email = 'E-mail é obrigatório';
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'E-mail inválido';
    }
    if (password.length < 8) {
      newErrors.password = 'Senha deve ter no mínimo 8 caracteres';
    }
    if (!/[A-Z]/.test(password)) {
      newErrors.password = 'Senha deve conter ao menos uma letra maiúscula';
    }
    if (!/[a-z]/.test(password)) {
      newErrors.password = 'Senha deve conter ao menos uma letra minúscula';
    }
    if (!/\d/.test(password)) {
      newErrors.password = 'Senha deve conter ao menos um número';
    }
    if (!/[^A-Za-z0-9]/.test(password)) {
      newErrors.password = 'Senha deve conter ao menos um caractere especial';
    }
    if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Senhas não correspondem';
    }
    if (!consent) {
      newErrors.consent = 'É necessário aceitar o tratamento dos seus dados';
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
      await signUp(name, username.trim(), email, password, consent);
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
        <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">Criar Conta</h1>

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
            label="Nome"
            placeholder="Seu nome completo"
            value={name}
            onChange={setName}
            error={errors.name}
            required
          />

          <FormField
            label="Nome de usuário"
            placeholder="ex.: joao_silva"
            value={username}
            onChange={setUsername}
            error={errors.username}
            required
          />

          <FormField
            label="E-mail"
            type="email"
            placeholder="seu@email.com"
            value={email}
            onChange={setEmail}
            error={errors.email}
            required
          />

          <FormField
            label="Senha"
            type="password"
            placeholder="Mínimo 8 caracteres, com número e símbolo"
            value={password}
            onChange={setPassword}
            error={errors.password}
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

          <div className="form-group">
            <div className="flex items-start gap-2">
              <input
                id="consent"
                type="checkbox"
                checked={consent}
                onChange={(event) => setConsent(event.target.checked)}
                className="mt-1 h-4 w-4 shrink-0 accent-primary-600"
                aria-invalid={!!errors.consent}
                aria-describedby={errors.consent ? 'consent-error' : undefined}
              />
              <label htmlFor="consent" className="text-sm">
                Autorizo o tratamento dos meus dados pessoais (nome e e-mail) para criação e uso da
                conta, conforme a LGPD. Posso excluir minha conta e meus dados a qualquer momento.
              </label>
            </div>
            {errors.consent && (
              <p id="consent-error" className="mt-1 text-sm text-red-500">
                {errors.consent}
              </p>
            )}
          </div>

          <button
            type="submit"
            className="btn-primary w-full mb-4 disabled:opacity-50"
            disabled={isLoading}
            aria-label="Criar conta"
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                Criando...
              </span>
            ) : (
              'Criar Conta'
            )}
          </button>
        </form>

        <p className="text-center text-gray-600">
          Já tem conta?{' '}
          <Link to="/login" className="text-primary-600 hover:text-primary-700 font-semibold">
            Fazer login
          </Link>
        </p>
      </div>
    </div>
  );
}
