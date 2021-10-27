# FastAPI + db (sqlalchemy, sqlmodel, asyncpg[encode/databases]) + opentelemetry (tracing)

Sample demo code instrumenting tracing FastAPI.

FastAPI -> Jaeger (OTEL/grpc 4317)

## Running

- Run `$ make run-jager` to run jager tracing, open http://localhost:16686 to access the Jaeger UI
- Execute `$ make` to run the fastapi app
- Access the available endpoint to trigger sending telemetry trace event
  - example: http://localhost:8000/name
