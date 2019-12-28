DROP TABLE IF EXISTS User;


CREATE TABLE User(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    lastName TEXT NOT NULL,
    birthDate DATE NOT NULL,
    email TEXT NOT NULL
);



