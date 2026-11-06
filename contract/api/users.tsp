using TypeSpec.Http;

namespace TaskManagerApi;

@doc("Список пользователей. Доступен только авторизованным.")
@get
@route("users")
op listUsers(@query page?: int32, @query page_size?: int32):
  | Page<UserRead>
  | Unauthorized;

@doc("Регистрация пользователя. Доступна без аутентификации, но требует CSRF-заголовок.")
@post
@route("users")
@useAuth(NoAuth)
op createUser(...CsrfHeader, @body body: UserCreate):
  | CreatedWithBody<UserRead>
  | BadRequest
  | Forbidden
  | Conflict;

@doc("Профиль пользователя. Доступен только авторизованным.")
@get
@route("users/{id}")
op getUser(@path id: int64): UserRead | Unauthorized | NotFound;

@doc("Изменение профиля. Только сам пользователь.")
@patch
@route("users/{id}")
op updateUser(@path id: int64, ...CsrfHeader, @body body: UserUpdate):
  | UserRead
  | BadRequest
  | Unauthorized
  | Forbidden
  | NotFound
  | Conflict;

@doc("Удаление профиля. Только сам пользователь. При наличии задач удаление отклоняется.")
@delete
@route("users/{id}")
op deleteUser(@path id: int64, ...CsrfHeader):
  | EmptyResponse
  | Unauthorized
  | Forbidden
  | NotFound
  | Conflict;
