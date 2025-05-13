FROM docker.n8n.io/n8nio/n8n:latest
USER root
RUN apk add --update --no-cache docker-cli
RUN addgroup -S docker && addgroup node docker 

USER node
# Verificar la instalación
RUN docker --version