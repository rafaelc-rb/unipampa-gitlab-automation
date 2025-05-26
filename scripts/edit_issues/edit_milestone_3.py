import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import gitlab
from consts import GITLAB_URL, PRIVATE_TOKEN, groups


def edit_issues(project):
    # Get the milestone
    milestone = next(
        (m for m in project.milestones.list() if m.title == "Avaliação Semanal 3"), None
    )

    if not milestone:
        print(
            f"⚠️ Milestone 'Avaliação Semanal 3' não encontrada no projeto {project.name}"
        )
        return

    # Get all issues from the milestone
    issues = project.issues.list(all=True, milestone=milestone.title)

    # Update each issue
    for issue in issues:
        try:
            issue.due_date = "2025-06-01"  # New due date
            issue.save()
            print(f"✓ Issue atualizada: {issue.title}")
        except gitlab.exceptions.GitlabUpdateError as e:
            print(f"⚠️ Erro ao atualizar a issue {issue.title}: {e}")


def main():
    gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)
    for nome, info in groups.items():
        print(f"\n=== Editando issues para {nome} ===")
        project = gl.projects.get(info["id"])
        edit_issues(project)


if __name__ == "__main__":
    main()
