import unittest
from unittest.mock import Mock, patch
import datetime
import sys
import os

# Adiciona o diretório raiz ao path do Python para permitir importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.create_issues import create_issues, validate_environment


class TestCreateIssues(unittest.TestCase):
    def setUp(self):
        # Dados de teste
        self.test_issues = [
            ("#01 Teste", "Descrição teste 1"),
            ("#02 Teste", "Descrição teste 2"),
        ]
        self.test_last_issue = ("#03 Teste final", "Descrição final")
        self.test_partitioned = [
            ("#03a Teste especial", "Parte 1"),
            ("#03b Teste especial", "Parte 2"),
        ]
        self.due_date = datetime.date(2025, 5, 1)
        self.milestone_title = "Teste Milestone"

        # Mock do projeto GitLab
        self.mock_project = Mock()
        self.mock_milestone = Mock()
        self.mock_milestone.id = 1
        self.mock_milestone.title = (
            self.milestone_title
        )  # Agora self.milestone_title já está definido
        self.mock_project.milestones.list.return_value = [self.mock_milestone]
        self.mock_project.issues.list.return_value = []
        self.mock_project.issues.create.return_value = Mock()

    def test_create_issues_normal_group(self):
        """Testa criação de issues para grupo normal"""
        create_issues(
            project=self.mock_project,
            group_name="grupo1",
            issues=self.test_issues,
            last_issue=self.test_last_issue,
            partitioned_last_issue=self.test_partitioned,
            due_date=self.due_date,
            milestone_title=self.milestone_title,
        )

        # Verifica se todas as issues foram criadas
        expected_calls = len(self.test_issues) + 1  # +1 para last_issue
        self.assertEqual(self.mock_project.issues.create.call_count, expected_calls)

    def test_create_issues_special_group(self):
        """Testa criação de issues para grupo especial (grupo3 ou grupo6)"""
        create_issues(
            project=self.mock_project,
            group_name="grupo3",
            issues=self.test_issues,
            last_issue=self.test_last_issue,
            partitioned_last_issue=self.test_partitioned,
            due_date=self.due_date,
            milestone_title=self.milestone_title,
        )

        # Verifica se todas as issues foram criadas (incluindo as particionadas)
        expected_calls = len(self.test_issues) + len(self.test_partitioned)
        self.assertEqual(self.mock_project.issues.create.call_count, expected_calls)

    def test_duplicate_issue(self):
        """Testa comportamento quando issue já existe"""
        # Simula uma issue existente
        existing_issue = Mock()
        existing_issue.title = "#01 Teste"
        self.mock_project.issues.list.return_value = [existing_issue]

        create_issues(
            project=self.mock_project,
            group_name="grupo1",
            issues=self.test_issues,
            last_issue=self.test_last_issue,
            partitioned_last_issue=self.test_partitioned,
            due_date=self.due_date,
            milestone_title=self.milestone_title,
        )

        # Verifica se a issue duplicada foi pulada
        expected_calls = len(
            self.test_issues
        )  # -1 para a issue duplicada +1 para last_issue
        self.assertEqual(self.mock_project.issues.create.call_count, expected_calls)

    def test_milestone_not_found(self):
        """Testa comportamento quando milestone não é encontrada"""
        self.mock_project.milestones.list.return_value = []

        create_issues(
            project=self.mock_project,
            group_name="grupo1",
            issues=self.test_issues,
            last_issue=self.test_last_issue,
            partitioned_last_issue=self.test_partitioned,
            due_date=self.due_date,
            milestone_title=self.milestone_title,
        )

        # Verifica se nenhuma issue foi criada
        self.assertEqual(self.mock_project.issues.create.call_count, 0)

    @patch("scripts.create_issues.GITLAB_URL", "http://test.gitlab.com")
    @patch("scripts.create_issues.PRIVATE_TOKEN", "test_token")
    @patch("scripts.create_issues.groups", {"grupo1": {"id": 1}})
    def test_validate_environment(self):
        """Testa validação do ambiente"""
        self.assertTrue(validate_environment())

    @patch("scripts.create_issues.GITLAB_URL", "")
    @patch("scripts.create_issues.PRIVATE_TOKEN", "test_token")
    @patch("scripts.create_issues.groups", {"grupo1": {"id": 1}})
    def test_validate_environment_missing_url(self):
        """Testa validação do ambiente com URL faltando"""
        self.assertFalse(validate_environment())


if __name__ == "__main__":
    unittest.main()
