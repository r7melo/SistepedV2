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
