CREATE TABLE Users (
    password VARCHAR(10) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(username)
);

CREATE TABLE Account (
    balance INT NOT NULL CHECK (balance > 0),
    created DATE NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(username),
    FOREIGN KEY(username) REFERENCES Users(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE FixedDepo (
    fdid INT AUTO INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    principal INT NOT NULL CHECK(principal > 0),
    interest INT NOT NULL CHECK(interest > 0),
    maturedate DATE NOT NULL,
    matured TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY(username) REFERENCES Users(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
