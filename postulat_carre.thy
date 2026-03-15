theory postulat_carre
  imports Complex_Main
begin

section "Unified Squared Rectangle and Prime Postulate"

locale postulat_carre =
  fixes w :: real
    and h :: real
    and s :: real
    and t :: real
    and p :: nat
    and diag :: real
    and area :: real
  assumes geom: "w > 0" "h > 0" "s > 0" "t > 0" "s <= w" "s <= h"
    and prime_p: "prime p"
begin

definition S_S :: real where
  "S_S = w * h"

definition S_F :: real where
  "S_F = s * s"

definition S_C :: real where
  "S_C = S_S - S_F"

definition d_S :: real where
  "d_S = sqrt (w * w + h * h)"

definition d_F :: real where
  "d_F = sqrt 2 * s"

definition d_C :: real where
  "d_C = sqrt (s * s + t * t)"

definition unit_p :: real where
  "unit_p = sqrt (real p) + 1"

text "
Conceptuellement, on peut définir k comme la position de p dans la liste
[2,3,...,p], plus 1. Cela donne la progression 1,2,4,6,10,12,16,...
pour p = 2,3,5,7,11,13,17,...

Formellement, on encode directement ce fait par :
k = p - 1.
"

definition k :: nat where
  "k = p - 1"

definition postulat_eq :: bool where
  "postulat_eq =
     ((diag * sqrt unit_p) ^ 2 = real k * area + h * h)"

definition ratio_height_square :: bool where
  "ratio_height_square =
     (h / s = sqrt (real p) + 1)"

definition ratio_trunc_square :: bool where
  "ratio_trunc_square =
     (t / s = sqrt (real p))"

lemma postulat_eq_p_minus_1:
  shows "postulat_eq \<longleftrightarrow> ((diag * sqrt unit_p) ^ 2 = real (p - 1) * area + h * h)"
  unfolding postulat_eq_def k_def by simp

end


section "Rectangle carre : equivalence avec un carre"

locale rectangle_carre =
  fixes w :: real
    and h :: real
    and s :: real
  assumes geom: "w > 0" "h > 0" "s > 0"
begin

definition area_rect :: real where
  "area_rect = w * h"

definition area_square :: real where
  "area_square = s * s"

definition rect_equiv_square :: bool where
  "rect_equiv_square =
     (area_rect = area_square)"

end


section "Axiomatisation du polygone au carre"

locale polygone_carre_axiomes =
  fixes p :: nat
    and h :: real
    and s :: real
    and t :: real
    and diag :: real
    and area :: real
  assumes prime_p: "prime p"
    and geom: "h > 0" "s > 0" "t > 0"
begin

definition eq_ratio_height :: bool where
  "eq_ratio_height =
     (h / s = sqrt (real p) + 1)"

definition eq_ratio_trunc :: bool where
  "eq_ratio_trunc =
     (t / s = sqrt (real p))"

definition eq_postulat :: bool where
  "eq_postulat =
     ((diag * sqrt (sqrt (real p) + 1)) ^ 2
        = area + h * h)"

definition polygone_defini :: bool where
  "polygone_defini =
     (eq_ratio_height \<and> eq_ratio_trunc \<and> eq_postulat)"

end


section "Exemple numerique pour p = 3"

locale exemple_p3 =
  fixes s3 :: real
    and h3 :: real
    and t3 :: real
    and diag3 :: real
    and area3 :: real
  assumes s3_pos: "s3 > 0"
    and ratio_height_3: "h3 / s3 = sqrt 3 + 1"
    and ratio_trunc_3: "t3 / s3 = sqrt 3"
    and diag_trunc_3: "sqrt (s3 * s3 + t3 * t3) = sqrt 6"
    and area_def_3: "area3 = s3 * h3"
begin

text "
Cet exemple formalise le cas p = 3.
Les valeurs numeriques (0.896575..., 1.552914..., etc.)
ne sont pas utilisees directement : seules les relations exactes
sont axiomatisées.
"

lemma hauteur_sur_cote:
  shows "h3 / s3 = sqrt 3 + 1"
  using ratio_height_3 .

lemma tronque_sur_cote:
  shows "t3 / s3 = sqrt 3"
  using ratio_trunc_3 .

lemma diagonale_tronquee_exacte:
  shows "sqrt (s3 * s3 + t3 * t3) = sqrt 6"
  using diag_trunc_3 .

lemma aire_rectangle:
  shows "area3 = s3 * h3"
  using area_def_3 .

end


section "Trois équations exactes : Octogone carré"

locale equations_octogone =
  fixes d1 :: real    (* diagonale A'B'EF *)
    and d2 :: real    (* diagonale EFC'D' *)
    and d3 :: real    (* diagonale A'B'C'D' *)
  assumes d1_def: "d1 = sqrt 8"
    and d2_def: "d2 = 2 * (1 / (sqrt (1/3) + sqrt (1/6)))"
    and d3_def: "d3 = sqrt (32 - 16 * sqrt 2)"
    and eq1_octogone:
      "(d2 * sqrt (sqrt 2 + 1))^2 = 8 + (d1 - 4)^2"
    and eq2_octogone:
      "((d1 - 4) * sqrt (sqrt 2 + 2))^2 = 8 + (d1 - 4)^2"
    and eq3_octogone:
      "(d3 * sqrt ((sqrt 2 + 1) / 2))^2 = (sqrt 128 - 8) + 8"
begin

text "
Cette locale encode les trois équations exactes qui définissent
l'octogone carré issu du postulat du carré.
"

end


section "Trois équations exactes : Hexagone carré"

locale equations_hexagone =
  fixes s3 :: real
    and h3 :: real
    and dH1 :: real
    and dH2 :: real
    and dH3 :: real
  assumes s3_def: "s3 = 1 / (sqrt (1/3) + sqrt (1/6))"
    and h3_def: "h3 = s3 * (sqrt 3 + 1)"
    and dH1_def: "dH1 = 2 * s3"
    and dH2_def: "dH2 = 3 - sqrt 3"
    and dH3_def: "dH3 = sqrt 6 + s3"
    and eq1_hexagone:
      "(dH1 * sqrt (sqrt 3 + 1))^2 = 2 * (s3 * h3) + 6"
    and eq2_hexagone:
      "(dH2 * sqrt (sqrt 3 + 3))^2 = 2 * (dH2^2) + 6"
    and eq3_hexagone:
      "(dH3 * sqrt (2 * sqrt 3 / (4 - sqrt 3)))^2 = 2 * (s3 * sqrt 6) + 6"
begin

text "
Cette locale encode les trois équations exactes qui définissent
l'hexagone carré issu du postulat du carré.
"

end

end