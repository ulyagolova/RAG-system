 # API

 

 ## Обзор

 

 FastAPI слой для работы с пользователями, курсами, рекомендациями и сервисными операциями.

 Базовый URL при локальном запуске: `http://localhost:8000`.

 **Примечание:** Некоторые эндпоинты помечены как *временные* и будут заменены в финальной версии. Новые эндпоинты добавляются в соответствии с развитием системы.

 

 ## Запуск

 

 ```bash

 python -m pip install -r requirements.txt -r requirements-dev.txt

 python -m src.api

 ```

 

 ## Swagger / OpenAPI

 

 - Swagger UI: `http://localhost:8000/docs`

 - OpenAPI JSON: `http://localhost:8000/openapi.json`

 

 ## Эндпоинты

 

 ### Health

 

 ```http

 GET /health

 ```

 

 Проверка работоспособности сервиса.

 

 Ответ:

 

 ```json

 {"status": "ok"}

 ```

 

 ### DB (инициализация базы данных) – временно

 

 ```http

 POST /db/init

 ```

 

 Инициализация таблиц, загрузка тестовых курсов. Используется только для прототипирования.

 

 Тело запроса:

 

 ```json

 {

   "drop_existing": false,

   "courses_file": "data/courses.json",

   "skip_courses_seed": false

 }

 ```

 

 Ответ:

 

 ```json

 {

   "courses_seeded": 0,

   "courses_count": 0,

   "chunks_count": 0,

   "collection_recreated": false

 }

 ```

 

 ### Courses

 

 ```http

 POST /courses/seed

 ```

 

 – временно. Загрузка курсов из JSON-файла.

 

 Тело запроса:

 

 ```json

 {"file_path": "data/courses.json"}

 ```

 

 Ответ:

 

 ```json

 {"inserted": 0}

 ```

 

 ```http

 GET /courses

 ```

 

 Получение списка всех курсов.

 

 Ответ:

 

 ```json

 [

   {"id": 1, "name": "Course name", "description": "..."}

 ]

 ```

 

 ### Users – некоторые эндпоинты временные

 

 ```http

 POST /users

 ```

 

 Создание нового пользователя (временный метод).

 

 Тело запроса:

 

 ```json

 {

   "login": "roman",

   "digital_footprints": "{\"events\":[]}"

 }

 ```

 

 Ответ:

 

 ```json

 {

   "id": 1,

   "login": "roman",

   "updated_at": "2026-02-16T20:00:00+00:00"

 }

 ```

 

 ```http

 GET /users

 ```

 

 Список пользователей.

 

 Ответ:

 

 ```json

 [

   {

     "id": 1,

     "login": "roman",

     "updated_at": "2026-02-16T20:00:00+00:00"

   }

 ]

 ```

 

 ```http

 POST /users/seed

 ```

 

 – временно. Загрузка цифровых следов из JSON.

 

 Тело запроса:

 

 ```json

 {"file_path": "data/digital-footprints.json"}

 ```

 

 Ответ:

 

 ```json

 {"created": 0, "updated": 0, "skipped": 0}

 ```

 

 ### Recommendations

 

 ```http

 POST /recommendations

 ```

 

 Сохранение рекомендации для пользователя (вручную).

 

 Тело запроса:

 

 ```json

 {

   "login": "roman",

   "text": "Начните с курса по Python"

 }

 ```

 

 Ответ:

 

 ```json

 {

   "id": 1,

   "text": "...",

   "created_at": "2026-02-16T20:00:00+00:00"

 }

 ```

 

 ```http

 GET /recommendations/{login}

 ```

 

 Получение всех рекомендаций пользователя.

 

 Ответ:

 

 ```json

 [

   {

     "id": 1,

     "text": "...",

     "created_at": "2026-02-16T20:00:00+00:00"

   }

 ]

 ```

 

 ```http

 POST /recommendations/generate

 ```

 

 Генерация рекомендации на основе портрета пользователя (тестовый режим).

 

 Тело запроса:

 

 ```json

 {

   "login": "alex_dev",

   "top_k": 5,

   "search_k": 20

 }

 ```

 

 Ответ:

 

 ```json

 {

   "recommendation": {

     "id": 1,

     "text": "...",

     "created_at": "2026-02-16T20:00:00+00:00"

   },

   "debug_file_path": "data/recs/20260216T000000Z_alex_dev.json",

   "query_text": "query: ...",

   "retrieved_courses": [

     {

       "course_id": 1,

       "name": "...",

       "description": "...",

       "score": 0.9

     }

   ]

 }

 ```

 

 ### Content (индексация контента) – новые эндпоинты

 

 ```http

 POST /content/parse

 ```

 

 Запуск индексации нового или обновлённого контента. Вызывается внешними системами (CMS Moodle, редакторы статей) при публикации материала. Задача выполняется асинхронно.

 

 Тело запроса:

 

 ```json

 {

   "resource_url": "https://moodle.moi-universitet.ru/course/view.php?id=123",

   "content_type": "course",

   "trigger_source": "moodle_hook",

   "metadata": {

     "title": "Курс Python",

     "author": "Иванов И.И.",

     "published_at": "2026-03-10"

   }

 }

 ```

 

 Ответ:

 

 ```json

 {

   "task_id": "parse_task_001",

   "status": "queued"

 }

 ```

 

 ```http

 GET /content/task/{task_id}

 ```

 

 Проверка статуса задачи индексации.

 

 Ответ (в процессе):

 

 ```json

 { "status": "processing" }

 ```

 

 Ответ (завершено):

 

 ```json

 {

   "status": "completed",

   "result": {

     "content_id": 456,

     "chunks_count": 24,

     "indexed_at": "2026-03-11T11:00:00Z"

   }

 }

 ```

 

 ```http

 POST /content/refresh

 ```

 

 Ручное обновление всего контента (полный реиндексинг). Требует прав администратора.

 

 Ответ:

 

 ```json

 { "task_id": "refresh_001" }

 ```

 

 ### Mautic (интеграция)

 

 ```http

 POST /mautic/webhook

 ```

 

 Вебхук для приёма цифровых следов от Mautic. Обработка асинхронная.

 

 Тело запроса (формат Mautic):

 

 ```json

 {

   "mautic_contact_id": 12345,

   "event": "page_hit",

   "details": {

     "url": "/courses/python",

     "title": "Курс Python",

     "timestamp": "2026-03-11T10:00:00Z"

   }

 }

 ```

 

 Ответ:

 

 ```json

 { "status": "accepted" }

 ```

 

 ```http

 POST /mautic/recommendations

 ```

 

 Запрос рекомендации для контакта Mautic (например, для вставки в email).

 

 Тело запроса:

 

 ```json

 {

   "mautic_contact_id": 12345,

   "campaign_id": "email_weekly",

   "context": {}

 }

 ```

 

 Ответ (синхронный, если готов):

 

 ```json

 {

   "recommendation_id": "rec_12345",

   "text": "Рекомендуем вам курс «Python для начинающих»",

   "course_id": 42,

   "created_at": "2026-03-11T10:05:00Z"

 }

 ```

 

 Ответ (асинхронный, если требуется время):

 

 ```json

 {

   "task_id": "task_67890",

   "status": "processing",

   "estimated_time_sec": 5

 }

 ```

 

 ### Survey (опрос)

 

 ```http

 POST /survey

 ```

 

 Отправка ответов на психологический опрос для формирования портрета пользователя.

 

 Тело запроса:

 

 ```json

 {

   "user_id": "uuid_or_login",

   "answers": [

     {"question_id": 1, "answer": "a"},

     {"question_id": 2, "answer": "c"}

   ]

 }

 ```

 

 Ответ:

 

 ```json

 { "status": "ok", "portrait_id": 789 }

 ```

 

 ### Admin (внутренние эндпоинты)

 

 Эндпоинты с префиксом `/internal` предназначены только для доверенных компонентов системы и не доступны извне.

 

 ```http

 POST /internal/users

 ```

 

 Создание или обновление пользователя при регистрации на сайте. Вызывается сайтом.

 

 Тело запроса:

 

 ```json

 {

   "external_id": "user_123",

   "login": "ivanov",

   "email": "ivanov@example.com"

 }

 ```

 

 Ответ:

 

 ```json

 { "internal_id": "uuid" }

 ```

 

 ```http

 GET /internal/users/{external_id}/portrait

 ```

 

 Получение текущего портрета пользователя (интересы + психотип) для внутренних нужд.

 

 Ответ:

 

 ```json

 {

   "user_id": "uuid",

   "interests_vector_preview": "[0.12, 0.45, ...]",

   "psychological_type": "ENFJ",

   "last_updated": "2026-03-11T12:00:00Z"

 }

 ```

 

 ### Метрики и мониторинг

 

 ```http

 GET /metrics

 ```

 

 Метрики в формате Prometheus.

 

 ```http

 GET /health/detailed

 ```

 

 Детальная информация о состоянии компонентов.

 

 Ответ:

 

 ```json

 {

   "status": "ok",

   "components": {

     "postgres": "up",

     "qdrant": "up",

     "llm": "up"

   }

 }

 ```

 

 ### Отладочные эндпоинты (доступны только в режиме разработки)

 

 ```http

 GET /debug/vector/{user_id}

 ```

 

 – показать вектор пользователя.

 

 ```http

 POST /debug/force-recommend

 ```

 

 – принудительно запустить пайплайн для тестового запроса.

 
