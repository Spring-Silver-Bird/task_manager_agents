import "@typespec/http";

using TypeSpec.Http;

@doc("HTML-страница приложения.")
model HtmlPage<Status extends int32> {
  @statusCode statusCode: Status;
  @header contentType: "text/html";
  @body body: string;
}

@doc("Редирект после успешного действия или при отсутствии прав.")
model Redirect302 {
  @statusCode statusCode: 302;
  @header location: string;
}

@doc("Пустой ответ.")
model NoContentResponse {
  @statusCode statusCode: 204;
}
