import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';

interface User {
  id: string;
  name: string;
  username: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  accessToken: string | null;
  isLoading: boolean;
  signUp: (
    name: string,
    username: string,
    email: string,
    password: string,
    consent: boolean
  ) => Promise<void>;
  /** RF02: `identifier` é o e-mail ou o nome de usuário. */
  login: (identifier: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize from localStorage on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('accessToken');
    const savedUser = localStorage.getItem('user');

    if (savedToken && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
        setAccessToken(savedToken);
      } catch (error) {
        // localStorage corrompido travava a aplicação antes de sair do loading.
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
      }
    }
    setIsLoading(false);
  }, []);

  const signUp = useCallback(
    async (
      name: string,
      username: string,
      email: string,
      password: string,
      consent: boolean
    ) => {
      const response = await fetch('/api/auth/sign-up', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, username, email, password, consent }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error?.message || 'Erro ao cadastrar');
      }

      // Auto-login after signup
      await login(email, password);
    },
    []
  );

  const login = useCallback(async (identifier: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ identifier, password }),
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error?.message || 'Erro ao fazer login');
    }

    const data = await response.json();
    setAccessToken(data.accessToken);
    setUser(data.user);
    localStorage.setItem('accessToken', data.accessToken);
    localStorage.setItem('user', JSON.stringify(data.user));
  }, []);

  const logout = useCallback(() => {
    fetch('/api/auth/logout', { method: 'POST', credentials: 'include' }).catch(() => undefined);
    setAccessToken(null);
    setUser(null);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user');
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        accessToken,
        isLoading,
        signUp,
        login,
        logout,
        isAuthenticated: !!accessToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
