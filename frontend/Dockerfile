FROM node:20-alpine

WORKDIR /app

# Copiamos package.json primero para aprovechar cache de Docker
COPY package*.json ./

# Instalamos dependencias
RUN npm install

# Copiamos el resto del código
COPY . .

# Construir la aplicación
RUN npm run build

# Exponemos el puerto de Vite
EXPOSE 5173

# Comando para modo desarrollo con hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
