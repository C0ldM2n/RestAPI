    uvicorn main:app --reload
---
    alembic revision --autogenerate
    alembic upgrade head
---
export $(xargs < .env)
env to virtual env.
---
**TODO List**: 
- [x] venv -> pipenv
- [x] alembic ini -> /migrations/
- [x] models v1 -> v2 (orm.mapped)
- [x] pydantic-settings (.env file)
- ? (in sublime 2 variants)
- [x] routers and models
- 
- [ ] fix import s in models
- [ ] fill the tables (for test)
- [ ] Base metadata - sqlalchemy
- ////
- [ ] tests
