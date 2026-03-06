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

## Certification de compilation

![Isabelle/HOL](https://img.shields.io/badge/Isabelle2025--2-Build%20Passing-brightgreen)
![LaTeX](https://img.shields.io/badge/LaTeX-PDF%20OK-brightgreen)

**État de certification :**  
Tous les fichiers Isabelle/HOL et LaTeX de ce dépôt ont été compilés avec succès  
le **3 mars 2026**, sous l’environnement suivant :

- **Isabelle2025‑2** (`isabelle build -D .`)
- **MiKTeX** (`pdflatex`)

Cette certification atteste uniquement que la version officielle du dépôt compile à cette date.

## Developer Certificate of Origin (DCO)

Ce dépôt utilise le **Developer Certificate of Origin (DCO)** afin de garantir que toutes les contributions respectent les droits d’auteur et les conditions de la licence.

En soumettant une contribution (commit, pull request ou modification), vous affirmez que :

- votre contribution est votre travail original **ou** vous avez le droit légal de la soumettre (par exemple, autorisation de votre employeur) ;
- vous acceptez que votre contribution soit distribuée sous la **licence Apache 2.0** du projet ;
- vous comprenez que vous êtes **entièrement responsable** de vos modifications et de leurs effets ;
- vous acceptez que l’auteur principal du dépôt ne fournit **aucune garantie** et n’assume **aucune responsabilité** concernant les versions modifiées par des tiers.

Chaque commit doit inclure une ligne de signature DCO :


Pour plus d’informations, consultez le texte officiel du DCO :  
https://developercertificate.org/

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

## Build certification

![Isabelle/HOL](https://img.shields.io/badge/Isabelle2025--2-Build%20Passing-brightgreen)
![LaTeX](https://img.shields.io/badge/LaTeX-PDF%20OK-brightgreen)

**Certification status:**  
All Isabelle/HOL and LaTeX files in this repository were successfully compiled  
on **March 3, 2026**, under the following environment:

- **Isabelle2025‑2** (`isabelle build -D .`)
- **MiKTeX** (`pdflatex`)

This certification only attests that the official version of the repository compiled on this date.

---

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