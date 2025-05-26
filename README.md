# RP1 Scripts

Scripts para automação de tarefas no GitLab da UNIPAMPA, voltados ao gerenciamento de milestones e issues em projetos acadêmicos de grupos. Este projeto facilita a criação e gerenciamento de milestones e issues para avaliações semanais e outras atividades acadêmicas.

---

## 📁 Estrutura

```
.
├── .venv/                  # Ambiente virtual (não versionar)
├── .env                    # Variáveis sensíveis (NÃO versionar)
├── .env.sample            # Exemplo de .env
├── consts.py              # Variáveis comuns (URL, token, grupos, milestones)
├── requirements.txt       # Dependências do projeto
├── README.md             # Este arquivo
├── tests/                # Testes automatizados
└── scripts/
    ├── create_milestones.py    # Criação de milestones para todos os grupos
    ├── create_issues.py        # Script principal para criação de issues
    ├── edit_issues/           # Scripts para edição de issues existentes
    └── legacy_create_issues/   # Scripts legados de criação de issues
```

---

## 🛠️ Pré-requisitos

- Python 3.8+
- Chave de acesso pessoal (Personal Access Token) no GitLab da UNIPAMPA com escopo `api`.

---

## ⚙️ Instalação

1. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate        # Windows
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Copie o arquivo `.env.sample` para `.env` e adicione seus dados:

```bash
cp .env.sample .env
```

Exemplo de `.env`:

```
GITLAB_URL=https://gitlab.unipampa.edu.br
GITLAB_TOKEN=seu_token_aqui
```

---

## 🛠️ Configuração

### Arquivo consts.py

O arquivo `consts.py` contém as configurações principais do projeto. Você deve atualizar as seguintes variáveis:

1. **Grupos**: Dicionário com os IDs dos projetos no GitLab
```python
groups = {
    "grupo1": {"id": 1086},
    "grupo2": {"id": 1087},
    # Adicione ou atualize os IDs dos grupos conforme necessário
}
```

2. **Milestones**: Lista de milestones com suas datas
```python
milestones = [
    ("Avaliação Semanal 1", "2025-05-19", "12/05 a 19/05"),
    ("Avaliação Semanal 2", "2025-05-26", "19/05 a 26/05"),
    # Adicione ou atualize as milestones conforme necessário
]
```

### Configuração de Issues

No arquivo `scripts/create_issues.py`, você precisa configurar as seguintes variáveis:

```python
# ===================== CONFIGURAÇÃO =====================
milestone_title = "Avaliação Semanal 1"  # Título da milestone
due_date_str = "2025-05-01"             # Data de entrega (YYYY-MM-DD)

# Lista de issues padrão (título, descrição)
issues: List[Tuple[str, str]] = [
    ("#01 Exemplo", "Descrição da issue 1"),
    ("#02 Exemplo", "Descrição da issue 2"),
]

# Issue final para grupos normais
last_issue: Tuple[str, str] = (
    "#03 Exemplo final",
    "Descrição da última issue para grupos normais",
)

# Issues especiais para grupos maiores (7 alunos)
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
```

Cada issue é definida como uma tupla contendo:
- Título da issue
- Descrição da issue

O script suporta dois tipos de grupos:
1. Grupos normais: recebem todas as issues da lista `issues` + a `last_issue`
2. Grupos maiores (7 alunos): recebem todas as issues da lista `issues` + as issues da lista `partitioned_last_issue`

---

## 🚀 Execução

### Criar Milestones para todos os grupos

```bash
python scripts/create_milestones.py
```

### Criar Issues

O script principal para criação de issues está em `scripts/create_issues.py`. Este script pode ser usado para criar issues para diferentes milestones e avaliações.

```bash
python scripts/create_issues.py
```

### Editar Issues Existentes

Os scripts para edição de issues estão localizados no diretório `scripts/edit_issues/`. Cada script é específico para um tipo de edição.

---

## 🧪 Testes

O projeto inclui testes automatizados no diretório `tests/`. Para executar os testes:

```bash
python -m pytest tests/
```

---

## 📝 Notas

- Mantenha seu token do GitLab seguro e nunca o compartilhe
- Faça backup das issues antes de executar scripts de edição em massa
- Consulte a documentação do GitLab API para mais detalhes sobre as operações disponíveis
- Atualize o arquivo `consts.py` sempre que houver mudanças nos grupos ou milestones
- Verifique se as datas das milestones estão corretas antes de executar os scripts
