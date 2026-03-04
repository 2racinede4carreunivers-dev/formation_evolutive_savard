import re

# Fichier source et fichier corrigé
source = "philosophie_geometrie_spectre_premier.tex"
output = "philosophie_geometrie_spectre_premier_pdflatex.tex"

# Remplacements Unicode → LaTeX
replacements = {
    "’": "'",          # apostrophe typographique
    "‘": "'",          # apostrophe ouvrante
    "“": "``",         # guillemet ouvrant
    "”": "''",         # guillemet fermant
    "…": r"\ldots{}",  # points de suspension
    "—": "---",        # tiret cadratin
    "–": "--",         # tiret demi-cadratin
    " ": " ",          # espace insécable unicode
}

# Lecture du fichier
with open(source, "r", encoding="utf-8") as f:
    text = f.read()

# Application des remplacements
for bad, good in replacements.items():
    text = text.replace(bad, good)

# Écriture du fichier corrigé
with open(output, "w", encoding="utf-8") as f:
    f.write(text)

print("Correction terminée. Fichier généré :", output)