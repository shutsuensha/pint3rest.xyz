FROM node:18-alpine

WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

COPY . .

# Запускаем проект
CMD ["npm", "run", "dev", "--", "--host"]
