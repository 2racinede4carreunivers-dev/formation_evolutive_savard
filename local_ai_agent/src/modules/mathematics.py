#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Mathematiques
====================
Gere les calculs, graphiques et preuves formelles.
"""

import os
import re
import logging
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import subprocess
import tempfile

logger = logging.getLogger(__name__)


class MathModule:
    """Module de calcul mathematique."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le module mathematiques.
        
        Args:
            config: Configuration de l'application
        """
        self.config = config
        self.wolfram_app_id = os.environ.get("WOLFRAM_APP_ID", "")
        self.isabelle_path = os.environ.get("ISABELLE_PATH", "")
        
        # Repertoire pour les graphiques
        self.plots_dir = Path(__file__).parent.parent.parent / "data" / "plots"
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        
        # Repertoire pour les preuves Isabelle
        self.proofs_dir = Path(__file__).parent.parent.parent / "data" / "proofs"
        self.proofs_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Module mathematiques initialise")
    
    async def calculate(self, query: str) -> str:
        """
        Effectue un calcul mathematique.
        
        Args:
            query: Question ou expression mathematique
            
        Returns:
            Resultat du calcul
        """
        # Essayer d'abord avec SymPy (local)
        sympy_result = await self._calculate_sympy(query)
        if sympy_result:
            return sympy_result
        
        # Sinon utiliser WolframAlpha
        if self.wolfram_app_id:
            return await self._calculate_wolfram(query)
        
        return "Impossible d'effectuer le calcul. Verifiez vos configurations."
    
    async def _calculate_sympy(self, query: str) -> Optional[str]:
        """
        Calcul avec SymPy.
        
        Args:
            query: Expression mathematique
            
        Returns:
            Resultat ou None
        """
        try:
            import sympy as sp
            from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
            
            # Nettoyer la requete
            expr_str = self._extract_expression(query)
            if not expr_str:
                return None
            
            # Parser l'expression
            transformations = standard_transformations + (implicit_multiplication_application,)
            
            # Variables communes
            x, y, z, t, n = sp.symbols('x y z t n')
            local_dict = {'x': x, 'y': y, 'z': z, 't': t, 'n': n, 'pi': sp.pi, 'e': sp.E}
            
            # Detecter le type de calcul
            if "derive" in query.lower() or "derivee" in query.lower():
                expr = parse_expr(expr_str, local_dict=local_dict, transformations=transformations)
                result = sp.diff(expr, x)
                return f"**Derivee:**\n\n$\\frac{{d}}{{dx}}({sp.latex(expr)}) = {sp.latex(result)}$"
            
            elif "integre" in query.lower() or "integrale" in query.lower():
                expr = parse_expr(expr_str, local_dict=local_dict, transformations=transformations)
                result = sp.integrate(expr, x)
                return f"**Integrale:**\n\n$\\int {sp.latex(expr)} \\, dx = {sp.latex(result)} + C$"
            
            elif "simplifie" in query.lower():
                expr = parse_expr(expr_str, local_dict=local_dict, transformations=transformations)
                result = sp.simplify(expr)
                return f"**Simplification:**\n\n${sp.latex(expr)} = {sp.latex(result)}$"
            
            elif "resous" in query.lower() or "equation" in query.lower():
                # Detecter une equation
                if "=" in expr_str:
                    left, right = expr_str.split("=")
                    left_expr = parse_expr(left.strip(), local_dict=local_dict, transformations=transformations)
                    right_expr = parse_expr(right.strip(), local_dict=local_dict, transformations=transformations)
                    equation = sp.Eq(left_expr, right_expr)
                    solutions = sp.solve(equation, x)
                else:
                    expr = parse_expr(expr_str, local_dict=local_dict, transformations=transformations)
                    solutions = sp.solve(expr, x)
                
                if solutions:
                    sol_latex = ", ".join([f"x = {sp.latex(s)}" for s in solutions])
                    return f"**Solutions:**\n\n${sol_latex}$"
                else:
                    return "Aucune solution trouvee."
            
            elif "limite" in query.lower():
                expr = parse_expr(expr_str, local_dict=local_dict, transformations=transformations)
                # Detecter vers quoi
                if "infini" in query.lower():
                    result = sp.limit(expr, x, sp.oo)
                else:
                    result = sp.limit(expr, x, 0)
                return f"**Limite:**\n\n$\\lim {sp.latex(result)}$"
            
            else:
                # Evaluation simple
                expr = parse_expr(expr_str, local_dict=local_dict, transformations=transformations)
                simplified = sp.simplify(expr)
                return f"**Resultat:**\n\n${sp.latex(expr)} = {sp.latex(simplified)}$"
                
        except Exception as e:
            logger.warning(f"Erreur SymPy: {e}")
            return None
    
    def _extract_expression(self, query: str) -> Optional[str]:
        """
        Extrait l'expression mathematique d'une requete.
        
        Args:
            query: Requete en langage naturel
            
        Returns:
            Expression mathematique ou None
        """
        # Patterns pour extraire les expressions
        patterns = [
            r"\$(.+?)\$",  # LaTeX inline
            r"```math\s*(.+?)\s*```",  # Code block
            r"(\d+[\s\+\-\*/\^\(\)x]+\d*)",  # Expression numerique
            r"([xyz][\s\+\-\*/\^\(\)0-9]+)",  # Expression avec variables
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # Essayer de trouver apres certains mots cles
        keywords = ["resous", "calcule", "simplifie", "derive", "integre"]
        for kw in keywords:
            if kw in query.lower():
                idx = query.lower().index(kw) + len(kw)
                remaining = query[idx:].strip()
                # Nettoyer
                remaining = remaining.lstrip(":").strip()
                if remaining:
                    return remaining
        
        return None
    
    async def _calculate_wolfram(self, query: str) -> str:
        """
        Calcul avec WolframAlpha.
        
        Args:
            query: Question mathematique
            
        Returns:
            Resultat de WolframAlpha
        """
        try:
            import wolframalpha
            
            client = wolframalpha.Client(self.wolfram_app_id)
            res = client.query(query)
            
            # Extraire les resultats
            results = []
            for pod in res.pods:
                if pod.title in ["Result", "Solution", "Definite integral", "Derivative"]:
                    for sub in pod.subpods:
                        if sub.plaintext:
                            results.append(f"**{pod.title}:** {sub.plaintext}")
            
            if results:
                return "\n\n".join(results)
            else:
                return "WolframAlpha n'a pas pu resoudre cette requete."
                
        except Exception as e:
            logger.error(f"Erreur WolframAlpha: {e}")
            return f"Erreur WolframAlpha: {str(e)}"
    
    async def prove(self, statement: str) -> str:
        """
        Genere ou verifie une preuve formelle avec Isabelle.
        
        Args:
            statement: Enonce a prouver
            
        Returns:
            Preuve ou resultat de verification
        """
        if not self.isabelle_path:
            return "Isabelle n'est pas configure. Verifiez ISABELLE_PATH dans .env"
        
        # Generer un fichier de theorie
        theory_content = self._generate_theory(statement)
        
        # Sauvegarder et executer
        theory_file = self.proofs_dir / "proof_attempt.thy"
        with open(theory_file, "w", encoding="utf-8") as f:
            f.write(theory_content)
        
        # Executer Isabelle
        result = await self._run_isabelle(theory_file)
        
        return result
    
    def _generate_theory(self, statement: str) -> str:
        """
        Genere une theorie Isabelle.
        
        Args:
            statement: Enonce a prouver
            
        Returns:
            Contenu du fichier .thy
        """
        return f'''theory proof_attempt
  imports Main
begin

(* Tentative de preuve automatique *)
(* Enonce: {statement} *)

(* TODO: L'utilisateur doit formaliser l'enonce *)
(* Exemple: *)
lemma example: "True"
  by simp

end
'''
    
    async def _run_isabelle(self, theory_file: Path) -> str:
        """
        Execute Isabelle sur un fichier de theorie.
        
        Args:
            theory_file: Chemin du fichier .thy
            
        Returns:
            Resultat de l'execution
        """
        try:
            isabelle_bin = Path(self.isabelle_path) / "bin" / "isabelle"
            
            if not isabelle_bin.exists():
                return f"Isabelle non trouve: {isabelle_bin}"
            
            # Executer Isabelle build
            result = subprocess.run(
                [str(isabelle_bin), "build", "-D", str(theory_file.parent)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return f"**Preuve verifiee avec succes!**\n\n```\n{result.stdout}\n```"
            else:
                return f"**Erreur de preuve:**\n\n```\n{result.stderr}\n```"
                
        except subprocess.TimeoutExpired:
            return "Timeout: La verification a pris trop de temps."
        except Exception as e:
            logger.error(f"Erreur Isabelle: {e}")
            return f"Erreur: {str(e)}"
    
    async def plot(self, query: str) -> str:
        """
        Genere un graphique mathematique.
        
        Args:
            query: Description du graphique
            
        Returns:
            Chemin du graphique ou message
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            import sympy as sp
            from sympy.parsing.sympy_parser import parse_expr
            
            # Extraire la fonction
            func_str = self._extract_expression(query)
            if not func_str:
                return "Impossible d'extraire la fonction a tracer."
            
            # Creer le graphique
            fig, ax = plt.subplots(figsize=(10, 6))
            
            x = sp.Symbol('x')
            expr = parse_expr(func_str, local_dict={'x': x, 'pi': sp.pi, 'e': sp.E})
            
            # Convertir en fonction numpy
            f = sp.lambdify(x, expr, modules=['numpy'])
            
            # Generer les points
            x_vals = np.linspace(-10, 10, 1000)
            y_vals = f(x_vals)
            
            # Tracer
            ax.plot(x_vals, y_vals, 'b-', linewidth=2)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'$f(x) = {sp.latex(expr)}$')
            
            # Limiter l'axe y pour eviter les valeurs extremes
            y_finite = y_vals[np.isfinite(y_vals)]
            if len(y_finite) > 0:
                y_min, y_max = np.percentile(y_finite, [5, 95])
                margin = (y_max - y_min) * 0.1
                ax.set_ylim(y_min - margin, y_max + margin)
            
            # Sauvegarder
            plot_path = self.plots_dir / f"plot_{hash(func_str) % 10000}.png"
            plt.savefig(plot_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return f"**Graphique genere:**\n\nFichier: `{plot_path}`\n\nFonction: $f(x) = {sp.latex(expr)}$"
            
        except Exception as e:
            logger.error(f"Erreur de tracage: {e}")
            return f"Erreur lors du tracage: {str(e)}"
    
    async def explain_concept(self, concept: str) -> str:
        """
        Explique un concept mathematique.
        
        Args:
            concept: Concept a expliquer
            
        Returns:
            Explication detaillee
        """
        # Cette methode utilise le LLM pour generer une explication
        # Elle est appelee depuis l'agent principal
        return f"Demande d'explication pour: {concept}"
