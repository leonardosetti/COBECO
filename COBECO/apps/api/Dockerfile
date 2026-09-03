FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
COPY apps/api/package.json apps/api/package.json
COPY apps/web/package.json apps/web/package.json
COPY packages/shared/package.json packages/shared/package.json
RUN npm ci
COPY tsconfig.json ./
COPY apps/api apps/api
COPY packages/shared packages/shared
RUN npx prisma generate --schema apps/api/prisma/schema.prisma && npm run build --workspace apps/api
EXPOSE 3333
CMD ["npm", "run", "start", "--workspace", "apps/api"]
