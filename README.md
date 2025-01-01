![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)

# Demo Microservice Intercommunication

This repository contains a demo application designed to showcase microservice-to-microservice communication and how to instrument services using OpenTelemetry. It demonstrates the flow of HTTP requests across multiple simulated services and visualizes the corresponding traces in a distributed tracing platform like Grafana Tempo.

## Key Features

- Microservice Chaining:
  - Multiple instances of the same application simulate intercommunication;
  - The chaining is achieved by configuring the EXTERNAL_CALL_URL environment variable:
    - microservice-1 makes a request to microservice-2;
    - microservice-2 makes a request to microservice-3;
    - Each instance contributes its own response, creating a combined output.
- Simulate Delays:
  - Use the RESPONSE_TIME environment variable to introduce artificial delays in the processing of each microservice;
  - The delay is specified in milliseconds, helping simulate real-world latency.
- OpenTelemetry Instrumentation:
  - Automatically collects and exports traces for HTTP requests, template rendering, and inter-service communication;
  - Visualizes the entire request flow across simulated services with detailed spans.
- Jinja2 Integration:
  - Each instance renders dynamic HTML using Jinja2 templates, showcasing template loading and rendering spans in traces.

## Purpose

This application is intended for conceptual and educational purposes. It is designed to help developers understand:
- How to instrument Python-based microservices using OpenTelemetry;
- How distributed tracing works in a microservices architecture;
- How to visualize end-to-end service communication using tools like Grafana Tempo;
- How latency or delays affect the overall request flow and response times.

## How It Works

- This is a single Python application. The chaining is simulated by deploying multiple instances of the same app and updating the EXTERNAL_CALL_URL environment variable to point to the next service in the chain;
- Requests to microservice-1 trigger a chain of requests across microservice-2 and microservice-3;
- Use the RESPONSE_TIME environment variable to simulate processing delays in any instance. For example:
  - Setting RESPONSE_TIME=500 introduces a 500ms delay in processing.
- All trace data is collected and sent to the configured OpenTelemetry collector, which exports it to a backend such as Grafana Tempo;
- Users can analyze the traces to observe inter-service communication, performance bottlenecks, and detailed spans for operations like HTTP calls and template rendering.

---