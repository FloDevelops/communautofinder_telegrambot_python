DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
	`telegram_user_id` varchar(20) NOT NULL,
	`telegram_username` varchar(255) NOT NULL,
	`telegram_first_name` varchar(255),
	`telegram_last_name` varchar(255),
	`telegram_language_code` char(2),
    `telegram_chat_id` varchar(20) NOT NULL,
	`is_enabled` tinyint(1) NOT NULL DEFAULT 0,
    `has_accepted_communications` tinyint(1) NOT NULL DEFAULT 0,
	`preferred_city_id` varchar(3),
	`created_at` timestamp NOT NULL DEFAULT current_timestamp(),
	`last_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	PRIMARY KEY `telegram_user_id` (`telegram_user_id`)
);

DESCRIBE `users`;

INSERT INTO users (telegram_user_id, telegram_username, telegram_first_name, telegram_last_name, telegram_language_code, telegram_chat_id) VALUES ("123456", "myUsername", "John", "Doe", "en", "456789");


CREATE TABLE `searches` (
    `search_id` int(11) NOT NULL AUTO_INCREMENT,
    `telegram_user_id` varchar(20) NOT NULL,
    `search_type` enum('station', 'flex') NOT NULL,
    `city_id` varchar(3) NOT NULL,
    `area_min_lat` decimal(10,8) NOT NULL,
    `area_max_lat` decimal(10,8) NOT NULL,
    `area_min_lon` decimal(11,8) NOT NULL,
    `area_max_lon` decimal(11,8) NOT NULL,
    `start_date` datetime NOT NULL,
    `end_date` datetime NOT NULL,
    `search_status` enum('pending', 'running', 'completed', 'failed') NOT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
    `last_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
    PRIMARY KEY `search_id` (`search_id`),
    KEY `telegram_user_id` (`telegram_user_id`)
);

DESCRIBE `searches`;



CREATE TABLE `jobs` (
    `job_id` int(11) NOT NULL AUTO_INCREMENT,
    `telegram_user_id` varchar(20) NOT NULL,
    `search_id` int(11) NOT NULL,
    `search_type` enum('station', 'flex') NOT NULL,
    `city_id` varchar(3) NOT NULL,
    `area_min_lat` decimal(10,8) NOT NULL,
    `area_max_lat` decimal(10,8) NOT NULL,
    `area_min_lon` decimal(11,8) NOT NULL,
    `area_max_lon` decimal(11,8) NOT NULL,
    `start_date` datetime NOT NULL,
    `end_date` datetime NOT NULL,
    `job_status` enum('pending', 'completed', 'failed') NOT NULL,
    `job_result` json,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
    `last_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
    PRIMARY KEY `job_id` (`job_id`),
    KEY `telegram_user_id` (`telegram_user_id`),
    KEY `search_id` (`search_id`)
);

DESCRIBE `jobs`;