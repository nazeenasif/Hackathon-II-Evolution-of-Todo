---
title: Full Stack Todo API
emoji: 📝
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: "3.11"
app_file: Dockerfile
---

# Full Stack Todo API

A FastAPI-based todo application with PostgreSQL database.

## Setup

### Environment Variables

Configure the following environment variables in your deployment platform:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql://username:password@localhost:5432/todo_app` |
| `SECRET_KEY` | JWT secret key | Required for production |
| `ENVIRONMENT` | Environment mode | `development` |
| `LOG_LEVEL` | Logging level | `info` |

### Database Setup

This application requires a PostgreSQL database. You can use:
- **Local PostgreSQL**: Install PostgreSQL locally
- **Supabase**: https://supabase.com (free tier)
- **Neon**: https://neon.tech (free tier)
- **Railway**: https://railway.app (free tier)

Example Supabase connection URL:
```
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
```

## Hugging Face Spaces Deployment

The Space runs on port 7860 and requires an external PostgreSQL database.

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set up .env file with your DATABASE_URL
echo "DATABASE_URL=postgresql://user:pass@localhost:5432/todo_app" > .env

# Run the application
uvicorn src.main:app --reload
```
