import numpy as np
def rmse_pourcent(predictions, valeur_reel ): 
    mask = valeur_reel != 0

    rmspe = np.sqrt(np.mean(np.square((valeur_reel[mask] - predictions[mask]) / valeur_reel[mask])))

    print(f"Score RMSPE Rossmann : {rmspe * 100:.2f}% (ou {rmspe:.4f} en valeur brute)")