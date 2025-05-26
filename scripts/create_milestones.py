import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import gitlab
from consts import GITLAB_URL, PRIVATE_TOKEN, groups, milestones


def ensure_milestone(project, title, due_date):
    existing = project.milestones.list()
    if not any(m.title == title for m in existing):
        project.milestones.create({"title": title, "due_date": due_date})
        print(f"✓ Milestone criada: {title}")
    else:
        print(f"• Milestone já existe: {title}")


def main():
    gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)
    for nome, info in groups.items():
        print(f"\n=== Processando {nome} ===")
        project = gl.projects.get(info["id"])
        for title, due_date, _ in milestones:
            ensure_milestone(project, title, due_date)


if __name__ == "__main__":
    main()
