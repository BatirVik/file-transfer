# Frontend
## Environment variables
**VITE_API_URL**
> URL to the backend api

## Run server
Build files
```bash
npm run build
```
Start the server to serve files
```bash
cd server
poetry install --no-root
poetry run uvicorn -p 8080 app:app
```