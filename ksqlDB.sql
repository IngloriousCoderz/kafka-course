-- 1. Creating a stream
CREATE STREAM login_attempts (username VARCHAR, ip_address VARCHAR, status VARCHAR)
WITH (KAFKA_TOPIC='login_logs', VALUE_FORMAT='JSON');

-- 2. Filtering a stream
CREATE STREAM failed_logins AS
    SELECT username, ip_address
    FROM login_attempts
    WHERE status = 'FAILED';

-- 3. Aggregating data
CREATE TABLE failed_login_count AS
    SELECT username, COUNT(*)
    FROM login_attempts
    WINDOW TUMBLING (SIZE 10 MINUTES)
    WHERE status = 'FAILED'
    GROUP BY username;

-- 4. Join data
CREATE STREAM enriched_logins AS
    SELECT l.username, l.status, u.user_info
    FROM login_attempts l
    INNER JOIN users_table u ON l.username = u.username;

-- 5. Continuous query
SELECT * FROM ORDERS EMIT CHANGES;
