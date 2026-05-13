# PRO3341 — Modelagem e Otimização de Sistemas de Produção

**Disciplina:** PRO3341 — 1º Semestre de 2026  
**Professora:** Prof.ª Dra. Celma O. Ribeiro  
**Escola Politécnica — USP**

---

## Descrição

Este repositório contém o projeto prático da disciplina PRO3341.
O projeto aplica técnicas de **Pesquisa Operacional** para resolver um problema real em parceria com uma empresa.

> **Empresa parceira:** [Nome da empresa]  
> **Problema:** [Breve descrição do problema]

---

## Estrutura do Repositório

```
.
├── main.tex              # Documento principal (inclui todos os relatórios)
├── capa.tex              # Capa do projeto
├── referencias.bib       # Referências bibliográficas (BibTeX)
├── Makefile              # Compilação automática
│
├── relatorio1/
│   └── relatorio1.tex    # R1 — Empresa, problema e concepção (entrega: 24/03)
├── relatorio2/
│   └── relatorio2.tex    # R2 — Formulação e primeiros resultados (entrega: 13/05)
├── relatorio3/
│   └── relatorio3.tex    # R3 — Resultados finais (entrega: 10/06)
│
├── figuras/              # Imagens e gráficos
└── codigo/               # Scripts Python / LINDO / Gurobi etc.
```

---

## Como Compilar

### Pré-requisitos
- TeX Live 2022+ ou MiKTeX (com pacotes `biblatex-abnt` e `biber`)
- `latexmk`

### Compilação
```bash
make          # gera main.pdf
make watch    # recompila automaticamente ao salvar
make clean    # remove arquivos auxiliares
```

Ou manualmente:
```bash
pdflatex main
biber main
pdflatex main
pdflatex main
```

---

## Cronograma de Entregas

| Relatório | Conteúdo | Entrega |
|-----------|----------|---------|
| 1º | Empresa, problema, concepção da modelagem, carta + artigo/exercício | **24/03/2026** |
| 2º | Formulação matemática, bibliografi, primeiros resultados | **13/05/2026** |
| 3º | Resultados finais, comparação, análise de sensibilidade, trabalhos futuros | **10/06/2026** |

---

## Grupo

- [Aluno 1]
- [Aluno 2]
- [Aluno 3]
- [Aluno 4]

---

## Referências Principais

- Winston & Venkataramanan, *Introduction to Mathematical Programming*, 4ª ed., Duxbury, 2002.
- Arenales et al., *Pesquisa Operacional para Cursos de Engenharia*, Campus, 2007.
- Hillier & Lieberman, *Introdução à Pesquisa Operacional*, McGraw-Hill, 2006.
