# Data Challenge — AssurPrime

Projet réalisé dans le cadre du cours **M2DS2526challenge1et2**.

## Contexte du challenge

Ce projet correspond à **Exercice (Data Challenge)** du cours Statistique en Grande dimension.  
Le challenge choisi sur la plateforme ChallengeData est :

**AssurPrime : Saurez-vous prédire la prime d'assurance ?**

Ce challenge est proposé dans le cadre de **Crédit Agricole Assurances**, filiale du Groupe Crédit Agricole dédiée à l'assurance. Le groupe est un acteur majeur de la bancassurance en Europe. Parmi ses entités figure **Pacifica**, qui gère notamment le contrat **Multirisque Agricole**.

Le contrat **Multirisque Agricole** est destiné aux agriculteurs afin de sécuriser leur exploitation. Il couvre l'activité professionnelle, les dommages aux bâtiments d'exploitation, le matériel stocké, ainsi que la protection financière et juridique. L'objectif est d'assurer une continuité d'activité en cas de sinistre, à la fois sur le plan matériel et financier.

Dans ce contexte, le **risque incendie** représente une part importante de la charge sinistre du contrat, ce qui en fait un enjeu central de modélisation.

- **Plateforme** : ChallengeData ENS
- **Challenge** : AssurPrime
- **Période du challenge** : du **1 décembre 2025** au **14 janvier 2026**
- **Lien du challenge** : https://challengedata.ens.fr/participants/challenges/161/

---

## Objectif métier

L'objectif du challenge est d'identifier le meilleur modèle pour **prédire la prime pure incendie**.

La modélisation repose sur deux composantes principales :

- un modèle pour la **fréquence** des sinistres ;
- un modèle pour le **coût moyen** des sinistres.

La variable cible finale, appelée **charge**, est calculée en combinant :

- la fréquence,
- le coût moyen,
- le nombre d'années depuis la souscription du contrat (`ANNEE_ASSURANCE`).

Autrement dit, la charge correspond à :
```text
CHARGE = FREQ × CM × ANNEE_ASSURANCE
```

où :

- `FREQ` = fréquence des sinistres
- `CM` = coût moyen d'un sinistre
- `ANNEE_ASSURANCE` = nombre d'années depuis la souscription du contrat

Cette approche est classique en assurance, où l'on modélise séparément **fréquence** et **sévérité**.

---

# Données

Les données comprennent plusieurs types de variables :

### Variables cibles

- `FREQ` : fréquence des sinistres
- `CM` : coût moyen des sinistres
- `CHARGE` : charge totale

### Données géographiques

- département
- variables météorologiques
- autres informations territoriales

### Données liées au contrat

- activité de l'assuré (cultivateur, polyculteur, etc.)
- garanties souscrites
- nombre de bâtiments
- nombre de salariés
- historique de sinistres

### Données de surface

Certaines surfaces sont anonymisées :

- `surface1`
- `surface2`
- etc.

### Données de capitaux assurés

Variables anonymisées :

- `capital1`
- `capital2`
- etc.

### Données de prévention

Variables anonymisées :

- `prev1`
- `prev2`
- etc.

---

# Benchmark fourni

Le challenge propose un benchmark basé sur des **GLM (Generalized Linear Models)**.

Deux modèles sont utilisés :

### Fréquence

- distribution : **Poisson**
- fonction de lien : **log**

### Coût moyen

- distribution : **Tweedie**
- fonction de lien : **log**

L'objectif est d'évaluer si des modèles plus avancés permettent d'améliorer les performances.

---

# Métrique d'évaluation

La métrique utilisée est la **RMSE (Root Mean Square Error)** :
```text
RMSE = sqrt( (1/n) × Σ (yi - ŷi)² )
```

où :

- `yi` = valeur réelle
- `ŷi` = valeur prédite
- `n` = nombre d'observations

---

# Résultat obtenu

Résultat obtenu sur la plateforme :

- **Classement public global : 51 / 358**
- **Classement académique : 2e**

Informations sur la meilleure soumission :

- **Participant** : `cmoutsihatsala`
- **Score public** : **5600.8415**
- **Date** : 30 décembre 2025

---

# Soumissions réalisées

Quatre soumissions ont été effectuées.

### Soumission 1

**XGBoost Tweedie + GLM (Poisson / Tweedie)**  
Score : **5600.8415**

→ **Meilleure soumission**

### Soumission 2

**XGBoost Tweedie (Pure Premium)**  
Score : **5601.5492**

### Soumission 3

**XGBoost Tweedie + XGBoost Poisson (Fréquence)**  
Score : **5601.5492**

### Soumission 4

**Random Forest (fréquence) + Gradient Boosting (coût moyen)**  
Score : **5604.5500**

---

# Modèle final retenu

Le modèle final est un **blend** entre :

- **XGBoost Tweedie**
- **GLM (Poisson / Tweedie)**

Paramètres principaux :

### XGBoost

- learning rate = 0.03
- max depth = 3
- min child weight = 60
- tweedie power = 1.2

### GLM Tweedie

- power = 1.1
- alpha = 1e-4

### Blend final
```text
Prediction_finale = 0.9 × XGBoost + 0.1 × GLM
```

---

# Contenu du dépôt

Le dépôt contient :

- le **rapport PDF du projet**
- le **notebook correspondant à la soumission finale**
- le **fichier soumission déposé sur le site**

---

# Installation

Installer les dépendances :
```bash
pip install -r requirements.txt
```

---

# Auteur

**Coletta Moutsiha**  
Master 2 Data Science  
Université d'Angers
