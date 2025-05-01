tags_metadata = [
    {
        "name": "users",
        "description": "👤 **Users**:\n"
        "- 🔹 Registration\n"
        "- 🔹 Email verification\n"
        "- 🔹 Password reset\n"
        "- 🔹 JWT authentication\n"
        "- 🔹 JWT token revocation\n"
        "- 🔹 Get user information\n"
        "- 🔹 Upload/update profile image\n"
        "- 🔹 Upload/update banner\n"
        "- 🔹 Update profile details",
    },
    {
        "name": "admin",
        "description": "🧑‍⚖️ **Administration**:\n"
        "- 🔹 Delete any pin\n"
        "- 🔹 Delete any comment\n",
    },
    {
        "name": "pins",
        "description": "📌 **Pins**:\n"
        "- 🔹 Retrieve a list of pins\n"
        "- 🔹 Create a pin\n"
        "- 🔹 Delete a pin\n"
        "- 🔹 Search by tags\n"
        "- 🔹 Upload an image/video\n"
        "- 🔹 Get an individual pin\n"
        "- 🔹 Retrieve all user pins\n"
        "- 🔹 Save and remove pins\n"
        "- 🔹 Retrieve list of liked pins",
    },
    {
        "name": "search",
        "description": "🔍 **Search**:\n"
        "- 🔹 Get a list of user search queries\n"
        "- 🔹 Save a search query\n"
        "- 🔹 Delete a search query\n",
    },
    {
        "name": "boards",
        "description": "📋 **Boards**:\n"
        "- 🔹 Retrieve list of boards\n"
        "- 🔹 Create a board\n"
        "- 🔹 Delete a board\n"
        "- 🔹 Get all pins on a board\n"
        "- 🔹 Save and remove pins on a board\n",
    },
    {
        "name": "recommendations",
        "description": "🧠 **Recommendations**:\n"
        "- 🔹 Check for recommendations for the user\n"
        "- 🔹 Retrieve list of recommended pins for the user\n",
    },
    {
        "name": "updates",
        "description": "🔔 **Updates**:\n"
        "- 🔹 Retrieve a list of updates for the user\n"
        "- 🔹 Get an individual update by ID\n"
        "- 🔹 Get the count of updates\n"
        "- 🔹 Change the read status of an update\n",
    },
    {
        "name": "tags",
        "description": "🏷 **Tags**:\n"
        "- 🔹 Retrieve all tags\n"
        "- 🔹 Create a tag\n"
        "- 🔹 Get pins by tag\n"
        "- 🔹 Get tags on a pin\n",
    },
    {
        "name": "comments",
        "description": "💬 **Comments**:\n"
        "- 🔹 Create a comment\n"
        "- 🔹 Retrieve a list of comments\n"
        "- 🔹 Count the number of comments\n"
        "- 🔹 Upload images/videos\n"
        "- 🔹 Create replies to comments\n"
        "- 🔹 Retrieve all replies to comments\n",
    },
    {
        "name": "likes",
        "description": "❤️ **Likes**:\n"
        "- 🔹 Like on pins/comments\n"
        "- 🔹 Remove a like\n"
        "- 🔹 Check if a like exists\n"
        "- 🔹 Count the number of likes\n",
    },
    {
        "name": "subscriptions",
        "description": "🔔 **Subscriptions**:\n"
        "- 🔹 Subscribe/unsubscribe to a user\n"
        "- 🔹 Check subscription status\n"
        "- 🔹 Retrieve list of subscribers\n"
        "- 🔹 Retrieve list of subscriptions\n"
        "- 🔹 Count number of subscribers/subscriptions\n",
    },
    {
        "name": "chats",
        "description": "💬 **Chats**:\n" "- 🔹 Change chat color, size, and visibility\n",
    },
    {
        "name": "messages",
        "description": "📩 **Messages**:\n"
        "- 🔹 Create messages\n"
        "- 🔹 Retrieve message history\n"
        "- 🔹 Get the latest message\n"
        "- 🔹 Check if chats exist\n"
        "- 🔹 Upload images/videos in messages\n"
        "- 🔹 Count unread messages\n",
    },
    {
        "name": "sse",
        "description": "📺 **Server-Sent Events**:\n"
        "- 🔹 SSE for chats (when another user sends you a message or starts a chat with you)\n"
        "- 🔹 SSE for updates (when another user saves/likes/comments on your pin or follows you)\n"
        "- 🔹 SSE for the unauthenticated page for streaming video\n",
    },
    {
        "name": "notauth",
        "description": "🏠 **Homepage**:\n" "- 🔹 Retrieve images for unauthenticated users\n",
    },
    {
        "name": "pins-cache",
        "description": "🗄 **Pins Cache (Example)**:\n"
        "- 🔹 Retrieve list of pins with caching\n"
        "- 🔹 Clear cache when a pin is created/deleted\n",
    },
    {
        "name": "users-google-auth",
        "description": "🔑 **Google OAuth2 (Example)**:\n"
        "- 🔹 Authentication via Google\n"
        "- 🔹 Retrieve data of the authenticated user\n",
    },
    {
        "name": "users-httpx",
        "description": "🔗 **HTTPX Users (Example)**:\n" "- 🔹 CRUD operations via HTTPX\n",
    },
    {
        "name": "users-mysql",
        "description": "🛢 **MySQL Users (Example)**:\n"
        "- 🔹 CRUD operations using sqlalchemy + aiomysql\n",
    },
    {
        "name": "users-mongodb",
        "description": "📦 **MongoDB Users (Example)**:\n"
        "- 🔹 CRUD operations using asynchronous MongoDB\n",
    },
    {
        "name": "users-celery",
        "description": "📤 **Celery (Example)**:\n"
        "- 🔹 Upload media via Celery worker\n"
        "- 🔹 Check task status\n",
    },
    {
        "name": "yandex-s3",
        "description": "☁ **Yandex S3 (Example)**:\n"
        "- 🔹 Upload media to a Yandex Bucket\n"
        "- 🔹 Retrieve files from storage\n",
    },
    {
        "name": "redis-stream",
        "description": "🚀 **Redis Stream (Example)**:\n"
        "- 🔹 Создание Consumer Group для потока сообщений\n"
        "- 🔹 Добавление сообщений в поток\n"
        "- 🔹 Запуск фонового воркера для обработки сообщений\n"
        "- 🔹 Получение всех сообщений из потока\n",
    },
    {
        "name": "rabbitmq-pub-sub",
        "description": "🚀 **RabbitMQ Pub/Sub + SSE (Example)**:\n"
        "- 🔹 Публикация сообщений в обменник RabbitMQ\n"
        "- 🔹 Запуск фонового подписчика на очередь\n"
        "- 🔹 Передача сообщений подписчику через Server-Sent Events (SSE)\n"
        "- 🔹 Простая клиентская страница для тестирования SSE подписки\n",
    },
    {
        "name": "rabbitmq-stream",
        "description": "🚀 **RabbitMQ Stream (Example)**:\n"
        "- 🔹 Publish messages to a RabbitMQ queue\n"
        "- 🔹 Consume messages from RabbitMQ queue\n",
    },
    {
        "name": "sentry-test",
        "description": "🛡️ **Sentry Test (Example)**:\n"
        "- 🔹 Route for triggering and testing server-side errors\n"
        "- 🔹 Used to verify error capturing and monitoring with Sentry\n",
    },
    {
        "name": "graphql",
        "description": "🔗 **GraphQL (Example)**:\n" "- 🔹 GraphQL API and documentation\n",
    },
]

description = """
### 🖼️ API Description
This API is designed to work with **Pinterest** – a platform for sharing images, videos, and ideas.

#### 🔑 Core Functionality:
- **Users**: registration, login, logout, Google authentication, email verification, password reset, JWT authentication (access/refresh tokens), token revocation, image upload, profile update, and retrieval of all user profiles.
- **Pins**: creation, deletion, saving, liking, search, media upload, management of saved, liked and created pins, retrieving all pins, and viewing individual pins along with related content.
- **Tags**: tag management and searching pins by tags.
- **Comments**: adding comments to a pin, replying to comments, media uploads, and retrieving pin comments.
- **Likes**: likes for pins and comments.
- **Subscriptions**: managing subscriptions, retrieving lists of subscribers and following users.
- **Realtime Chats and Messages**: viewing chats, retrieving chat history, and sending messages.
- **Realtime Updates**: receiving updates from other users.
- **Recommendations**: users receive pin recommendations based on their viewed content.
- **Search**: users can retrieve and delete their latest search queries.
- **Admin**: administrators can delete any pin or comment.
- **Boards**: users can create/delete boards, select a board, add pins to a selected board, view all boards, view pins on a board, and remove pins from a board.

#### 🛠️ Technologies Used:
- **FastAPI** – REST and GraphQL API.
- **FastAPI-Cache** – for API-level caching.
- **FastAPI-Mail** – for sending emails via FastAPI.
- **SQLAlchemy** – ORM for database management.
- **Pydantic** – for request/response validation and **pydantic-settings** for managing environment variables.
- **JWT** – access/refresh tokens and token revocation.
- **OAuth2** – Google authentication.
- **PostgreSQL, MySQL, MongoDB** – for working with both relational and non-relational databases.
- **Redis** – for data caching, token revocation, message brokering, retrieving Celery results, and Celery RedBeat.
- **Celery** – for sending verification/password reset emails and processing images (saving, resizing, and updating the database).
- **Celery Beat** – for sending promotional emails.
- **Docker** – for containerizing applications.
- **Docker Compose** – for managing multi-container applications.
- **Nginx** – reverse proxy with routing for API, WebSocket, Vue.js, SSE, and Prometheus with basic auth
- **SSL** – for secure HTTPS connections.
- **VPS** – for hosting the application on a virtual server.
- **Yandex S3** – for file storage and retrieval (Yandex bucket).
- **httpx** – for interacting with external APIs.
- **Websockets** – for implementing chats with FastAPI.websockets.
- **SSE (Server-Sent Events)** – for real-time notifications from the server to the client.
- **Asyncio** – for asynchronous programming.
- **Aiofiles** – for asynchronous file system operations.
- **Logging** – for application logging.
- **Pytest** – for testing and quality assurance.
- **Ruff** – for linting and formatting.
- **Alembic** – for database migrations.
- **GitLab CI/CD** – for configuring the CI/CD pipeline (build, lint/format, migrations, testing, deployment).
- **GraphQL (Strawberry)** – for building the GraphQL API.
- **Redis pub/sub** — для обмена сообщениями между Celery и FastAPI.
- **Redis Stream** — для обработки сообщений с помощью Consumer Group и фоновых воркеров.
- **RabbitMQ** — как broker/result + celery.
- **RabbitMQ как pub/sub** — для публикации сообщений и подписки на очереди с передачей через SSE.
- **RabbitMQ Stream** — для публикации и потребления сообщений из очереди RabbitMQ
- **Sentry** — для мониторинга ошибок, логирования исключений и отслеживания производительности.
- **Prometheus** — для сбора метрик с FastAPI (через prometheus_fastapi_instrumentator), VPS (через node-exporter) и Nginx (через nginx-exporter) для мониторинга производительности и состояния системы.
- **Grafana** - для визуализации метрик, собранных с помощью Prometheus, что позволяет мониторить производительность и состояние системы.
- **Loki** – для сбора и агрегации логов.
- **Promtail** – для отправки логов в Loki с серверов и контейнеров.


#### 📝 Author:
- 🐰 **Daniil Kupryianchyk**

#### 📬 Contacts:
- 📧 **Email**: [dankupr21@gmail.com](mailto:dankupr21@gmail.com)
- 💬 **Telegram**: [@evalshine](https://t.me/evalshine)
- 🐙 **GitHub**: [shutsuensha](https://github.com/shutsuensha)

#### 🔗 Useful Links:
- 🚀 **GraphQL API**: [`pint3rest.xyz/api/graphql`](https://pint3rest.xyz/api/graphql)
- 📜 **Documentation (Swagger UI)**: [`pint3rest.xyz/api/docs`](https://pint3rest.xyz/api/docs)
- 📑 **Documentation (ReDoc)**: [`pint3rest.xyz/api/redoc`](https://pint3rest.xyz/api/redoc)
- 📜 **OpenAPI JSON**: [`pint3rest.xyz/api/openapi.json`](https://pint3rest.xyz/api/openapi.json)
- 🌐 **Homepage**: [`pint3rest.xyz`](https://pint3rest.xyz)
"""

title = "Pinterest Rest API"
version = "1.0.0"

license_info = {
    "name": "MIT LICENSE",
    "url": "https://github.com/shutsuensha/pint3rest.xyz/blob/main/LICENSE",
}
