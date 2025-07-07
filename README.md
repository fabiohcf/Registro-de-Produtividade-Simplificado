Registro de Produtividade Simplificado

Este projeto é uma aplicação web desenvolvida como parte da disciplina Imersão Profissional: Implementação de uma Aplicação, do curso de Análise e Desenvolvimento de Sistemas (UNIASSELVI). O sistema foi idealizado para facilitar o registro de sessões de estudo, definição de metas semanais e acompanhamento da produtividade de forma simples e visual.

Funcionalidades Principais:

- Cadastro de sessões com descrição, tipo de atividade, tempo líquido e bruto.
- Definição de metas semanais de horas de estudo/trabalho.
- Relatórios interativos com gráficos (Chart.js) que indicam se a meta foi atingida.
- Banco de dados local SQLite para persistência das informações.

Tecnologias Utilizadas:

- Python 3
- Flask (framework web)
- SQLite (banco de dados embutido)
- HTML, CSS, Jinja2
- Chart.js (visualização de dados)
- Render (deploy na nuvem)
- Git (controle de versão)

Estrutura do Projeto:
´´´
├── app.py
├── database.py
├── sessoes.db
├── Procfile
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── meta.html
│   ├── relatorio.html
├── static/
│   ├── style.css
│   ├── relatorio.css
│   ├── script.js
´´´

Siga os passos abaixo para executar o projeto em ambiente local:

Clone este repositório:
git clone https://github.com/fabiohcf/Registro-de-Produtividade-Simplificado/
cd Registro-de-Produtividade-Simplificado

Crie um ambiente virtual Python:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows

Instale as dependências:
pip install -r requirements.txt

Execute o servidor local:
python app.py

Acesse o sistema no navegador:
http://127.0.0.1:5000

Deploy em Produção:
A aplicação está disponível em ambiente de produção na plataforma Render:
[🔗 Acesse aqui](https://registro-de-produtividade-simplificado.onrender.com/)

Licença:
Uso educacional para fins de demonstração acadêmica.

Autor:
Desenvolvido por Fábio Henrique Costa Ferreira
Aluno do curso de Análise e Desenvolvimento de Sistemas - UNIASSELVI

Este repositório é parte de uma atividade acadêmica e tem como objetivo demonstrar na prática conceitos de desenvolvimento web, banco de dados, versionamento de código e publicação em nuvem.
