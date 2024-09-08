import subprocess

def start_mlflow_server(tracking_uri="http://0.0.0.0:5000", port=5000):
    """
    Démarre un serveur MLflow.    
    :param tracking_uri: L'URI de suivi pour le serveur MLflow.
    :param port: Le port sur lequel le serveur MLflow sera lancé.
    """
    command = [
        "mlflow", "server",
        "--host", "0.0.0.0",
        "--port", str(port)
    ]

    # Lancement du serveur MLflow en arrière-plan
    process = subprocess.Popen(command)
    print(f"MLflow server started at {tracking_uri}")
    
    return process

# Exemple d'utilisation

if __name__ == "__main__":
    server_process = start_mlflow_server()
