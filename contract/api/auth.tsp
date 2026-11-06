using TypeSpec.Http;

namespace TaskManagerApi;

@doc("Получить CSRF-токен и cookie csrftoken. Доступно без аутентификации.")
@get
@route("auth/csrf")
@useAuth(NoAuth)
op getCsrf(): CsrfTokenResponse;

@doc("Текущий пользователь.")
@get
@route("auth/me")
op getMe(): UserRead | Unauthorized;

@doc("Вход по username и password. При успехе ставит cookie sessionid.")
@post
@route("auth/login")
@useAuth(NoAuth)
op login(...CsrfHeader, @body body: LoginRequest):
  | LoginResponse
  | BadRequest
  | Unauthorized
  | Forbidden;

@doc("Выход. Требует session cookie и CSRF-заголовок.")
@post
@route("auth/logout")
op logout(...CsrfHeader): EmptyResponse | Unauthorized | Forbidden;
