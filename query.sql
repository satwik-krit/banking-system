DROP DATABASE IF EXISTS Bank;
CREATE DATABASE Bank;
USE Bank;

CREATE TABLE Users (
    password VARCHAR(10) NOT NULL,
    username VARCHAR(50),
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    phone VARCHAR(15) NOT NULL,
    inactive TINYINT(1) NOT NULL DEFAULT 0,

    PRIMARY KEY(username),
    CHECK(age > 0)
);

CREATE TABLE Account (
    balance INT NOT NULL,
    created DATE NOT NULL,
    frozen TINYINT(1) NOT NULL DEFAULT 0,
    username VARCHAR(50),

    PRIMARY KEY(username),
    CHECK(balance >= 0),
    FOREIGN KEY(username) REFERENCES Users(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE FixedDepo (
    fdName VARCHAR(30),
    username VARCHAR(50),
    principal INT NOT NULL,
    interest INT NOT NULL,
    creationdate DATE NOT NULL,
    timeperiod INT NOT NULL,
    maturedate DATE NOT NULL,
    withdrawn INT NOT NULL DEFAULT 0,

    PRIMARY KEY(fdName, username),
    CHECK(principal > 0),
    CHECK(interest > 0),
    CHECK(timeperiod BETWEEN 0 AND 10),
    CHECK(maturedate = DATE_ADD(creationdate, INTERVAL timeperiod YEAR)),
    FOREIGN KEY(username) REFERENCES Users(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Transactions (
    transID INT AUTO_INCREMENT,
    payerID VARCHAR(50) NOT NULL,
    receiverID VARCHAR(50) NOT NULL,
    transDate DATE NOT NULL,
    amount INT NOT NULL,
    comment TINYTEXT,

    PRIMARY KEY(transID),
    CHECK(amount > 0),
    FOREIGN KEY(payerID) REFERENCES Users(username)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
    FOREIGN KEY(payerID) REFERENCES Users(username)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE Updates (
    username VARCHAR(50) NOT NULL,
    baseContent TINYTEXT NOT NULL,
    extraContent TEXT NOT NULL,
    updateDate DATE,

    FOREIGN KEY(username) REFERENCES Users(username)
);

CREATE TABLE EnvInfo (
    DBCreationDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO EnvInfo 
VALUES ();