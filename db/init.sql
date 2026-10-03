-- Runs once on first container init (empty data volume) via docker-entrypoint-initdb.d
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
