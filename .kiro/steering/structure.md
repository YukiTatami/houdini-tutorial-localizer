# Project Structure

## Root Directory Organization
```
houdini-tutorial-localizer/
├── .kiro/                    # Kiro spec-driven development files
│   ├── steering/             # Project steering documents
│   └── specs/                # Feature specifications
├── backend/                  # Python FastAPI backend application
├── frontend/                 # React TypeScript frontend application  
├── shared/                   # Shared types and utilities
├── scripts/                  # Development and deployment scripts
├── docs/                     # Project documentation
├── tests/                    # End-to-end integration tests
├── docker/                   # Docker configuration files
├── .github/                  # GitHub Actions workflows
├── pyproject.toml           # Python project configuration
├── package.json             # Node.js project configuration
├── docker-compose.yml       # Local development orchestration
└── README.md                # Project overview and setup guide
```

## Subdirectory Structures

### Backend (`backend/`)
```
backend/
├── app/
│   ├── api/                 # API endpoints
│   │   ├── v1/              # Version 1 API routes
│   │   │   ├── tutorials.py # Tutorial processing endpoints
│   │   │   ├── glossary.py  # Terminology management
│   │   │   └── jobs.py      # Job status endpoints
│   │   └── deps.py          # Common dependencies
│   ├── core/                # Core functionality
│   │   ├── config.py        # Configuration management
│   │   ├── security.py      # Authentication/authorization
│   │   └── exceptions.py    # Custom exceptions
│   ├── models/              # Database models
│   │   ├── tutorial.py      # Tutorial data model
│   │   ├── glossary.py      # Glossary entries
│   │   └── job.py           # Processing job model
│   ├── services/            # Business logic services
│   │   ├── translator.py    # Translation service interface
│   │   ├── extractor.py     # Text extraction service
│   │   ├── validator.py     # Translation validation
│   │   └── processor.py     # Tutorial processing pipeline
│   ├── db/                  # Database related
│   │   ├── base.py          # Database base configuration
│   │   └── session.py       # Database session management
│   ├── tasks/               # Celery background tasks
│   │   ├── translate.py     # Translation tasks
│   │   └── process.py       # Processing tasks
│   └── main.py             # FastAPI application entry point
├── alembic/                 # Database migrations
├── tests/                   # Backend unit tests
└── requirements.txt         # Python dependencies
```

### Frontend (`frontend/`)
```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── common/          # Shared UI components
│   │   ├── tutorial/        # Tutorial-related components
│   │   ├── glossary/        # Glossary management UI
│   │   └── layout/          # Layout components
│   ├── pages/               # Page-level components
│   │   ├── Dashboard.tsx    # Main dashboard
│   │   ├── TutorialList.tsx # Tutorial management
│   │   ├── ProcessJob.tsx   # Job processing view
│   │   └── Settings.tsx     # Application settings
│   ├── services/            # API client services
│   │   ├── api.ts           # Base API configuration
│   │   ├── tutorials.ts     # Tutorial API calls
│   │   └── glossary.ts      # Glossary API calls
│   ├── store/               # Redux store
│   │   ├── slices/          # Redux slices
│   │   └── hooks.ts         # Typed Redux hooks
│   ├── types/               # TypeScript type definitions
│   ├── utils/               # Utility functions
│   ├── App.tsx              # Root application component
│   └── main.tsx             # Application entry point
├── public/                  # Static assets
├── tests/                   # Frontend tests
└── package.json             # Frontend dependencies
```

### Shared (`shared/`)
```
shared/
├── types/                   # Shared TypeScript interfaces
│   ├── tutorial.ts          # Tutorial data types
│   ├── glossary.ts          # Glossary types
│   └── api.ts               # API response types
└── constants/               # Shared constants
    ├── languages.ts         # Supported languages
    └── formats.ts           # Supported file formats
```

## Code Organization Patterns
- **Domain-Driven Design**: Organize code by business domains (tutorials, glossary, jobs)
- **Service Layer Pattern**: Business logic encapsulated in service classes
- **Repository Pattern**: Database access through repository interfaces
- **Dependency Injection**: Use FastAPI's dependency injection for services
- **Component-Based UI**: React components follow atomic design principles

## File Naming Conventions
- **Python Files**: `snake_case.py` for modules and scripts
- **TypeScript/React**: `PascalCase.tsx` for components, `camelCase.ts` for utilities
- **Test Files**: `test_*.py` for Python, `*.test.tsx` for React
- **Configuration**: `.env` files for environment-specific config
- **Documentation**: `UPPERCASE.md` for root docs, `lowercase.md` for subdirectories

## Import Organization
```python
# Python imports order
# 1. Standard library imports
import os
import sys
from typing import List, Optional

# 2. Third-party imports
import fastapi
from sqlalchemy import Column

# 3. Local application imports
from app.core.config import settings
from app.models.tutorial import Tutorial
```

```typescript
// TypeScript imports order
// 1. External dependencies
import React from 'react';
import { useSelector } from 'react-redux';

// 2. Internal absolute imports
import { TutorialService } from '@/services/tutorials';
import { Button } from '@/components/common';

// 3. Relative imports
import { formatDate } from './utils';
import type { TutorialProps } from './types';
```

## Key Architectural Principles
- **Separation of Concerns**: Clear boundaries between frontend, backend, and business logic
- **Type Safety**: Full TypeScript coverage in frontend, Python type hints in backend
- **Async First**: Use async/await patterns throughout for scalability
- **API Versioning**: Version APIs from the start (`/api/v1/`)
- **Configuration as Code**: All configuration in version control
- **Test Coverage**: Maintain minimum 80% test coverage
- **Documentation**: Every module includes docstrings/JSDoc
- **Error Handling**: Consistent error response format across APIs
- **Logging**: Structured logging with correlation IDs
- **Security by Default**: Input validation, rate limiting, CORS configuration