# Дипломная работа к профессии Python-разработчик «API Сервис заказа товаров для розничных сетей».

## Описание

Приложение предназначено для автоматизации закупок в розничной сети. Пользователи сервиса — покупатель (менеджер торговой сети, который закупает товары для продажи в магазине) и поставщик товаров.

**Клиент (покупатель):**

- Менеджер закупок через API делает ежедневные закупки по каталогу, в котором
  представлены товары от нескольких поставщиков.
- В одном заказе можно указать товары от разных поставщиков — это
  повлияет на стоимость доставки.
- Пользователь может авторизироваться, регистрироваться и восстанавливать пароль через API.
    
**Поставщик:**

- Через API информирует сервис об обновлении прайса.
- Может включать и отключать прием заказов.
- Может получать список оформленных заказов (с товарами из его прайса).
- 

## Installation
Скопировать данный репозиторий

Создать и активировать виртуальное окружение Python.

Установить зависимости из файла **requirements.txt**:
```bash
pip3 install -r requirements.txt
```
* Команды для запуска redis:
```bash
# установка пакета для python
pip3 install redis
# установка самого Redis (Ubuntu-like OS)
sudo apt-get install redis
# проверка работы сервиса
sudo systemctl status redis-server.service
# если не активен, то запускаем службу:
sudo systemctl start redis-server.service
# либо как отдельного демона в терминале:
redis-server
```

* Команда для запуска celery:
```bash
python3 -m celery -A diploma worker
```
* Настроить подключение к БД в diploma/settings.py
* Команда для создания миграций приложения для базы данных
```bash
python manage.py makemigrations
python manage.py migrate
```
* Команда для запуска сервера:
```bash
python manage.py runserver
```
### Приложение будет доступно по адресу: http://127.0.0.1:8000/

### Для контроля отправки электронных писем можно использовать MailHog (https://github.com/mailhog/MailHog.git) 
