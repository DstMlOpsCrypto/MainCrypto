import pytest

# __init__.py
import os
import sys
from os.path import dirname, join, normpath, abspath

print("Je suis bien passé par init_py dans le src")

# Récupérer le chemin d'accès du répertoire courant du dossier
current_dir = os.getcwd()
# Accéder au répertoire parent en utilisant os.pardir
parent_current_dir = abspath(os.path.join(current_dir, os.pardir))

# Accéder au répertoire parent en utilisant os.pardir
grand_current_dir = abspath(os.path.join(parent_current_dir, os.pardir))

#ajout du chemin dans sys
sys.path.append(parent_current_dir)
sys.path.append(grand_current_dir)
sys.path.append(current_dir)
                
# sys.path.append("..")  # Add the parent directory to the Python path)  
