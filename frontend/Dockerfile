FROM node:18-alpine AS base

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN npm run build


FROM node:18-alpine AS final

WORKDIR /app

COPY --from=base /app/next.config.ts ./
COPY --from=base /app/package.json ./
COPY --from=base /app/package-lock.json ./
COPY --from=base /app/public ./public
COPY --from=base /app/.next ./.next

RUN npm install --omit=dev

EXPOSE 3000

CMD ["npm", "start"]
