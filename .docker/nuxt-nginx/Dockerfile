FROM node:21-slim as base

ARG DJANGO_URL
ENV DJANGO_URL=${DJANGO_URL}

WORKDIR /code
COPY ./client .

RUN npm install
RUN npm run generate

##### Development #####
FROM base as development

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
#######################

##### Production #####
WORKDIR /code

FROM nginx:1.25 as production

WORKDIR /build
COPY --from=base /code/.output/public .
COPY ./nginx/default.conf.template /etc/nginx/templates/default.conf.template

CMD ["nginx", "-g", "daemon off;"]
########################