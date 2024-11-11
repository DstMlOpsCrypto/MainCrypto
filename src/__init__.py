import pytest

# __init__.py
import os
import sys
from os.path import dirname, join, normpath, abspath

print("Execution du fichier __init__.py dans le repertoire src")

# Récupérer le chemin d'accès du répertoire courant du dossier
current_dir = os.getcwd()
# Accéder au répertoire parent en utilisant os.pardir
parent_dir = abspath(os.path.join(current_dir, os.pardir))
# Accéder au répertoire parent en utilisant os.pardir
grand_parent_dir = abspath(os.path.join(parent_dir, os.pardir))
# Construire le chemin vers le répertoire `src`
src_dir = abspath(os.path.join(grand_parent_dir, 'src'))
scripts_dir = abspath(os.path.join(grand_parent_dir, 'scripts'))

#ajout du chemin dans sys
sys.path.append(current_dir)
sys.path.append(parent_dir)
sys.path.append(grand_parent_dir)
sys.path.append(src_dir)
sys.path.append(scripts_dir)
# sys.path.append("..")  # Add the parent directory to the Python path

print("Modification du PATH terminée")
