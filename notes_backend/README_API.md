Ocean Professional Notes API

Quickstart
- Run migrations:
  python manage.py migrate
- Start server:
  python manage.py runserver 0.0.0.0:8000

Key endpoints
- GET /api/health/ -> {"message": "Server is up!"}
- GET /api/notes/ -> list notes (search, ordering, pagination supported)
- POST /api/notes/ -> create note
- GET /api/notes/{id}/ -> retrieve by UUID
- PUT /api/notes/{id}/ -> update
- PATCH /api/notes/{id}/ -> partial update
- DELETE /api/notes/{id}/ -> soft delete

Docs
- Swagger UI: /docs/
- ReDoc: /redoc/
- Raw schema: /swagger.json

Notes
- id in responses is the public UUID.
- Soft delete is applied; records remain in DB with deleted_at set.
