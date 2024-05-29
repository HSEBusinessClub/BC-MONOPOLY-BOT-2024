FROM postgres
ENV POSTGRES_DB bot-db
ENV POSTGRES_USER bot-user
ENV POSTGRES_PASSWORD qwerty123
COPY init.sql /docker-entrypoint-initdb.d/