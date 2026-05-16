import re
import tempfile
import shutil
import subprocess
import os

class IsabelleAuto:

    @staticmethod
    def run_isabelle(path: str):
        """Exécute Isabelle sur un fichier ou un dossier."""
        try:
            result = subprocess.run(
                ["isabelle", "build", "-D", os.path.dirname(path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode == 0, result.stdout + "\n" + result.stderr
        except Exception as e:
            return False, str(e)

    # -------------------------------------------------------------
    # 1. AUTO UPDATE SECTION
    # -------------------------------------------------------------
    @staticmethod
    def auto_update_section(file_path: str, section_name: str, agent):
        """L’agent lit la section, génère du code, teste, corrige, met à jour."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if section_name not in content:
            return False, f"Section '{section_name}' introuvable."

        # Demander à l’agent de générer le nouveau contenu
        prompt = (
            f"Voici le contenu d’un fichier Isabelle/HOL.\n"
            f"Section à mettre à jour : {section_name}\n"
            f"Contenu complet :\n{content}\n\n"
            f"Génère une version améliorée et complète de cette section, "
            f"en Isabelle/HOL strictement valide."
        )
        new_section = agent.llm.generate(prompt)

        updated = content.replace(section_name, new_section)

        # Test dans un fichier temporaire
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_file = os.path.join(tmpdir, os.path.basename(file_path))
            shutil.copytree(os.path.dirname(file_path), tmpdir, dirs_exist_ok=True)

            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write(updated)

            ok, output = IsabelleAuto.run_isabelle(tmp_file)

            if not ok:
                return False, output

        # Si OK → écrire dans le fichier final
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated)

        return True, "Mise à jour réussie."

    # -------------------------------------------------------------
    # 2. AUTO FIX ERRORS
    # -------------------------------------------------------------
    @staticmethod
    def auto_fix_errors(file_path: str, agent):
        """Analyse les erreurs Isabelle et tente de corriger automatiquement."""
        ok, output = IsabelleAuto.run_isabelle(file_path)

        if ok:
            return True, "Aucune erreur à corriger."

        # Demander à l’agent une correction
        prompt = (
            f"Voici un fichier Isabelle/HOL qui contient des erreurs.\n"
            f"Erreurs Isabelle :\n{output}\n\n"
            f"Corrige le fichier en produisant une version valide."
        )

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        corrected = agent.llm.generate(prompt)

        # Test dans un fichier temporaire
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_file = os.path.join(tmpdir, os.path.basename(file_path))
            shutil.copytree(os.path.dirname(file_path), tmpdir, dirs_exist_ok=True)

            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write(corrected)

            ok2, output2 = IsabelleAuto.run_isabelle(tmp_file)

            if not ok2:
                return False, output2

        # Écrire la version corrigée
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(corrected)

        return True, "Fichier corrigé avec succès."

    # -------------------------------------------------------------
    # 3. AUTO GENERATE PROOFS
    # -------------------------------------------------------------
    @staticmethod
    def auto_generate_proofs(file_path: str, agent):
        """Détecte les 'sorry' et génère automatiquement les preuves."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "sorry" not in content:
            return True, "Aucun 'sorry' trouvé."

        prompt = (
            f"Voici un fichier Isabelle/HOL contenant des 'sorry'.\n"
            f"Remplace chaque 'sorry' par une preuve complète et valide.\n\n"
            f"Contenu :\n{content}"
        )

        new_content = agent.llm.generate(prompt)

        # Test dans un fichier temporaire
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_file = os.path.join(tmpdir, os.path.basename(file_path))
            shutil.copytree(os.path.dirname(file_path), tmpdir, dirs_exist_ok=True)

            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write(new_content)

            ok, output = IsabelleAuto.run_isabelle(tmp_file)

            if not ok:
                return False, output

        # Écrire la version finale
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return True, "Toutes les preuves ont été générées."

    # -------------------------------------------------------------
    # 4. EXPLAIN ERROR
    # -------------------------------------------------------------
    @staticmethod
    def explain_error(error_text: str, agent):
        """Explique une erreur Isabelle en langage clair."""
        prompt = (
            f"Explique clairement cette erreur Isabelle/HOL :\n\n{error_text}"
        )
        explanation = agent.llm.generate(prompt)
        return explanation
