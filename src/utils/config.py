import json
import os
from pathlib import Path

def load_json(json_name):

    """
    Charge le json présent dans le projet
    
    :param jason_nam: str, le nom du fichier json à charger avec son extension .json.
    :return: dictionnaire dans json chargé
    """

    # Récupérer le chemin d'accès du répertoire courant
    current_dir = os.getcwd()
    
    # Accéder au répertoire parent en utilisant os.pardir : on accède alors au repertoire scr
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    
    # Accéder de nouveau au répertoire parent en utilisant os.pardir : on accède alors au repertoire du projet lui-même
    grand_parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

    # Associer à une variable le chemin d'accès absolu du repertoire du projet
    data_project_path = Path(grand_parent_dir)

    # Rechercher le fichier dans le dossier et ses sous-dossiers de ce projet
    file_list = list(data_project_path.rglob(json_name))
    
    # Vérifier si au moins un fichier correspondant au nom a été trouvé
    if file_list:    
        with open(file_list[0], 'r') as config_file:
            config = json.load(config_file)
        print(f"Json loaded successfully from {file_list[0]}")
        return config
    else:
        print(f"Le fichier {json_name} n'a pas été trouvé dans le repertoire parent {data_project_path} ou ses sous-dossiers.")
        return None
 