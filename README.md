# Webdriverを動かす

## コマンド

```bash
docker compose up -d
docker compose exec python3 bash
docker exec -it python3 python opt/main.py
```

```bash
docker rmi -f $(docker images -q)
docker system prune
```

## webdriver

```bash
res=$(curl -X POST -H "Content-Type: application/json" -d '{"capabilities":{}}' http://localhost:9515/session)
```

```bash
sessionId=$(echo $res | jq -r '.value.sessionId')
```

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://www.google.co.jp/"}' "http://localhost:9515/session/$sessionId/url"
```

```bash
curl -X GET -H "Content-Type: application/json" "http://localhost:9515/session/$sessionId/title"
```

```bash
curl -X DELETE -H "Content-Type: application/json" "http://localhost:9515/session/$sessionId"
```
