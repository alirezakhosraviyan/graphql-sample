CREATE DATABASE images_service_db;
CREATE USER images_service_user WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE images_service_db TO images_service_user;