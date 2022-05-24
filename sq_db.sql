CREATE TABLE IF NOT EXISTS contacts(
    id integer PRIMARY KEY AUTOINCREMENT,
    email text NOT NULL,
    username text NOT NULL,
    password text NOT NULL
);

CREATE TABLE IF NOT EXISTS name_lastname (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    lastname text NOT NULL
)