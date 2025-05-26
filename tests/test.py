import gitlab
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("GITLAB_URL")
token = os.getenv("GITLAB_TOKEN")

gl = gitlab.Gitlab(url, private_token=token)

project_id = 1087  # substitua aqui por um dos IDs do seu consts.py

print(gl.projects.list())
print(url)
print(token)
try:
    project = gl.projects.get(project_id)
    print(f"Acesso OK: {project.name_with_namespace}")
except gitlab.exceptions.GitlabGetError as e:
    print(f"Erro: {e}")
