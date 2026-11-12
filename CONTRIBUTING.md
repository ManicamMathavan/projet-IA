# Guide de contribution

Ce document décrit la manière de travailler sur le projet d'équipe
**Rossmann Store Sales**. Lisez-le avant de créer une branche ou de modifier
un notebook.

## 1. Règles essentielles

1. Ne jamais pousser directement sur `main`.
2. Une branche correspond à une tâche précise et limitée.
3. Toute Pull Request doit être relue par au moins un autre membre.
4. Ne jamais versionner les données, secrets, environnements virtuels ou
   modèles lourds.
5. Toute expérience doit être documentée dans
   [`experiments/log.csv`](./experiments/log.csv).
6. Utiliser `uv` pour l'environnement et les dépendances ; ne pas utiliser
   `pip install` dans ce projet.
7. Respecter la validation temporelle et éviter toute fuite de données futures.

## 2. Installer le projet avec uv

Installer `uv` une seule fois.

Windows PowerShell :

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

macOS/Linux :

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Puis cloner et synchroniser le projet :

```bash
git clone <url-du-depot>
cd projet-IA
uv python install 3.11
uv sync
```

`uv sync` crée `.venv` et installe les versions définies dans
[`pyproject.toml`](./pyproject.toml) et verrouillées dans [`uv.lock`](./uv.lock).

Commandes courantes :

| Besoin | Commande |
|---|---|
| Synchroniser l'environnement | `uv sync` |
| Exécuter un script | `uv run python -m src.train` |
| Lancer Jupyter | `uv run jupyter lab` |
| Ajouter une dépendance | `uv add <package>` |
| Ajouter une dépendance de développement | `uv add --dev <package>` |
| Supprimer une dépendance | `uv remove <package>` |
| Régénérer le lockfile | `uv lock` |
| Vérifier la version de Python | `uv run python --version` |

Ne modifiez pas `uv.lock` à la main. Après une modification de dépendance,
commitez toujours ensemble `pyproject.toml` et `uv.lock`.

## 3. Données et secrets

Les fichiers Kaggle doivent être placés dans `data/raw/` :

```text
data/raw/
├── train.csv
├── test.csv
├── store.csv
└── sample_submission.csv
```

Les données de `data/raw/` et `data/processed/` ne sont pas versionnées.
Les clés Kaggle, fichiers `.env`, tokens GitHub et identifiants ne doivent
jamais apparaître dans le dépôt ou dans un notebook.

Pour télécharger les données avec l'outil Kaggle installé dans l'environnement :

```bash
uv run kaggle competitions download -c rossmann-store-sales -p data/raw
```

Les données ne sont téléchargeables qu'après acceptation des règles de la
compétition sur Kaggle.

## 4. Structure et responsabilités des fichiers

- `src/` : fonctions réutilisables de chargement, features, métriques,
  validation et entraînement.
- `notebooks/` : exploration, visualisations et essais, en important les
  fonctions de `src/`.
- `data/` : fichiers locaux non versionnés.
- `experiments/log.csv` : résultats de chaque expérience.
- `submissions/` : petits fichiers CSV envoyés à Kaggle.
- `report/` : rapport final et figures.

Ne copiez pas une même logique dans plusieurs notebooks. Si une fonction peut
être réutilisée, placez-la dans `src/`.

## 5. Workflow Git

### Créer une branche

```bash
git switch main
git pull --rebase origin main
uv sync
git switch -c feat/features-temporelles
```

Préfixes recommandés :

| Préfixe | Utilisation | Exemple |
|---|---|---|
| `feat/` | nouvelle fonctionnalité | `feat/date-features` |
| `exp/` | expérience de modélisation | `exp/lightgbm-baseline` |
| `fix/` | correction de bug | `fix/rmspe-zero-sales` |
| `docs/` | documentation | `docs/contributing` |
| `chore/` | configuration ou maintenance | `chore/update-uv-lock` |

### Commiter

Avant de commiter :

```bash
git status
git diff
```

Ajouter seulement les fichiers attendus :

```bash
git add src/features.py notebooks/ experiments/log.csv
git commit -m "feat: add date features"
```

Les messages doivent être courts et explicites. Exemples :

- `feat: add store metadata merge`
- `fix: exclude zero sales from rmspe`
- `exp: compare lightgbm parameters`
- `docs: explain colab workflow`

Évitez les messages vagues comme `update`, `modif` ou `final`.

### Pousser et ouvrir une Pull Request

```bash
git fetch origin
git rebase origin/main
git push -u origin feat/features-temporelles
```

La Pull Request doit préciser :

- le problème traité ;
- les fichiers modifiés ;
- la manière de vérifier le changement ;
- le RMSPE obtenu avant/après pour une expérience ;
- les nouvelles dépendances éventuelles.

Une Pull Request doit avoir au moins une relecture avant fusion. Après le
merge, supprimer la branche locale :

```bash
git switch main
git pull --rebase origin main
git branch -d feat/features-temporelles
```

## 6. Qualité du code et validation

Le code doit respecter les règles suivantes :

- utiliser des chemins relatifs à la racine du projet ;
- fixer les seeds, notamment `random_state=42` ;
- écrire des fonctions courtes et testables ;
- ne pas modifier inutilement les DataFrames reçus en entrée ;
- utiliser une seule implémentation du RMSPE dans `src/metrics.py` ;
- utiliser un découpage temporel, jamais un découpage aléatoire pour ce projet ;
- ne jamais utiliser une information postérieure à la date prédite.

Avant une Pull Request, exécuter au minimum :

```bash
uv run python -m compileall src
uv run python -m src.train
```

La commande d'entraînement nécessite les fichiers Kaggle dans `data/raw/`.
Si les outils de développement `ruff` sont ajoutés au projet, lancer aussi :

```bash
uv run ruff check .
uv run ruff format --check .
```

## 7. Notebooks

Un notebook appartient à un seul auteur et suit le format :

```text
01_eda_<prenom>.ipynb
02_preprocessing_<prenom>.ipynb
03_modeling_<prenom>.ipynb
```

Règles :

- ne pas modifier le notebook d'un autre membre sans accord ;
- ne pas utiliser de chemins absolus ;
- exécuter le notebook de haut en bas avant la Pull Request ;
- ne pas enregistrer de données ou de secrets dans les cellules ;
- exporter les figures utiles dans `report/figures/` ;
- supprimer les sorties inutiles avant le commit afin de limiter les conflits.

Lancer Jupyter avec :

```bash
uv run jupyter lab
```

## 8. Travailler avec Google Colab

Dans Colab, cloner le dépôt puis installer `uv` et synchroniser
l'environnement :

```python
!git clone <url-du-depot>
%cd projet-IA
!curl -LsSf https://astral.sh/uv/install.sh | sh
!~/.local/bin/uv sync
```

Utiliser ensuite :

```python
!~/.local/bin/uv run python -m src.train
```

Pour un dépôt privé, utiliser un secret Colab pour le token GitHub ; ne jamais
écrire le token directement dans le notebook. Les données et modèles peuvent
être stockés temporairement sur Google Drive, mais ne doivent pas être
commités.

Toujours noter le commit utilisé pour un entraînement Colab :

```python
!git rev-parse --short HEAD
```

## 9. Expériences et soumissions

Ajouter une ligne dans `experiments/log.csv` pour chaque expérience :

```text
date,author,model,features,validation_start,validation_end,rmspe,notes
```

Les résultats négatifs doivent également être conservés. Une soumission doit
être enregistrée dans `submissions/` avec un nom explicite, par exemple :

```text
submission_lgbm_v01.csv
```

Vérifier que le fichier contient exactement les colonnes `Id` et `Sales`.
Indiquer dans le journal le nom du fichier et le score Kaggle lorsqu'il est
disponible.

## 10. Résoudre un conflit

1. Lire les deux versions et supprimer les marqueurs
   `<<<<<<<`, `=======`, `>>>>>>>`.
2. Conserver la version correcte ou combiner les changements.
3. Vérifier le fichier puis exécuter :

```bash
git add <fichier>
git rebase --continue
```

Pour annuler un rebase :

```bash
git rebase --abort
```

Pour `uv.lock`, ne résolvez pas le fichier manuellement. Résolvez d'abord
`pyproject.toml`, puis régénérez :

```bash
uv lock
uv sync
git add pyproject.toml uv.lock
```

## 11. Checklist avant Pull Request

- [ ] Je travaille sur une branche dédiée.
- [ ] Ma branche est synchronisée avec `main`.
- [ ] `uv sync` fonctionne.
- [ ] Le code est exécutable avec `uv run`.
- [ ] Les données, secrets et fichiers lourds ne sont pas suivis par Git.
- [ ] Le notebook a été exécuté de haut en bas.
- [ ] Les chemins sont relatifs.
- [ ] L'expérience est enregistrée dans `experiments/log.csv`.
- [ ] `pyproject.toml` et `uv.lock` sont cohérents si les dépendances ont changé.
- [ ] La Pull Request explique clairement le changement et sa vérification.

## 12. Répartition des rôles

À compléter par l'équipe :

| Rôle | Responsabilités | Responsable |
|---|---|---|
| EDA | qualité des données, visualisations, analyse | À définir |
| Prétraitement et features | merge `store`, nettoyage, variables | À définir |
| Modélisation | baselines, LightGBM, réglage des paramètres | À définir |
| Validation et soumissions | RMSPE, journal, fichiers Kaggle | À définir |
| Rapport | rédaction, figures et résultats | À définir |

Chaque membre relit le travail d'un autre afin que toute l'équipe comprenne
le projet.
