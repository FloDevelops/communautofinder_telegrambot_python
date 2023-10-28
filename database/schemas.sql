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
	`created_at` timestamp NOT NULL DEFAULT current_timestamp(),
	`last_updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	PRIMARY KEY `telegram_user_id` (`telegram_user_id`)
);

DESCRIBE `users`;

INSERT INTO users (telegram_user_id, telegram_username, telegram_first_name, telegram_last_name, telegram_language_code, telegram_chat_id) VALUES ("123456", "myUsername", "John", "Doe", "en", "456789");