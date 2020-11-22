DROP TABLE IF EXISTS example_test;

-- Create a table for the example_test data 
CREATE TABLE example_test
(
    row_id INTEGER,
    group_num INTEGER,
    timestamp NUMERIC(11),
    user_id INTEGER,
    content_id INTEGER,
    content_type_id INTEGER,
    task_container_id INTEGER,
    prior_question_elapsed_time NUMERIC(8),
    prior_question_had_explanation CHAR(5),
    prior_group_answers_correct CHAR(100),
    prior_group_responses CHAR(100)
);