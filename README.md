# bttc

## Локальный запуск проекта:

Для запуска контейнеров нужно переименовать файл .env.docker в .env
(см. '.env.example')

Запуск контейнеров.
```
docker compose up
```

При первом запуске нужно выполнить миграции и собрать статику.
```
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic
```