# TypeSpec contract

Контракт описывает две поверхности проекта:

- `web/` — текущий server-rendered HTML UI;
- `api/` — будущий JSON API `/api/v1`.

Оба контракта нормативные: они фиксируют целевую модель, даже если текущий код ещё не приведён к ней.

## Требования

- Node.js >= 22 (см. `.nvmrc` в корне репозитория);
- npm.

## Сборка

```bash
cd contract
nvm use
npm ci
npm run compile
```

Команды из корня репозитория:

```bash
make contract-install
make contract-build
make contract-check
```

`make contract-check` пересобирает OpenAPI и проверяет, что сгенерированные файлы закоммичены.

## Результат

- `tsp-output/openapi/web.yaml`
- `tsp-output/openapi/api.yaml`

Файлы генерируются из `.tsp`-исходников. Не редактировать их вручную: изменения вносить в TypeSpec и пересобирать.

## Структура

- `shared/html.tsp` — HTML-ответы и редиректы для web-контракта.
- `shared/problem.tsp` — `ProblemDetails`, ошибки и общие ответы API.
- `web/` — HTML-страницы, формы и CSRF.
- `api/` — JSON-модели, session/CSRF-аутентификация и REST endpoints.

## Аутентификация

- Session cookie: `sessionid`.
- CSRF для web: поле формы `csrfmiddlewaretoken`.
- CSRF для API: заголовок `X-CSRFToken`; токен и cookie `csrftoken` выдаёт `GET /api/v1/auth/csrf`.

## Статусы

- `when_to_apply` — необязательный текст: когда применять статус.
- `status_type` — обязательный тип: `backlog`, `todo`, `in_progress`, `review`, `blocked`, `done`.

## Целевые правила доступа

- Список и профили пользователей доступны только авторизованным.
- Регистрация публичная.
- Изменять и удалять пользователя может только сам пользователь.
- Изменять и удалять задачу может только автор.
- Статусы и метки доступны и изменяются любым авторизованным пользователем.

## Расхождения с текущим кодом

- `UserListView` сейчас публичный; по контракту нужен логин.
- `TaskUpdateView` сейчас доступен любому авторизованному; по контракту только автор.
- JSON API пока не реализован.
- В API добавлены пагинация и ошибки `ProblemDetails`.
- Web-контракт описывает целевые правила, а не текущие расхождения.
