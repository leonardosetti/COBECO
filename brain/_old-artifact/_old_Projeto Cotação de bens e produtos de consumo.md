# Objetivo do projeto

Definir as necessidades fundamentais para o desenvolvimento de um sistema web-based que permita a qualquer usuário criar listas de compras genéricas — como supermercado, roupas, hardware, instrumentos, brinquedos etc. — e, a partir delas, comparar fornecedores simulados de acordo com uma categoria escolhida, com o objetivo de identificar o melhor preço total da lista.

O sistema deve lidar com situações em que nem todos os fornecedores possuem todos os itens solicitados, gerando agrupamentos de listas paralelas conforme a disponibilidade comum ou parcial dos itens. Também deve permitir orçamentos separados por grupo ou um orçamento geral, destacando itens faltantes, valores estimados, menor orçamento e, opcionalmente, maior orçamento.

A solução não deve reter dados do usuário, não deve exigir cadastro, deve operar com fornecedores mockados por meio de API REST alimentada por dados pré-populados em banco de dados e deve permitir exportação ou impressão das listas e orçamentos gerados.

Além disso, o projeto deve impor boas práticas de UI/UX, usabilidade, arquitetura de software, qualidade de código, privacidade, acessibilidade e testabilidade.

---

## 1. Contexto e problema

Ao planejar uma compra composta por vários itens, o usuário frequentemente precisa comparar preços em diferentes fornecedores. Porém:

- Nem sempre um único fornecedor possui todos os itens desejados.
- Alguns fornecedores têm preços melhores para certos itens, mas não atendem a lista inteira.
- Comparar manualmente listas grandes é trabalhoso e sujeito a erros.
- O usuário pode desejar saber:
  - Qual fornecedor tem o menor preço para os itens disponíveis.
  - Qual seria o custo estimado considerando itens faltantes em outros fornecedores.
  - Quais itens ficariam faltando em cada fornecedor.
  - Quais fornecedores possuem cobertura total ou parcial da lista.
  - Como dividir a lista em grupos de fornecedores com disponibilidade semelhante.

O sistema proposto resolve esse problema de forma simulada, sem integração real com fornecedores, usando um catálogo mockado em banco de dados para validar a lógica de comparação, agrupamento e orçamento.

---

## 2. Público-alvo

O sistema é destinado a usuários comuns que desejam planejar compras de forma rápida e comparativa, sem necessidade de autenticação ou persistência de dados pessoais.

Exemplos de uso:

- Comparar preços de supermercados.
- Comparar lojas de roupas.
- Comparar lojas de peças ou hardware.
- Comparar lojas de instrumentos musicais.
- Comparar lojas de brinquedos.
- Preparar uma lista impressa para conferência física durante a compra.

---

## 3. Escopo do projeto

### 3.1. Dentro do escopo

- Criação de listas de compras sem autenticação.
- Definição de itens com nome, quantidade, unidade e, quando possível, identificador normalizado.
- Seleção de categoria da lista.
- Seleção de fornecedores simulados compatíveis com a categoria.
- Comparação de disponibilidade de itens entre fornecedores mockados.
- Agrupamento de fornecedores por cobertura total ou parcial da lista.
- Geração de listas paralelas conforme itens comuns.
- Cálculo de orçamento por fornecedor.
- Cálculo de orçamento por grupo de fornecedores.
- Exibição de itens faltantes por fornecedor.
- Exibição de valores estimados para itens faltantes, quando houver referência em outro fornecedor.
- Destaque do menor orçamento.
- Opção de destacar o maior orçamento.
- Exportação de listas e orçamentos para arquivo imprimível.
- API REST mockada para fornecedores, produtos, categorias e simulação de orçamento.
- Banco de dados com dados pré-populados apenas para fins de simulação.
- Aplicação de boas práticas de UI/UX, acessibilidade, arquitetura, testes e privacidade.

### 3.2. Fora do escopo

- Cadastro de usuários.
- Login ou autenticação.
- Persistência de listas pessoais em servidor.
- Histórico de compras do usuário.
- Pagamentos reais.
- Integração real com fornecedores externos.
- Coleta de dados pessoais para marketing.
- Rastreamento individual do usuário.
- Recomendações personalizadas baseadas em perfil.
- Gestão de estoque real de fornecedores.
- Atualização automática de preços em fontes externas.

---

## 4. Premissas e restrições fundamentais

### 4.1. Premissas

- Os fornecedores são simulados e representam apenas dados de referência.
- O catálogo de produtos e preços é previamente populado em banco de dados.
- O usuário não precisa se identificar.
- A lista criada pelo usuário é efêmera e não deve ser armazenada no servidor.
- A comparação depende de itens normalizados ou mapeados para produtos conhecidos no catálogo mockado.
- O sistema pode funcionar com estado mantido apenas no navegador durante a sessão.
- A exportação local de arquivos pode ser usada como mecanismo de preservação opcional pelo usuário.

### 4.2. Restrições

- Nenhuma lista, orçamento ou entrada do usuário pode ser persistida em servidor.
- Não deve haver banco de dados com dados pessoais.
- Logs não devem conter dados que permitam identificar o usuário ou reconstruir listas pessoais.
- A API deve ser stateless em relação ao usuário.
- Qualquer rascunho salvo localmente no navegador deve ser opcional, transparente e removível pelo usuário.
- O sistema deve funcionar sem depender de serviços externos de terceiros para dados do usuário.

---

## 5. Requisitos funcionais fundamentais

| ID   | Requisito                        | Descrição                                                                                                                            | Prioridade |
| ---- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| RF01 | Criar lista de compras           | O usuário deve poder criar uma lista com itens genéricos, sem cadastro.                                                              | MVP        |
| RF02 | Definir itens                    | Cada item deve possuir ao menos descrição e quantidade. Unidade de medida deve ser suportada.                                        | MVP        |
| RF03 | Editar lista                     | O usuário deve poder adicionar, remover, editar e reordenar itens.                                                                   | MVP        |
| RF04 | Selecionar categoria             | O usuário deve poder escolher uma categoria para a lista, como supermercado, roupas, hardware etc.                                   | MVP        |
| RF05 | Listar fornecedores mock         | O sistema deve listar fornecedores simulados compatíveis com a categoria escolhida.                                                  | MVP        |
| RF06 | Selecionar fornecedores          | O usuário deve poder escolher quais fornecedores participarão da comparação.                                                         | MVP        |
| RF07 | Normalizar itens                 | O sistema deve permitir associar itens da lista a produtos conhecidos no catálogo mockado quando possível.                           | MVP        |
| RF08 | Verificar disponibilidade        | O sistema deve verificar quais itens da lista existem em cada fornecedor selecionado.                                                | MVP        |
| RF09 | Agrupar fornecedores             | O sistema deve agrupar fornecedores conforme conjuntos de itens disponíveis.                                                         | MVP        |
| RF10 | Gerar listas paralelas           | O sistema deve gerar listas ou grupos decrementais conforme cobertura comum ou parcial dos itens.                                    | MVP        |
| RF11 | Orçamento por grupo              | O usuário deve poder visualizar orçamento separado por grupo de fornecedores.                                                        | MVP        |
| RF12 | Orçamento geral                  | O usuário deve poder visualizar orçamento geral considerando todos os fornecedores selecionados.                                     | MVP        |
| RF13 | Exibir itens faltantes           | Cada orçamento deve mostrar claramente os itens faltantes, quantidades e valor estimado quando aplicável.                            | MVP        |
| RF14 | Calcular total por fornecedor    | O sistema deve calcular o valor total disponível em cada fornecedor.                                                                 | MVP        |
| RF15 | Calcular total estimado completo | O sistema deve calcular um total estimado incluindo itens faltantes com base em fornecedores alternativos, quando houver referência. | MVP        |
| RF16 | Destacar menor orçamento         | O sistema deve destacar automaticamente o menor orçamento.                                                                           | MVP        |
| RF17 | Destacar maior orçamento         | O usuário deve poder inverter a lógica e destacar o maior orçamento.                                                                 | MVP        |
| RF18 | Exportar lista                   | O sistema deve permitir exportar a lista em arquivo imprimível.                                                                      | MVP        |
| RF19 | Exportar orçamento               | O sistema deve permitir exportar orçamento em arquivo imprimível.                                                                    | MVP        |
| RF20 | Impressão amigável               | O sistema deve possuir layout de impressão limpo, legível e sem elementos desnecessários.                                            | MVP        |
| RF21 | Não reter dados do usuário       | O backend não deve salvar listas, orçamentos ou dados pessoais.                                                                      | MVP        |
| RF22 | Recalcular automaticamente       | Alterações na lista, categoria ou fornecedores devem permitir novo cálculo.                                                          | MVP        |
| RF23 | Tratar itens não mapeados        | Itens não encontrados no catálogo devem ser sinalizados e não devem quebrar o fluxo.                                                 | MVP        |
| RF24 | Tratar itens ausentes            | Itens ausentes em todos os fornecedores devem ser exibidos como indisponíveis.                                                       | MVP        |
| RF25 | Exibir cobertura                 | O sistema deve mostrar percentual ou proporção de itens atendidos por fornecedor.                                                    | Alta       |
| RF26 | Comparar grupos                  | O usuário deve poder comparar visualmente grupos gerados.                                                                            | Alta       |
| RF27 | Alternar métrica de destaque     | O usuário deve poder alternar entre menor/maior total disponível ou total estimado completo.                                         | Alta       |
| RF28 | Importar lista exportada         | O usuário deve poder importar lista previamente exportada, se desejado.                                                              | Média      |
| RF29 | Rascunho local opcional          | O sistema pode permitir rascunho local no navegador, apenas com ação explícita do usuário.                                           | Média      |
| RF30 | Limpar sessão                    | O usuário deve poder limpar todos os dados da sessão local.                                                                          | Alta       |

---

## 6. Regras de negócio essenciais

### 6.1. Lista de compras

Uma lista de compras é composta por itens solicitados pelo usuário.

Cada item deve conter, no mínimo:

- Descrição.
- Quantidade.
- Unidade de medida, quando aplicável.
- Identificador de produto normalizado, quando disponível.
- Categoria associada, direta ou indiretamente.

Exemplo:

| Item | Descrição     | Quantidade | Unidade |
| ---- | ------------- | ---------: | ------- |
| 1    | Arroz 5kg     |          2 | unidade |
| 2    | Feijão 1kg    |          3 | unidade |
| 3    | Camiseta azul |          1 | unidade |

Para fins de comparação automática, o sistema deve tentar mapear cada item para um produto conhecido no catálogo mockado.

---

### 6.2. Categoria

A categoria define o contexto da comparação.

Exemplos:

- Supermercado.
- Roupas.
- Hardware.
- Instrumentos musicais.
- Brinquedos.
- Peças.

Somente fornecedores vinculados à categoria selecionada devem ser exibidos para comparação.

Caso a lista possua itens incompatíveis com a categoria selecionada, o sistema deve exibir aviso.

---

### 6.3. Fornecedores

Fornecedores são entidades simuladas cadastradas previamente no banco de dados.

Cada fornecedor deve possuir:

- Identificador.
- Nome.
- Categoria ou categorias atendidas.
- Situação ativa/inativa.
- Conjunto de produtos disponíveis.
- Preço por produto.
- Estoque simulado opcional.

Não há integração real com fornecedores externos.

---

### 6.4. Produtos

Produtos representam itens padronizados no catálogo mockado.

Cada produto deve possuir:

- Identificador.
- Nome.
- Categoria.
- Unidade de medida.
- Identificadores alternativos ou sinônimos, se necessário.
- Preços por fornecedor.
- Estoque por fornecedor, opcional.

A comparação de disponibilidade deve ocorrer preferencialmente por identificador normalizado de produto, não apenas por texto livre.

---

### 6.5. Disponibilidade de itens

Para cada fornecedor selecionado, o sistema deve calcular o conjunto de itens da lista que estão disponíveis.

Um item é considerado disponível quando:

- O fornecedor possui o produto correspondente em seu catálogo mockado.
- O produto possui preço válido.
- O produto está ativo.
- Caso haja controle de estoque simulado, há quantidade suficiente total ou parcialmente.

Caso o estoque seja menor que a quantidade solicitada, o sistema deve tratar como disponibilidade parcial.

Exemplo:

- Quantidade solicitada: 5.
- Estoque no fornecedor: 3.
- Situação: disponível parcialmente.
- Quantidade faltante: 2.

---

### 6.6. Itens faltantes

Um item é faltante para um fornecedor quando:

- O fornecedor não possui o produto.
- O produto está inativo.
- Não há preço válido.
- O estoque é insuficiente, caracterizando falta parcial.
- O item não pôde ser normalizado para o catálogo.

Para cada item faltante, o sistema deve exibir:

- Identificação do item.
- Quantidade solicitada.
- Quantidade faltante.
- Motivo da falta, quando possível.
- Valor unitário de referência, se houver outro fornecedor selecionado que possua o item.
- Valor total estimado da falta, quando aplicável.

---

### 6.7. Valor de referência para itens faltantes

Quando um item não estiver disponível em um fornecedor, mas estiver disponível em outro fornecedor selecionado, o sistema pode calcular um valor de referência.

Regra recomendada:

- O valor de referência deve ser o menor preço unitário disponível entre os fornecedores selecionados.
- O valor total estimado do item faltante deve ser:

```text
quantidade_faltante × menor_preço_unitário_disponível
```

Se nenhum fornecedor selecionado possuir o item:

- O item deve ser marcado como indisponível.
- O valor estimado deve ficar nulo ou zerado.
- O sistema deve exibir alerta de item não cotável.

---

## 7. Agrupamento de fornecedores e listas paralelas

### 7.1. Conceito

Quando a lista não é completamente atendida por todos os fornecedores selecionados, o sistema deve dividir a análise em grupos ou listas paralelas.

O agrupamento deve permitir visualizar:

- Quais fornecedores possuem exatamente os mesmos itens da lista.
- Quais fornecedores possuem coberturas parciais semelhantes.
- Quais itens são comuns a todos os fornecedores selecionados.
- Quais itens são comuns apenas a subconjuntos de fornecedores.
- Quais fornecedores possuem itens exclusivos ou ausência de itens.

---

### 7.2. Lista comum global

O sistema deve identificar os itens comuns a todos os fornecedores selecionados.

Exemplo:

Se os fornecedores selecionados possuem, em comum, os itens:

```text
1, 4, 5, 8, 9
```

Então a lista comum global é:

```text
Lista comum: 1, 4, 5, 8, 9
```

Essa lista comum pode ser exibida como um destaque inicial, mas não substitui necessariamente os grupos por cobertura.

---

### 7.3. Agrupamento por perfil de cobertura

A regra principal de agrupamento recomendada é:

> Fornecedores com exatamente o mesmo conjunto de itens disponíveis para a lista devem pertencer ao mesmo grupo.

Essa regra atende diretamente o exemplo apresentado.

Dado:

```text
Itens da lista: 1,2,3,4,5,6,7,8,9
Fornecedores: A,B,C,D,E,F,G,H
```

Com disponibilidade:

| Fornecedor | Itens disponíveis |
| ---------- | ----------------- |
| A          | 1,2,3,4,5,6,7,8,9 |
| B          | 1,2,3,4,5,6,7,8,9 |
| C          | 1,2,3,4,5,6,8,9   |
| D          | 1,2,4,5,8,9       |
| E          | 1,2,3,4,5,6,8,9   |
| F          | 1,2,3,4,5,6,8,9   |
| G          | 1,3,4,5,8,9       |
| H          | 1,2,3,4,5,6,8,9   |

O agrupamento esperado é:

### Lista I

Fornecedores com cobertura total da lista:

| Grupo   | Fornecedores | Itens disponíveis |
| ------- | ------------ | ----------------- |
| Lista I | A, B         | 1,2,3,4,5,6,7,8,9 |

### Lista II

Fornecedores com a mesma cobertura parcial:

| Grupo    | Fornecedores | Itens disponíveis |
| -------- | ------------ | ----------------- |
| Lista II | C, E, F, H   | 1,2,3,4,5,6,8,9   |

### Lista III

Fornecedor com cobertura própria:

| Grupo     | Fornecedores | Itens disponíveis |
| --------- | ------------ | ----------------- |
| Lista III | D            | 1,2,4,5,8,9       |

### Lista IV

Fornecedor com cobertura própria:

| Grupo    | Fornecedores | Itens disponíveis |
| -------- | ------------ | ----------------- |
| Lista IV | G            | 1,3,4,5,8,9       |

---

### 7.4. Algoritmo básico de agrupamento

Entrada:

```text
L = conjunto de itens da lista
S = conjunto de fornecedores selecionados
```

Processamento:

```text
para cada fornecedor s em S:
    A_s = conjunto de itens de L disponíveis em s

agrupar fornecedores cujo conjunto A_s seja idêntico

para cada grupo G:
    itens_comuns_do_grupo = A_s
    itens_faltantes_do_grupo = L - A_s
```

Ordenação recomendada dos grupos:

1. Maior quantidade de itens disponíveis.
2. Maior quantidade de fornecedores no grupo.
3. Menor quantidade de itens faltantes.
4. Ordem alfabética dos fornecedores, se necessário.

---

### 7.5. Estratégia decremental opcional

Além do agrupamento por perfil idêntico, o sistema pode oferecer uma visão decremental por interseção.

Exemplo:

1. Identificar itens presentes em 100% dos fornecedores selecionados.
2. Remover esses itens da análise residual.
3. Identificar itens presentes em subconjuntos de fornecedores.
4. Repetir até que todos os itens sejam classificados.

Essa abordagem é útil para responder:

- Quais itens todo mundo tem?
- Quais itens a maioria tem?
- Quais itens apenas alguns fornecedores têm?
- Quais itens nenhum fornecedor tem?

Para o MVP, o agrupamento por perfil de cobertura é suficiente e aderente ao exemplo apresentado.

---

## 8. Orçamento

### 8.1. Tipos de orçamento

O sistema deve suportar duas visões principais:

1. **Orçamento por grupo**
   - Exibe valores por grupo de fornecedores.
   - Útil quando a lista foi dividida em listas paralelas.
   - Permite comparar fornecedores dentro do mesmo perfil de cobertura.

2. **Orçamento geral**
   - Exibe todos os fornecedores selecionados em uma única visão consolidada.
   - Mantém destaque de itens faltantes.
   - Permite comparar o custo global entre todos os fornecedores.

---

### 8.2. Orçamento por fornecedor

Para cada fornecedor, o sistema deve calcular:

- Subtotal dos itens disponíveis.
- Subtotal estimado dos itens faltantes, quando houver referência.
- Total disponível.
- Total estimado completo.
- Quantidade de itens atendidos.
- Percentual de cobertura da lista.
- Quantidade de itens faltantes.
- Lista detalhada de itens faltantes.

Fórmulas recomendadas:

```text
total_disponível =
soma(preço_unitário × quantidade_atendida)
para itens disponíveis no fornecedor

total_estimado_faltantes =
soma(preço_unitário_de_referência × quantidade_faltante)
para itens faltantes com referência

total_estimado_completo =
total_disponível + total_estimado_faltantes
```

---

### 8.3. Exemplo de orçamento por fornecedor

Para um fornecedor com:

```text
Itens disponíveis: 1,2,3,4,5,6,8,9
Itens faltantes: 7
```

O orçamento deve mostrar:

| Campo                                | Valor           |
| ------------------------------------ | --------------- |
| Itens disponíveis                    | 1,2,3,4,5,6,8,9 |
| Itens faltantes                      | 7               |
| Quantidade faltante                  | 1               |
| Valor de referência do item faltante | R$ 10,00        |
| Total disponível                     | R$ 250,00       |
| Total estimado completo              | R$ 260,00       |

---

### 8.4. Critério de destaque

O sistema deve permitir destacar:

- Menor orçamento.
- Maior orçamento.

Métricas possíveis para destaque:

| Métrica                       | Descrição                                                          |
| ----------------------------- | ------------------------------------------------------------------ |
| Menor total disponível        | Considera apenas itens vendidos pelo próprio fornecedor.           |
| Maior total disponível        | Considera apenas itens vendidos pelo próprio fornecedor.           |
| Menor total estimado completo | Considera itens disponíveis mais referência para faltantes.        |
| Maior total estimado completo | Considera itens disponíveis mais referência para faltantes.        |
| Melhor cobertura              | Destaca quem atende mais itens, podendo usar preço como desempate. |

Recomendação para MVP:

- Padrão: destacar o **menor total estimado completo**.
- Alternativa: destacar o **menor total disponível**.
- Opção adicional: destacar o **maior orçamento**, conforme escolha do usuário.

O destaque deve sempre indicar claramente qual métrica está sendo usada.

---

### 8.5. Empates

Em caso de empate:

- Exibir todos os fornecedores empatados com o mesmo destaque.
- Indicar que há empate técnica.
- Permitir ordenação secundária por:
  - Maior cobertura.
  - Menor quantidade de itens faltantes.
  - Ordem alfabética.

---

---

## 7. Critérios de Qualidade Aplicados

| Critério                           | Como foi atendido                                                                                                                            |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Aderência ao MVP**               | Apenas casos priorizados como "MVP" e "Alta" foram modelados. Funcionalidades fora do escopo (login, pagamentos, histórico) foram excluídas. |
| **Privacidade**                    | Nenhum caso prevê autenticação, cadastro ou persistência server-side.                                                                        |
| **Separação de responsabilidades** | Casos internos (UC15–UC17) abstraem lógica de domínio pura, alinhando-se à arquitetura recomendada.                                          |
| **Independência de tecnologia**    | O diagrama é agnóstico: serve igualmente para Frontend JS/Python, API Python/Go, MySQL/PostgreSQL.                                           |
| **Coesão de ator**                 | API Mock aparece apenas em casos de leitura de catálogo, refletindo corretamente seu papel passivo.                                          |
| **Testabilidade**                  | Casos internos isolados facilitam criação de testes unitários de regras de negócio.                                                          |
