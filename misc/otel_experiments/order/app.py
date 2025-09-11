# Импорт Flask для создания веб-приложения
from flask import Flask
# Импорт модуля random для генерации случайных чисел
import random
# Импорт модуля time для создания задержек
import time
# Импорт основного модуля трейсинга OpenTelemetry
from opentelemetry import trace
# Импорт экспортера для отправки трейсов в Jaeger через Thrift протокол
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
# Импорт констант и классов для создания ресурсов (метаданные сервиса)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
# Импорт провайдера трейсов - основного компонента для управления трейсингом
from opentelemetry.sdk.trace import TracerProvider
# Импорт процессора для батчевой отправки спанов в экспортер
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# Импорт автоматической инструментации Flask приложений
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Создание и установка провайдера трейсов для текущего приложения
trace.set_tracer_provider(
   TracerProvider(
       # Создание ресурса с метаданными сервиса (имя сервиса = "order")
       resource=Resource.create({SERVICE_NAME: "order"})
   )
)
# Создание экспортера для отправки трейсов в Jaeger
jaeger_exporter = JaegerExporter(
   # Указание хоста где запущен Jaeger agent (в Docker это имя контейнера)
   agent_host_name="jaeger",
   # Порт Jaeger agent для приема трейсов по UDP протоколу
   agent_port=6831,
)
# Добавление процессора спанов к провайдеру трейсов
trace.get_tracer_provider().add_span_processor(
   # BatchSpanProcessor собирает спаны в батчи и отправляет их через экспортер
   BatchSpanProcessor(jaeger_exporter)
)
# Создание Flask приложения
app = Flask(__name__)
# Автоматическая инструментация Flask - создает спаны для всех HTTP-запросов
FlaskInstrumentor().instrument_app(app)

# Определение корневого маршрута / для обработки заказов
@app.route("/")
def order():
    # Создание кастомного спана с именем "order" для трейсинга бизнес-логики
    with trace.get_tracer(__name__).start_as_current_span("order"):
        # Генерация случайного номера заказа от 1 до 500
        random_order_number = random.randint(1, 500)
        # Имитация времени обработки заказа (задержка в миллисекундах)
        time.sleep(random_order_number*0.001) #задержка
        # Возврат номера заказа в виде строки
        return str(random_order_number)