DROP TABLE IF EXISTS user;

DROP TABLE IF EXISTS product;

DROP TABLE IF EXISTS genre;

DROP TABLE IF EXISTS product_genre;

DROP TABLE IF EXISTS product_order;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    product_name TEXT UNIQUE NOT NULL,
    product_description TEXT,
    product_imdb_id TEXT NOT NULL,
    product_is_stock_left INTEGER NOT NULL,
    product_image_filename TEXT,
    price REAL NOT NULL CHECK (
        price >= 0
        AND price <= 1000000
    )
);

CREATE TABLE genre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    genre_name TEXT UNIQUE NOT NULL
);

CREATE TABLE product_genre(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY(product_id) REFERENCES product(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(genre_id) REFERENCES genre(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE product_order (
    id integer PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    country TEXT NOT NULL,
    city TEXT NOT NULL,
    street TEXT NOT NULL,
    house_number TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    email TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES user (id) ON UPDATE CASCADE ON DELETE NO ACTION,
    FOREIGN KEY (product_id) REFERENCES product (id) ON UPDATE CASCADE ON DELETE NO ACTION
);