FROM postgres:16

# Copie les fichiers de configuration temporaires
COPY pg_hba.conf /tmp/pg_hba.conf
COPY postgresql.conf /tmp/postgresql.conf
COPY server.crt /tmp/server.crt
COPY server.key /tmp/server.key

# Copie le script shell de customisation d'initdb
COPY docker-entrypoint-init-custom.sh /docker-entrypoint-initdb.d/init-custom.sh

# Copie tous les scripts d'initialisation SQL et SH dans le dossier approprié
COPY docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/

# Fixe les permissions sur la clé privée et les fichiers de conf
RUN chmod 600 /tmp/server.key && \
    chown postgres:postgres /tmp/server.key /tmp/server.crt /tmp/pg_hba.conf /tmp/postgresql.conf

RUN chmod +x /docker-entrypoint-initdb.d/init-custom.sh

# (optionnel) Fixe les permissions sur tous les scripts d'init pour éviter les soucis
RUN chmod -R 755 /docker-entrypoint-initdb.d/

# (optionnel) Fixe le propriétaire pour tous les scripts d'init
RUN chown -R postgres:postgres /docker-entrypoint-initdb.d/
