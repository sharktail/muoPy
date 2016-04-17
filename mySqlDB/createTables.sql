drop database if exists muoPy;
create database muoPy;
use muoPy;

CREATE TABLE Users 
(
	Id int NOT NULL AUTO_INCREMENT,
	UserName varchar(20) NOT NULL Unique,
	Password varchar(255) NOT NULL,
	LastName varchar(40) NOT NULL,
	FirstName varchar(40) NOT NULL,
	Email varchar(255) NOT NULL,
	Address varchar(255),
	City varchar(20),
	Primary Key(Id)	
)ENGINE=INNODB;

Create Table AccountInfo
( 
	Id int Not NULL AUTO_INCREMENT,
	Path varchar(40) NOT NULL, 
	LastLogin TIMESTAMP Default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PreviousLogin TIMESTAMP Default CURRENT_TIMESTAMP,
	User_Id INT, 
	INDEX User_Index(Id), 
	Foreign Key(User_Id) References Users(Id),
	Primary Key(Id)
)ENGINE=INNODB;