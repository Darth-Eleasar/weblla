# Frontend - Huella App

Esta carpeta contiene una aplicación React (Vite) mínima que consume la API en `/api/huellas/`.

Requisitos:
- Node.js 18+ (nvm o instalador oficial)

Instalación y ejecución:

```powershell
cd frontend
npm install
npm run dev
```

La app correrá por defecto en `http://localhost:5173` y consumirá la API en `http://localhost:8000/api/huellas/`.

Notas:
- Si tu backend no está en la misma máquina/host, ajusta `API_URL` en `src/components/HuellaList.jsx` (usar URL completa con http://host:puerto/api/huellas/).
- Asegúrate de que CORS está permitido en el backend (en `huella_project/settings.py` ya hay `corsheaders` y `CORS_ALLOW_ALL_ORIGINS = DEBUG`).
- Para construir para producción: `npm run build` y servir el contenido de `dist/` mediante un servidor.
