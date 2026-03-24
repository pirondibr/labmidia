# Processo: Relatorio SEO Comparativo (Cliente vs Concorrente)

Documentacao do fluxo completo para gerar um relatorio HTML de SEO comparando a performance organica de um cliente contra concorrentes, utilizando dados do Semrush via MCP.

---

## Visao Geral

| Item | Detalhe |
|------|---------|
| **Cliente** | lacoscorporativos.com.br |
| **Concorrente base** | matbrindes.com.br |
| **Benchmark adicional** | somarcas.com.br |
| **Banco de dados** | Brasil (br) |
| **Ferramenta** | Semrush API via MCP no Cursor |
| **Saida** | Relatorio HTML publicado no GitHub Pages |

---

## Etapas do Processo

### 1. Configuracao do Semrush MCP

1. Instalar o pacote na pasta do projeto:
   ```
   npm init -y
   npm install semrush-mcp
   ```
2. Criar o arquivo `.cursor/mcp.json` para registrar o servidor no Cursor:
   ```json
   {
     "mcpServers": {
       "semrush": {
         "command": "npx",
         "args": ["semrush-mcp"]
       }
     }
   }
   ```
3. Recarregar o Cursor (`Ctrl+Shift+P` > `Developer: Reload Window`).
4. Verificar se o servidor `semrush` aparece em Settings > MCP/Tools.

### 2. Coleta de Dados do Concorrente (Dominio Base)

1. Usar o endpoint `semrush_domain_organic_keywords` com:
   - `domain`: dominio do concorrente (ex: `matbrindes.com.br`)
   - `database`: `br`
   - `limit`: `30` (top 30 palavras)
2. O retorno contem: keyword, posicao, volume de busca, CPC, URL, trafego estimado, etc.
3. Anotar as 30 keywords e suas metricas para usar como base de comparacao.

### 3. Coleta de Dados do Cliente e Benchmarks

1. Usar o mesmo endpoint para cada dominio adicional com `limit: 1000`:
   - `lacoscorporativos.com.br`
   - `somarcas.com.br`
2. Exportar os dados para arquivos `.xlsx` com colunas: Keyword, Position, Search Volume, CPC, URL, etc.
3. Arquivos gerados:
   - `lacos-keywords-posicoes.xlsx`
   - `somarcas-keywords-posicoes.xlsx`

### 4. Cruzamento de Posicoes

1. Para cada uma das 30 keywords do concorrente, buscar a posicao correspondente nos arquivos XLSX do cliente e benchmarks.
2. **Normalizacao obrigatoria**: converter keywords para minusculas e remover acentos antes de comparar, para evitar falhas de correspondencia (ex: `mães` vs `maes`).
3. **Duplicatas**: quando a mesma keyword aparece mais de uma vez no XLSX (URLs diferentes), usar a **melhor posicao (menor numero)**.
4. Marcar como `N/R` (Nao Ranqueia) quando a keyword nao for encontrada no recorte do dominio.

### 5. Coleta de Dados de Trafego

1. Usar o endpoint `semrush_domain_overview` para cada dominio com `database: br`.
2. Extrair: Organic Traffic, Organic Keywords, Organic Cost.
3. Montar tabela comparativa de trafego entre os dominios.

### 6. Montagem do Relatorio HTML

O relatorio final contem as seguintes secoes:

| Secao | Conteudo |
|-------|----------|
| **Header** | Dominios analisados, base de dados, data |
| **Cards de metricas** | Palavras analisadas, cobertura do cliente, nao ranqueadas |
| **Resumo Executivo** | Analise textual do cenario |
| **Situacao do Trafego SEO** | Grafico historico de trafego organico do cliente (imagem) |
| **Tabela Comparativa** | Top 30 palavras com pesquisa mensal, posicao do concorrente e do cliente |
| **Comparativo de Trafego** | Cards visuais com trafego organico total de cada dominio |
| **Metodologia** | Descricao tecnica do processo |

### 7. Versoes de Layout

Foram criadas 3 versoes com estilos diferentes para escolha:

| Versao | Arquivo | Estilo |
|--------|---------|--------|
| V1 | `relatorio-v1-dark.html` | Dark mode executivo com gradientes |
| V2 | `relatorio-v2-corporate.html` | Corporate clean com barras visuais |
| V3 | `relatorio-v3-modern.html` | Moderno colorido com badges e glass morphism |
| **V2 Final** | `relatorio-v2-final.html` | V2 refinado com grafico de trafego e ajustes |

### 8. Publicacao no GitHub Pages

1. Inicializar repositorio git na pasta do projeto:
   ```
   git init
   git add -A
   git commit -m "Relatorio comparativo SEO"
   ```
2. Conectar ao repositorio remoto:
   ```
   git remote add origin https://github.com/usuario/repo.git
   git branch -M main
   git push -u origin main
   ```
3. Tornar o repositorio publico (necessario para Pages no plano free):
   ```
   gh repo edit usuario/repo --visibility public --accept-visibility-change-consequences
   ```
4. Ativar GitHub Pages via API:
   ```powershell
   '{"source":{"branch":"main","path":"/"}}' | gh api repos/usuario/repo/pages -X POST --input -
   ```
5. Links ficam disponiveis em: `https://usuario.github.io/repo/nome-do-arquivo.html`

---

## Cuidados e Licoes Aprendidas

### Normalizacao de Keywords
- **Sempre** normalizar keywords (lowercase + remover acentos) antes de cruzar dados entre dominios.
- Sem isso, palavras com acentos (ex: `mães`) nao casam com variantes sem acento (ex: `maes`).

### Duplicatas no XLSX
- O Semrush pode retornar a mesma keyword para URLs diferentes do mesmo dominio.
- Usar sempre a **melhor posicao** (menor numero) para representar o dominio.

### Limites da API
- O endpoint de keywords organicas pode ter limite de `1000` linhas dependendo do plano.
- Requests acima do limite retornam erro `403`.

### Keywords de Marca
- Remover keywords de marca do concorrente (ex: `matbrindes`) da tabela comparativa, pois nao sao disputaveis.

### Nomes de Arquivos
- Evitar espacos em nomes de arquivos HTML publicados na web. Usar hifens (`-`) no lugar.

---

## Estrutura de Arquivos do Projeto

```
semrush relatorio/
├── .cursor/
│   └── mcp.json                          # Config do Semrush MCP
├── .gitignore
├── grafico-trafego-lacos.png             # Screenshot do grafico Semrush
├── lacos-keywords-posicoes.xlsx          # Export keywords Lacos
├── somarcas-keywords-posicoes.xlsx       # Export keywords So Marcas
├── relatorio-v2-final.html              # Relatorio final (versao escolhida)
├── relatorio-v1-dark.html               # Layout dark mode
├── relatorio-v2-corporate.html          # Layout corporate
├── relatorio-v3-modern.html             # Layout moderno
├── Relatorio-Seo-Ia-lacos.html          # Relatorio de visibilidade em IA
├── processo-relatorio-seo.md            # Este documento
├── package.json
└── package-lock.json
```

---

## Links Publicados

- **Relatorio V2 Final**: https://pirondibr.github.io/labmidia/relatorio-v2-final.html
- **Relatorio SEO IA**: https://pirondibr.github.io/labmidia/Relatorio-Seo-Ia-lacos.html
- **Repositorio**: https://github.com/pirondibr/labmidia
