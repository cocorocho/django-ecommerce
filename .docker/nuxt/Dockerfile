FROM node:21-slim as base

ARG DJANGO_URL
ENV DJANGO_URL=${DJANGO_URL}

WORKDIR /code
COPY ./client .

RUN npm install

# Dev
FROM base as development
EXPOSE 3000
CMD ["npm", "run", "dev"]


# Prod
FROM base as production
RUN npm run build
CMD ["node", ".output/server/index.mjs"]