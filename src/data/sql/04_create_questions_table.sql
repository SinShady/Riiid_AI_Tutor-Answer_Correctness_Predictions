DROP TABLE IF EXISTS questions;

-- Create a table for the questions data
CREATE TABLE questions
(
    question INTEGER,
    bundle_id INTEGER,
    correct_answer INTEGER,
    part INTEGER,
    tags CHAR(50)
);
