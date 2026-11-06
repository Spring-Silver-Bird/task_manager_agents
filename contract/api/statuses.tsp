using TypeSpec.Http;

namespace TaskManagerApi;

@doc("Список статусов.")
@get
@route("statuses")
op listStatuses(@query page?: int32, @query page_size?: int32):
  | Page<StatusRead>
  | Unauthorized;

@doc("Создание статуса.")
@post
@route("statuses")
op createStatus(...CsrfHeader, @body body: StatusWrite):
  | CreatedWithBody<StatusRead>
  | BadRequest
  | Unauthorized
  | Forbidden
  | Conflict;

@doc("Изменение статуса.")
@patch
@route("statuses/{id}")
op updateStatus(@path id: int64, ...CsrfHeader, @body body: StatusWrite):
  | StatusRead
  | BadRequest
  | Unauthorized
  | Forbidden
  | NotFound
  | Conflict;

@doc("Удаление статуса. При использовании в задачах удаление отклоняется.")
@delete
@route("statuses/{id}")
op deleteStatus(@path id: int64, ...CsrfHeader):
  | EmptyResponse
  | Unauthorized
  | Forbidden
  | NotFound
  | Conflict;
