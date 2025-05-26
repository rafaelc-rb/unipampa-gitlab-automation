import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import gitlab
from consts import GITLAB_URL, PRIVATE_TOKEN, groups


def create_issues(project, group_name):
    milestone = next(
        (m for m in project.milestones.list() if m.title == "Avaliação Semanal 1"), None
    )

    issues = [
        (
            "#01 Organizar a Wiki",
            "Organizar o repositório de versionamento (GitLab) e criar Wiki com a estrutura do Software Requirement Specification (SRS) - template ISO/IEC/IEEE 29148:2018.",
        ),
        (
            "#02 Descrever o SRS",
            "Descrever a Seção Propósito do SRS. Descrever a Seção Escopo do SRS. Descrever a Seção Visão Geral do Produto do SRS (Perspectiva do Produto, Funções do Produto).",
        ),
        (
            "#03 Definição de Técnicas de Requisitos",
            "Definir 2 técnicas de elicitação de requisitos. Elaborar planejamento de aplicação das técnicas de elicitação.",
        ),
        ("#04 Criar o Storytelling", "Elaborar uma storytelling para o projeto."),
        ("#05 Criar o Storyboard", "Elaborar uma storyboard para o projeto."),
    ]

    if group_name in ["grupo3", "grupo6"]:
        issues.extend(
            [
                (
                    "#06 Identificar os Stakeholders",
                    "Identificar stakeholders (Onion Model); Gerenciamento de stakeholders:",
                ),
                (
                    "#07 Gerenciar os Stakeholders",
                    "Gerenciar os stakeholders (planilha de gerenciamento, priorização). Descrever a Seção Visão Geral do Produto do SRS (Características do Usuário, Limitações).",
                ),
            ]
        )
    else:
        issues.append(
            (
                "#06 Identificar e Gerenciar os Stakeholders",
                "Identificar stakeholders (Onion Model); Gerenciar os stakeholders (planilha de gerenciamento, priorização). Descrever a Seção Visão Geral do Produto do SRS (Características do Usuário, Limitações).",
            )
        )

    for title, description in issues:
        try:
            project.issues.create(
                {
                    "title": title,
                    "description": description,
                    "due_date": "2025-05-19",
                    "milestone_id": milestone.id,
                }
            )
            print(f"✓ Issue criada: {title}")
        except gitlab.exceptions.GitlabCreateError:
            print(f"⚠️ Erro ao criar a issue: {title}")


def main():
    gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)
    for nome, info in groups.items():
        print(f"\n=== Criando issues para {nome} ===")
        project = gl.projects.get(info["id"])
        create_issues(project, nome)


if __name__ == "__main__":
    main()
