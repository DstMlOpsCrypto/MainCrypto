# __init__.py
import os
import sys
from os.path import dirname, join, normpath, abspath

# Récupérer le chemin d'accès du répertoire courant du dossier
current_dir = os.getcwd()
# Accéder au répertoire parent en utilisant os.pardir
parent_current_dir = abspath(os.path.join(current_dir, os.pardir))

# Accéder au répertoire grand parent
grand_parent_dir = abspath(os.path.join(parent_current_dir, os.pardir))

SRC_DIR = normpath(join(grand_parent_dir, 'src'))
SCRIPTS_DIR = normpath(join(grand_parent_dir, 'scripts'))

#ajout du chemin dans sys
sys.path.append(grand_parent_dir)
sys.path.append(SRC_DIR)
sys.path.append(SCRIPTS_DIR)