# COBECO — Bug Log (Primeira Release / MVP)

**Versão:** 1.0  
**Data:** 14/11/2026  
**Release:** v1.0.0-RC1  
**Responsável:** QA Lead  
**Status:** EM ANÁLISE  

---

## 1. Resumo de Bugs Identificados

| Severidade | Total | Crítico | Alto | Médio | Baixo |
|------------|-------|---------|------|-------|-------|
| **Total** | 12 | 0 | 2 | 6 | 4 |

---

## 2. Lista de Bugs

### BUG-001: Refresh Token não salvo no banco durante login
| Campo | Valor |
|-------|-------|
| **ID** | BUG-001 |
| **Título** | Refresh Token não persistido na tabela `sessoes` durante login |
| **Severidade** | **ALTO** |
| **Prioridade** | **P0 - Crítico** |
| **Módulo** | Backend - Auth (`auth.py`, `LoginUseCase`) |
| **Descoberto em** | Desenvolvimento do framework de testes |
| **Status** | **EM CORREÇÃO** |

**Descrição:**
O endpoint `/v1/auth/login` gera access token e refresh token, define o cookie httpOnly, mas **não persiste o hash do refresh token na tabela `sessoes`**. Isso impede:
- Revogação real de sessões no logout
- Listagem de sessões ativas
- Logout de todos os dispositivos
- Limpeza de sessões expiradas

**RCA (Root Cause Analysis):**
1. **Causa Raiz:** A implementação do `LoginUseCase.executar()` retorna apenas `LoginOutput` (tokens) mas não recebe `SessaoRepository` para persistir a sessão.
2. **Causa Contribuinte:** O endpoint `/login` em `auth.py` cria a sessão manualmente após o usecase, mas usa `hash_senha()` (bcrypt) em vez de `hash_refresh_token()` (SHA256) para o hash do refresh token.
3. **Falha de Design:** O `LogoutUseCase` espera `invalidar_refresh_fn` mas não há implementação que busque por hash SHA256.

**Evidência:**
```python
# auth.py - linha ~470: cria sessão mas usa hash_senha (bcrypt)
refresh_hash = hash_senha(tokens.refresh_token)  # ERRADO: bcrypt truncaria JWT >72 bytes

# usecases.py - LoginUseCase não recebe SessaoRepository
class LoginUseCase:
    def __init__(self, repo, verificar_senha_fn, criar_token_fn, rate_limiter_fn):
        # FALTA: sessao_repo
```

**Medida Corretiva:**
1. Adicionar `SessaoRepository` ao `LoginUseCase.__init__`
2. Modificar `LoginUseCase.executar()` para persistir `Sessao` com `hash_refresh_token()`
3. Atualizar endpoint `/login` para injetar `SessaoRepository`
4. Corrigir `hash_refresh_token()` para usar SHA256 (já implementado)
5. Ajustar `LogoutUseCase` para usar `SessaoRepository.buscar_por_token_hash()`

**Teste de Regressão:** `test_login_retorna_refresh_token_cookie` + verificação em `sessoes` table

---

### BUG-002: Tabela `sessoes` não criada no seed/migration
| Campo | Valor |
|-------|-------|
| **ID** | BUG-002 |
| **Título** | Tabela `sessoes` não existe no banco (falta migration/seed) |
| **Severidade** | **ALTO** |
| **Prioridade** | **P0 - Crítico** |
| **Módulo** | Backend - Database (Alembic/Seed) |
| **Descoberto em** | Implementação `SessaoModel` |
| **Status** | **PENDENTE** |

**Descrição:**
A model `SessaoModel` foi adicionada em `models.py` mas **não há migration Alembic** correspondente. A tabela `sessoes` não existe no banco.

**RCA:**
- Model adicionado em `models.py` sem gerar migration correspondente
- Seed SQL não inclui tabela `sessoes`
- `init_db()` usa `Base.metadata.create_all` apenas em dev, não em produção

**Medida Corretiva:**
1. Gerar migration: `alembic revision --autogenerate -m "add sessoes table"`
2. Revisar migration gerada
3. Aplicar: `alembic upgrade head`
4. Atualizar seed se necessário

---

### BUG-003: Username com underscore rejeitado pelo backend
| Campo | Valor |
|-------|-------|
| **ID** | BUG-003 |
| **Título** | Backend rejeita username com underscore (`_`) mas frontend permite |
| **Severidade** | **MÉDIO** |
| **Prioridade** | **P1 - Alto** |
| **Módulo** | Backend - Validação `CadastrarUsuarioRequest` |
| **Descoberto em** | Testes E2E `cadastro.spec.ts` |
| **Status** | **CONFIRMADO** |

**Descrição:**
Frontend gera usernames como `user_1794617099014` (com underscore) mas backend valida com regex `^[a-zA-Z0-9]+$` que **não aceita underscore**.

**RCA:**
- Frontend `createTestUser()` gera `user_{timestamp}` (underscore)
- Backend `CadastrarUsuarioRequest.nome_usuario` pattern: `^[a-zA-Z0-9]+$`
- Frontend HTML `pattern="[a-zA-Z0-9]+"` também não permite underscore

**Medida Corretiva (Opção A - Recomendada):**
Atualizar regex backend para `^[a-zA-Z0-9_]+$` (permite underscore)
```python
# config.py ou auth.py
nome_usuario: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
```

**Opção B:** Alterar frontend para gerar sem underscore: `user{timestamp}`

**Decisão:** Opção A (backend mais permissivo, underscore é comum em usernames)

---

### BUG-004: Tabela `sessoes` não tem índice composto otimizado
| Campo | Valor |
|-------|-------|
| **ID** | BUG-004 |
| **Título** | Índice `ix_sessao_usuario_expira` não cobre queries de revogação |
| **Severidade** | **MÉDIO** |
| **Prioridade** | **P2 - Normal** |
| **Módulo** | Backend - Database Model |
| **Status** | **IDENTIFICADO** |

**Descrição:**
Índice `ix_sessao_usuario_expira` em `(usuario_id, expira_em)` não cobre query `buscar_por_token_hash` que filtra por `refresh_token_hash`.

**Medida Corretiva:**
Adicionar índice em `refresh_token_hash` (já tem `unique=True, index=True`) - verificar se Alembic criou corretamente.

---

### BUG-005: Frontend - `escapeHtml` não escapa aspas simples
| Campo | Valor |
|-------|-------|
| **ID** | BUG-005 |
| **Título** | `escapeHtml()` não escapa `'` (apóstrofo) - risco XSS em atributos HTML |
| **Severidade** | **MÉDIO** |
| **Prioridade** | **P1 - Alto** |
| **Módulo** | Frontend - `app.js` (`escapeHtml`) |
| **Status** | **CORRIGIDO PARCIALMENTE** |

**Descrição:**
`escapeHtml` usa `textContent` → `innerHTML` que escapa `<`, `>`, `&`, `"` mas **não `'` (apóstrofo)**. Risco em: `<input value='{{user_input}}'>`

**RCA:**
```javascript
const escapeHtml = (text) => {
  const div = document.createElement('div');
  div.textContent = String(text);
  return div.innerHTML; // Não escapa '
};
```

**Medida Corretiva:**
```javascript
const escapeHtml = (text) => {
  if (text === null || text === undefined) return '';
  return String(text)
    .replace(/&/g, '&')
    .replace(/</g, '<')
    .replace(/>/g, '>')
    .replace(/"/g, '"')
    .replace(/'/g, '''); // Adiciona escape de apóstrofo
};
```

---

### BUG-006: Frontend - CSP permite `unsafe-inline` em styles
| Campo | Valor |
|-------|-------|
| **ID** | BUG-006 |
| **Título** | CSP `style-src 'self' 'unsafe-inline'` enfraquece proteção |
| **Severidade** | **BAIXO** |
| **Prioridade** | **P3 - Baixo** |
| **Módulo** | Backend - `main.py` (security_headers_middleware) |
| **Status** | **ACEITO COMO RISCO** |

**Descrição:**
CSP permite `'unsafe-inline'` em `style-src` para suportar Tailwind JIT ou estilos inline legados.

**Justificativa:**
- Tailwind CSS usa estilos inline em desenvolvimento
- Migração para CSS-in-JS ou classes utilitárias seria breaking change
- Risco mitigado: `script-src 'self'` (sem unsafe-inline)

**Mitigação Futura:** Migrar para Tailwind CSS compilado (sem JIT) ou CSS Modules.

---

### BUG-007: Frontend - `showToast` não escapa HTML em mensagens de sucesso
| Campo | Valor |
|-------|-------|
| **ID** | BUG-007 |
| **Título** | Toast de sucesso pode executar XSS se mensagem vier de API |
| **Severidade** | **MÉDIO** |
| **Prioridade** | **P1 - Alto** |
| **Módulo** | Frontend - `app.js` (`showToast`) |
| **Status** | **CORRIGIDO** |

**Descrição:**
`showToast` usa `innerHTML` sem sanitização. Se backend retornar mensagem com HTML, executa.

**Correção Aplicada:**
```javascript
toast.innerHTML = `
  <span class="flex-1">${escapeHtml(message)}</span>
  <button class="text-white/80 hover:text-white" aria-label="Fechar">&times;</button>
`;
```

---

### BUG-008: Frontend - `showConfirm` não escapa título/mensagem
| Campo | Valor |
|-------|-------|
| **ID** | BUG-008 |
| **Título** | Modal de confirmação vulnerável a XSS via title/message/footer |
| **Severidade** | **MÉDIO** |
| **Prioridade** | **P1 - Alto** |
| **Módulo** | Frontend - `app.js` (`showConfirm`, `showModal`) |
| **Status** | **CORRIGIDO** |

**Correção Aplicada:**
```javascript
// showConfirm
<h2 id="modal-title" class="text-lg font-semibold">${escapeHtml(title)}</h2>
<p class="text-gray-700">${escapeHtml(message)}</p>
<button ...>${escapeHtml(confirmText)}</button>

// showModal
${options.title ? `<h2...>${escapeHtml(options.title)}</h2>` : ''}
<div class="modal-body">${content}</div> // content já é HTML confiável
```

---

### BUG-009: Backend - Rate limit recovery não retorna 429
| Campo | Valor |
|-------|-------|
| **ID** | BUG-009 |
| **Título** | Rate limit de recovery retorna 200 genérico em vez de 429 |
| **Severidade** | **BAIXO** |
| **Prioridade** | **P3 - Baixo** |
| **Módulo** | Backend - `auth.py` (`rate_limiter_recovery`) |
| **Status** | **COMPORTAMENTO INTENCIONAL** |

**Descrição:**
Após 3 tentativas de recovery/hora, retorna 200 com mensagem genérica em vez de 429 Too Many Requests.

**Justificativa:**
- Segurança: não revelar que rate limit existe (mesmo comportamento de usuário inexistente)
- Frontend trata ambos como "instruções enviadas"

---

### BUG-010: Frontend - Autocomplete não limpa resultados ao limpar input
| Campo | Valor |
|-------|-------|
| **ID** | BUG-010 |
| **Título** | Resultados do autocomplete persistem ao limpar campo |
| **Severidade** | **BAIXO** |
| **Prioridade** | **P3 - Baixo** |
| **Módulo** | Frontend - `app.js` (Views.criarLista/editarLista) |
| **Status** | **IDENTIFICADO** |

**Descrição:**
Ao digitar no autocomplete e depois limpar o campo, resultados anteriores permanecem visíveis.

**Medida Corretiva:**
```javascript
produtoInput.addEventListener('input', () => {
  if (!produtoInput.value.trim()) {
    autocompleteResults.classList.add('hidden');
    autocompleteResults.innerHTML = '';
  }
  // ... busca
});
```

---

### BUG-011: Backend - `RECOVERY_MODE=log` vaza token em produção
| Campo | Valor |
|-------|-------|
| **ID** | BUG-011 |
| **Título** | Variável `RECOVERY_MODE=log` expõe token de recovery no stdout |
| **Severidade** | **ALTO** |
| **Prioridade** | **P0 - Crítico** |
| **Módulo** | Backend - Config/UseCases |
| **Status** | **MITIGADO PARCIALMENTE** |

**Descrição:**
Variável default era `log`, expondo tokens de recuperação nos logs do container.

**Mitigação Aplicada:**
1. Default alterado para `"email"` em `config.py`
2. Removido `print()` do token em `usecases.py` (`RecuperarSenhaUseCase.solicitar_reset`)
3. Modo `log` mantido apenas para desenvolvimento explícito

---

### BUG-012: Frontend - Botão "Exportar PDF" não desabilita durante geração
| Campo | Valor |
|-------|-------|
| **ID** | BUG-012 |
| **Título** | Botão exportar PDF permite cliques múltiplos durante geração |
| **Severidade** | **BAIXO** |
| **Prioridade** | **P3 - Baixo** |
| **Módulo** | Frontend - `app.js` (exportação) |
| **Status** | **IDENTIFICADO** |

**Descrição:**
Clicar múltiplas vezes em "Exportar PDF" dispara múltiplos downloads simultâneos.

**Medida Corretiva:**
```javascript
btnExportar.addEventListener('click', async () => {
  btnExportar.disabled = true;
  btnExportar.innerHTML = '<span class="spinner"></span> Gerando...';
  try {
    const response = await fetch(...);
    // download
  } finally {
    btnExportar.disabled = false;
    btnExportar.innerHTML = 'Exportar PDF';
  }
});
```

---

## 3. Resumo de Ações por Severidade

### P0 - Crítico (Executar IMEDIATAMENTE)
| Bug | Ação | Responsável | Prazo |
|-----|------|-------------|-------|
| BUG-001 | Corrigir persistência de refresh token | Backend Dev | Hoje |
| BUG-002 | Criar migration tabela `sessoes` | Backend Dev | Hoje |
| BUG-011 | Confirmar `RECOVERY_MODE=email` default | Backend Dev | Hoje |

### P1 - Alto (Esta Sprint)
| Bug | Ação | Responsável | Prazo |
|-----|------|-------------|-------|
| BUG-003 | Ajustar regex username (permitir `_`) | Backend Dev | 2 dias |
| BUG-005 | Corrigir `escapeHtml` (apóstrofo) | Frontend Dev | 1 dia |
| BUG-007 | Confirmar fix `showToast` | Frontend Dev | 1 dia |
| BUG-008 | Confirmar fix `showConfirm`/`showModal` | Frontend Dev | 1 dia |

### P2 - Normal (Próxima Sprint)
| Bug | Ação | Responsável | Prazo |
|-----|------|-------------|-------|
| BUG-004 | Verificar índices tabela `sessoes` | Backend Dev | 1 semana |
| BUG-006 | Documentar risco CSP `unsafe-inline` | Sec/Arch | 1 semana |

### P3 - Baixo (Backlog)
| Bug | Ação | Responsável | Prazo |
|-----|------|-------------|-------|
| BUG-009 | Documentar comportamento recovery rate limit | QA | 2 semanas |
| BUG-010 | Fix autocomplete limpar resultados | Frontend Dev | 2 semanas |
| BUG-012 | Desabilitar botão durante exportação | Frontend Dev | 2 semanas |

---

## 4. Métricas de Qualidade Pós-Correção

| Métrica | Antes | Meta Após Correção |
|---------|-------|-------------------|
| **Bugs Críticos (P0)** | 3 | 0 |
| **Bugs Altos (P1)** | 4 | 0 |
| **Bugs Médios (P2)** | 2 | 1 |
| **Bugs Baixos (P3)** | 3 | 3 (aceitos) |
| **Cobertura RF** | 100% | 100% |
| **Security Scan** | 0 High | 0 High |

---

## 5. Próximos Passos

1. **Hoje:** Corrigir BUG-001, BUG-002, BUG-011
2. **Amanhã:** Corrigir BUG-003, BUG-005, BUG-007, BUG-008
3. **PR:** Abrir PRs com testes de regressão
4. **CI:** Validar pipeline completo
5. **Release:** Tag `v1.0.0` após Go/No-Go

---

**Última Atualização:** 14/11/2026 04:15 UTC  
**Arquivo:** `docs/operacao/BUG-LOG.md`  
**Próxima Revisão:** Pós-correção P0/P1