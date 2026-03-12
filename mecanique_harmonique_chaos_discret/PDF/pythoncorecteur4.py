import re

# ======================================================================
#  TABLE DE CONVERSION UNICODE → ASCII / LaTeX
# ======================================================================

UNICODE_MAP = {
    # Math
    "≤": r"\\leq ",
    "≥": r"\\geq ",
    "≠": r"\\neq ",
    "∈": r"\\in ",
    "∉": r"\\notin ",
    "∧": r"\\wedge ",
    "∨": r"\\vee ",
    "¬": r"\\neg ",
    "∀": r"\\forall ",
    "∃": r"\\exists ",
    "→": r"\\rightarrow ",
    "⇒": r"\\Rightarrow ",
    "↔": r"\\leftrightarrow ",
    "×": r"\\times ",
    "√": r"\\sqrt{}",
    "°": r"^{\\circ}",

    # Espaces invisibles
    "\u200B": "",   # ZERO WIDTH SPACE
    "\u202F": " ",  # NARROW NBSP
    "\u00A0": " ",  # NBSP

    # Guillemets français
    "«": "<<",
    "»": ">>",

    # Tirets
    "–": "--",
    "—": "---",
}

# ======================================================================
#  FONCTION DE NETTOYAGE
# ======================================================================

def clean_latex(text):
    """Nettoie un fichier LaTeX en remplaçant les Unicode problématiques."""

    cleaned_lines = []
    inside_minted = False

    for line in text.splitlines():

        # Détection des environnements minted
        if "\\begin{minted" in line:
            inside_minted = True
        if "\\end{minted" in line:
            inside_minted = False

        # Si on est dans minted → NE RIEN TOUCHER
        if inside_minted:
            cleaned_lines.append(line)
            continue

        # Sinon → nettoyer la ligne
        for uni, latex in UNICODE_MAP.items():
            line = line.replace(uni, latex)

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

# ======================================================================
#  TRAITEMENT FICHIER
# ======================================================================

def process_file(input_path):
    output_path = input_path.replace(".tex", "_ascii.tex")

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    cleaned = clean_latex(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"[OK] Fichier nettoyé : {output_path}")

# ======================================================================
#  MAIN — AVEC TON FICHIER DÉJÀ RÉGLÉ
# ======================================================================

if __name__ == "__main__":
    print("=== Correcteur Unicode LaTeX → ASCII safe ===")

    # TON FICHIER EXACT :
    path = r"C:\univers_carre\mecanique_harmonique_chaos_discret\PDF\mecanique_harmonique_chaos_discret.tex"

    print(f"Traitement du fichier : {path}")
    process_file(path)