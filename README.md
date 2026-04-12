# formation_evolutive_savard

### Portfolio evolutif — Formation en dessin industriel & Theorie mathematique

![Build Isabelle + LaTeX](https://github.com/2racinede4carreunivers-dev/formation_evolutive_savard/actions/workflows/build.yml/badge.svg)

---

## Presentation

Ce depot est un **portfolio professionnel evolutif** qui documente chronologiquement mon parcours, de ma theorie mathematique personnelle _L'Univers est au Carre_ jusqu'a ma formation en dessin industriel au CFP Neufchatel (debut : aout 2026).

Il sert de **CV dynamique** pour les recruteurs et employeurs, leur permettant de :

- Observer l'evolution de mes competences dans le temps
- Evaluer la rigueur de mon travail mathematique et technique
- Constater l'influence de la formation sur mes projets personnels

Chaque mise a jour est horodatee et chaque fichier source est certifie par attestation SLSA.

---

## Contenu du depot

### Theorie mathematique — _L'Univers est au Carre_

La theorie est presentee en quatre chapitres :

| # | Chapitre | Fichiers source |
|---|----------|----------------|
| 1 | **Geometrie du spectre des nombres premiers** | `src/tex/geometry_prime_spectrum.tex`, `src/hol/methode_spectral.thy`, `src/hol/methode_de_philippot.thy` |
| 2 | **Mecanique harmonique du chaos discret** | `src/tex/mecanique_harmonique_du_chaos_discret.tex`, `src/hol/mecanique_discret.thy` |
| 3 | **Postulat de l'univers est au carre** | `src/tex/postulat_de_univers_carre.tex`, `src/hol/postulat_carre.thy` |
| 4 | **Espace de Philippot** | `src/tex/espace_de_philippot.tex`, `src/hol/espace_philippot.thy` |

### Documents et preuves formelles

| Type | Emplacement | Description |
|------|-------------|-------------|
| `.tex` | `src/tex/` | Sources LaTeX des chapitres |
| `.thy` | `src/hol/` | Preuves formelles Isabelle/HOL |
| `.pdf` | `src/pdf/` | Documents compiles automatiquement |
| Images | `assets/images/` | Illustrations mathematiques (~15 images) |

### Application web — 3 IA collaboratives

Le dossier `Ia_geo_spec_prem_app_deplo/` contient une application web integrant trois intelligences artificielles :

1. **IA Collaborative** — Repond aux questions sur la theorie
2. **IA Socratique** — Guide par le questionnement
3. **IA Evolutive** — Banque de Q&R qui s'ameliore a chaque interaction

### Banque de questions/reponses

Le repertoire `qa_bank/` contient une banque evolutive de 56 Q&R validees, consultable dans `qa_bank/CATALOGUE.md`.

---

## Workflow et certification

### Build principal (actif)

A chaque push sur `main`, le workflow execute :

1. **Compilation Isabelle** — Les fichiers `.thy` sont compiles par Isabelle 2024
2. **Compilation LaTeX** — Les fichiers `.tex` sont compiles en PDF par TeX Live
3. **Attestation SLSA** — Certification cryptographique garantissant la provenance et l'integrite des 19 fichiers principaux
4. **Release automatique** — Creation d'une release versionnee avec les PDF et logs

### Workflows archives (code conserve, execution suspendue)

Les workflows suivants sont **neutralises** mais leur code reste visible pour illustrer les capacites du systeme :

| Workflow | Frequence originale | Statut |
|----------|-------------------|--------|
| Q&R Quotidien (`auto-daily-qa.yml`) | 3x/jour | Archive — code visible |
| Propositions Hebdomadaires (`auto-weekly-proposals.yml`) | Vendredi 14h UTC | Archive — code visible |
| Maintenance Mensuelle (`auto-monthly-maintenance.yml`) | 1er du mois 9h UTC | Archive — code visible |
| Generation Q&R au build (`build.yml` → job `generate_qa`) | A chaque push | Archive — code visible |

Ces workflows demonstrent la capacite a mettre en place une infrastructure CI/CD complete avec generation de contenu automatisee.

---

## Structure du depot

```
.github/workflows/          Workflows GitHub Actions (build + 3 archives)
.github/SECURITY.md         Politique de securite
src/tex/                    Sources LaTeX des chapitres
src/hol/                    Preuves formelles Isabelle/HOL (+ ROOT)
src/pdf/                    PDF compiles par le build
src/arborescence_*.md       Arborescences de coherence
assets/images/              Illustrations mathematiques
assets/animation/           Captures d'ecran et animations
scripts/                    Scripts Python (Q&R, maintenance, validation)
qa_bank/                    Banque Q&R evolutive (SQLite + catalogue)
docs/guides/                Guides d'utilisation (compilation, HOL, IA, securite)
proposals/                  Propositions d'amelioration
archive/                    Base de donnees du corpus Isabelle
Ia_geo_spec_prem_app_deplo/ Application web 3 IA collaboratives
geometrie_spectre_premier/  Sous-projet geometrie du spectre
corpus/                     Dependances Isabelle (Poly/ML)
CHANGELOG.md                Journal des modifications
SCRIPT_NARRATIF.md          Script narratif pour animation video
VERSION                     Version actuelle du depot
LICENSE                     Licence Apache 2.0
```

---

## Formation en dessin industriel

**Etablissement :** CFP Neufchatel, Quebec  
**Debut :** Aout 2026

Cette section sera enrichie au fil de la formation avec :

- Les modules completes et travaux realises
- L'influence de la formation sur mes projets mathematiques
- Les competences acquises en DAO, modelisation 3D, lecture de plans

Les mises a jour seront documentees chronologiquement dans le portfolio web associe.

---

## Guides d'utilisation

- [Guide de compilation](docs/guides/guide_compilation.md) — Compiler les fichiers LaTeX et Isabelle
- [Guide HOL](docs/guides/guide_HOL.md) — Utiliser les preuves formelles Isabelle/HOL
- [Guide de contribution](docs/guides/guide_contribution.md) — Comment contribuer
- [Guide de securite](docs/guides/guide_securite.md) — Politique de securite

---

## Licence

Ce depot est distribue sous la licence **Apache 2.0** ([LICENSE](LICENSE)).

Pour signaler une vulnerabilite : **philippethomassavard@gmail.com**

---

## Cloner le depot

```bash
git clone https://github.com/2racinede4carreunivers-dev/formation_evolutive_savard.git
```

---

*Philippe Thomas Savard — Portfolio evolutif — 2016–2026*
