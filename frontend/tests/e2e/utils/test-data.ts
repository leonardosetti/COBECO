export const PERGUNTAS_SEGURANCA = [
  { value: 'pet', label: 'Qual seu pet?' },
  { value: 'cidade', label: 'Cidade natal?' },
  { value: 'escola', label: 'Escola?' },
] as const;

export const VALID_USER_DATA = {
  nome_usuario: 'usuario_valido',
  email: 'valido@teste.com',
  nome: 'Usuário Válido',
  senha: 'Senha@123',
  confirmar_senha: 'Senha@123',
  pergunta_seguranca: 'cidade' as const,
  resposta_seguranca: 'São Paulo',
};

export const INVALID_EMAILS = [
  'invalido',
  'invalido@',
  '@dominio.com',
  'invalido@dominio',
  'invalido@.com',
  'invalido@dominio.',
];

export const WEAK_PASSWORDS = [
  '123',
  'senha',
  'Senha',
  'SENHA@123',
  'senha@123',
  'Senha123',
  'Senha@',
  'a'.repeat(7),
];

export const STRONG_PASSWORDS = [
  'Senha@123',
  'Minh@Senh@Forte1',
  'Complex@Pass123',
];

export const TEST_USER_BASE = {
  senha: 'Senha@123',
  confirmar_senha: 'Senha@123',
  pergunta_seguranca: 'cidade' as const,
  resposta_seguranca: 'São Paulo',
};

interface TestUserOverrides {
  nome_usuario?: string;
  email?: string;
  nome?: string;
  senha?: string;
  confirmar_senha?: string;
  pergunta_seguranca?: typeof PERGUNTAS_SEGURANCA[number]['value'];
  resposta_seguranca?: string;
}

export function createTestUser(overrides: TestUserOverrides = {}) {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 8);
  return {
    nome_usuario: overrides.nome_usuario || `user${timestamp}${random}`,
    email: overrides.email || `user${timestamp}${random}@test.com`,
    nome: overrides.nome || `User ${timestamp}${random}`,
    senha: overrides.senha || TEST_USER_BASE.senha,
    confirmar_senha: overrides.confirmar_senha || TEST_USER_BASE.confirmar_senha,
    pergunta_seguranca: overrides.pergunta_seguranca || TEST_USER_BASE.pergunta_seguranca,
    resposta_seguranca: overrides.resposta_seguranca || TEST_USER_BASE.resposta_seguranca,
  };
}

export function createListaData(overrides: Partial<{ titulo: string; descricao: string; publica: boolean }> = {}) {
  const timestamp = Date.now();
  return {
    titulo: `Lista ${timestamp}`,
    descricao: `Descrição da lista ${timestamp}`,
    publica: false,
    ...overrides,
  };
}