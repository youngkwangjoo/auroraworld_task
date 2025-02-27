-- =============================================
-- ✅ users 테이블 정의
-- =============================================
CREATE TABLE users_customuser (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- ✅ feedmanager 테이블 정의
-- =============================================
CREATE TABLE feedmanager_weblink (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    category VARCHAR(100) DEFAULT 'personal',
    created_by_id INTEGER NOT NULL REFERENCES users_customuser(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE feedmanager_sharedweblink (
    id SERIAL PRIMARY KEY,
    web_link_id INTEGER NOT NULL REFERENCES feedmanager_weblink(id) ON DELETE CASCADE,
    recipient_id INTEGER NOT NULL REFERENCES users_customuser(id) ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES users_customuser(id) ON DELETE CASCADE,
    permission VARCHAR(10) DEFAULT 'read',
    UNIQUE (web_link_id, recipient_id)  
);
