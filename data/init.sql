CREATE DATABASE test;
use test;

CREATE TABLE names (
    id INT NOT NULL AUTO_INCREMENT.
    f_name VARCHAR(15)
    l_name VARCHAR(25)
    phone_number UNSIGNED INT
    email VARCHAR(40)

    PRIMARY KEY (id)
);

INSERT INTO names
    (f_name, l_name, phone_number, email)
VALUES
    ('Betsy', 'Turner', NULL, 'bturner@yahoo.com'),
    ('Sombra', 'Colomar', '6235942179', NULL),
    ('John', 'Smith', '5208083505', NULL),
    ('Cole', 'Cassidy', NULL, 'highnoon@icloud.com');