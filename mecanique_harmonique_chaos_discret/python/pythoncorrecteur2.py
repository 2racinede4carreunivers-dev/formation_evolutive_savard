from pathlib import Path

# Nom du fichier à corriger
INPUT = Path("mecanique_harmonique_chaos_discret.tex")
OUTPUT = Path("mecanique_harmonique_chaos_discret_fixed.tex")

# Table de conversion UTF‑8 → LaTeX
REPLACE = {
    "é": r"\'e", "è": r"\`e", "ê": r"\^e", "ë": r"\"e",
    "à": r"\`a", "â": r"\^a", "ä": r"\"a",
    "ù": r"\`u", "û": r"\^u", "ü": r"\"u",
    "ô": r"\^o",
    "î": r"\^i", "ï": r"\"i",
    "ç": r"\c{c}",

    "É": r"\'E", "È": r"\`E", "Ê": r"\^E", "Ë": r"\"E",
    "À": r"\`A", "Â": r"\^A", "Ç": r"\c{C}", "Ô": r"\^O",

    "’": "'", "‘": "`",
    "«": "<<", "»": ">>",

    "–": "--",   # en-dash
    "—": "---",  # em-dash

    "≤": r"\leq", "≥": r"\geq", "≠": r"\neq",
    "∈": r"\in", "∉": r"\notin",
    "∧": r"\wedge", "∨": r"\vee", "¬": r"\neg",
    "∀": r"\forall", "∃": r"\exists",
    "→": r"\rightarrow", "⇒": r"\Rightarrow",
    "⟶": r"\longrightarrow", "⟹": r"\Longrightarrow",
    "↔": r"\leftrightarrow", "⟷": r"\longleftrightarrow",
    "×": r"\times", "⋀": r"\bigwedge",
    "√": r"\sqrt{}",
}

def fix_file(input_path: Path, output_path: Path, table: dict):
    text = input_path.read_text(encoding="utf-8")
    replaced = {}

    for bad, good in table.items():
        if bad in text:
            replaced[bad] = good
            text = text.replace(bad, good)

    output_path.write_text(text, encoding="utf-8")

    print("\n=== CARACTÈRES CORRIGÉS ===")
    for k, v in replaced.items():
        print(f"{k}  →  {v}")

    print(f"\nFichier corrigé écrit dans : {output_path}\n")

if __name__ == "__main__":
    fix_file(INPUT, OUTPUT, REPLACE)