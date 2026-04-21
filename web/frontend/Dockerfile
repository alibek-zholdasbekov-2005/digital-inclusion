# ---------- Stage 1: build ----------
FROM node:20-alpine AS build

WORKDIR /app

# Use BuildKit cache for faster rebuilds
COPY package.json ./
RUN npm install --no-audit --no-fund

COPY tsconfig.json tsconfig.node.json vite.config.ts ./
COPY postcss.config.js tailwind.config.js ./
COPY index.html ./
COPY public ./public
COPY src ./src

# Allow baking API URL into the production bundle
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# ---------- Stage 2: serve ----------
FROM nginx:1.27-alpine

# Replace default config with SPA-friendly one
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

# Render/most PaaS inject $PORT. Substitute at container start.
ENV PORT=8080
EXPOSE 8080

CMD ["/bin/sh", "-c", "envsubst '$PORT' < /etc/nginx/conf.d/default.conf > /tmp/default.conf && mv /tmp/default.conf /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
