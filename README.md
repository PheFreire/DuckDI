<p align="center">
  <img src="assets/logo.png" alt="DuckDI Logo" width="150" />
</p>

# 🦆 DuckDI

**DuckDI** is a minimal and powerful dependency injection framework for Python, inspired by duck typing and explicit architecture.

It allows you to declare your interfaces, register adapters, and resolve dependencies at runtime using a simple TOML file.

---

## 🚀 Features

- ✅ Clean and lightweight API  
- ✅ Zero dependencies  
- ✅ Fully type-safe  
- ✅ Uses TOML to map interfaces to adapters  
- ✅ Clear and informative error messages  
- ✅ Environment-based configuration (`INJECTIONS_PATH`)

---

## 📦 Installation

Using [Poetry](https://python-poetry.org):

```bash
poetry add duckdi
```

Or manually with pip:

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

### 2. Register an adapter

```python
from duckdi import register

class PostgresUserRepository:
    def get_user(self, user_id: str) -> dict:
        return {"id": user_id, "name": "John Doe"}

register(PostgresUserRepository)
```

### 3. Create your injection payload

Create a file called `injections.toml`:

```toml
[injections]
"user_repository" = "postgres_user_repository"
```

### 4. Set the environment variable

You **must** set the path to the injection file using the `INJECTIONS_PATH` environment variable:

```bash
export INJECTIONS_PATH=./injections.toml
```

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

Raised when no injection payload file is found at the given path.

### `InvalidAdapterImplementationError`

Raised when the registered adapter does not properly implement the expected interface.

---

## 📁 Project Structure

```
duckdi/
├── pyproject.toml
├── README.md
├── src/
│   └── duckdi/
│       ├── duck.py
│       ├── __init__.py
│       ├── errors/
│       │   ├── __init__.py
│       │   ├── invalid_adapter_implementation_error.py
│       │   └── missing_injection_payload_error.py
│       └── utils/
│           ├── __init__.py
│           ├── buffer_readers.py
│           └── serializers.py
└── tests/
```

---

## 🧩 Advanced Example

You can register multiple adapters and resolve them dynamically:

```python
from duckdi import Interface, register, Get

@Interface
class INotifier:
    def send(self, msg: str): ...

class EmailNotifier:
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

## 📄 License

Licensed under the MIT License.  
See the [LICENSE](LICENSE) file for more information.

---

## 👤 Author

Developed with ❤️ by **PhePato**  
Pull requests, feedback and contributions are welcome!
