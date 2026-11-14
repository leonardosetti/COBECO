# DPIA / Threat Model — COBECO MVP

**Documento:** Avaliação de Impacto à Proteção de Dados / Modelo de Ameaças  
**Versão:** 1.0  
**Status:** Ativo | Arquivado  
**Data:** DD/MM/AAAA  
**Autor:** <Nome>  
**Conformidade:** LGPD (Lei Geral de Proteção de Dados — Brasil)

---

## 1. Descrição do tratamento de dados

Quais dados são coletados, por quê, por quem e por quanto tempo.

---

## 2. Classificação de dados

| Tipo de dado | Fonte | Sensibilidade | PII? | Retenção |
|---|---|---|---|---|
| nome_usuario | Cadastro do usuário | Baixa | Não | Até exclusão |
| email | Cadastro do usuário | Média | Não (pseudonimizado) | Até exclusão |
| senha_hash | Cadastro do usuário | Alta | Não | Até exclusão |
| listas / itens | Usuário autenticado | Baixa | Não | Até exclusão |
| preços / fornecedores | Seed (mock) | Baixa | Não | Estático (seed) |

**Princípio LGPD (Constitution Art. 3.5):** dados sintéticos apenas; zero PII reais em seeds, fixtures, logs ou backups.

---

## 3. Modelo de ameaças (Threat Model)

| Ameaça | Vetor | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| SQL injection | Entrada HTTP não validada | Média | Alta | Parameterized queries (Art. 7.2) |
| Exposição de credenciais | Commit acidental de `config-env-0001-env-example-v1.0` | Baixa | Crítica | `.gitignore`, sanitização pré-commit (Art. 7.7) |
| Brute force de login | Tentativas repetidas | Média | Média | Rate limiting 6 req/15min (RNF10) |
| JWT roubado | Cookie não seguro | Baixa | Alta | `httpOnly`, `SameSite=Strict`, 15 min access |
| Vazamento de PII real | Dados reais em logs/seeds | Baixa | Crítica | Dados sintéticos apenas (Art. 3.5) |

---

## 4. Controles de segurança

- Validação de entrada em todas as fronteiras HTTP (Pydantic)
- Parameterized queries apenas (proteção contra SQLi)
- bcrypt salt=12 para senhas
- JWT access 15 min (memória) + refresh 7 dias (cookie httpOnly/SameSite=Strict)
- Erros genéricos (sem traceback, sem payload de usuário)
- Rate limiting 6 req/15min por IP + username

---

## 5. Avaliação de conformidade LGPD

| Requisito LGPD | Status | Comentário |
|---|---|---|
| Consentimento / base legal | N/A | Dados sintéticos, uso acadêmico |
| Minimização de dados | Conforme | Apenas dados necessários ao MVP |
| Segurança da informação | Conforme | Criptografia de senha, JWT, rate limiting |
| Direitos do titular | N/A | Sem PII real |
| Notificação de vazamento | N/A | Sem PII real |

---

## 6. Revisão recorrente

A DPIA/Threat Model deve ser revisada a cada sprint e antes de qualquer lançamento que toque dados reais (Constitution Art. 7.6, 16.4).

---

**Fim do DPIA / Threat Model**
