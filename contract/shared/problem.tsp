import "@typespec/http";

using TypeSpec.Http;

@doc("Описание ошибки в формате RFC 9457 Problem Details.")
model ProblemDetails {
  type: string;
  title: string;
  status: int32;
  detail?: string;
  errors?: Record<string[]>;
}

@error
model BadRequest {
  @statusCode statusCode: 400;
  @body body: ProblemDetails;
}

@error
model Unauthorized {
  @statusCode statusCode: 401;
  @body body: ProblemDetails;
}

@error
model Forbidden {
  @statusCode statusCode: 403;
  @body body: ProblemDetails;
}

@error
model NotFound {
  @statusCode statusCode: 404;
  @body body: ProblemDetails;
}

@error
model Conflict {
  @statusCode statusCode: 409;
  @body body: ProblemDetails;
}

@doc("Успешное создание ресурса.")
model CreatedWithBody<T> {
  @statusCode statusCode: 201;
  @body body: T;
}

@doc("Пустой ответ.")
model EmptyResponse {
  @statusCode statusCode: 204;
}
