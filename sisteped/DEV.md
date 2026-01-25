# Guia do Desenvolvedo

## 1. Versão do Python

Obrigatório: **Python 3.12.10**

Verificação:
```
python --version
```

---

## 2. Criação do Ambiente Virtual

### Windows
```
py -3.12 -m venv venv
```

### Linux / Mac
```
py -3.12  -m venv venv
```

---

## 3. Ativação do Ambiente

### Windows
```
.\venv\Scripts\activate
```

### Linux / Mac
```
source venv/bin/activate
```

---

## 4. Atualização do Pip

Obrigatório após criar o venv:
```
python -m pip install --upgrade pip
```

---

## 5. Instalação das Dependências

```
pip install -r requirements.txt
```

---

## 6. Execução do Projeto (Desenvolvimento)

```
python run.py --dev
```

0BS: Verificar o **config.db_host** se está de acordo com o ambiente.
- Windows: `host.docker.internal`
- Linux: `localhost`

---

## 7. Instalação de Novas Bibliotecas

Sempre com o ambiente virtual ativo:
```
pip install nome-da-biblioteca
```

Após instalar, **atualizar os requisitos**:
```
pip freeze > requirements.txt
```

---

## 8. Atualização de Bibliotecas Existentes

```
pip install --upgrade nome-da-biblioteca
pip freeze > requirements.txt
```

## 9. Configuração com Docker


Build da Imagem Docker

```
docker build -t sisteped_app .
```
Rodar o Container

- Windows/Mac
    ```
    docker run -d --name sisteped -p 5000:5000 sisteped_app
    ```
- Linux:
    ```
    docker run -d --name sisteped --network host sisteped_app
    ```

Remove o Container

```
docker rm -f sisteped
```

## 10. Configuração com Docker (Servidor)

Compactar imagem (Local)

```
docker save -o sisteped_app.tar sisteped_app
```

Enviar para o servidor (Local)
```
scp sisteped_app.tar USER@IP-SERVER:PATH
```

Carregar imagem (Server)

```
docker load -i sisteped_app.tar
```

Rodar conteiner
```
docker run -d --name sisteped --network host sisteped_app
```

Monitorar
```
docker logs sisteped --tail 50
```