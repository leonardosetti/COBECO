# COBECO Frontend — Dockerfile (nginx + Vanilla JS)
# Multi-stage: build Tailwind → serve with nginx

# ============================================================
# BUILD STAGE — Tailwind CSS compilation
# ============================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Instala dependências para build
COPY package*.json ./
RUN npm install

# Copia fontes
COPY src ./src
COPY tailwind.config.js ./
COPY postcss.config.js ./

# Build Tailwind CSS
RUN npx tailwindcss -i ./src/styles/input.css -o ./src/styles/output.css --minify

# ============================================================
# RUNTIME STAGE — nginx serving static files
# ============================================================
FROM nginx:alpine AS runtime

# Copia configuração nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.dev.conf /etc/nginx/nginx.dev.conf

# Copia arquivos buildados
COPY --from=builder /app/src /usr/share/nginx/html

# Cria usuário não-root e diretórios necessários
RUN adduser -D -H -h /usr/share/nginx/html nginxuser && \
    chown -R nginxuser:nginxuser /usr/share/nginx/html /var/cache/nginx /var/log/nginx /etc/nginx/nginx.conf && \
    mkdir -p /run/nginx && chown nginxuser:nginxuser /run/nginx

USER nginxuser

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]