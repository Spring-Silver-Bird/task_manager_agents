using TypeSpec.Http;

namespace TaskManagerWeb;

@doc("Список меток.")
@get
@route("/labels/")
op labelsList(): HtmlPage<200> | Redirect302;

@doc("Страница создания метки.")
@get
@route("/labels/create/")
op labelCreatePage(): HtmlPage<200> | Redirect302;

@doc("Создание метки.")
@post
@route("/labels/create/")
op labelCreate(
  @header contentType: "application/x-www-form-urlencoded",
  @body form: NameForm,
): Redirect302 | HtmlPage<200> | HtmlPage<403>;

@doc("Страница изменения метки.")
@get
@route("/labels/{id}/update/")
op labelUpdatePage(@path id: int64):
  | HtmlPage<200>
  | Redirect302
  | HtmlPage<404>;

@doc("Изменение метки.")
@post
@route("/labels/{id}/update/")
op labelUpdate(
  @path id: int64,
  @header contentType: "application/x-www-form-urlencoded",
  @body form: NameForm,
): Redirect302 | HtmlPage<200> | HtmlPage<403> | HtmlPage<404>;

@doc("Страница удаления метки.")
@get
@route("/labels/{id}/delete/")
op labelDeletePage(@path id: int64):
  | HtmlPage<200>
  | Redirect302
  | HtmlPage<404>;

@doc("Удаление метки. При использовании в задачах удаление отклоняется.")
@post
@route("/labels/{id}/delete/")
op labelDelete(
  @path id: int64,
  @header contentType: "application/x-www-form-urlencoded",
  @body form: DeleteForm,
): Redirect302 | HtmlPage<403> | HtmlPage<404>;
