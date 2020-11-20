DROP TABLE IF EXISTS train;

-- Create a table for the train data
CREATE TABLE train
(
    row_id INTEGER,
    timestamp INTEGER,
    user_id INTEGER,
    content_id INTEGER,
    content_type_id INTEGER,
    task_container_id INTEGER,
    user_answer INTEGER,
    answered_correctly INTEGER,
    prior_question_elapsed_time NUMERIC(5),
    prior_question_had_explanation CHAR(5)
);