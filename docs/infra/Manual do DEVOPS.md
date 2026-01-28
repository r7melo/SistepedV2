# Deploy Sisteped

---

## Reset
Use apenas em caso de conflito de porta, nome ou ambiente quebrado.

```bash
docker-compose down
```

Para apagar o volume de dados: `-v`

---

## Deploy completo
Primeira execução ou mudanças estruturais.

```bash
docker-compose up --build -d
```



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
