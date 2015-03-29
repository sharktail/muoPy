drop database if exists muoPy;
create database muoPy;
use muoPy;

CREATE TABLE users 
(
	P_Id int NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255),
	Address varchar(255),
	City varchar(255)	
)ENGINE=INNODB;

