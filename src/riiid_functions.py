import psycopg2
import pandas as pd

def engineer_data(data, question_difficulty):

    # read in questions and lectures tables from database
    DBNAME = "riiid_education"
    conn = psycopg2.connect(dbname=DBNAME)
    cursor = conn.cursor()
    questions = pd.read_sql("SELECT * FROM questions;", conn)
    conn.close()
    
    # Drop all rows with answered_correctly is blank (-1) since these are lectures, not questions
    data = data[data.content_type_id != 1]
    df = data.merge(questions, left_on='content_id', right_on='question', how='left')
    
    # Drop the columns we don't need
    # question is already there as content id
    # user_answer doesn't make sense to have - we can't know that in advance
    # There are only 2 unique content_type_ids and we dropped one type, no point having a column of zeros
    df.drop(['tags', 'question', 'user_answer', 'content_type_id'], axis=1, inplace=True)
    
    # Engineer Feature for how many questions this user has answered prior
    df["user_question_count"] = df.groupby("user_id").cumcount() + 1
    
    # Engineer Feature for average time per questions per user for prior questions
    cumsum = df.groupby("user_id")["prior_question_elapsed_time"].cumsum()
    count = df.groupby("user_id").cumcount() + 1
    df["avg_time_per_question"] = round(cumsum/count, 0)
    
    # Merge question_difficulty_binned into main DataFrame
    df= df.merge(question_difficulty, on='content_id', how="left")
    
    # Change string object type to bool on prior_question_had_explanation
    df['prior_question_had_explanation'] = df['prior_question_had_explanation'].astype('bool')
    
    return df

def time_reformat_seconds(millis):
    seconds=(millis/1000)%60
    seconds = int(seconds)

    return seconds