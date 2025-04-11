# Bonus Service

Гибкий микросервис для расчёта бонусов с применением правил.
Chain of Responsibility и расширяемой архитектурой (Hexagonal, DI).

---

## Cтарт

```bash
# Клонировать репозиторий
git clone https://github.com/koroteevdmitry/bonus
cd bonus-service

# Запустить сервис
docker-compose up --build

После этого, сервис будет доступен по адресу http://0.0.0.0:8000/docs