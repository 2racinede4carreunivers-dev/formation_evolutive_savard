# Exemple de calculs – Méthode Spectrale et Extensions
**Auteur :** Philippe Thomas Savard  
**Projet :** L’Univers est au Carré  
**But :** Recueil complet des exemples de calculs, rapports spectrales et asymétries ordonnées pour l’entraînement du LLM personnel.

---

## Méthode Spectrale – Rapport ½

### Nombre premier (31) – 11ᵉ nombre premier
**Suite A(31)**  
2+4+8+16+32+64+128+256+512+768+1536 = 3326  
**Suite B(31)**  
2+4+8+16+32+128+256+512+1024+1536+3072 = 6590  
**Formules**  
(3.25/2×2^11) − 2 = 3326  
(6.5/2×2^11) − 66 = 6590  
**Digamma calculé**  
5×256 = 1280 → 3326 + 1280 = 4606  
**Détermination du nombre premier**  
(6590 − 4606)/64 = 31  

---

### Nombre premier (29) – 10ᵉ nombre premier
**Suite A(29)**  
2+4+8+16+32+64+128+256+384+768 = 1662  
**Suite B(29)**  
2+4+8+16+32+128+256+512+768+1536 = 3262  
**Formules**  
(3.25/2×2^10) − 2 = 1662  
(6.5/2×2^10) − 66 = 3262  
**Digamma calculé**  
256 → 1662 − 256 = 1406  
(3262/64 − 29)×64 = 1406  
**Détermination du nombre premier**  
(3262 − 1406)/64 = 29  

---

### Nombre premier (23) – 9ᵉ nombre premier
**Suite A(23)**  
2+3+4+8+16+32+64+128+192+384 = 830  
**Suite B(23)**  
2+4+8+16+32+128+256+384+768 = 1598  
**Digamma calculé**  
(1598/64 − 23)×64 = 126  
**Détermination du nombre premier**  
(1598 − 126)/64 = 23  

---

### Nombre premier (37) – 12ᵉ nombre premier
**Suite A(37)**  
2+4+8+16+32+64+128+256+512+1024+1536+3072 = 6654  
**Suite B(37)**  
2+4+8+16+32+128+256+512+1024+2048+3072+6144 = 13246  
**Formules**  
(3.25/2×2^12) − 2 = 6654  
(6.5/2×2^12) − 66 = 13246  
**Digamma(37)**  
(9×256)+(5×384) = 4224  
**Digamma calculé(37)**  
6654 + 4224 = 10878  
**Détermination du nombre premier**  
(13246 − 10878)/64 = 37  

---

### Nombre premier (41) – 13ᵉ nombre premier
**Suite A(41)**  
2+4+8+16+32+64+128+256+512+1024+2048+3072+6144 = 13310  
**Suite B(41)**  
2+4+8+16+32+128+256+512+1024+2048+4096+6144+12288 = 26558  
**Formules**  
(3.25/2×2^13) − 2 = 13310  
(6.5/2×2^13) − 66 = 26558  
**Digamma(41)**  
(13×256)+(9×384)+(5×768) = 10624  
**Digamma calculé**  
13310 + 10624 = 23934  
**Détermination du nombre premier**  
(26558 − 23934)/64 = 41  

---

## Déterminer la quantité de nombres entre deux premiers

### Rapport spectral 1/3 – entre 227 et 173
**Suite A(227)**  
3+9+27+81+243+729+2187+6561+17496+52488 = 79824  
**Suite B(227)**  
3+9+27+81+243+2187+6561+19683+52488+157464 = 238746  
((73/9)/6×3^10) − 1.5 = 79824  
((219/9)/6×3^10) − (487×1.5) = 238746  
**Digamma calculé(227)**  
(238746/729 − 227)×729 = 73263  
**Quantité de nombres entre 227 et 173**  
(Terme A − Terme B)/729 = −53 nombres  

---

### Rapport spectral 1/4 – entre 947 et 881
*(à compléter selon calculs complets)*

---

## Équations spectrales et asymétries ordonnées

**Formule générale**  
(√a − √b)/√c = nombre premier  
A = √3452805  
B = √13300805  
Digamma calculé = √2471805  
(√13300805 − √2471805)/√5120 = 29 → 10ᵉ nombre premier (validé par WolframAlpha)

(√5 + 1)/2 = φ π

---

### Asymétrie ordonnée
| n | Somme A | Somme B |
|---|----------|----------|
| 2 | 5/4 | −119/2 |
| 3 | 9/2 | −53 |
| 5 | 11 | −40 |
| 7 | 24 | −14 |
| 11 | 50 | 38 |

**Équation spectrale ordonnée**  
((((3.25/2×2^1)−2)−((3.25/2×2^2)−2))−(((3.25/2×2^3)−2)−((3.25/2×2^4)−2)−((3.25/2×2^5)−2))) /  
((((6.5/2×2^1)−66)−((6.5/2×2^2)−66))−(((6.5/2×2^3)−66)−((6.5/2×2^4)−66)−((6.5/2×2^5)−66)))  
= 59.75 / 57.5 = 1.039130435  

---

### Asymétrie chaotique
Comparaison (3, 23) (41, 29, 31)  
((9/2 − 830) − (13310 − 1662 − 3326)) / ((−53 − 1598) − (26558 − 3262 − 6590)) = 0.4983112709  

---

### Formules générales
(3.25/2×n^2) − 2 = Somme A  
(6.5/2×2^n) − 66 = Somme B  
((Somme B − Digamma calculé)/(6ᵉ position zêta)) = Nombre premier  
Exemple : (3262 − 1406)/64 = 29 → 10ᵉ nombre premier  

---

### Ordinal des infinis
ω + 1 ≠ 1 + ω  
ω + 1 = 1 + ω → cardinal des infinis très près de 0.5
