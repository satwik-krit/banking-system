-- DROP TABLE IF EXISTS users;
CREATE TABLE Users (
    password VARCHAR(10) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    age INT NOT NULL CHECK (age > 0),
    phone VARCHAR(15) NOT NULL,
    inactive TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY(username)
);


-- DROP TABLE IF EXISTS Account;
CREATE TABLE Account (
    balance INT NOT NULL CHECK (balance >= 0),
    created DATE NOT NULL,
    frozen TINYINT(1) NOT NULL DEFAULT 0,
    username VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(username),
    FOREIGN KEY(username) REFERENCES Users(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- DROP TABLE IF EXISTS FixedDepo;
CREATE TABLE FixedDepo (
    fdID INT AUTO_INCREMENT,
    fdName VARCHAR(30) DEFAULT 'Fixed Deposit',
    username VARCHAR(50) NOT NULL UNIQUE,
    principal INT NOT NULL CHECK(principal > 0),
    interest INT NOT NULL CHECK(interest > 0),
    maturedate DATE NOT NULL,
    matured TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY(fdID),
    FOREIGN KEY(username) REFERENCES Users(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- DROP TABLE Transactions;
CREATE TABLE Transactions (
    transID INT AUTO_INCREMENT,
    payerID VARCHAR(50) NOT NULL UNIQUE,
    receieverID VARCHAR(50) NOT NULL UNIQUE,
    transDate DATE,
    amount INT NOT NULL CHECK(amount > 0),
    comment TINYTEXT,
    PRIMARY KEY(transID),
    FOREIGN KEY(payerID) REFERENCES Users(username)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
    FOREIGN KEY(payerID) REFERENCES Users(username)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

-- DROP TABLE Updates;
CREATE TABLE Updates (
    username VARCHAR(50) NOT NULL,
    content TINYTEXT NOT NULL,
    updateDate DATE,
    FOREIGN KEY(username) REFERENCES Users(username)
);
