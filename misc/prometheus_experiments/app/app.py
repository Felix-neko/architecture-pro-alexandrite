# Импортируем модуль random для генерации случайных чисел
import random
# Импортируем модуль time для работы с временными метками и задержками
import time

# Импортируем основной класс Flask для создания веб-приложения
# и объект request для доступа к данным HTTP-запроса
from flask import Flask, request
# Импортируем Histogram для создания гистограммы метрик времени выполнения
# и make_wsgi_app для создания WSGI-приложения, которое отдает метрики
from prometheus_client import Histogram, make_wsgi_app
# Импортируем Response для создания HTTP-ответов с кастомными параметрами
from werkzeug import Response
# Импортируем DispatcherMiddleware для объединения нескольких WSGI-приложений
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Создаем экземпляр Flask-приложения
app = Flask(__name__)
# Оборачиваем основное приложение в DispatcherMiddleware, чтобы:
# - основное приложение обрабатывало все запросы, кроме /metrics
# - запросы к /metrics обрабатывались отдельным WSGI-приложением Prometheus
app.wsgi_app = DispatcherMiddleware(
    app.wsgi_app, {"/metrics": make_wsgi_app()}
)

# Создаем гистограмму для измерения времени выполнения HTTP-запросов
HTTP_REQUEST_DURATION = Histogram(
    # Имя метрики в Prometheus
    "http_request_duration",
    # Описание метрики для документации
    "Requests durations",
    # Лейблы (теги) для группировки метрик по методу, URL и коду ответа
    ["method", "url", "code"],
    # Границы бакетов для гистограммы (в секундах):
    # 0.01с, 0.1с, 0.5с, 2с, бесконечность
    buckets=[0.01, 0.1, 0.5, 2, float("inf")],
)

# Определяем декоратор для автоматического измерения времени выполнения функций
def observe_http(func):
    # Внутренняя функция-обертка, которая заменит оригинальную функцию
    def wrapper(*args, **kwargs):
        # Запоминаем время начала выполнения функции
        start = time.time()
        # Вызываем оригинальную функцию и сохраняем её результат
        response = func(*args, **kwargs)
        # Запоминаем время окончания выполнения функции
        end = time.time()
        # Записываем измерение в гистограмму с соответствующими лейблами:
        HTTP_REQUEST_DURATION.labels(
            method=request.method,      # HTTP-метод (GET, POST, etc.)
            code=response.status_code,  # HTTP-код ответа (200, 404, etc.)
            url=request.url,           # Полный URL запроса
        ).observe(end - start)         # Время выполнения в секундах
        # Возвращаем оригинальный ответ функции
        return response
    # Возвращаем функцию-обертку
    return wrapper

# Определяем маршрут для корневого пути "/"
@app.route("/")
# Также определяем маршрут для "/health" (та же функция обработает оба пути)
@app.route("/health")
def check_health():
    # Возвращаем простое текстовое сообщение о том, что сервис работает
    return "I am still alive!"

# Определяем маршрут для "/rand_metrics"
@app.route("/rand_metrics")
# Применяем декоратор для измерения времени выполнения этой функции
@observe_http
def random_metric():
    # Генерируем случайную задержку от 1 до 50 миллисекунд
    # random.randint(1, 50) дает число от 1 до 50
    # умножение на 0.001 переводит миллисекунды в секунды
    random_duration = random.randint(1, 50) * 0.001
    # Делаем паузу на сгенерированное время (имитация работы)
    time.sleep(random_duration) # задержка
    # Случайно выбираем HTTP-код ответа из списка
    # 200 встречается 5 раз из 8, что дает ему больший вес (62.5% вероятность)
    # 400, 401, 500 встречаются по одному разу (по 12.5% каждый)
    response_code = random.choice([200, 200, 200, 200, 200, 400, 401, 500]) # коды ответа
    # Создаем HTTP-ответ с выбранным кодом в качестве тела ответа и статуса
    return Response(str(response_code), status=response_code)

# Точка входа для запуска приложения
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)