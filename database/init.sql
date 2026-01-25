CREATE DATABASE IF NOT EXISTS sisteped;
USE sisteped;

-- ============================
-- USERS
-- ============================
CREATE TABLE IF NOT EXISTS Users (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(150) NOT NULL,
    Email VARCHAR(150) NOT NULL UNIQUE,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NULL
);

-- ============================
-- USER CREDENTIALS
-- ============================
CREATE TABLE IF NOT EXISTS UserCredentials (
    UserId INT PRIMARY KEY,
    PasswordHash VARCHAR(255) NOT NULL,
    Role VARCHAR(50) NOT NULL DEFAULT 'User',
    CONSTRAINT FK_UserCredentials_Users
        FOREIGN KEY (UserId)
        REFERENCES Users(Id)
        ON DELETE CASCADE
);

-- ============================
-- ESCOLA
-- ============================
CREATE TABLE IF NOT EXISTS Escola (
    idEscola INT AUTO_INCREMENT PRIMARY KEY,
    instituicaoEscolar VARCHAR(255) NOT NULL,
    entidadeMantenedora VARCHAR(255),
    numeroReconhecimento VARCHAR(100)
);

-- ============================
-- PROFESSOR
-- ============================
CREATE TABLE IF NOT EXISTS Professor (
    idProfessor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    senha VARCHAR(255) NOT NULL
);

-- ============================
-- DISCIPLINA
-- ============================
CREATE TABLE IF NOT EXISTS Disciplina (
    idDisciplina INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- ============================
-- TURMA
-- ============================
CREATE TABLE IF NOT EXISTS Turma (
    idTurma INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    anoLetivo VARCHAR(20),
    idEscola INT NOT NULL,
    CONSTRAINT FK_Turma_Escola
        FOREIGN KEY (idEscola)
        REFERENCES Escola(idEscola)
);

-- ============================
-- ALUNO
-- ============================
CREATE TABLE IF NOT EXISTS Aluno (
    idAluno INT AUTO_INCREMENT PRIMARY KEY,
    nomeCompleto VARCHAR(255) NOT NULL,
    dataNascimento DATE,
    filiacao VARCHAR(255),
    naturalidade VARCHAR(100),
    nacionalidade VARCHAR(100),
    identidade VARCHAR(50),
    cpf VARCHAR(14) UNIQUE,
    idTurma INT NULL,
    CONSTRAINT FK_Aluno_Turma
        FOREIGN KEY (idTurma)
        REFERENCES Turma(idTurma)
);

-- ============================
-- ENDERECO
-- ============================
CREATE TABLE IF NOT EXISTS Endereco (
    idEndereco INT AUTO_INCREMENT PRIMARY KEY,
    rua VARCHAR(255),
    numero VARCHAR(20),
    cidade VARCHAR(100),
    bairro VARCHAR(100),
    idAluno INT NOT NULL,
    CONSTRAINT FK_Endereco_Aluno
        FOREIGN KEY (idAluno)
        REFERENCES Aluno(idAluno)
);

-- ============================
-- CONTATO
-- ============================
CREATE TABLE IF NOT EXISTS Contato (
    idContato INT AUTO_INCREMENT PRIMARY KEY,
    telefone VARCHAR(20),
    email VARCHAR(255),
    idAluno INT NOT NULL,
    CONSTRAINT FK_Contato_Aluno
        FOREIGN KEY (idAluno)
        REFERENCES Aluno(idAluno)
);

-- ============================
-- AVALIACAO
-- ============================
CREATE TABLE IF NOT EXISTS Avaliacao (
    idAvaliacao INT AUTO_INCREMENT PRIMARY KEY,
    conteudo VARCHAR(255),
    nota DECIMAL(5,2),
    data DATE,
    tipo VARCHAR(50),
    idAluno INT NOT NULL,
    CONSTRAINT FK_Avaliacao_Aluno
        FOREIGN KEY (idAluno)
        REFERENCES Aluno(idAluno)
);

-- ============================
-- COMPORTAMENTO
-- ============================
CREATE TABLE IF NOT EXISTS Comportamento (
    idComportamento INT AUTO_INCREMENT PRIMARY KEY,
    tag VARCHAR(50),
    data DATE,
    observacao TEXT, -- TEXT equivale ao VARCHAR(MAX)
    idAluno INT NOT NULL,
    CONSTRAINT FK_Comportamento_Aluno
        FOREIGN KEY (idAluno)
        REFERENCES Aluno(idAluno)
);

-- ============================
-- PROFESSOR_TURMA
-- ============================
CREATE TABLE IF NOT EXISTS ProfessorTurma (
    idProfessor INT NOT NULL,
    idTurma INT NOT NULL,
    PRIMARY KEY (idProfessor, idTurma),
    CONSTRAINT FK_ProfessorTurma_Professor
        FOREIGN KEY (idProfessor)
        REFERENCES Professor(idProfessor),
    CONSTRAINT FK_ProfessorTurma_Turma
        FOREIGN KEY (idTurma)
        REFERENCES Turma(idTurma)
);

-- ============================
-- PROFESSOR_DISCIPLINA
-- ============================
CREATE TABLE IF NOT EXISTS ProfessorDisciplina (
    idProfessor INT NOT NULL,
    idDisciplina INT NOT NULL,
    PRIMARY KEY (idProfessor, idDisciplina),
    CONSTRAINT FK_ProfessorDisciplina_Professor
        FOREIGN KEY (idProfessor)
        REFERENCES Professor(idProfessor),
    CONSTRAINT FK_ProfessorDisciplina_Disciplina
        FOREIGN KEY (idDisciplina)
        REFERENCES Disciplina(idDisciplina)
);
