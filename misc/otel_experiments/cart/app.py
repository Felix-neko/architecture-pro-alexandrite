# Импорт Flask для создания веб-приложения
from flask import Flask
# Импорт requests для выполнения HTTP-запросов к другим сервисам
import requests
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
# Импорт автоматической инструментации HTTP-запросов через requests
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Создание и установка провайдера трейсов для текущего приложения
trace.set_tracer_provider(
   TracerProvider(
       # Создание ресурса с метаданными сервиса (имя сервиса = "cart")
       resource=Resource.create({SERVICE_NAME: "cart"})
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
# Автоматическая инструментация requests - создает спаны для исходящих HTTP-запросов
RequestsInstrumentor().instrument()

# Определение маршрута /buy для обработки покупок
@app.route("/buy")
def buy():
    # Создание кастомного спана с именем "buy" для трейсинга бизнес-логики
    with trace.get_tracer(__name__).start_as_current_span("buy"):
        # HTTP-запрос к сервису billing (автоматически создастся спан благодаря RequestsInstrumentor)
        res = requests.get("http://billing:8000")
        # Возврат ответа от billing сервиса
        return res.text