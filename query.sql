CREATE TABLE Users (
    password VARCHAR(10) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    age INT NOT NULL CHECK (age > 0),
    inactive TINYINT(1) NOT NULL DEFAULT 0,
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
    fdID INT AUTO INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    principal INT NOT NULL CHECK(principal > 0),
    interest INT NOT NULL CHECK(interest > 0),
    maturedate DATE NOT NULL,
    matured TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY(username) REFERENCES Users(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Transactions (
    transID INT AUTO INCREMENT,
    payerID VARCHAR(50) NOT NULL UNIQUE,
    receieverID VARCHAR(50) NOT NULL UNIQUE,
    transDate DATE,
    amount INT NOT NULL CHECK(amount > 0),
    comment TINYTEXT DEFAULT "Empty",
    PRIMARY KEY(transID),
    FOREIGN KEY(payerID) REFERENCES Users(username)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
    FOREIGN KEY(payerID) REFERENCES Users(username)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE Updates (
    username VARCHAR(50) NOT NULL,
    content TINYTEXT NOT NULL,
    date DATE,
);
