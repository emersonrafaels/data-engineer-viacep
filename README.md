# API ViaCEP - Lambda Function

Este repositório contém uma implementação de uma função AWS Lambda que simula a consulta de CEPs utilizando a API ViaCEP. O objetivo é demonstrar boas práticas de desenvolvimento, testes automatizados e integração contínua em um projeto de engenharia de dados.

---

## O que você aprenderá com este repositório

1. **Boas práticas de desenvolvimento em Python**:
   - Uso de ferramentas como `flake8`, `bandit`, `black` e `isort` para garantir qualidade e segurança do código.
   - Estruturação de projetos Python para facilitar a manutenção e escalabilidade.

2. **Testes automatizados**:
   - Como escrever testes unitários utilizando `pytest` e `unittest.mock`.
   - Garantir a cobertura de código e a validação de cenários de sucesso e erro.

3. **Integração contínua (CI)**:
   - Configuração de workflows no GitHub Actions para executar testes, verificar qualidade do código e realizar deploy automático.

4. **Deploy na AWS Lambda**:
   - Empacotamento e deploy de uma função Lambda utilizando o AWS CLI.

---

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas:

- **Python 3.9 ou superior**: [Download](https://www.python.org/downloads/)
- **Pip**: Gerenciador de pacotes do Python.
- **AWS CLI**: [Instalação](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- **Git**: [Instalação](https://git-scm.com/)

---

## Como executar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/api-viacep-lambda.git
cd api-viacep-lambda
```

### 2. Crie um ambiente virtual
Crie e ative um ambiente virtual para isolar as dependências do projeto:
```bash
python -m venv venv
# Ativar no Windows
venv\Scripts\activate
# Ativar no Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
Instale as dependências do projeto listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Execute os testes
Certifique-se de que todos os testes estão passando:
```bash
pytest tests/
```

### 5. Verifique a qualidade do código
Execute as ferramentas de análise estática para garantir a qualidade e segurança do código:
```bash
flake8 .
bandit -r .
```

### 6. Empacote a aplicação
Empacote a função Lambda para deploy:
```bash
mkdir package
pip install -r requirements.txt -t package/
cp lambda_function.py package/
cd package
zip -r9 ../lambda_function.zip .
```

### 7. Faça o deploy na AWS Lambda
Certifique-se de que suas credenciais AWS estão configuradas e execute o comando abaixo para fazer o deploy:
```bash
aws lambda update-function-code \
    --function-name api_viacep \
    --zip-file fileb://lambda_function.zip \
    --publish
```

---

## Estrutura do projeto

```plaintext
api-viacep-lambda/
├── .github/
│   └── workflows/
│       └── deploy.yml         # Workflow para CI/CD no GitHub Actions
├── tests/
│   └── test_lambda_function.py # Testes unitários para a função Lambda
├── lambda_function.py         # Código principal da função Lambda
├── requirements.txt           # Dependências do projeto
├── .pre-commit-config.yaml    # Configuração do pre-commit
├── .yamllint                  # Configuração do yamllint
└── README.md                  # Documentação do projeto
```

---

## Ferramentas utilizadas

- **[Flake8](https://flake8.pycqa.org/)**: Verificação de estilo e qualidade do código.
- **[Bandit](https://bandit.readthedocs.io/)**: Análise de segurança do código.
- **[Black](https://black.readthedocs.io/)**: Formatação automática do código.
- **[isort](https://pycqa.github.io/isort/)**: Organização de importações.
- **[Pytest](https://docs.pytest.org/)**: Framework de testes.
- **[GitHub Actions](https://github.com/features/actions)**: Integração contínua e deploy.

---

## Contribuindo

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -m "[ADD] Minha nova feature"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
