# Deploy Sisteped

---

## Reset
Use apenas em caso de conflito de porta, nome ou ambiente quebrado.

```bash
docker-compose down
docker rm -f sisteped_app sisteped_mysql
```

---

## Deploy completo
Primeira execução ou mudanças estruturais.

```bash
docker-compose up --build -d
```

Para apagar o volume de dados: `-v`

---

## Deploy APP

```bash
docker-compose up --build -d app
```

---

## Deploy DATABASE

```bash
docker-compose up --build -d database
```

---

## Verificações

Containers ativos:
```bash
docker ps
```

Logs gerais:
```bash
docker-compose logs -f
```

Logs do app:
```bash
docker logs -f sisteped_app
```
