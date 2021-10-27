all:
	uvicorn fasttrace.main:app --reload


run-jaeger:
	docker run --name jaeger -p 13133:13133 -p 16686:16686 -p 4317:55680 -d --restart=unless-stopped jaegertracing/opentelemetry-all-in-one
