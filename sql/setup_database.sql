-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Criação do usuário e concessão de permissões
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON db_name.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
