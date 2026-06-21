use reddit_leaderboards;

CREATE TABLE subreddit_leaderboard(
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    subreddit VARCHAR(100) UNIQUE,
    subreddit_name_prefixed VARCHAR(255) NOT NULL,
    created_utc FLOAT NOT NULL,
    subreddit_subscribers BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

