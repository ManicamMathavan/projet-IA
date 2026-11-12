from utils.rmse_pourcent import rmse_pourcent
import pandas as pd
from sklearn.metrics import root_mean_squared_error

def display_submit_file(predictions,original_test_data, create_csv = False):
    # On fabrique le fichier final en remettant l'Id d'origine en face des prédictions
    submission = pd.DataFrame({
        'Id': original_test_data['Id'],       # On prend l'Id d'origine qui était au chaud
        'Sales': predictions # On colle la prédiction de l'IA en face
    })

    if create_csv:
        submission.to_csv('submission_rossmann.csv', index=False)
    display(submission.head())

def display_prediction_comparaison(predictions, data_frame_valeur_reel: pd.DataFrame ):
    # On met les vraies ventes et les prédictions dans un petit DataFrame pour comparer visuellement
    resultats_df = pd.DataFrame({
        'Vraies_Ventes': data_frame_valeur_reel.values,
        'Pred_Ventes': predictions
    })

    # Afficher les 10 premières lignes de comparaison
    print("Comparaison Vraies ventes vs Prédictions de l'IA :")
    display(resultats_df.head(10))

    # 4. Calculer une métrique simple d'erreur (la racine de l'erreur quadratique moyenne - RMSE)

    rmse = root_mean_squared_error(data_frame_valeur_reel, predictions)
    print(f"\nErreur globale (RMSE) sur la validation : {rmse:.2f}")

    # Petit piège de Rossmann : on évite de diviser par zéro si des ventes réelles valent 0
    # (même si normalement les magasins fermés sont à 0)
    rmse_pourcent(predictions, data_frame_valeur_reel)

