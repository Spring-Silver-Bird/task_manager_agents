import "@typespec/http";
import "@typespec/openapi";
import "@typespec/openapi3";
import "../shared/problem.tsp";
import "./models.tsp";
import "./auth.tsp";
import "./users.tsp";
import "./statuses.tsp";
import "./labels.tsp";
import "./tasks.tsp";

using TypeSpec.Http;
using TypeSpec.OpenAPI;

@service(#{ title: "Task Manager API" })
@info(#{ version: "1.0.0" })
@server("http://localhost:8000", "Local development")
@useAuth(ApiKeyAuth<ApiKeyLocation.cookie, "sessionid">)
@route("/api/v1")
namespace TaskManagerApi;
