import "../shared/status.tsp";

@doc("Форма входа.")
model LoginForm {
  username: string;
  password: string;
  csrfmiddlewaretoken: string;
}

@doc("Форма регистрации.")
model RegisterForm {
  first_name: string;
  last_name: string;
  username: string;
  password1: string;
  password2: string;
  csrfmiddlewaretoken: string;
}

@doc("Форма изменения профиля.")
model UpdateUserForm {
  first_name: string;
  last_name: string;
  username: string;
  password1?: string;
  password2?: string;
  csrfmiddlewaretoken: string;
}

@doc("Форма статуса.")
model StatusForm {
  name: string;
  when_to_apply?: string;
  status_type: StatusType;
  csrfmiddlewaretoken: string;
}

@doc("Форма метки.")
model LabelForm {
  name: string;
  meaning?: string;
  karma_effect?: string;
  csrfmiddlewaretoken: string;
}

@doc("Форма задачи. labels передаётся повторяющимся полем формы.")
model TaskForm {
  name: string;
  description?: string;
  status: int64;
  executor?: int64;
  labels?: int64[];
  csrfmiddlewaretoken: string;
}

@doc("Форма подтверждения действия.")
model DeleteForm {
  csrfmiddlewaretoken: string;
}
