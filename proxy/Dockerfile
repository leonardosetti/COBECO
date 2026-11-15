# COBECO Proxy — nginx reverse proxy
# Single-stage: nginx alpine with custom config

FROM nginx:alpine

# Copia configuração nginx
COPY config-nginx-0003-proxy-nginx-v1.0.conf /etc/nginx/nginx.conf:ro

# Cria usuário não-root e diretórios necessários
RUN adduser -D -H -h /var/www nginxuser && \
    chown -R nginxuser:nginxuser /var/cache/nginx /var/log/nginx /etc/nginx/nginx.conf && \
    mkdir -p /run/nginx && chown nginxuser:nginxuser /run/nginx

USER nginxuser

EXPOSE 8380

CMD ["nginx", "-g", "daemon off;"]