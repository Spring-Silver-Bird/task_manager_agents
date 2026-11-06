using TypeSpec.Http;

namespace TaskManagerWeb;

@doc("Главная страница.")
@get
@route("/")
@useAuth(NoAuth)
op index(): HtmlPage<200>;

@doc("Страница входа.")
@get
@route("/login/")
@useAuth(NoAuth)
op loginPage(): HtmlPage<200>;

@doc("Вход по username и password. При успехе ставит cookie sessionid.")
@post
@route("/login/")
@useAuth(NoAuth)
op login(
  @header contentType: "application/x-www-form-urlencoded",
  @body form: LoginForm,
): Redirect302 | HtmlPage<200> | HtmlPage<403>;

@doc("Выход. Требует POST и CSRF.")
@post
@route("/logout/")
op logout(
  @header contentType: "application/x-www-form-urlencoded",
  @body form: DeleteForm,
): Redirect302 | HtmlPage<403>;
