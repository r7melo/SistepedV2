# DOCUMENTAÇÃO TÉCNICA – MÓDULOS E SERVIÇOS  

Este documento descreve de forma detalhada os **módulos de rotas (controllers)** e a **camada de serviços (lógica de negócio)** do Sisteped, explicitando responsabilidades, fluxos e garantias de segurança e integridade dos dados.

---

## 1. Módulos de Rotas (Controllers)

Os **Controllers** constituem a camada de interface entre o utilizador e o sistema.  
São responsáveis por:
- Receber requisições HTTP
- Validar sessão e permissões
- Orquestrar chamadas à camada de serviços
- Preparar dados para renderização das views ou respostas de API

Nenhuma regra de negócio ou acesso direto ao banco ocorre nesta camada.

---

## 1.1 Módulo de Alunos (`src/routes/alunos.py`)
Gerencia o ciclo de vida completo dos estudantes no sistema.

### **index**
- Verifica se o professor está autenticado.
- Solicita ao `aluno_service.listar_alunos` todos os alunos acessíveis.
- Renderiza a lista de alunos agrupada por turma.
- Garante que apenas alunos vinculados ao professor sejam exibidos.

### **cadastrar_aluno**
- Método GET:
  - Carrega formulário de cadastro.
  - Solicita ao `turma_service.listar_turmas` as turmas disponíveis.
- Método POST:
  - Recebe dados biográficos, filiação e contactos.
  - Valida campos obrigatórios.
  - Encaminha os dados para `aluno_service.criar_aluno`.
  - Redireciona após sucesso ou exibe erros de validação.

### **editar_aluno**
- Método GET:
  - Recupera o aluno via `aluno_service.obter_aluno_por_id`.
  - Pré-preenche formulário com dados atuais.
- Método POST:
  - Recebe alterações nos dados biográficos e de contacto.
  - Encaminha para `aluno_service.atualizar_aluno`.
  - Mantém integridade entre tabelas relacionadas.

### **excluir_aluno**
- Recebe o identificador do aluno.
- Solicita exclusão ao `aluno_service.deletar_aluno`.
- Garante que o aluno pertence a uma turma do professor.
- Remove todos os dados dependentes antes do registo principal.

### **importar_csv**
- Recebe ficheiro CSV via upload.
- Valida formato e estrutura mínima.
- Encaminha o ficheiro para `aluno_service.cadastrar_alunos_em_lote`.
- Retorna feedback de sucesso ou falhas por linha.

### **api_alunos_por_turma**
- Endpoint REST utilizado por componentes dinâmicos.
- Recebe `id_turma`.
- Valida permissão do professor.
- Retorna JSON com `idAluno` e `nomeCompleto`.

---

## 1.2 Módulo de Autenticação (`src/routes/auth.py`)
Responsável pelo controle de acesso e sessões.

### **index**
- Rota raiz do sistema.
- Verifica se existe sessão ativa.
- Redireciona para:
  - Dashboard (gráficos) se autenticado
  - Login caso contrário

### **login**
- Método GET:
  - Renderiza formulário de login.
- Método POST:
  - Recebe e-mail e senha.
  - Encaminha para `auth_service.validar_usuario`.
  - Cria sessão (`user_id`, `user_name`) se válido.
  - Retorna erro se credenciais forem inválidas.

### **register**
- Método GET:
  - Exibe formulário de criação de conta.
- Método POST:
  - Valida confirmação de senha.
  - Encaminha dados para `auth_service.criar_usuario`.
  - Impede duplicidade de e-mail.

### **logout**
- Limpa completamente a sessão.
- Remove dados temporários de navegação.
- Redireciona para login.

---

## 1.3 Módulo de Comportamento (`src/routes/comportamento.py`)
Registo qualitativo da conduta dos alunos.

### **index**
- Solicita ao `comportamento_service.listar_comportamentos_professor`.
- Exibe histórico de ocorrências.
- Permite filtragem por aluno ou tag.

### **cadastrar**
- Recebe dados do formulário:
  - Aluno
  - Tag
  - Observação
- Valida vínculo aluno–professor.
- Encaminha para `comportamento_service.salvar_comportamento`.

### **excluir**
- Recebe identificador do comportamento.
- Solicita exclusão segura via `excluir_comportamento_seguro`.
- Impede remoção de registos de outros professores.

---

## 1.4 Módulo de Disciplinas (`src/routes/disciplinas.py`)
Gestão das matérias lecionadas.

### **index**
- Solicita ao `disciplina_service.listar_disciplinas_por_professor`.
- Renderiza lista de disciplinas ativas.

### **cadastrar**
- Recebe nome da disciplina.
- Encaminha para `criar_disciplina_com_vinculo`.
- Associa automaticamente ao professor logado.

### **excluir**
- Recebe identificador da disciplina.
- Remove o vínculo de forma segura.
- Garante que a disciplina pertence ao professor.

---

## 1.5 Módulo de Gráficos (`src/routes/graficos.py`)
Camada de visualização analítica.

### **index**
- Renderiza o dashboard principal.
- Inicializa gráficos de desempenho e comportamento.

### **api_comportamento**
- Retorna estatísticas de ocorrências disciplinares.
- Utiliza `graficos_service.obter_resumo_comportamento`.

### **api_timeline**
- Retorna evolução temporal das médias.
- Baseado em `obter_timeline_notas`.

### **api_disciplinas**
- Retorna médias comparativas por disciplina.
- Utiliza `obter_medias_disciplinas`.

### **api_distribuicao**
- Retorna distribuição de notas por faixas.
- Utiliza `obter_distribuicao_notas`.

---

## 1.6 Módulo de Notas (`src/routes/notas.py`)
Gestão do desempenho académico.

### **index**
- Lista todas as avaliações acessíveis.
- Formata o campo `conteudo` separando atividade e disciplina.

### **cadastrar_notas**
- Método GET:
  - Carrega turmas e disciplinas.
- Método POST:
  - Itera sobre notas submetidas.
  - Encaminha cada registo para `salvar_avaliacao`.

### **atualizar_individual**
- Endpoint para edição rápida via modal.
- Atualiza apenas o valor da nota.

### **excluir_individual**
- Remove um único registo de avaliação.
- Não afeta outros dados do aluno.

---

## 1.7 Módulo de Relatórios (`src/routes/relatorios.py`)
Extração e exportação de dados.

### **index**
- Lista modelos de relatórios disponíveis.
- Exibe relatórios previamente gerados.

### **exportar**
- Recebe filtros:
  - Turma
  - Disciplina
  - Intervalo de datas
- Encaminha consulta para `relatorios_service.buscar_dados_notas`.
- Retorna ficheiro CSV ou PDF.

---

## 1.8 Módulo de Turmas (`src/routes/turmas.py`)
Organização das unidades de ensino.

### **index**
- Lista turmas do professor logado.
- Baseado no vínculo `ProfessorTurma`.

### **cadastrar_turma**
- Recebe nome e ano letivo.
- Cria turma via `criar_turma`.
- Estabelece vínculo automático com o professor.

### **editar_turma**
- Permite alterar nome e ano letivo.
- Valida propriedade da turma.

### **excluir_turma**
- Remove a turma do sistema.
- Garante que apenas o professor proprietário possa excluí-la.

---


## 2. Camada de Serviços (Lógica de Negócio)

A camada de serviços concentra **toda a regra de negócio**, validações, integridade referencial e controle de acesso aos dados.  
Nenhuma rota acessa o banco diretamente: todas as operações passam por esta camada.

---

### 2.1 `aluno_service.py`
Responsável pela manipulação completa dos dados dos estudantes.

- **criar_aluno(dados_aluno, contatos, id_turma)**  
  Insere um novo aluno na tabela `Aluno`.  
  - Concatena nome do pai e da mãe no campo `filiacao`.  
  - Associa o aluno a uma turma específica.  
  - Insere registos na tabela `Contato`, se fornecidos.  
  - Garante unicidade de CPF por turma.

- **listar_alunos(id_professor)**  
  Retorna todos os alunos acessíveis ao professor logado.  
  - Executa JOIN entre `Aluno`, `Turma` e `ProfessorTurma`.  
  - Impede visualização de alunos fora da permissão do docente.

- **obter_aluno_por_id(id_aluno, id_professor)**  
  Recupera os dados completos de um aluno.  
  - Valida se o aluno pertence a uma turma do professor.  
  - Separa o campo `filiacao` em pai/mãe para edição.  
  - Retorna contactos e metadados da turma.

- **atualizar_aluno(id_aluno, novos_dados, contatos)**  
  Atualiza dados biográficos do aluno.  
  - Gerencia atualização ou inserção de novos contactos.  
  - Mantém consistência entre tabelas relacionadas.

- **deletar_aluno(id_aluno, id_professor)**  
  Remove o aluno de forma segura.  
  - Executa exclusão manual em cascata:
    - Contactos  
    - Avaliações  
    - Registos de comportamento  
  - Remove o aluno apenas se pertencer ao professor.

- **cadastrar_alunos_em_lote(arquivo_csv, id_turma)**  
  Processa ficheiros CSV para cadastro massivo.  
  - Valida estrutura do ficheiro.  
  - Itera linha a linha chamando `criar_aluno`.  
  - Ignora ou reporta registos inválidos.

---

### 2.2 `auth_service.py`
Centraliza autenticação e segurança.

- **criar_usuario(nome, email, senha)**  
  Cria um novo professor.  
  - Verifica duplicidade de e-mail.  
  - Gera hash seguro da senha (`werkzeug.security`).  
  - Insere o registo na tabela `Professor`.

- **validar_usuario(email, senha)**  
  Autentica o login.  
  - Busca o professor pelo e-mail.  
  - Compara senha informada com o hash armazenado.  
  - Retorna dados mínimos para criação da sessão.

---

### 2.3 `turma_service.py`
Gerencia turmas e permissões.

- **listar_turmas(id_professor)**  
  Retorna apenas as turmas associadas ao professor.  
  - Baseado na tabela `ProfessorTurma`.

- **criar_turma(nome, ano_letivo, id_professor)**  
  Cria uma nova turma.  
  - Insere na tabela `Turma`.  
  - Cria automaticamente o vínculo em `ProfessorTurma`.  
  - Executa ambas operações numa única transação.

- **obter_turma_por_id(id_turma, id_professor)**  
  Recupera dados da turma validando propriedade.  
  - Impede acesso a turmas não pertencentes ao professor.

- **atualizar_turma(id_turma, novos_dados)**  
  Atualiza nome e ano letivo da turma.

- **deletar_turma(id_turma, id_professor)**  
  Remove a turma com segurança.  
  - Exclui primeiro o vínculo em `ProfessorTurma`.  
  - Remove a turma da tabela principal.

---

### 2.4 `notas_service.py`
Controla o registo e cálculo de desempenho académico.

- **listar_notas(id_professor)**  
  Retorna o histórico de avaliações acessíveis ao professor.  
  - Filtra por turmas vinculadas.

- **listar_alunos_por_turma(id_turma, id_professor)**  
  Retorna alunos de uma turma específica.  
  - Valida o acesso do professor à turma.

- **salvar_avaliacao(id_aluno, nota, titulo, disciplina, data)**  
  Insere uma nova avaliação.  
  - Formata o campo `conteudo` como:  
    `Título (Disciplina)`.

- **atualizar_nota_individual(id_avaliacao, nova_nota)**  
  Atualiza apenas o valor da nota.

- **remover_nota_individual(id_avaliacao)**  
  Remove um único registo de avaliação.

- **listar_alunos_notas(id_professor)**  
  Retorna alunos, turmas e notas para visualização consolidada.

---

### 2.5 `comportamento_service.py`
Registo qualitativo disciplinar.

- **salvar_comportamento(id_aluno, tag, observacao, id_professor)**  
  Regista uma ocorrência comportamental.  
  - Valida vínculo aluno–professor.

- **excluir_comportamento_seguro(id_comportamento, id_professor)**  
  Remove um registo garantindo permissão.

- **listar_comportamentos_professor(id_professor)**  
  Retorna o histórico de ocorrências do docente.

- **listar_tags_distintas_professor(id_professor)**  
  Recupera todas as tags usadas pelo professor.

---

### 2.6 `disciplina_service.py`
Gestão das disciplinas lecionadas.

- **listar_disciplinas_por_professor(id_professor)**  
  Retorna disciplinas vinculadas ao professor.

- **criar_disciplina_com_vinculo(nome_disciplina, id_professor)**  
  Cria a disciplina e associa automaticamente ao docente.

- **deletar_disciplina_seguro(id_disciplina, id_professor)**  
  Remove a disciplina validando propriedade.

---

### 2.7 `graficos_service.py`
Processamento estatístico para dashboards.

- **obter_resumo_comportamento(id_professor)**  
  Gera estatísticas de ocorrências por tag.

- **obter_timeline_notas(id_professor)**  
  Processa evolução temporal das médias.

- **obter_medias_disciplinas(id_professor)**  
  Calcula médias por disciplina.

- **obter_distribuicao_notas(id_professor)**  
  Analisa concentração de notas por faixas.

---

### 2.8 `relatorios_service.py`
Extração avançada de dados.

- **buscar_dados_notas(filtros)**  
  Executa consultas complexas com filtros por:
  - Turma  
  - Disciplina  
  - Intervalo de datas  
  Retorna dados estruturados para CSV ou PDF.

---

### 2.9 `db.py`
Infraestrutura de persistência.

- **get_db_connection()**  
  Cria e retorna uma conexão ativa com o MySQL.  
  - Utiliza configurações do sistema (JSON ou variáveis de ambiente).  
  - Centraliza a gestão de conexões do projeto.

---