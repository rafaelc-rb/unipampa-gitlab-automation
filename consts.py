import os
from dotenv import load_dotenv

load_dotenv()

# Variáveis de ambiente
GITLAB_URL = os.getenv("GITLAB_URL")
PRIVATE_TOKEN = os.getenv("PRIVATE_TOKEN")

# IDs reais dos projetos devem ser preenchidos aqui
groups = {
    "grupo1": {"id": 1086},
    "grupo2": {"id": 1087},
    "grupo3": {"id": 1088},  # 7 integrantes
    "grupo4": {"id": 1089},
    "grupo5": {"id": 1090},
    "grupo6": {"id": 1091},  # 7 integrantes
    "grupo7": {"id": 1092},
    "grupo8": {"id": 1093},
}

# Lista de milestones (nome, data de entrega, intervalo de datas)
milestones = [
    ("Avaliação Semanal 1", "2025-05-19", "12/05 a 19/05"),
    ("Avaliação Semanal 2", "2025-05-26", "19/05 a 26/05"),
    ("Avaliação Semanal 3", "2025-06-02", "26/05 a 02/06"),
    ("Avaliação Semanal 4", "2025-06-09", "02/06 a 09/06"),
    ("Avaliação Semanal 5", "2025-06-16", "09/06 a 16/06"),
    ("Avaliação Semanal 6", "2025-06-23", "16/06 a 23/06"),
    ("Avaliação Semanal 7", "2025-06-30", "23/06 a 30/06"),
]
