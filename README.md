<p align="center">
  <img src="assets/logo.png" alt="DuckDI Logo" width="150" />
</p>

# 🦆 DuckDI

**DuckDI** is a minimal, type-safe and runtime-resolvable dependency injection framework for Python — inspired by duck typing and clean architecture principles.

It empowers you to declare interfaces, register adapters, and resolve dependencies via a simple TOML-based injection map.

---

## 🚀 Features

- ✅ Clean, minimal, and explicit API  
- ✅ Zero runtime dependencies  
- ✅ Fully type-safe with `Protocol` support  
- ✅ Environment-based injection configuration (`INJECTIONS_PATH`)  
- ✅ Informative error handling  
- ✅ Singleton and transient adapter support  
- ✅ Runtime-validated adapters with structural checks  
- ✅ TOML-based mapping for clarity and separation of concerns  

---

## 📦 Installation

Using [Poetry](https://python-poetry.org):

```bash
poetry add duckdi
```

Or using pip:

```bash
pip install duckdi
```

---

## 🛠️ Usage

### 1. Define an interface

```python
from duckdi import Interface

@Interface
class IUserRepository:
    def get_user(self, user_id: str) -> dict: ...
```

> You can optionally use `@runtime_checkable` if you want to support `isinstance()` or `issubclass()` checks.

---

### 2. Register an adapter

```python
from duckdi import register

class PostgresUserRepository(IUserRepository):
    def get_user(self, user_id: str) -> dict:
        return {"id": user_id, "name": "John Doe"}

register(PostgresUserRepository)
```

For singleton behavior (one instance only):

```python
register(PostgresUserRepository, is_singleton=True)
```

---

### 3. Create your injection payload

Create a file named `injections.toml`:

```toml
[injections]
"user_repository" = "postgres_user_repository"
```

---

### 4. Set the environment variable

You **must** define the injection file path using the `INJECTIONS_PATH` environment variable:

```bash
export INJECTIONS_PATH=./injections.toml
```

---

### 5. Resolve dependencies at runtime

```python
from duckdi import Get

repo = Get(IUserRepository)
user = repo.get_user("123")
print(user)  # {'id': '123', 'name': 'John Doe'}
```

---

## 💥 Error Handling

### `MissingInjectionPayloadError`
Raised when the injection file is not found or not configured via `INJECTIONS_PATH`.

### `InvalidAdapterImplementationError`
Raised when the registered adapter does not implement the required interface.

### `InterfaceAlreadyRegisteredError`
Raised when an interface is registered twice with the same name or label.

### `AdapterAlreadyRegisteredError`
Raised when an adapter is registered more than once under the same label.

---

## 📁 Project Structure

```
duckdi/
├── pyproject.toml
├── README.md
├── src/
│   └── duckdi/
│       ├── __init__.py
│       ├── cli.py
│       ├── errors/
│       │   ├── __init__.py
│       │   ├── adapter_already_registered_error.py
│       │   ├── interface_already_registered_error.py
│       │   ├── invalid_adapter_implementation_error.py
│       │   └── missing_injection_payload_error.py
│       ├── injections/
│       │   ├── injections_container.py
│       │   ├── injections_payload.py
│       └── utils/
│           ├── __init__.py
│           ├── buffer_readers.py
│           ├── serializers.py
│           └── to_snake.py
└── tests/
    ├── test_register.py
    ├── test_get.py
    ├── test_interface.py
```

---

## 🧩 Advanced Example

Registering and resolving different services dynamically:

```python
from duckdi import Interface, register, Get

@Interface
class INotifier:
    def send(self, msg: str): ...

class EmailNotifier(INotifier):
    def send(self, msg: str):
        print(f"Sending email: {msg}")

register(EmailNotifier)

# injections.toml
# [injections]
# "notifier" = "email_notifier"

notifier = Get(INotifier)
notifier.send("Hello from DuckDI!")
```

---

## 🧪 Testing

DuckDI supports full static type checking. You can run tests with:

```bash
make test
```

Or directly:

```bash
pytest
```

To check types and formatting:

```bash
make check
```

---

## 📄 License

Licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Developed with ❤️ by **PhePato**  
Pull requests, discussions, and contributions are always welcome!
