import pandas as pd

def create_train_value(train_value, iso_date_to_split = '2015-06-01', columns_to_drop=['Sales', 'Date', 'Date_time', 'Customers']):
    # --- 4. LE SPLIT TEMPOREL (On utilise 'Date_temp' pour couper) ---
    # Par exemple, on prend tout ce qui est avant juin 2015 pour entraîner, et après pour valider
    date_coupure = pd.to_datetime(iso_date_to_split)

    train_set = train_value[train_value['Date_time'] < date_coupure]
    val_set = train_value[train_value['Date_time'] >= date_coupure]

    # 5. On sépare les Features (X) et la Cible (y -> 'Sales'), en dégageant la date et les colonnes inutiles
    X_train = train_set.drop(columns=columns_to_drop, errors='ignore')
    y_train = train_set['Sales']

    X_val = val_set.drop(columns=columns_to_drop, errors='ignore')
    y_val = val_set['Sales']
    
    return X_train, y_train, X_val, y_val


def add_lag_features(train_df, test_df, attributes=['Sales', 'Customers'], lag_days=[364, 49]):
    # 1. Conversion des dates au bon format
    train_df['Date_time'] = pd.to_datetime(train_df['Date_time'])
    if 'Date_time' in test_df.columns:
        test_df['Date_time'] = pd.to_datetime(test_df['Date_time'])

    # Récupération de l'historique complet pour les attributs demandés
    cols_to_keep = ['Store', 'Date_time'] + list(attributes)
    histo = train_df[cols_to_keep].copy()

    # Pour faire les jointures facilement via un index multi-niveau
    histo = histo.set_index(['Store', 'Date_time'])

    # Fonction interne pour récupérer les lags pour un dataframe cible
    def get_lags(target_df):
        target_df = target_df.copy()
        target_df['Date_time'] = pd.to_datetime(target_df['Date_time'])

        fill_values = {}

        # Boucle sur chaque attribut et chaque nombre de jours de lag
        for attr in attributes:
            for lag in lag_days:
                col_name = f"{attr}_lag_{lag}"
                
                # Calcul de la date cible décalée
                target_date = target_df['Date_time'] - pd.Timedelta(days=lag)
                
                # Clés de jointure (Store, Date_décalée)
                keys = list(zip(target_df['Store'], target_date))
                
                # Récupération des données via l'index multi-niveau
                lag_data = histo.reindex(keys).reset_index(drop=True)
                
                # Assignation dans le dataframe cible
                target_df[col_name] = lag_data[attr].values
                
                # Préparation du remplissage des valeurs manquantes à 0
                fill_values[col_name] = 0

        # Remplissage des valeurs manquantes créées par le décalage
        target_df.fillna(fill_values, inplace=True)
        return target_df

    # --- FILTRAGE AUTOMATIQUE INTELLIGENT ---
    # On trouve la date la plus ancienne dans l'historique d'entraînement
    min_histo_date = train_df['Date_time'].min()
    
    # On calcule le lag maximum demandé (ex: 364 jours)
    max_lag = max(lag_days) if lag_days else 0
    
    # La date limite devient : Date min de l'historique + Le plus grand lag
    # Tout ce qui est inférieur n'a pas assez de recul pour alimenter les lags
    cutoff_date = min_histo_date + pd.Timedelta(days=max_lag)
    
    print(f"Date minimale de l'historique : {min_histo_date.strftime('%Y-%m-%d')}")
    print(f"Lag maximum appliqué : {max_lag} jours")
    print(f"Filtrage automatique du train à partir du : {cutoff_date.strftime('%Y-%m-%d')}")

    # Filtrage du train en fonction de ce seuil dynamique
    train_filtered = train_df[train_df['Date_time'] >= cutoff_date].copy()
    test_filtered = test_df.copy() # Le jeu de test reste intact

    print("Calcul des lags pour le jeu d'entraînement...")
    train_filtered = get_lags(train_filtered)

    print("Calcul des lags pour le jeu de test...")
    test_filtered = get_lags(test_filtered)

    return train_filtered, test_filtered