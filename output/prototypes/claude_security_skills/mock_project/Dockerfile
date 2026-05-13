FROM node:latest

ENV DB_PASSWORD=production_secret_123
ENV API_TOKEN=tok_live_abcdef

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y curl vim

EXPOSE 3000
CMD ["node", "server.js"]
