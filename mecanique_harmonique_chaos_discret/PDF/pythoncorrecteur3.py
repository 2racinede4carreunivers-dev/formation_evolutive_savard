import re

# Dictionnaire de remplacement pour nettoyer le LaTeX
REPLACEMENTS = {
    "⟹": "==>",
    "⇒": "=>",
    "→": "->",
    "≥": ">=",
    "≤": "<=",
    "≠": "~=",
    "¬": "~",
    "∧": "\\wedge ",
    "∨": "\\vee ",
    "⟷": "<->",
    "↔": "<->",
    "∈": "\\in ",
    "∉": "\\notin ",
    "∀": "\\forall ",
    "∃": "\\exists ",
    "√": "\\sqrt{}",
    "×": "\\times ",
    "•": "\\cdot ",
    "…": "...",
    "−": "-",
    "“": "\"",
    "”": "\"",
    "’": "'",
    "‹": "\"",
    "›": "\"",
}

def clean_latex(text):
    """Remplace les caractères Unicode problématiques dans un fichier LaTeX."""
    for uni, ascii_val in REPLACEMENTS.items():
        text = text.replace(uni, ascii_val)
    return text

def process_file(input_path, output_path):
    """Nettoie un fichier LaTeX complet."""
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    cleaned = clean_latex(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"[OK] Nettoyé : {input_path} → {output_path}")

if __name__ == "__main__":
    print("=== Nettoyage Unicode LaTeX → ASCII safe ===")
    input_path = input("Chemin du fichier LaTeX (.tex) : ").strip()

    if not input_path.endswith(".tex"):
        print("Erreur : veuillez fournir un fichier .tex")
    else:
        output_path = input_path.replace(".tex", "_ascii.tex")
        process_file(input_path, output_path)