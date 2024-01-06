CREATE DATABASE IF NOT EXISTS  `warikanman`;

DROP USER IF EXISTS `warikanman`@`%`;
CREATE USER warikanman IDENTIFIED BY 'warikanman';
GRANT ALL PRIVILEGES ON warikanman.* TO 'warikanman'@'%';

USE `warikanman`;

CREATE TABLE IF NOT EXISTS `projects`(
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `project_id` VARCHAR(255) NOT NULL UNIQUE, 
    `datetime` TIMESTAMP NOT NULL,
    `participant_number` INT NOT NULL
);
CREATE TABLE IF NOT EXISTS `users`(
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` VARCHAR(255) NOT NULL UNIQUE,
    `name` VARCHAR(255) NOT NULL
);
CREATE TABLE  IF NOT EXISTS `payments`(
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `project_id` VARCHAR(255) NOT NULL,
    `user_id` VARCHAR(255) NOT NULL,
    `datetime` TIMESTAMP NOT NULL,
    `amount` INT NOT NULL,
    `message` VARCHAR(255) NOT NULL
);

ALTER TABLE `payments` ADD FOREIGN KEY (`project_id`)
 REFERENCES `projects`(`project_id`) ON DELETE CASCADE ON UPDATE CASCADE;