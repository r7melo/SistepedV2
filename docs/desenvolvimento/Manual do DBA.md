# MANUAL DO ADMINISTRADOR DE BANCO DE DADOS (DBA) - SISTEPED

Este documento descreve a configuração, inicialização e manutenção 
do banco de dados MySQL utilizando Docker.

## 1. ESTRUTURA DE ARQUIVOS

```
database/
├── docker-compose.yml   # Definição do container e volumes
└── init.sql             # Script SQL executado apenas na 1ª criação
```

## 2. TECNOLOGIAS E VERSÕES

- Sistema: MySQL Server
- Versão: 8.0 (Imagem Docker: mysql:8.0)
- Orquestrador: Docker Compose

## 3. CREDENCIAIS DE ACESSO

Para conectar:

- **HOST:** localhost
- **PORTA:** 3306
- **DATABASE:** sisteped
- **USUÁRIO:** root
- **SENHA:** DB!pass00

## 4. COMO INICIAR O BANCO

Para subir o banco de dados em segundo plano (modo detached):

1. Abra o terminal na pasta 'database'.
2. Execute:

```
docker-compose up -d
```

3. Aguarde cerca de 10 a 20 segundos para a inicialização completa.

## 5. COMO PARAR O BANCO

Para parar o serviço mantendo os dados salvos:

```
docker-compose down
```

## 6. COMO RESETAR O BANCO 

**ATENÇÃO:** Este procedimento apaga TODOS os dados cadastrados e 
recria as tabelas do zero usando o script 'init.sql'.

1. Derrube o container e apague os volumes:

```
docker-compose down -v
```

2. Suba novamente:

```
docker-compose up -d
```

## 7. ACESSO VIA TERMINAL

Para executar comandos SQL diretamente pelo terminal do container:

1. Acesse o shell do MySQL:

```
docker exec -it sisteped_mysql mysql -u root -p
```

2. Digite a senha: `DB!pass00`
3. Selecione o banco:

```
USE sisteped;
```

4. Exemplo de teste:

```
SHOW TABLES;
```

## 8. RESOLUÇÃO DE PROBLEMAS

Se o banco não iniciar, verifique os logs de erro:

```
docker-compose logs -f
```

## 9. Configuração com Docker (Servidor)

Compactar imagem (Local)

```
docker save -o sisteped_db.tar sisteped_db
```

Enviar para o servidor (Local)
```
scp sisteped_db.tar USER@IP-SERVER:PATH
```

Carregar imagem (Server)

```
docker load -i sisteped_db.tar
```

Executar imagem (Server)

```
docker load -i sisteped_db.tar
```