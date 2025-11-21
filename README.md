## Technology Stack

- **Django 5.2** - Web framework
- **HTMX 1.9.10** - Dynamic interactions
- **Tailwind CSS** - Styling
- **Requests** - API client
- **Poetry** - Dependency management

## Installation

### Prerequisites
- Python 3.13+
- Poetry

### Setup

1. Clone the repository:
```bash
cd django-mealdb
```

2. Install dependencies:
```bash
poetry install
```

3. Run migrations:
```bash
poetry run python manage.py migrate
```

4. Start the development server:
```bash
poetry run python manage.py runserver
```

5. Open your browser and navigate to:
```
http://127.0.0.1:8000
```
