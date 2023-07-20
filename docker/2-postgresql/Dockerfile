FROM postgis/postgis:12-3.3-alpine

# Allow connections; we don't map out any ports so only linked docker containers can connect    
# Customize default user/pass/db
ENV POSTGRES_DB ckan
ENV POSTGRES_USER ckan
ARG POSTGRES_PASSWORD
ARG DS_RO_PASS


EXPOSE 5432