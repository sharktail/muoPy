drop database if exists muoPy;
create database muoPy;
use muoPy;

CREATE TABLE Users 
(
	Id int NOT NULL AUTO_INCREMENT,
	UserName varchar(255) NOT NULL Unique,
	Password varchar(255) NOT NULL,
	LastName varchar(255) NOT NULL,
	FirstName varchar(255) NOT NULL,
	Address varchar(255),
	City varchar(255),
	Primary Key(Id)	
)ENGINE=INNODB;

