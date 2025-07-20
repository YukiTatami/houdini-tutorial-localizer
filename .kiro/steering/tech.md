# Technology Stack

## Architecture
- **Application Type**: Hybrid CLI/Web application with modular architecture
- **Design Pattern**: Service-oriented with clear separation of concerns
- **Processing Model**: Asynchronous job queue for batch processing
- **API Design**: RESTful API with OpenAPI specification
- **Deployment**: Container-based with Docker support

## Frontend
- **Framework**: React 18+ with TypeScript
- **UI Library**: Material-UI (MUI) for consistent design
- **State Management**: Redux Toolkit for complex state
- **Build Tool**: Vite for fast development and optimized builds
- **Styling**: CSS Modules with Tailwind CSS utilities
- **Testing**: Jest + React Testing Library

## Backend
- **Primary Language**: Python 3.10+
- **Web Framework**: FastAPI for high-performance async API
- **Translation Engine**: 
  - Primary: Google Cloud Translation API
  - Alternative: DeepL API for higher quality
  - Fallback: Local models (Helsinki-NLP/Opus-MT)
- **Queue System**: Celery with Redis for background jobs
- **Database**: PostgreSQL with SQLAlchemy ORM
- **File Processing**: 
  - Video: ffmpeg-python for subtitle extraction
  - Documents: PyPDF2, python-docx, beautifulsoup4
- **Testing**: pytest with coverage

## Development Environment
- **Package Management**: 
  - Python: Poetry for dependency management
  - Node.js: npm with lockfile
- **Version Control**: Git with conventional commits
- **Code Quality**:
  - Python: Black formatter, Flake8 linter, mypy type checker
  - JavaScript/TypeScript: ESLint, Prettier
- **Documentation**: Sphinx for API docs, Storybook for UI components

## Common Commands
```bash
# Backend Development
poetry install              # Install Python dependencies
poetry run dev              # Start FastAPI development server
poetry run test             # Run Python tests
poetry run lint             # Run linters and formatters

# Frontend Development  
npm install                 # Install Node dependencies
npm run dev                 # Start Vite dev server
npm run build              # Build production bundle
npm run test               # Run Jest tests
npm run storybook          # Start Storybook

# Database
poetry run alembic upgrade head    # Run migrations
poetry run alembic revision        # Create new migration

# Docker
docker-compose up          # Start all services
docker-compose run tests   # Run test suite in container
```

## Environment Variables
```bash
# API Keys
GOOGLE_TRANSLATE_API_KEY=   # Google Cloud Translation
DEEPL_API_KEY=              # DeepL API (optional)

# Database
DATABASE_URL=postgresql://user:pass@localhost/houdini_localizer
REDIS_URL=redis://localhost:6379/0

# Application
APP_ENV=development         # development, staging, production
LOG_LEVEL=INFO             # DEBUG, INFO, WARNING, ERROR
SECRET_KEY=                # Application secret key

# Storage
UPLOAD_PATH=/tmp/uploads   # File upload directory
OUTPUT_PATH=/tmp/outputs   # Processed file output

# Feature Flags
ENABLE_BATCH_PROCESSING=true
MAX_CONCURRENT_JOBS=5
```

## Port Configuration
- **Frontend Dev Server**: 3000
- **Backend API**: 8000
- **PostgreSQL**: 5432
- **Redis**: 6379
- **Storybook**: 6006
- **API Documentation**: 8000/docs (Swagger UI)

## External Services
- **Translation APIs**: Google Cloud Translation, DeepL
- **Storage**: Local filesystem (development), S3-compatible (production)
- **Monitoring**: Sentry for error tracking
- **Analytics**: Plausible for privacy-friendly usage metrics