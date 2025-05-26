import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import gitlab
from consts import GITLAB_URL, PRIVATE_TOKEN, groups


def create_issues(project, group_name):
    milestone = next(
        (m for m in project.milestones.list() if m.title == "Avaliação Semanal 3"), None
    )

    issues = [
        # 01
        (
            "RNF Segurança, Proteção e Desempenho",
            """
            Identificar as necessidades relativas aos requisitos não funcionais de Segurança, Proteção e Desempenho considerando a realidade do ambiente ao qual se destina o software.

            Deve-se, portanto, descrever o nível de segurança, proteção e desempenho necessários ao software, apresentando detalhes sempre que possível. 

            Complementarmente, se forem identificados outros requisitos não funcionais importantes para o sistema, estes também devem ser descritos, com exceção dos pedidos na atividade 2. 

            Crie uma página Wiki espeficiamente para documentar os RNF.

            Dica de vídeo: https://www.youtube.com/watch?v=obdObvy5OxA
            """,
        ),
        # 02
        (
            "RNF Confiabilidade, Usabilidade e Acessibilidade",
            """
            Identificar as necessidades relativas aos requisitos não funcionais de Confiabilidade, Usabilidade e Acessibilidade considerando a realidade do ambiente ao qual se destina o software.

            Deve-se, portanto, descrever o nível de confiabilidade, usabilidade e acessibilidade necessários ao software, apresentando detalhes sempre que possível. 

            Complementarmente, se forem identificados outros requisitos não funcionais importantes para o sistema, estes também devem ser descritos, com exceção dos pedidos na atividade 1. 

            Crie uma página Wiki espeficiamente para documentar os RNF.

            Dica de vídeo: https://www.youtube.com/watch?v=obdObvy5OxA
            """,
        ),
        # 03
        (
            "Diagrama de Casos de Uso",
            """
            Desenvolva o diagrama de casos de uso (DCU) para o sistema de governança hoteleira considerando seus requisitos funcionais bem como quais atores poderão utilizá-los. 

            Crie uma página Wiki para documentar o DCU e descreva os elementos do diagrama.

            Dica de vídeos https://www.youtube.com/watch?v=qVemjrDKw2k&list=PLMI4h2donpGxP3ZwrbEJdYE-OvRFiCAEG e https://www.youtube.com/watch?v=r-k0Q7RHN4E&list=PLMI4h2donpGxP3ZwrbEJdYE-OvRFiCAEG&index=2
            """,
        ),
        # 04
        (
            "Modelar o Diagrama de Classes (CD) Conceitual",
            """
            Produza o diagrama de classes (CD) - modelo conceitual para o sistema de governança hoteleira considerando a descrição dos requisitos elicitados.

            Neste diagrama devem ser apresentadas somente classes de entidade (eventualmente classes de enumeração podem ser aceitas). O diagrama deve descrever também como as classes se relacionam.

            Crie uma página Wiki para documentar o CD e descreva os elementos do diagrama.

            Dica de vídeos: https://www.youtube.com/watch?v=uaq6KOUgP14&list=PLMI4h2donpGxn0z1mSCN9eBhQWa_a1tk0 - Nessa playlist há vários vídeos sobre o diagrama de classes, um em particular explica para os iniciantes como identificar classes.
            """,
        ),
        # 05
        (
            "Modelar o Diagrama de Máquina de Estados (SMD)",
            """
            Produza diagramas de máquina de estados (SMD) descrevendo os estados de objetos de classes do sistema que apresente um conjunto de estados (no mínimo 2 estados) pertinentes.

            Assim, se for identificado que os objetos de uma determinada classe podem possuir um conjunto de estados deve-se criar um diagrama de máquina de estados para ele.

            Crie uma página Wiki para documentar o(s) SMD(s) e descreva os elementos do(s) diagrama(s).

            Dica de vídeos: https://www.youtube.com/watch?v=p-qtIBZtxbc&list=PLMI4h2donpGx0NRd-_ghuGgIeQT0NjMzP Atenção: é para produzir máquina de estados para objetos e não para casos de uso.
            """,
        ),
    ]

    if group_name in ["grupo3", "grupo6"]:
        issues.extend(
            [
                # 06a
                (
                    "Prototipação de telas e Workflow",
                    """
                    Produza e/ou refatore protótipos para o sistema e produza workflows para eles descrevendo como eles serão utilizados, que informações serão inseridas, quais o s resultados gerados, esse tipo de coisa.
                    """,
                ),
                # 06b
                (
                    "Validação dos Protótipos de Tela junto ao Cliente",
                    """
                    Validem os protótipos com o cliente para verificar se ele está de acordo com a proposta, documentando a validação com as melhorias sugeridas em uma página Wiki.
                    """,
                ),
            ]
        )
    else:
        issues.append(
            # 06
            (
                "Prototipação de telas e Workflow Validação dos Protótipos de Tela junto ao Cliente",
                """
            Produza e/ou refatore protótipos para o sistema e produza workflows para eles descrevendo como eles serão utilizados, que informações serão inseridas, quais o s resultados gerados, esse tipo de coisa.

            Após isso, validem os protótipos com o cliente para verificar se ele está de acordo com a proposta, documentando a validação com as melhorias sugeridas em uma página Wiki.
            """,
            ),
        )

    for title, description in issues:
        try:
            project.issues.create(
                {
                    "title": title,
                    "description": description,
                    "due_date": "2025-06-01",
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
