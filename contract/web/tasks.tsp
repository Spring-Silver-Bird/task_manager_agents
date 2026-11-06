using TypeSpec.Http;

namespace TaskManagerWeb;

@doc("Список задач с фильтрами status, executor, labels и self_tasks.")
@get
@route("/tasks/")
op tasksList(
  @query status?: int64,
  @query executor?: int64,
  @query labels?: int64,
  @query self_tasks?: boolean,
): HtmlPage<200> | Redirect302;

@doc("Страница создания задачи.")
@get
@route("/tasks/create/")
op taskCreatePage(): HtmlPage<200> | Redirect302;

@doc("Создание задачи. Автор устанавливается автоматически.")
@post
@route("/tasks/create/")
op taskCreate(
  @header contentType: "application/x-www-form-urlencoded",
  @body form: TaskForm,
): Redirect302 | HtmlPage<200> | HtmlPage<403>;

@doc("Детальная страница задачи.")
@get
@route("/tasks/{id}/")
op taskDetail(@path id: int64): HtmlPage<200> | Redirect302 | HtmlPage<404>;

@doc("Страница изменения задачи. Только автор.")
@get
@route("/tasks/{id}/update/")
op taskUpdatePage(@path id: int64): HtmlPage<200> | Redirect302 | HtmlPage<404>;

@doc("Изменение задачи. Только автор.")
@post
@route("/tasks/{id}/update/")
op taskUpdate(
  @path id: int64,
  @header contentType: "application/x-www-form-urlencoded",
  @body form: TaskForm,
): Redirect302 | HtmlPage<200> | HtmlPage<403> | HtmlPage<404>;

@doc("Страница удаления задачи. Только автор.")
@get
@route("/tasks/{id}/delete/")
op taskDeletePage(@path id: int64): HtmlPage<200> | Redirect302 | HtmlPage<404>;

@doc("Удаление задачи. Только автор.")
@post
@route("/tasks/{id}/delete/")
op taskDelete(
  @path id: int64,
  @header contentType: "application/x-www-form-urlencoded",
  @body form: DeleteForm,
): Redirect302 | HtmlPage<403> | HtmlPage<404>;
