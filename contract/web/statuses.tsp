using TypeSpec.Http;

namespace TaskManagerWeb;

@doc("Список статусов.")
@get
@route("/statuses/")
op statusesList(): HtmlPage<200> | Redirect302;

@doc("Страница создания статуса.")
@get
@route("/statuses/create/")
op statusCreatePage(): HtmlPage<200> | Redirect302;

@doc("Создание статуса.")
@post
@route("/statuses/create/")
op statusCreate(
  @header contentType: "application/x-www-form-urlencoded",
  @body form: StatusForm,
): Redirect302 | HtmlPage<200> | HtmlPage<403>;

@doc("Страница изменения статуса.")
@get
@route("/statuses/{id}/update/")
op statusUpdatePage(@path id: int64):
  | HtmlPage<200>
  | Redirect302
  | HtmlPage<404>;

@doc("Изменение статуса.")
@post
@route("/statuses/{id}/update/")
op statusUpdate(
  @path id: int64,
  @header contentType: "application/x-www-form-urlencoded",
  @body form: StatusForm,
): Redirect302 | HtmlPage<200> | HtmlPage<403> | HtmlPage<404>;

@doc("Страница удаления статуса.")
@get
@route("/statuses/{id}/delete/")
op statusDeletePage(@path id: int64):
  | HtmlPage<200>
  | Redirect302
  | HtmlPage<404>;

@doc("Удаление статуса. При использовании в задачах удаление отклоняется.")
@post
@route("/statuses/{id}/delete/")
op statusDelete(
  @path id: int64,
  @header contentType: "application/x-www-form-urlencoded",
  @body form: DeleteForm,
): Redirect302 | HtmlPage<403> | HtmlPage<404>;
