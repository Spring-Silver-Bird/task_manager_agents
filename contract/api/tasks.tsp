using TypeSpec.Http;

namespace TaskManagerApi;

@doc("Список задач. Фильтры: status_id, executor_id, label_id, self_tasks.")
@get
@route("tasks")
op listTasks(
  @query status_id?: int64,
  @query executor_id?: int64,
  @query label_id?: int64,
  @query self_tasks?: boolean,
  @query page?: int32,
  @query page_size?: int32,
): Page<TaskRead> | Unauthorized;

@doc("Создание задачи. Автор устанавливается автоматически.")
@post
@route("tasks")
op createTask(...CsrfHeader, @body body: TaskCreate):
  | CreatedWithBody<TaskRead>
  | BadRequest
  | Unauthorized
  | Forbidden
  | Conflict;

@doc("Детали задачи.")
@get
@route("tasks/{id}")
op getTask(@path id: int64): TaskRead | Unauthorized | NotFound;

@doc("Изменение задачи. Только автор.")
@patch
@route("tasks/{id}")
op updateTask(@path id: int64, ...CsrfHeader, @body body: TaskUpdate):
  | TaskRead
  | BadRequest
  | Unauthorized
  | Forbidden
  | NotFound
  | Conflict;

@doc("Удаление задачи. Только автор.")
@delete
@route("tasks/{id}")
op deleteTask(@path id: int64, ...CsrfHeader):
  | EmptyResponse
  | Unauthorized
  | Forbidden
  | NotFound;
