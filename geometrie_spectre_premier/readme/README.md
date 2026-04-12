formation_evolutive_savard/
├── .github/
│   └── workflows/
│       └── build-and-attest.yml
│
├── espace_philippot/
│   ├── espace_philippot.tex
│   └── espace_philippot.thy
│
├── geometrie_spectre_premier/
│   ├── HOL/
│   ├── LaTeX/
│   ├── pdf_finaux/
│   ├── python/
│   └── readme/
│
├── mecanique_harmonique_chaos_discret/
│   ├── HOL/
│   ├── LaTeX/
│   ├── PDF/
│   └── python/
│
├── squaring/
│   ├── postulat_carre.thy
│   └── postulat_univers_carre.tex
│
├── LaTeX/
│   └── images/
│
├── python/
│
├── CHANGELOG.md
├── VERSION
├── README.md
└── divers fichiers .tex, .thy et images à la racine

#  Structure du projet

Voici les dossiers principaux du dépôt, chacun lié à sa fonction dans la théorie.

- [geometrie_spectre_premier/](https://github.com/2racinede4carreunivers-dev/analyse-de-la-conjecture-zeta-riemann-savard/tree/main/geometrie_spectre_premier)  
  → Théorie géométrique du spectre des nombres premiers, LaTeX, images, PDF, IA évolutive.

- [mecanique_harmonique_chaos_discret/](https://github.com/2racinede4carreunivers-dev/analyse-de-la-conjecture-zeta-riemann-savard/tree/main/mecanique_harmonique_chaos_discret)  
  → Formalisation du chaos discret, mécanique harmonique, Isabelle/HOL, PDF.

- [LaTeX/](https://github.com/2racinede4carreunivers-dev/analyse-de-la-conjecture-zeta-riemann-savard/tree/main/LaTeX)  
  → Sources LaTeX globales du projet.

- [pdf_finaux/](https://github.com/2racinede4carreunivers-dev/analyse-de-la-conjecture-zeta-riemann-savard/tree/main/pdf_finaux)  
  → Documents finaux prêts pour publication.

- [python/](https://github.com/2racinede4carreunivers-dev/analyse-de-la-conjecture-zeta-riemann-savard/tree/main/python)  
  → Scripts Python utilitaires.

- [readme/](https://github.com/2racinede4carreunivers-dev/analyse-de-la-conjecture-zeta-riemann-savard/tree/main/readme)  
  → Documentation détaillée : guides, licences, sécurité.

- [app/](https://github.com/2racinede4carreunivers-dev/analyse-de-la-conjecture-zeta-riemann-savard/tree/main/app)  
  → (Racine) Dossier réservé pour extensions futures ou outils externes.

# Géométrie du spectre des nombres premiers
Projet conceptuel et formel de Philippe Thomas Savard

Ce dépôt présente un projet d’analyse conceptuelle lié à la conjecture de la fonction zêta de Bernhard Riemann. L’approche développée ici, appelée géométrie du spectre des nombres premiers, propose un outil dynamique permettant d’examiner la structure des nombres premiers et leur relation avec les propriétés analytiques de la fonction zêta.

Le projet repose sur deux méthodes validées par des scripts Isabelle/HOL, accompagnées de documents LaTeX explicatifs en français et en anglais. L’ensemble du contenu est distribué sous licence Apache 2.0.

---

## 1. Présentation générale

L’objectif du projet est d’explorer la conjecture de Riemann à travers une approche personnelle et conceptuelle. Deux scripts Isabelle/HOL structurent cette démarche :

- `methode_de_philippot.thy`
- `methode_spectral.thy`

Ces fichiers sont validés par Isabelle/HOL et inclus dans le dépôt. Les documents LaTeX associés détaillent les méthodes, les exemples de calculs et les fondements conceptuels.

---

## 2. Méthode de Philippôt

La méthode de Philippôt constitue le premier chapitre du projet. Elle vise à vérifier qu’il est cohérent de poser la question de la conjecture de Riemann avant d’en entreprendre l’analyse.

Les idées principales sont les suivantes :

- Les zéros non triviaux de la fonction zêta sont infinis.
- Les nombres premiers sont également infinis.
- La conjecture affirme que tous les zéros non triviaux ont une partie réelle égale à \(1/2\).
- La méthode explore, par des suites rationnelles et des opérations itératives, la possibilité de générer indéfiniment la valeur \(1/2\).
- Si cette génération s’était révélée impossible, la conjecture aurait été infirmée par l’absurde.

Le fichier `methode_de_philippot.thy` formalise cette méthode et en assure la validité logique.

---

## 3. Méthode spectrale

Le second chapitre, formalisé dans `methode_spectral.thy`, présente la méthode spectrale, cœur de la géométrie du spectre des nombres premiers.

Cette méthode repose sur l’idée que :

> Pour tout entier \(n \ge 1\) ou \(n \le -1\), chaque valeur de \(n\) correspond à un nombre premier \(P\). Les suites \(A\) et \(B\) déterminent la valeur de \(n\), et le rapport spectral \(1/k\) est numériquement valide mais algébriquement incohérent.

Le fichier détaille notamment :

- la construction des suites \(A\) et \(B\),
- la substitution liée à la lettre grecque zêta et au digamma,
- les équations généralisées pour déterminer les suites,
- des exemples de calculs (29, 31, 37, 41),
- le rôle particulier du digamma,
- la détermination des nombres premiers à partir de \(n\),
- les rapports spectraux \(1/2\), \(1/3\), \(1/4\),
- les écarts entre nombres premiers selon ces rapports,
- l’axiomatisation reliant :
  - la fonction zêta,
  - le rapport spectral,
  - la valeur de \(n\),
  - la densité des zéros sur la droite critique.

---

## 7. Mécanique harmonique du chaos discret

Ce chapitre formalise la **mécanique harmonique du chaos discret**, un système géométrique et matriciel structuré en trois parties :

### A. Axiomatisation géométrique
- Carrés emboîtés de côté \(1.5^n\).
- Triangle inscrit dépendant d’un nombre premier \(p\).
- Rapport fondamental demi‑base / hauteur = \(\sqrt{p}\).
- Angle associé : \(\theta(p) = \arctan(\sqrt{p})\).
- Définition et invariance de l’unité géométrique \(U(p) = \sqrt{p} + 1\).

### B. Cardan sans blocage
- Construction polaire d’un cardan géométrique.
- Angles structurants : 60°, 75°, 45°.
- Longueurs internes définies formellement.
- Points du cardan utilisés pour la structure matricielle.

### C. Matrice à dérivée première
- Définition des coefficients C1…C9 et des lignes R1…R3.
- Matrice M1 (mesures du plan).
- Matrice M2 (matrice de transition).
- Version simplifiée basée sur des nombres premiers.
- Introduction de l’inconnue unique \(u = \sqrt{3.375}\).
- Facteur trigonométrique alternatif lié à \(1/\sqrt{p}\).

### Documents associés
- Isabelle/HOL : [`mecanique_discret.thy`](./mecanique_harmonique_chaos_discret/mecanique_discret.thy)  
- LaTeX : [`mecanique_discret.tex`](./mecanique_harmonique_chaos_discret/mecanique_discret.tex)

Ce chapitre constitue un élément central de la théorie **L’univers est au carré**, reliant géométrie, trigonométrie, nombres premiers et structures matricielles.


## 8. Postulat de l’Univers Carré

Ce chapitre formalise le **postulat du carré unifié**, une structure reliant rectangles, carrés, polygones et nombres premiers au sein de la théorie **L’univers est au carré**.

### 1. Postulat carré et nombres premiers
- Définition des surfaces :  
  - \(S_S\) (surface totale),  
  - \(S_F\) (surface carrée interne),  
  - \(S_C\) (surface complémentaire).
- Définition des diagonales : \(d_S\), \(d_F\), \(d_C\).
- Unité associée au nombre premier :  
  

\[
  unit_p = \sqrt{p} + 1
  \]


- Définition de l’indice \(k\) via la liste \([2 ..< p+1]\).
- Équation centrale du postulat :  
  

\[
  (diag \cdot \sqrt{unit_p})^2 = k \cdot area + h^2
  \]


- Deux rapports fondamentaux :  
  - rapport hauteur/côté : \(h/s = \sqrt{p} + 1\),  
  - rapport tronqué : \(t/s = \sqrt{p}\).

### 2. Rectangle carré : équivalence
- Définition de l’aire d’un rectangle et d’un carré.
- Condition d’équivalence :  
  

\[
  w \cdot h = s^2
  \]



### 3. Axiomatisation du polygone carré
- Trois équations fondamentales :  
  - ratio de hauteur,  
  - ratio tronqué,  
  - équation du postulat.  
- Définition d’un **polygone carré** comme satisfaction simultanée des trois équations.

### 4. Exemple formel pour \(p = 3\)
- Vérification symbolique des trois rapports et de la diagonale tronquée.
- Définition de l’aire associée.

### Documents associés
- Isabelle/HOL : [`postulat_carre.thy`](./postulat_carre/postulat_carre.thy)  
- LaTeX : [`postulat_carre.tex`](./postulat_carre/postulat_carre.tex)

Ce chapitre établit la structure mathématique du **postulat carré**, reliant surfaces, diagonales, rapports géométriques et nombres premiers dans la théorie *L’univers est au carré*.


## 6. Espace de Philippôt

Le chapitre *Espace de Philippôt* constitue le troisième pilier de la théorie unifiée **L’univers est au carré**.  
Il s’ajoute aux deux méthodes fondatrices — la méthode de Philippôt et la méthode spectrale — et introduit une nouvelle structure conceptuelle permettant d’étendre la géométrie du spectre des nombres premiers.

Ce chapitre repose sur deux fichiers principaux :

- `espace_philippot.thy`  
  → Formalisation Isabelle/HOL de la structure de l’espace de Philippôt, de ses axiomes et de ses propriétés internes.

- `espace_philippot.tex`  
  → Document LaTeX décrivant les fondements conceptuels, les définitions, les exemples et les interprétations géométriques associées.

### Objectifs du chapitre

L’espace de Philippôt vise à :

- introduire une structure géométrique complémentaire aux suites spectrales ;
- définir un espace conceptuel permettant de relier les rapports spectraux aux transformations internes de la théorie ;
- proposer une extension naturelle de la méthode spectrale, en intégrant des propriétés topologiques et dynamiques ;
- offrir un cadre unifié pour l’interprétation des valeurs rationnelles, des rapports spectraux et des comportements asymptotiques.

### Rôle dans la théorie unifiée

L’espace de Philippôt agit comme un **espace de cohérence** entre :

- les suites rationnelles de la méthode de Philippôt ;
- les rapports spectraux de la méthode spectrale ;
- les transformations internes de la théorie *L’univers est au carré*.

Il permet d’exprimer ces trois composantes dans un cadre unique, cohérent et formellement vérifiable.

### Intégration au dépôt

Le chapitre est intégré dans la structure existante du projet :

- les fichiers `.thy` sont validés automatiquement par Isabelle/HOL ;
- les fichiers `.tex` sont compilés automatiquement en PDF ;
- le chapitre est inclus dans les documents finaux du dépôt.

Ce chapitre constitue une extension majeure du projet et renforce la cohérence globale de la théorie.


## 4. Documents LaTeX

Deux documents LaTeX (français et anglais) accompagnent les scripts Isabelle/HOL. Ils présentent :

- des explications détaillées des deux méthodes,
- des exemples de calculs,
- des illustrations conceptuelles,
- des démonstrations textuelles rédigées par l’auteur.

Ces documents servent de guide pour les utilisateurs souhaitant comprendre ou modifier le projet.

---

## 5. Référence au code Lean consulté

Pour la section portant sur l’axiomatisation de la fonction zêta et de la conjecture, du code Lean provenant du dépôt suivant a été consulté et adapté conformément à la licence Apache 2.0 :

Dépôt Lean (mathlib3) :  
https://github.com/leanprover-community/mathlib3.git

Ce dépôt contient la formalisation Lean de la fonction zêta, des L‑fonctions et d’éléments liés à l’hypothèse de Riemann.

---

## Certification continue (CI)

Depuis mars 2026, la compilation du dépôt est entièrement automatisée grâce au workflow GitHub Actions intégré au projet.

### Fonctionnement de la certification

À **chaque commit manuel** poussé vers le dépôt :

1. Isabelle/HOL compile automatiquement l’ensemble des fichiers `.thy` du projet, incluant :
   - `methode_de_philippot.thy`
   - `methode_spectral.thy`
   - `espace_philippot.thy`
   - ainsi que tous les modules associés.

2. MiKTeX compile automatiquement tous les fichiers LaTeX `.tex`, incluant :
   - les documents principaux,
   - les annexes,
   - les chapitres additionnels,
   - `espace_philippot.tex`.

3. Le workflow vérifie :
   - la validité logique des fichiers Isabelle/HOL,
   - la génération correcte des PDF,
   - l’absence d’erreurs de compilation.

### Garantie de stabilité

Cette certification continue assure que :

- **chaque commit** du dépôt est garanti compilable ;
- les fichiers `.thy` sont toujours logiquement valides ;
- les documents LaTeX sont toujours générés sans erreur ;
- les chapitres nouveaux (dont *Espace de Philippôt*) sont automatiquement intégrés dans le pipeline.

### Environnement de compilation

Le workflow utilise :

- **Isabelle2025‑2**  
- **MiKTeX**  
- **Ubuntu GitHub Actions Runner**

Les badges de compilation reflètent désormais l’état **en temps réel** du dépôt.

## Developer Certificate of Origin (DCO)

This repository uses the **Developer Certificate of Origin (DCO)** to ensure that all contributions comply with copyright rules and the project’s licensing terms.

By submitting a contribution (commit, pull request, or modification), you certify that:

- your contribution is your own original work **or** you have the legal right to submit it (for example, permission from your employer);
- you agree that your contribution will be distributed under the project’s **Apache 2.0 license**;
- you understand that you are **fully responsible** for your modifications and their consequences;
- you acknowledge that the main author provides **no warranty** and assumes **no liability** for versions modified by third parties.

Each commit must include a DCO signature line:

For more information, see the official DCO text:  
https://developercertificate.org/

## 6. Licence

Ce projet est distribué sous licence Apache 2.0. Les utilisateurs peuvent consulter, utiliser, modifier et redistribuer le contenu selon les termes de la licence incluse dans le dépôt.


Texte officiel du DCO :  
https://developercertificate.org/

---

## 6. Licence (version anglaise officielle)

Ce projet est distribué sous la licence **Apache 2.0**.  
Le texte complet de la licence se trouve dans le fichier `LICENSE` :

https://www.apache.org/licenses/LICENSE-2.0

# Geometry of the Prime Number Spectrum
Conceptual and formal project by Philippe Thomas Savard

formation_evolutive_savard/
├── .github/
│   └── workflows/
│       └── build-and-attest.yml
│
├── espace_philippot/
│   ├── espace_philippot.tex
│   └── espace_philippot.thy
│
├── geometrie_spectre_premier/
│   ├── HOL/
│   ├── LaTeX/
│   ├── pdf_finaux/
│   ├── python/
│   └── readme/
│
├── mecanique_harmonique_chaos_discret/
│   ├── HOL/
│   ├── LaTeX/
│   ├── PDF/
│   └── python/
│
├── squaring/
│   ├── postulat_carre.thy
│   └── postulat_univers_carre.tex
│
├── LaTeX/
│   └── images/
│
├── python/
│
├── CHANGELOG.md
├── VERSION
├── README.md
└── divers fichiers .tex, .thy et images à la racine


This repository presents a conceptual analysis project related to Bernhard Riemann’s zeta function conjecture. The approach developed here, called the *geometry of the prime number spectrum*, proposes a dynamic tool to examine the structure of prime numbers and their relationship with the analytic properties of the zeta function.

The project is based on two methods validated by Isabelle/HOL scripts, accompanied by explanatory LaTeX documents in both French and English. All content is distributed under the Apache 2.0 license (official English version).

---

## 1. General overview

The goal of this project is to explore the Riemann Hypothesis through a personal and conceptual approach. Two Isabelle/HOL scripts structure this work:

- `methode_de_philippot.thy`
- `methode_spectral.thy`

These files are validated by Isabelle/HOL and included in the repository. The associated LaTeX documents provide detailed explanations, examples, and conceptual foundations.

---

## 2. Philippôt’s method

Philippôt’s method forms the first chapter of the project. It aims to verify that it is coherent to pose the question of the Riemann Hypothesis before attempting to analyze it.

Key ideas include:

- The nontrivial zeros of the zeta function are infinite.
- Prime numbers are also infinite.
- The conjecture states that all nontrivial zeros have real part equal to 1/2.
- The method explores, through rational sequences and iterative operations, the possibility of generating the value 1/2 indefinitely.
- If such generation had proven impossible, the conjecture would have been refuted by contradiction.

The file `methode_de_philippot.thy` formalizes this method and ensures its logical validity.

---

## 3. Spectral method

The second chapter, formalized in `methode_spectral.thy`, presents the spectral method, the core of the geometry of the prime number spectrum.

This method is based on the idea that:

> For any integer \(n \ge 1\) or \(n \le -1\), each value of \(n\) corresponds to a prime number \(P\). The sequences \(A\) and \(B\) determine the value of \(n\), and the spectral ratio \(1/k\) is numerically valid but algebraically inconsistent.

The file details:

- the construction of sequences \(A\) and \(B\),
- the substitution involving the Greek letter zeta and the digamma,
- generalized equations for determining the sequences,
- calculation examples (29, 31, 37, 41),
- the special role of the digamma,
- determining prime numbers from \(n\),
- spectral ratios 1/2, 1/3, 1/4,
- prime gaps according to these ratios,
- the axiomatisation linking:
  - the zeta function,
  - the spectral ratio,
  - the value of \(n\),
  - the density of zeros on the critical line.

---

## 7. Harmonic Mechanics of Discrete Chaos

This chapter formalizes the **harmonic mechanics of discrete chaos**, a geometric and matrix‑based system structured into three main components:

### A. Geometric Axiomatization
- Nested squares of side \(1.5^n\).
- An inscribed triangle defined by a prime number \(p\).
- Fundamental ratio: half‑base / height = \(\sqrt{p}\).
- Associated angle: \(\theta(p) = \arctan(\sqrt{p})\).
- Definition and invariance of the geometric unit \(U(p) = \sqrt{p} + 1\).

### B. Block‑Free Cardan Mechanism
- Polar construction of a geometric cardan.
- Structural angles: 60°, 75°, 45°.
- Formal definitions of internal segment lengths.
- Cardan points used as the basis for matrix construction.

### C. First‑Derivative Matrix
- Coefficients C1…C9 and row sums R1…R3.
- M1 matrix (plan‑based measurements).
- M2 matrix (transition matrix).
- Simplified version based on prime numbers.
- Introduction of the unique parameter \(u = \sqrt{3.375}\).
- Alternative trigonometric factor linked to \(1/\sqrt{p}\).

### Associated Documents
- Isabelle/HOL: [`mecanique_discret.thy`](./mecanique_harmonique_chaos_discret/mecanique_discret.thy)  
- LaTeX: [`mecanique_discret.tex`](./mecanique_harmonique_chaos_discret/mecanique_discret.tex)

This chapter is a central component of the unified theory **The Universe Squared**, connecting geometry, trigonometry, prime numbers, and matrix structures.
---

## 8. Squared‑Universe Postulate

This chapter formalizes the **Unified Squared Rectangle Postulate**, establishing geometric relations between rectangles, squares, polygons, and prime numbers within the unified theory **The Universe Squared**.

### 1. Squared Rectangle and Prime Postulate
- Definitions of the three surfaces:  
  - \(S_S\) (total surface),  
  - \(S_F\) (inner square),  
  - \(S_C\) (complementary region).
- Diagonals: \(d_S\), \(d_F\), \(d_C\).
- Prime‑based unit:  
  

\[
  unit_p = \sqrt{p} + 1
  \]


- Definition of the index \(k\) from the list \([2 ..< p+1]\).
- Central postulate equation:  
  

\[
  (diag \cdot \sqrt{unit_p})^2 = k \cdot area + h^2
  \]


- Two fundamental ratios:  
  - height ratio: \(h/s = \sqrt{p} + 1\),  
  - truncation ratio: \(t/s = \sqrt{p}\).

### 2. Squared Rectangle Equivalence
- Rectangle area: \(w \cdot h\).  
- Square area: \(s^2\).  
- Equivalence condition:  
  

\[
  w \cdot h = s^2
  \]



### 3. Axioms for the Squared Polygon
- Height ratio equation.  
- Truncation ratio equation.  
- Postulate equation.  
- A polygon is **square‑defined** when all three equations hold simultaneously.

### 4. Formal Example for \(p = 3\)
- Symbolic verification of the height ratio, truncation ratio, diagonal, and area relations.

### Associated Documents
- Isabelle/HOL: [`postulat_carre.thy`](./postulat_carre/postulat_carre.thy)  
- LaTeX: [`postulat_carre.tex`](./postulat_carre/postulat_carre.tex)

This chapter establishes the mathematical structure of the **Squared‑Universe Postulate**, linking surfaces, diagonals, geometric ratios, and prime numbers within *The Universe Squared*.

--- 

## 6. Philippôt Space

The *Philippôt Space* chapter forms the third structural component of the unified theory **The Universe Squared**.  
It complements the two foundational methods — Philippôt’s method and the spectral method — by introducing a new conceptual space that extends the geometry of the prime number spectrum.

This chapter is based on two main files:

- `espace_philippot.thy`  
  → Isabelle/HOL formalization of the axioms, internal structure, and properties of the Philippôt Space.

- `espace_philippot.tex`  
  → LaTeX document presenting the conceptual foundations, definitions, examples, and geometric interpretations.

### Chapter objectives

The Philippôt Space aims to:

- introduce a geometric structure complementary to the spectral sequences;
- define a conceptual space linking spectral ratios to internal transformations of the theory;
- extend the spectral method by incorporating topological and dynamic properties;
- provide a unified framework for interpreting rational values, spectral ratios, and asymptotic behaviors.

### Role within the unified theory

The Philippôt Space acts as a **coherence space** connecting:

- the rational sequences of Philippôt’s method,
- the spectral ratios of the spectral method,
- the internal transformations of *The Universe Squared*.

It provides a unified, formally verifiable framework for expressing these three components.

### Integration into the repository

The chapter is fully integrated into the project structure:

- `.thy` files are automatically validated by Isabelle/HOL,
- `.tex` files are automatically compiled into PDF,
- the chapter is included in the final documentation.

This chapter represents a major extension of the project and strengthens the overall coherence of the theory.


## 4. LaTeX documents

Two LaTeX documents (French and English) accompany the Isabelle/HOL scripts. They include:

- detailed explanations of both methods,
- calculation examples,
- conceptual illustrations,
- textual demonstrations written by the author.

---

## 5. Lean code reference

For the section concerning the axiomatisation of the zeta function and the conjecture, Lean code from the following repository was consulted and adapted in accordance with the Apache 2.0 license:

Lean repository (mathlib3):  
https://github.com/leanprover-community/mathlib3.git

This repository contains the Lean formalization of the zeta function, L‑functions, and elements related to the Riemann Hypothesis.

---

## Continuous Certification (CI)

Since March 2026, the repository uses a fully automated continuous‑integration workflow based on GitHub Actions.  
This system ensures that every manual commit pushed to the repository is automatically validated through a complete build of all Isabelle/HOL and LaTeX components.

### How the certification works

For **each manual commit**, the GitHub Actions workflow performs the following steps:

1. **Isabelle/HOL compilation**  
   All `.thy` files in the project are automatically built, including:
   - `methode_de_philippot.thy`
   - `methode_spectral.thy`
   - `espace_philippot.thy`
   - and all related modules.

2. **LaTeX compilation**  
   All `.tex` documents are compiled into PDF using MiKTeX, including:
   - the main documents,
   - appendices,
   - supplementary chapters,
   - `espace_philippot.tex`.

3. **Validation checks**  
   The workflow verifies:
   - logical correctness of all Isabelle/HOL files,
   - successful PDF generation,
   - absence of compilation errors,
   - integration of new chapters into the build pipeline.

### Stability guarantee

This continuous certification ensures that:

- every commit in the repository is guaranteed to compile successfully,
- all `.thy` files remain logically valid at all times,
- all LaTeX documents are consistently generated without errors,
- new chapters (including *Philippôt Space*) are automatically included in the validation process.

### Build environment

The automated workflow uses the following environment:

- **Isabelle2025‑2**  
- **MiKTeX**  
- **Ubuntu GitHub Actions Runner**

The build badges displayed in the README now reflect the **real‑time compilation status** of the repository.

# Téléchargement BitTorrent / BitTorrent Download

## 🇫🇷 Téléchargement via BitTorrent

Le projet complet est disponible en téléchargement via BitTorrent.  
Ce mode de distribution permet de partager efficacement des fichiers volumineux sans dépendre des limites de GitHub.

**Lien magnet :**

```
magnet:?xt=urn:btih:8c96be1fde9107e8af8ca8dc38efa297c9bdf92c
```

**Instructions :**
- Copiez le lien ci‑dessus.  
- Ouvrez votre client BitTorrent (qBittorrent recommandé).  
- Choisissez *Ajouter un lien torrent* et collez le lien magnet.  
- Le téléchargement commencera automatiquement.

Ce lien donne accès à l’ensemble des fichiers du projet, incluant la documentation, les PDF, les sources, les modules et les ressources associées.

---

## 🇬🇧 Download via BitTorrent

The complete project is available through BitTorrent.  
This distribution method allows efficient sharing of large scientific files without GitHub storage limitations.

**Magnet link:**

```
magnet:?xt=urn:btih:8c96be1fde9107e8af8ca8dc38efa297c9bdf92c
```

**Instructions:**
- Copy the magnet link above.  
- Open your BitTorrent client (qBittorrent recommended).  
- Select *Add torrent link* and paste the magnet link.  
- The download will start automatically.

This link provides access to the full project, including documentation, PDFs, source files, modules, and associated resources.

## Developer Certificate of Origin (DCO)

This repository uses the **Developer Certificate of Origin (DCO)** to ensure that all contributions comply with copyright rules and the project’s licensing terms.

By submitting a contribution (commit, pull request, or modification), you certify that:

- your contribution is your own original work **or** you have the legal right to submit it;
- you agree that your contribution will be distributed under the project’s **Apache 2.0 license**;
- you understand that you are **fully responsible** for your modifications;
- you acknowledge that the main author assumes **no liability** for versions modified by third parties.

Each commit must include a DCO signature line:



Official DCO text:  
https://developercertificate.org/

---

## 6. License (official English version)

This project is distributed under the **Apache 2.0 License**.  
The full license text is available in the `LICENSE` file:

https://www.apache.org/licenses/LICENSE-2.0