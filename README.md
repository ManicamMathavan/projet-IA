# Rossmann Store Sales

Projet d'équipe de prédiction des ventes quotidiennes des magasins Rossmann,
réalisé dans le cadre de la compétition Kaggle
[Rossmann Store Sales](https://www.kaggle.com/competitions/rossmann-store-sales).

L'objectif est de construire un pipeline reproductible : téléchargement des
données, exploration, nettoyage, création de variables, validation temporelle,
entraînement et génération d'une soumission Kaggle.

## Structure du projet

```text
rossmann-sales/
├── README.md
├── pyproject.toml
├── uv.lock                 # Versions résolues par uv
├── .gitignore
├── data/
│   ├── raw/                 # Données Kaggle originales, jamais versionnées
│   └── processed/           # Données nettoyées et features, jamais versionnées
├── models/                  # Modèles entraînés, jamais versionnés
├── notebooks/
│   ├── 01_eda_<prenom>.ipynb
│   ├── 02_preprocessing_<prenom>.ipynb
│   └── 03_modeling_<prenom>.ipynb
├── src/
│   ├── data.py              # Chargement et jointure train/store
│   ├── features.py          # Feature engineering sans effet de bord
│   ├── metrics.py           # RMSPE et évaluation
│   ├── validation.py        # Découpage temporel
│   ├── models.py            # Création des modèles
│   └── train.py             # Entraînement et soumission
├── experiments/
│   └── log.csv              # Journal partagé des expériences
├── submissions/             # Soumissions CSV et scores (petits fichiers)
└── report/
    ├── main.tex
    └── figures/
```

Les fichiers historiques présents dans `src/` peuvent être conservés pendant
la migration ; le nouveau pipeline Rossmann utilise les modules listés
ci-dessus.

## Installation locale

Python 3.11 ou 3.12 est recommandé. Python 3.10+ est supporté par le projet.
La gestion de l'environnement et des dépendances se fait exclusivement avec
[uv](https://docs.astral.sh/uv/).

Installer `uv` une seule fois :

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Sous macOS/Linux :

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Puis ouvrir un nouveau terminal et vérifier l'installation :

```bash
uv --version
```

```powershell
git clone <url-du-depot>
cd rossmann-sales
uv python install 3.11
uv sync
```

`uv sync` crée automatiquement `.venv`, installe les dépendances de
`pyproject.toml` et respecte les versions verrouillées dans `uv.lock`.
Pour activer l'environnement dans PowerShell :

```bash
.\.venv\Scripts\Activate.ps1
```

Sous macOS/Linux :

```bash
source .venv/bin/activate
```

Les commandes Python peuvent aussi être exécutées sans activation :

```bash
uv run python -m src.train
uv run jupyter lab
```

Après toute modification des dépendances :

```bash
uv lock
uv sync
```

## Données Kaggle

1. Accepter les règles de la compétition sur Kaggle.
2. Télécharger `train.csv`, `test.csv` et `store.csv`.
3. Placer les fichiers dans `data/raw/` :

```text
data/raw/
├── train.csv
├── test.csv
└── store.csv
```

Les données ne sont volontairement pas commitées : elles sont volumineuses et
soumises aux conditions d'utilisation de Kaggle. Ne mettez jamais de clé API,
token ou identifiant privé dans le dépôt.

Avec l'API Kaggle, après configuration locale de `KAGGLE_API_TOKEN` :

```bash
kaggle competitions download -c rossmann-store-sales -p data/raw
```

Décompressez ensuite l'archive dans `data/raw/`.

## Exécuter le pipeline

Les notebooks sont conçus pour être exécutés dans l'ordre :

1. `01_eda_<prenom>.ipynb` : qualité des données, distributions et premières
   hypothèses ;
2. `02_preprocessing_<prenom>.ipynb` : jointure avec `store.csv`, nettoyage et
   génération des variables dans `data/processed/` ;
3. `03_modeling_<prenom>.ipynb` : validation temporelle, entraînement,
   comparaison des modèles et export d'une soumission dans `submissions/`.

Le script d'entraînement peut également être lancé depuis la racine :

```bash
uv run python -m src.train
```

Chaque exécution doit être reproductible : fixer la seed, enregistrer les
paramètres dans `experiments/log.csv` et ne jamais utiliser de lignes futures
pour calculer des variables d'entraînement.

## Exécuter les notebooks localement

Jupyter est installé par `uv sync`. Lancer Jupyter :

```bash
uv run python -m ipykernel install --user --name rossmann-sales --display-name "Python (rossmann-sales)"
uv run jupyter lab
```

Ouvrir ensuite `notebooks/` et sélectionner le kernel `Python (rossmann-sales)`.
Un notebook personnel doit être nommé avec le prénom de son auteur, par
exemple `01_eda_mahdi.ipynb`. Les notebooks ne doivent pas contenir de
chemins absolus vers l'ordinateur d'un membre de l'équipe.

## Exécuter sur Google Colab

1. Importer le dépôt dans Colab avec **File > Open notebook > GitHub**, ou
   cloner le dépôt dans une cellule :

   ```python
   !git clone <url-du-depot>
   %cd rossmann-sales
   !curl -LsSf https://astral.sh/uv/install.sh | sh
   !~/.local/bin/uv sync
   ```

2. Dans une cellule suivante, utiliser `!~/.local/bin/uv run ...` pour lancer
   Python ou Jupyter. Importer les fichiers Kaggle dans `data/raw/` via le panneau de fichiers,
   ou utiliser l'API Kaggle avec un secret Colab. Ne commitez jamais
   `kaggle.json`.
3. Ouvrir le notebook souhaité et exécuter les cellules de haut en bas.
4. Télécharger les résultats produits dans `submissions/` et les partager via
   le dépôt ou un espace de stockage autorisé.

## Méthode de travail en équipe

- Une branche par fonctionnalité ou expérience :
  `feature/preprocessing-mahdi`, `experiment/lightgbm-split`.
- Synchroniser avant de commencer :
  `git pull --rebase origin main`.
- Faire des commits petits et explicites :
  `feat: add date features` ou `exp: compare lgbm and random forest`.
- Ouvrir une Pull Request vers `main` ; demander une relecture avant fusion.
- Ne jamais commiter `data/`, `models/`, les checkpoints ou les secrets.
- Une personne responsable d'un notebook le maintient ; les fonctions
  réutilisables vont dans `src/` plutôt que dans une cellule.
- Avant une PR : exécuter le notebook modifié de haut en bas, vérifier les
  chemins relatifs et ajouter une ligne à `experiments/log.csv`.

Exemple de workflow :

```bash
git switch main
git pull --rebase origin main
git switch -c feature/features-calendrier
# travail, tests et exécution du notebook
git add src notebooks experiments/log.csv
git commit -m "feat: add calendar features"
git push -u origin feature/features-calendrier
```

## Validation et métrique

La métrique Kaggle est la **RMSPE** (Root Mean Square Percentage Error).
Le découpage doit respecter l'ordre chronologique : un modèle ne doit jamais
apprendre sur une date postérieure à sa validation. Les scores locaux et les
paramètres sont consignés dans `experiments/log.csv`.

Format recommandé pour le journal :

```text
date,author,model,features,validation_start,validation_end,rmspe,notes
```

## Soumissions

Les fichiers finaux peuvent être ajoutés dans `submissions/` avec un nom
explicite, par exemple `submission_lgbm_v01.csv`, accompagné d'un court
compte-rendu du score Kaggle dans le journal d'expériences. Vérifier les
colonnes `Id` et `Sales` avant l'envoi.
