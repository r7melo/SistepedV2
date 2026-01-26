# Documentação Técnica — SISTEPED (Gestão Pedagógica)

---

## 1. Arquitetura do Sistema

### 1.1 Arquitetura Lógica

O **Sisteped** utiliza uma arquitetura de **Server-Side Rendering (SSR)**, organizada em camadas para separar interface, regras de negócio e persistência de dados.  
A modularização é feita com **Blueprints do Flask**, permitindo evolução e manutenção independentes.

### Estrutura de Diretórios

```
sisteped/
├── run.py                  # Ponto de entrada e seletor de ambiente
└── src/
    ├── routes/             # Rotas e controladores HTTP
    ├── services/           # Lógica de negócio e acesso ao SQL
    ├── templates/          # Templates HTML (Jinja2)
    ├── static/             # CSS e JavaScript
    └── main.py             # Configuração da aplicação
```

---

### 1.2 Descrição das Camadas

- **Apresentação (Routes)**  
  Recebe requisições HTTP, valida sessões e renderiza páginas.

- **Aplicação (Services)**  
  Implementa regras de negócio como cálculo de médias e validações pedagógicas.

- **Infraestrutura (DB)**  
  Gerencia a conexão com o **MySQL 8.0** via variáveis de ambiente ou JSON.

---

## 2. Tecnologias Utilizadas

- **Linguagem:** Python 3.12.10  
- **Framework:** Flask 3.1.2  
- **Banco de Dados:** MySQL 8.0  

### Bibliotecas

- mysql-connector-python  
- Werkzeug  
- Chart.js  
- Gunicorn  

---

## 3. Padrões e Convenções

### 3.1 Codificação

- snake_case para funções e variáveis  
- Senhas com hash criptográfico (PBKDF2)  
- Sessões protegidas por chave secreta SHA-256  

### 3.2 Design

- **Service Layer:** SQL isolado das rotas  
- **Template Inheritance:** base.html para padronização visual  

---

## 4. Estrutura de Dados

- **Professor:** id, nome, e-mail, hash da senha  
- **Aluno:** CPF, filiação, dados pessoais  
- **Turma:** identificação e ano letivo  
- **Avaliação:** notas, conteúdos e datas  
- **ProfessorTurma:** vínculo professor–turma  

---

## 5. Funcionalidades

### 5.1 Gestão de Alunos (/alunos)

- Cadastro com validação de CPF  
- Edição e remoção segura  

### 5.2 Lançamento de Notas (/notas)

- Lançamento em massa  
- Histórico individual  
- Indicadores visuais de desempenho  

### 5.3 Monitorização (/graficos)

- Dashboard com médias mensais  
- Identificação de alunos em risco  

---

## 6. Deploy e Implantação

### 6.1 Docker

```
docker-compose up --build -d
```

A aplicação ficará disponível em:  
http://localhost:5000

### 6.2 Manutenção

**Reset completo**
```
docker-compose down -v
```

**Logs**
```
docker logs -f sisteped_app
```
