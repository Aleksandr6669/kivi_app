# Flet App

A Flet app using the Flet extension.

## To Run the App

### 1. Install Dependencies

Install the dependencies from `pyproject.toml`:

```sh
poetry install
```

### 2. Build the App

Build the app for macOS:

```sh
poetry run flet build macos -v
```

```sh
flet build macos
```

Build the app for Web App PWA:

```sh
poetry run flet build web -v
```

```sh
flet build web
```

### 3. Run the App

Run the app:

```sh
poetry run flet run
```

```sh
flet run
```

Run the app ios:

```sh
poetry run flet run --ios  
```

```sh
flet run --ios  
```