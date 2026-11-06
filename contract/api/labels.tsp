using TypeSpec.Http;

namespace TaskManagerApi;

@doc("Список меток.")
@get
@route("labels")
op listLabels(@query page?: int32, @query page_size?: int32):
  | Page<LabelRead>
  | Unauthorized;

@doc("Создание метки.")
@post
@route("labels")
op createLabel(...CsrfHeader, @body body: LabelWrite):
  | CreatedWithBody<LabelRead>
  | BadRequest
  | Unauthorized
  | Forbidden
  | Conflict;

@doc("Изменение метки.")
@patch
@route("labels/{id}")
op updateLabel(@path id: int64, ...CsrfHeader, @body body: LabelWrite):
  | LabelRead
  | BadRequest
  | Unauthorized
  | Forbidden
  | NotFound
  | Conflict;

@doc("Удаление метки. При использовании в задачах удаление отклоняется.")
@delete
@route("labels/{id}")
op deleteLabel(@path id: int64, ...CsrfHeader):
  | EmptyResponse
  | Unauthorized
  | Forbidden
  | NotFound
  | Conflict;
