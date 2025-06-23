-- Crée l'utilisateur Prefect avec un mot de passe sécurisé
CREATE USER prefectsuperadmin WITH PASSWORD 'prefectsuperultrasecuremdp';

-- Crée la base Prefect et en donne la propriété à l'utilisateur Prefect
CREATE DATABASE prefect OWNER prefectsuperadmin;

-- Donne tous les droits sur la base Prefect à l'utilisateur Prefect
GRANT ALL PRIVILEGES ON DATABASE prefect TO prefectsuperadmin;
