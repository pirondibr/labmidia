# Processo: Pesquisa SEO de Palavras (Topo x Fundo de Funil)

Este documento descreve o processo usado para criar um relatório SEO em HTML, separando palavras-chave entre **Topo de Funil** (educação/intenção informacional) e **Fundo de Funil** (compra/comparação/intenção comercial), usando dados do **Semrush via MCP** dentro do Cursor.

---

## Objetivo

- **Entrada**: Um site/cliente (ex.: `apetsaude.com.br`) + banco Semrush (ex.: `br`)
- **Saída**: Um arquivo HTML com:
  - lista de palavras-chave em **Fundo de funil** e **Topo de funil**
  - **Pesquisa Mensal** (volume) e **posição do domínio** quando existir
  - uma seção de metodologia
- **Publicação**: Subir o HTML para o GitHub e acessar via GitHub Pages

---

## Contexto (o que foi analisado no site)

Para `apetsaude.com.br`, a análise rápida do conteúdo identificou os principais “pilares” do produto:

- **Plano de saúde / assistência pet** (cães e gatos)
- **Reembolso** (processo digital + documentação)
- **Teleconsulta veterinária** (telemedicina 24h)
- **Coberturas** (consulta, especialista, internação, cirurgias, exames, vacinas, etc.)
- **Planos** (nomes e níveis: Amigoo, Melhor Amigoo, etc.)

Esses pilares viram “seeds” (termos base) para gerar palavras relacionadas no Semrush.

---

## Ferramentas usadas (Semrush MCP)

No Cursor, usamos as ferramentas do Semrush expostas via MCP. As principais usadas neste fluxo foram:

- **`semrush_domain_overview`**
  - objetivo: obter panorama do domínio (keywords orgânicas, tráfego orgânico, custo orgânico etc.)
- **`semrush_domain_organic_keywords`** (neste workspace aparece como `semrush_domain_organid3c9dda`)
  - objetivo: listar keywords orgânicas do domínio com posição, volume, URL etc.
- **`semrush_broad_match_keywords`**
  - objetivo: gerar ideias de keywords por correspondência ampla (ótimo para descobrir variações)
- **`semrush_related_keywords`**
  - objetivo: descobrir termos próximos e variações
- **`semrush_phrase_questions`**
  - objetivo: coletar perguntas (ótimo para Topo de Funil)

Banco usado: **Brasil (`br`)**.

---

## Passo a passo do processo

### 1) Checar visão geral do domínio (baseline)

Chamada:

- `semrush_domain_overview` com:
  - `domain`: `apetsaude.com.br`
  - `database`: `br`

Usamos isso para:
- validar se o domínio já tem tração orgânica
- registrar números do topo do relatório (keywords orgânicas e tráfego)

---

### 2) Baixar keywords orgânicas do domínio (para preencher posições reais)

Chamada:

- `semrush_domain_organic_keywords` (tool `semrush_domain_organid3c9dda`) com:
  - `domain`: `apetsaude.com.br`
  - `database`: `br`
  - `limit`: 200 (ou mais, dependendo do objetivo)

Por quê isso é importante:
- Muitas vezes a “sensação” é que o site não ranqueia, mas ele pode estar ranqueando em termos relevantes.
- O relatório final precisa mostrar **posição real**, quando existir (ex.: “plano de saúde pet” em #22).

Regra usada:
- Se a keyword aparecer mais de uma vez (URLs diferentes), considerar a **melhor posição** (menor número).

---

### 3) Gerar ideias de keywords com “seeds” do negócio

Seeds usadas (exemplos):
- `plano de saude pet`
- `plano veterinario`
- `convenio pet`
- `teleconsulta veterinaria`
- `seguro saude pet`
- `assistencia pet`

Chamadas típicas:
- `semrush_broad_match_keywords` com `keyword=<seed>`, `database=br`, `limit=25`
- `semrush_related_keywords` com `keyword=<seed>`, `database=br`, `limit=25`
- `semrush_phrase_questions` com `keyword=<seed>`, `database=br`, `limit=20`

Objetivo:
- levantar termos de **compra/comparação** (Fundo)
- levantar termos em formato de **pergunta** e “como/quanto/vale a pena” (Topo)

---

### 4) Classificar em Topo vs Fundo de funil

Heurística prática usada:

- **Fundo de funil** (intenção comercial):
  - termos como “plano”, “convênio”, “seguro”, “preço”, “sem coparticipação”, “sem carência”
  - termos de produto/solução direta (ex.: “plano de saúde pet”, “plano veterinário”)

- **Topo de funil** (intenção informacional):
  - perguntas: “qual”, “como”, “vale a pena”, “quanto custa”, “o que cobre”
  - dúvidas sobre regras/uso: carência, preexistência, reembolso, documentação

Observação:
- Algumas perguntas podem ter volume baixo/zero no Semrush; mesmo assim são úteis para **conteúdo FAQ** e cauda longa.

---

### 5) Montar o relatório em HTML

Arquivo gerado:
- `relatorio-apet-seo-funil.html`

Conteúdo do relatório:
- cards com baseline (tráfego orgânico, keywords orgânicas, etc.)
- tabela **Fundo de Funil** (compra/comparação)
- tabela **Topo de Funil** (perguntas/dúvidas)
- metodologia

Preenchimento de posição no HTML:
- Se a keyword estiver nas orgânicas do domínio: mostrar a posição (ex.: #22)
- Caso não esteja: usar `0`

---

### 6) Publicar no GitHub Pages

Comandos usados:

```bash
git add relatorio-apet-seo-funil.html
git commit -m "Add APet SEO funnel report (top vs bottom keywords)"
git push origin main
```

Depois, o arquivo fica disponível via GitHub Pages em:

- `https://pirondibr.github.io/labmidia/relatorio-apet-seo-funil.html`

---

## Checklist rápido (para repetir em qualquer cliente)

- [ ] Identificar 5–10 “seeds” do negócio (serviços, produto, dores, diferenciais)
- [ ] Rodar `domain_overview` (baseline)
- [ ] Rodar `domain_organic_keywords` (posições reais)
- [ ] Rodar `broad_match`, `related`, `questions` para cada seed
- [ ] Selecionar e deduplicar keywords
- [ ] Classificar em Topo vs Fundo
- [ ] Preencher posição do domínio (melhor posição se houver duplicata)
- [ ] Gerar HTML e publicar

