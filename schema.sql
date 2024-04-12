create table original (
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `document_number` VARCHAR(6) NOT NULL,
    `html` MEDIUMTEXT NOT NULL,
    `createAt` datetime NOT NULL default now(),
    `updateAt` datetime NOT NULL default now() on update now()
);

create table translated (
    `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `document_number` VARCHAR(6) NOT NULL,
    `html` MEDIUMTEXT NOT NULL,
    `createAt` datetime NOT NULL default now(),
    `updateAt` datetime NOT NULL default now() on update now()
);