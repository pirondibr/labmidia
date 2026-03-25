# Processo: Analise-Concorrencia-Seo

Este processo gera um relatório em HTML para analisar **concorrência orgânica no Google** para uma palavra-chave específica, comparando o cliente com o **Top 10 da SERP** e (quando possível via Semrush) trazendo **tráfego de marca vs. sem marca**.

---

## Entradas

- **Site do cliente**: `apetsaude.com.br`
- **Palavra-chave**: `plano de saude pet`
- **Base Semrush**: `br`

---

## Saída

- Um HTML com:
  - Top 10 domínios do Google para a keyword
  - Tráfego do cliente (marca / sem marca) e o mesmo para concorrentes (quando disponível)
  - Uma coluna comparando em **%** a **marca do cliente** com a marca de cada concorrente

---

## Etapas (Semrush MCP)

### 1) Top 10 concorrentes no Google (SERP orgânica)

Ferramenta:
- `semrush_keyword_organic`

Parâmetros:
- `keyword`: `plano de saude pet`
- `database`: `br`
- `limit`: `10`

Isso retorna os domínios e URLs que aparecem hoje nas 10 primeiras posições.

---

### 2) Tráfego orgânico total por domínio (baseline)

Ferramenta:
- `semrush_domain_overview`

Parâmetros:
- `domain`: domínio do cliente e de cada concorrente do Top 10
- `database`: `br`

Saídas esperadas:
- `Organic Traffic`
- `Organic Keywords`

---

### 3) Split de tráfego: Marca vs. Sem marca (estimativa)

Ferramenta:
- `semrush_domain_organic_keywords`

Parâmetros:
- `domain`: domínio a analisar
- `database`: `br`
- `limit`: `1000` (quanto maior, melhor a estimativa)

Método (estimativa prática):
- Separar keywords em:
  - **Marca**: contém tokens de marca (ex.: para APet: `apet`, `apetsaude`, `amigoo`)
  - **Sem marca**: o restante
- Somar `Traffic (%)` das keywords de marca vs. total
- Estimar:
  - `Trafego Marca ≈ OrganicTraffic * (ShareMarca)`
  - `Trafego SemMarca ≈ OrganicTraffic - TrafegoMarca`

Observação:
- Se houver duplicatas da mesma keyword para URLs diferentes, usar a **melhor posição** quando precisar de posição; para share por tráfego, somar por keyword normalizada (evita dupla contagem).

---

### 4) Comparativo % (marca do cliente vs concorrentes)

Para cada concorrente:

\[
%MarcaClienteVsConcorrente = \\frac{MarcaCliente}{MarcaConcorrente} \\times 100
\]

Tratamento de borda:
- Se `MarcaConcorrente = 0`, marcar como `N/A`.

---

## Limitação encontrada nesta execução (importante)

Durante esta execução, as chamadas de domínio do Semrush retornaram **HTTP 403** (Forbidden) para:
- `semrush_domain_overview`
- `semrush_domain_organic_keywords`

Mas as chamadas de SERP e keyword overview continuaram funcionando.

Impacto:
- Foi possível gerar o **Top 10 do Google** via Semrush.
- Não foi possível preencher **tráfego marca/sem marca** e o **comparativo %** automaticamente nesta rodada.

Solução recomendada:
- Reexecutar as etapas 2 e 3 quando o acesso às rotas de domínio estiver liberado (quota/unidades/permite do plano).

---

## Arquivo gerado nesta rodada

- `relatorio-apet-concorrencia-seo.html`

