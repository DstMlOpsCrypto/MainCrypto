from sklearn.model_selection import GridSearchCV
import joblib

class GridSearch:
    
    def __init__(self, estimator, param_grid, cv=5, scoring='neg_root_mean_squared_error', verbose=1, n_jobs=-1):
        """
        Initialisation avec des arguments dynamiques.

        :param estimator: Le modèle/estimateur sur lequel effectuer la recherche par grille.
        :param param_grid: Grille de paramètres à tester pour l'estimateur.
        :param cv: Nombre de plis pour la validation croisée.
        :param scoring: Métrique de scoring à utiliser.
        :param verbose: Niveau de verbosité de la sortie.
        :param n_jobs: Nombre de jobs à exécuter en parallèle.
        """
        self.grid_search = GridSearchCV(estimator, param_grid, cv=cv, scoring=scoring, verbose=verbose, n_jobs=n_jobs)

    def fit(self, X, y):
        """
        Exécute la recherche par grille sur les données fournies.

        :param X: Les caractéristiques d'entraînement.
        :param y: Les étiquettes cibles.
        """

        self.grid_search.fit(X, y)
        self.cv_results_ = self.grid_search.cv_results_
        print(f"Meilleurs paramètres: {self.grid_search.best_params_}")
        print(f"Meilleur score: {self.grid_search.best_score_}")

    def predict(self, X):
        """
        Fait des prédictions avec le meilleur modèle trouvé.
        
        :param X: Les caractéristiques pour lesquelles faire des prédictions.
        :return: Les prédictions du modèle.
        """
        if self.grid_search is None:
            raise Exception("GridSearchCV n'a pas encore été ajusté.")
        return self.grid_search.predict(X)

    def save_best_model(self, file_path):
        """
        Sauvegarde le meilleur modèle trouvé sur le disque.
        
        :param file_path: Chemin du fichier où sauvegarder le modèle.
        """
        if self.grid_search is None:
            raise Exception("GridSearchCV n'a pas encore été ajusté.")
        joblib.dump(self.grid_search.best_estimator_, file_path)
