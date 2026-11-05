-- events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL,
    time TEXT NOT NULL,
    location TEXT NOT NULL,
    host_id INTEGER NOT NULL,
    FOREIGN KEY (host_id) REFERENCES users(id)
);

-- users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

-- guests table
CREATE TABLE guests (
    id INTEGER PRIMARY KEY,
    event_id INTEGER,
    guest_id INTEGER,
    FOREIGN KEY (guest_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);