# FastAPI

This part presents an overview of FastAPI tool for educational purposes.

## Introduction to FastAPI

FastAPI is—a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.


=== "Creator"

    * **Name**: Sebastián Ramírez, also known as @tiangolo on GitHub
    * **Background**: Sebastián is a software developer from Colombia who currently resides in Berlin, Germany
    * **Contribution**: He is the creator of several popular open-source projects, including FastAPI, Typer, SQLModel, and Asyncer

=== "Use Cases"

    * **API Development**
        * Building RESTful APIs: FastAPI is designed to create robust and efficient RESTful APIs with minimal code.
        * GraphQL APIs: FastAPI supports GraphQL, allowing for flexible and powerful API designs.

    * **Microservices Development**
        * Microservices Architecture: FastAPI is ideal for developing microservices due to its simplicity and performance.
        * Service-to-Service Communication: Facilitates communication between different microservices in a distributed system.
    * **Real-time Applications**
        * WebSockets: Supports real-time communication using WebSockets for applications like chat apps and live updates.
        * Server-Sent Events (SSE): Enables server-to-client communication for real-time data streaming.
    * **Machine Learning and Data Science
        * Model Serving: Expose machine learning models as APIs for predictions and inference.
        * Data Pipelines: Automate and orchestrate data processing and model training workflows.
    * **Backend Services**
        * Authentication and Authorization: Implement secure authentication and authorization mechanisms.
        * CRUD Operations: Handle Create, Read, Update, and Delete operations for various resources.
    * **Automation and Orchestration**
        * Task Scheduling: Schedule and manage background tasks and jobs.
        * Workflow Automation: Orchestrate complex workflows involving multiple steps and services.
    * **Integration with Other Tools**
        * Database Integration: Seamlessly integrate with databases like PostgreSQL, MySQL, and MongoDB.
        * Third-Party Services: Connect with external APIs and services for enhanced functionality.
    * **Custom Applications**
        * Custom Business Logic: Implement specific business logic tailored to unique requirements.
        * Prototyping: Quickly prototype and iterate on new ideas and features.

### Key Points

* High performance, on par with Node.js and Go
* Easy to use and learn
* Based on standard Python type hints

## Main Characteristics of FastAPI

### Performance: 

* **High Performance**: Built on Starlette for the web parts and Pydantic for the data parts. By using asynchronous programming, FastAPI can handle more requests per second compared to many other frameworks. Benchmarks show that it is one of the fastest Python web frameworks available.

* **Asynchronous Capabilities**: FastAPI supports asynchronous request handling, enabling better performance, especially for I/O-bound operations.

### Ease of Use

* **Simple Syntax**: FastAPI is known for its simple and intuitive syntax. Developers can quickly build APIs without extensive boilerplate code.

* **Minimal Setup**: Getting started with FastAPI is straightforward, with minimal setup required to create a fully functional API.

* **Interactive Development**: The framework allows for an interactive development experience with instant feedback, making it easier for developers to debug and iterate.

### Validation and Serialization

* **Pydantic Integration**: FastAPI leverages Pydantic for data validation and serialization. This ensures that data is validated against the schema before processing, preventing many common bugs.

* **Automatic Type Checking**: By using Python type hints, FastAPI can automatically generate validation rules, ensuring that the data conforms to the expected types.

* **Error Handling**: FastAPI provides detailed error messages when validation fails, helping developers quickly identify and fix issues.

### Dependency Injection

* **Built-in Dependency Injection**: FastAPI has built-in support for dependency injection, allowing developers to manage and inject dependencies into their functions easily.

* **Modularity**: This feature promotes modular and reusable code, as dependencies can be defined once and used across multiple endpoints.

* **Scalability**: With dependency injection, it’s easier to scale applications by managing complex dependencies in a clear and organized manner.

### Auto-generated Documentation

* **Interactive API Docs**: FastAPI automatically generates interactive API documentation using Swagger UI and ReDoc. These docs allow developers and users to interact with the API directly from the browser.

* **Self-updating**: The documentation is always up-to-date with the code, thanks to FastAPI's reliance on Python type hints and Pydantic models.

* **User-friendly**: The auto-generated docs are highly user-friendly and provide comprehensive information about each endpoint, making it easier for developers to understand and use the API.

### Security Features

* **OAuth2 and JWT**: FastAPI has built-in support for OAuth2 and JSON Web Tokens (JWT), making it easier to implement secure authentication and authorization mechanisms.

* **Security Dependencies**: The framework provides security dependencies that can be used to enforce authorization rules, ensuring that only authorized users can access certain endpoints.

* **HTTPS and CORS**: FastAPI supports HTTPS and Cross-Origin Resource Sharing (CORS) out-of-the-box, enhancing the security of web applications.

### Key Points:

* High performance due to asynchronous capabilities
* Simple and intuitive, quick development
* Automatic documentation with Swagger UI and ReDoc
* Robust data validation with Pydantic
* Built-in dependency injection and security

## Architecture of FastAPI

### Components Overview

* **ASGI Server**: Explain that FastAPI is built on the ASGI (Asynchronous Server Gateway Interface), which allows for async programming.

* **Starlette**: Describe how Starlette provides the web microframework capabilities.
* **Pydantic**: Highlight how Pydantic is used for data validation and settings management.
* **Routing**: Explain the routing mechanism, how endpoints are defined using Python decorators.

### ASGI Server

ASGI (Asynchronous Server Gateway Interface):

* **Description**: ASGI is a specification that serves as a standard interface between asynchronous web servers and web applications or frameworks. It is designed to handle asynchronous programming, allowing for non-blocking operations and better performance.

* **Role in FastAPI**: FastAPI relies on ASGI to handle asynchronous requests, making it capable of high concurrency and efficient resource utilization. It enables FastAPI to support WebSockets, background tasks, and other async features seamlessly.

* **Popular ASGI Servers**: Examples include Uvicorn and Daphne, which can run ASGI applications like FastAPI.

### Starlette

Starlette Framework:

* **Description**: Starlette is a lightweight ASGI framework/toolkit for building high-performance asynchronous web applications and services. It provides the core functionality for routing, middleware, and server-side components in FastAPI.

* **Role in FastAPI**: FastAPI is built on top of Starlette, leveraging its features for handling web requests, middleware, WebSocket support, and more. This integration ensures that FastAPI applications are both fast and scalable.

* **Key Features**: Starlette includes support for sessions, authentication, WebSockets, and background tasks, all of which enhance the capabilities of FastAPI.

### Pydantic

Pydantic Library:

* **Description**: Pydantic is a data validation and settings management library that uses Python type annotations. It ensures that data conforms to predefined schemas, providing automatic type checking and serialization.

* **Role in FastAPI**: FastAPI uses Pydantic for data validation, serialization, and documentation. Pydantic models are used to define request bodies, query parameters, and response schemas.

* **Key Features**: Pydantic provides robust error handling, detailed validation error messages, and support for complex data types, making it easier to handle and validate input data in FastAPI applications

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
```

### Routing

Routing in FastAPI:

* **Description**: Routing refers to the process of defining URL paths and associating them with specific handler functions that process requests and generate responses.

* **Role in FastAPI**: FastAPI uses a simple and intuitive decorator-based syntax for defining routes. This makes it easy to create and manage endpoints.

* **Key Features**: FastAPI supports path parameters, query parameters, and request body parsing through its routing system. It also provides automatic validation and documentation for defined routes.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```


### Key Points

* **ASGI**: Core of asynchronous capabilities
* **Starlette**: Foundation for web components
* **Pydantic**: Ensures robust data handling
* **Routing**: Simplified with decorators

### Integration and Extensions

#### Middleware

Allows you to run code before and after each request. It's useful for tasks like logging, authentication, and request/response transformation.
To create middleware, you use the @app.middleware("http") decorator on a function. 

from fastapi import FastAPI, Request
import time

```python
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

#### Custom Components

Allow you to extend the framework's functionality. This can include creating custom middleware, customizing the API documentation UI, or adding new features to your API

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("Before request")
        response = await call_next(request)
        print("After request")
        return response
```

#### Third-Party Integrations

FastAPI supports integration with third-party libraries and services. You can use any ASGI middleware that follows the ASGI specification.

```python
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()
app.add_middleware(UnicornMiddleware, some_config="rainbow")
```


### Key Points:

* Flexible middleware integration
* Extendable with custom components
* Easy integration with third-party tools


## Benefits and Limitations

### Benefits

* High performance and efficient handling of concurrent requests.
* Ease of development with type hints and auto-generated docs.
* Strong community support and extensive documentation.
* Automatic interactive documentation enhances developer experience.

### Limitations

* Newer framework with a smaller ecosystem compared to Django or Flask.
* Requires understanding of asynchronous programming and type hints.
* May not be suitable for all types of applications, especially those not requiring high performance or asynchronous capabilities.
