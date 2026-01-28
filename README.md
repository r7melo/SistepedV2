# SISTEPED — Sistema de Gestão Pedagógica

## 1. Descrição do Projeto

O **SISTEPED** é um sistema de gestão pedagógica voltado para professores, com foco
no acompanhamento de turmas, alunos, avaliações e indicadores de desempenho.  
Seu objetivo central é oferecer uma visão estruturada e confiável da evolução
pedagógica por conteúdo, apoiando a tomada de decisões no processo de ensino.

---

## 2. Arquitetura do Sistema

O Sisteped utiliza uma arquitetura baseada em **micro-serviços containerizados**
em conjunto com o padrão **MVC (Model-View-Controller)**, adaptado ao framework Flask.

- **Camada de Visão (View):**  
  Templates HTML renderizados no lado do servidor utilizando **Jinja2**.

- **Camada de Controle (Controller):**  
  Rotas organizadas em **Blueprints**, responsáveis por gerenciar as requisições HTTP.

- **Camada de Serviço (Service):**  
  Lógica de negócio e persistência de dados isoladas das rotas, promovendo separação
  de responsabilidades.

- **Banco de Dados (Database):**  
  MySQL, utilizado para persistência relacional dos dados.

---

## 3. Tecnologias Utilizadas

- **Linguagem / Backend:** Python 3.12.10  
- **Framework Web:** Flask 3.1.2  
- **Frontend:** HTML5, CSS3 (customizado) e JavaScript (Vanilla)  
- **Banco de Dados:** MySQL 8.0  
- **Servidor WSGI:** Gunicorn (ambiente de produção)  
- **Infraestrutura:** Docker e Docker Compose  

---

## 4. Padrões e Convenções

- **Nomenclatura:**  
  Funções e variáveis seguem o padrão `snake_case`, conforme a PEP 8.

- **Organização de Rotas:**  
  Uso de **Blueprints** para modularização por domínio funcional  
  (Disciplina, Turmas, Alunos, Notas e Comportamento).

- **Segurança:**  
  Criptografia de senhas utilizando `generate_password_hash` e validação com
  `check_password_hash` da biblioteca **Werkzeug**.

- **Isolamento de Dados:**  
  Todas as consultas SQL são filtradas obrigatoriamente pelo `idProfessor`
  presente na sessão, garantindo privacidade entre usuários.

---

## 5. Estrutura do Código

```text
/sisteped
 ├── run.py          # Script de entrada da aplicação
 └── src/
     ├── main.py     # Configuração do Flask e registro dos Blueprints
     ├── routes/     # Definição dos endpoints HTTP
     ├── services/   # Lógica de negócio e acesso ao MySQL
     ├── static/     # Arquivos estáticos (CSS, JS, imagens)
     └── templates/  # Templates HTML (Jinja2)
```

---

## 6. Instalação e Execução (Docker)

A aplicação é totalmente containerizada, garantindo consistência entre os
ambientes de desenvolvimento e produção.

### Passos

1. Certifique-se de ter **Docker** e **Docker Compose** instalados  
2. Na raiz do projeto, execute:

   ```bash
   docker-compose up --build -d
   ```

3. Acesse a aplicação em:  
   http://localhost:5000

---

## 7. Configuração do Banco de Dados

- **Host:** localhost (porta 3306)  
- **Usuário:** root  
- **Senha:** DB!pass00  
- **Banco:** sisteped  

A persistência é garantida através de volumes Docker (`mysql_data`), evitando
perda de dados em reinicializações dos containers.

---

## 8. Deploy

O deploy é realizado via **Docker**, assegurando que o ambiente de produção seja
idêntico ao de desenvolvimento.

- Variáveis de ambiente (`DB_HOST`, `DB_USER`, `DB_PASSWORD`) são injetadas no
  container da aplicação para conexão segura com o banco de dados.

## 9. Documentação do Projeto

O repositório contém documentação complementar essencial para compreensão,
manutenção e evolução do sistema. Localiza-se na pasta `docs/` na raiz do projeto.

### `docs/database/`

Esta pasta concentra **todo o projeto da base de dados**, incluindo:

- Modelo relacional completo do sistema  
- **Diagrama Entidade–Relacionamento (DER)**  
- Scripts SQL de criação, relacionamento e integridade  
- Definição de chaves primárias, estrangeiras e regras de consistência  

Ela serve como referência única para qualquer alteração ou auditoria estrutural
no banco de dados.

### `docs/projeto/`

A pasta de projeto contém a **documentação lógica e funcional do sistema**, sendo
o principal guia para desenvolvedores.

Nela encontram-se:

- **Documentação técnica** do sistema
- **Casos de uso** do sistema  
- **Diagramas de Caso de Uso**, descrevendo interações entre usuários e sistema  
- Regras de negócio e fluxos principais  
- Base conceitual necessária para implementar novas funcionalidades ou refatorar
  módulos existentes  

### `docs/design/`

Esta pasta concentra a parte de **design e experiência do usuário**, contendo:

- **Protótipos de interface**  
- Especificações visuais e estruturais  
- Diretrizes de layout e organização das telas  

Ela define como o projeto deve se apresentar visualmente e garante consistência
entre implementação e concepção original.

### `docs/desenvolvimento/`

Esta pasta contém os manuais excenciais para desenvolvimento do projeto.

- **Manual do DBA**: regras importantes sobre o desenvolvimento da base de dados
- **Manual do DEV**: regras importantes sober o desenvolvimento do projeto

### `docs/infra/`

Esta pasta contém o manual excencial para o deploy.

- **Manual do DEVOPS**: regras importantes para o gerenciamento dos deploys e monitoramento
