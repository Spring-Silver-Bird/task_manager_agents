import "@typespec/http";
import "../shared/status.tsp";

using TypeSpec.Http;

@doc("Краткие данные пользователя.")
model UserRef {
  id: int64;
  username: string;
  first_name: string;
  last_name: string;
}

@doc("Пользователь.")
model UserRead {
  id: int64;
  username: string;
  first_name: string;
  last_name: string;
  date_joined: utcDateTime;
}

@doc("Регистрация пользователя.")
model UserCreate {
  username: string;
  first_name?: string;
  last_name?: string;
  password: string;
  password_confirmation: string;
}

@doc("Изменение профиля. Пароль опционален.")
model UserUpdate {
  username?: string;
  first_name?: string;
  last_name?: string;
  password?: string;
  password_confirmation?: string;
}

@doc("Краткие данные статуса.")
model StatusRef {
  id: int64;
  name: string;
}

@doc("Статус.")
model StatusRead {
  id: int64;
  name: string;
  when_to_apply: string;
  status_type: StatusType;
  created_at: utcDateTime;
}

@doc("Создание или изменение статуса.")
model StatusWrite {
  name: string;
  when_to_apply?: string;
  status_type: StatusType;
}

@doc("Краткие данные метки.")
model LabelRef {
  id: int64;
  name: string;
}

@doc("Метка.")
model LabelRead {
  id: int64;
  name: string;
  created_at: utcDateTime;
}

@doc("Создание или изменение метки.")
model LabelWrite {
  name: string;
}

@doc("Задача.")
model TaskRead {
  id: int64;
  name: string;
  description: string;
  status: StatusRef;
  labels: LabelRef[];
  author: UserRef;
  executor?: UserRef;
  created_at: utcDateTime;
}

@doc("Создание задачи. Автор устанавливается автоматически.")
model TaskCreate {
  name: string;
  description?: string;
  status_id: int64;
  executor_id?: int64;
  label_ids?: int64[];
}

@doc("Изменение задачи. Только автор.")
model TaskUpdate {
  name?: string;
  description?: string;
  status_id?: int64;
  executor_id?: int64;
  label_ids?: int64[];
}

@doc("Страница результатов.")
model Page<T> {
  items: T[];
  total: int64;
  page: int32;
  page_size: int32;
}

@doc("Данные для входа.")
model LoginRequest {
  username: string;
  password: string;
}

@doc("CSRF-токен и cookie csrftoken.")
model CsrfTokenResponse {
  @header("Set-Cookie") set_cookie: string;
  @body body: {
    csrf_token: string;
  };
}

@doc("Успешный вход и cookie sessionid.")
model LoginResponse {
  @header("Set-Cookie") set_cookie: string;
  @body user: UserRead;
}

@doc("CSRF-заголовок для изменяющих запросов.")
model CsrfHeader {
  @header("X-CSRFToken") csrf_token: string;
}
