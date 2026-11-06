using TypeSpec.Http;

namespace TaskManagerWeb;

@doc("Список пользователей. Доступен только авторизованным.")
@get
@route("/users/")
op usersList(): HtmlPage<200> | Redirect302;

@doc("Страница регистрации.")
@get
@route("/users/create/")
@useAuth(NoAuth)
op userCreatePage(): HtmlPage<200>;

@doc("Регистрация пользователя.")
@post
@route("/users/create/")
@useAuth(NoAuth)
op userCreate(
  @header contentType: "application/x-www-form-urlencoded",
  @body form: RegisterForm,
): Redirect302 | HtmlPage<200> | HtmlPage<403>;

@doc("Страница изменения профиля. Только сам пользователь.")
@get
@route("/users/{id}/update/")
op userUpdatePage(@path id: int64): HtmlPage<200> | Redirect302 | HtmlPage<404>;

@doc("Изменение профиля. Только сам пользователь.")
@post
@route("/users/{id}/update/")
op userUpdate(
  @path id: int64,
  @header contentType: "application/x-www-form-urlencoded",
  @body form: UpdateUserForm,
): Redirect302 | HtmlPage<200> | HtmlPage<403> | HtmlPage<404>;

@doc("Страница удаления профиля. Только сам пользователь.")
@get
@route("/users/{id}/delete/")
op userDeletePage(@path id: int64): HtmlPage<200> | Redirect302 | HtmlPage<404>;

@doc("Удаление профиля. Только сам пользователь. При наличии задач удаление отклоняется.")
@post
@route("/users/{id}/delete/")
op userDelete(
  @path id: int64,
  @header contentType: "application/x-www-form-urlencoded",
  @body form: DeleteForm,
): Redirect302 | HtmlPage<403> | HtmlPage<404>;
