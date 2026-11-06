import "@typespec/http";
import "@typespec/openapi";
import "@typespec/openapi3";
import "../shared/html.tsp";
import "./forms.tsp";
import "./auth.tsp";
import "./users.tsp";
import "./statuses.tsp";
import "./labels.tsp";
import "./tasks.tsp";

using TypeSpec.Http;
using TypeSpec.OpenAPI;

@service(#{ title: "Task Manager Web UI" })
@info(#{ version: "1.0.0" })
@server("http://localhost:8000", "Local development")
@useAuth(ApiKeyAuth<ApiKeyLocation.cookie, "sessionid">)
namespace TaskManagerWeb;
