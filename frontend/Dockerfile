# frontend/Dockerfile
FROM node:21.7.1-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build

# Копируем собранные файлы в директорию, доступную через volume
CMD ["cp", "-r", "/app/build/.", "/frontend_static/"]

#FROM node:21.7.1-alpine
#WORKDIR /app
#COPY package*.json ./
#RUN npm install
#COPY . ./
#RUN npm run build
#CMD cp -r build result_build

