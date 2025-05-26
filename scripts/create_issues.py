import logging
import datetime
from typing import List, Tuple, Optional

import gitlab
from consts import GITLAB_URL, PRIVATE_TOKEN, groups


def validate_environment() -> bool:
    """Valida se as variáveis de ambiente necessárias estão definidas."""
    if not GITLAB_URL or not PRIVATE_TOKEN or not groups:
        logging.error(
            "GITLAB_URL, PRIVATE_TOKEN e groups devem estar definidos em consts.py"
        )
        return False
    return True


def create_issues(
    project: object,
    group_name: str,
    issues: List[Tuple[str, str]],
    last_issue: Optional[Tuple[str, str]],
    partitioned_last_issue: List[Tuple[str, str]],
    due_date: datetime.date,
    milestone_title: str,
) -> None:
    """
    Cria issues em um projeto GitLab de acordo com as configurações fornecidas.

    Args:
        project: Instância do projeto GitLab.
        group_name: Nome do grupo (str).
        issues: Lista de (title, description) para issues gerais.
        last_issue: (title, description) para grupos normais.
        partitioned_last_issue: Lista de (title, description) para grupos especiais.
        due_date: Data de entrega (datetime.date).
        milestone_title: Nome da milestone (str).
    """
    # Busca a milestone pelo título usando filtro de busca
    mlist = project.milestones.list(search=milestone_title)
    milestone = next((m for m in mlist if m.title == milestone_title), None)
    if not milestone:
        logging.warning(
            "Milestone '%s' não encontrada no projeto %s",
            milestone_title,
            project.name,
        )
        return

    # Prepara lista de issues para o grupo
    group_issues = list(issues)
    if group_name in ("grupo3", "grupo6"):
        group_issues.extend(partitioned_last_issue)
    elif last_issue:
        group_issues.append(last_issue)

    for title, description in group_issues:
        # Verifica se já existe issue com mesmo título
        existing = [i for i in project.issues.list(search=title) if i.title == title]
        if existing:
            logging.info("Issue já existe e será ignorada: %s", title)
            continue

        payload = {
            "title": title,
            "description": description,
            "due_date": due_date.isoformat(),
            "milestone_id": milestone.id,
        }
        try:
            project.issues.create(payload)
            logging.info("Issue criada: %s", title)
        except gitlab.exceptions.GitlabCreateError as e:
            logging.error(
                "Falha ao criar issue '%s': %s",
                title,
                getattr(e, "error_message", str(e)),
            )


def main() -> None:
    # ===================== CONFIGURAÇÃO =====================
    milestone_title = "Avaliação Semanal 1"
    due_date_str = "2025-05-01"
    # Issues
    issues: List[Tuple[str, str]] = [
        ("#01 Exemplo", "Descrição da issue 1"),
        ("#02 Exemplo", "Descrição da issue 2"),
    ]
    last_issue: Tuple[str, str] = (
        "#03 Exemplo final",
        "Descrição da última issue para grupos normais",
    )
    partitioned_last_issue: List[Tuple[str, str]] = [
        (
            "#03a Exemplo especial",
            "Descrição para grupos de 7 alunos - parte 1",
        ),
        (
            "#03b Exemplo especial",
            "Descrição para grupos de 7 alunos - parte 2",
        ),
    ]
    # ========================================================

    # Configuração do logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Validação do ambiente
    if not validate_environment():
        return

    # Converte e valida due_date
    try:
        due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        logging.error("Formato de data inválido: %s. Use YYYY-MM-DD.", due_date_str)
        return

    # Autenticação na API GitLab
    gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)

    # Loop por cada grupo definido em consts.grupos
    for group_name, info in groups.items():
        logging.info("=== Criando issues para grupo: %s ===", group_name)
        try:
            project = gl.projects.get(info["id"])
        except gitlab.exceptions.GitlabGetError as e:
            logging.error(
                "Falha ao acessar projeto %s: %s",
                info["id"],
                getattr(e, "error_message", str(e)),
            )
            continue

        create_issues(
            project=project,
            group_name=group_name,
            issues=issues,
            last_issue=last_issue,
            partitioned_last_issue=partitioned_last_issue,
            due_date=due_date,
            milestone_title=milestone_title,
        )


if __name__ == "__main__":
    main()
