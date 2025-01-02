### Описание

Приложение **Wallet** позволяет создать кошелёк и проводить с его балансом операции внесения и вывода средств.

### Стек технологий

- Django 3.2
- Django Rest Framework 3.12
- PostgreSQL 13.10

### Запуск приложения

Клонировать репозиторий:
```
git clone git@github.com:Randy-Colt/wallet.git
cd wallet/
```
Запустить контейнеры:
```
docker compose up -d
```

При желании можно удостовериться, что приложение работает корректно, запустив тесты:
```
docker compose exec backend python manage.py test
```

### Параметры приложения

В директории wallet_app находится пример файла окружения с различными параметрами приложения и базы данных. При изменении параметров необходимо сохранить изменения в файле и перезапустить контейнеры:
```
docker compose restart
```

*Значения параметров:*
- SECRET_KEY='*secret_key*' - секретный ключ Django
- DEBUG=False - режим дебага; по умолчанию False
- SQLITE=True - использовать SQLite (True) или PostgreSQL (False)
- DEFAULT_ROUTER=False - использовать DefaultRouter в DRF (True) или нет (False); по умолчанию False
- POSTGRES_DB=wallet - имя базы данных PostgreSQL; по умолчанию 'django'
- POSTGRES_USER=user - имя пользователя PostgreSQL; по умолчанию 'django'
- POSTGRES_PASSWORD=password - пароль PostgreSQL; по умолчанию пустая строка
- DB_HOST=db - хост PostgreSQL; по умолчанию пустая строка
- DB_PORT=5432 - порт PostgreSQL; по умолчанию 5432
- ALLOWED_HOSTS=... - доступные хосты для Django; по умолчанию 'localhost, 127.0.0.1'

### Примеры запросов

1. Создать кошелёк.
request POST:
```
http://127.0.0.1:8000/api/v1/wallets/
```
response:
```
{
    "id": "fa79d4ca-1d84-4bc1-8ad1-e7f3dd6786d5",
    "balance": 0.0
}
```

2. Получить баланс кошелька.
request GET:
```
http://127.0.0.1:8000/api/v1/wallets/{WALLET_UUID}/
```
response:
```
{
    "id": "fa79d4ca-1d84-4bc1-8ad1-e7f3dd6786d5",
    "balance": 0.0
}
```

3. Внести средства.
request POST:
```
http://127.0.0.1:8000/api/v1/wallets/{WALLET_UUID}/operation/
```
request data:
```
{
    "operationType": "DEPOSIT",
    "amount": 1000
}
```
respone:
```
{
    "operationType": "DEPOSIT",
    "amount": 1000.0,
    "balance": 1000.0
}
```

4. Вывести средства.
request POST:
```
http://127.0.0.1:8000/api/v1/wallets/{WALLET_UUID}/operation/
```
request data:
```
{
    "operationType": "WITHDRAW",
    "amount": 1000
}
```
respone:
```
{
    "operationType": "WITHDRAW",
    "amount": 1000.0,
    "balance": 0.0
}
```
