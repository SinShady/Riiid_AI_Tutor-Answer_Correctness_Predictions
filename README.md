# Riiid---Answer-Correctness-Prediction
Predicting Student Performance on future interactions with an AI tutor

## Table of Contents

### Reports
- [Presentation PowerPoint](https://github.com/SinShady/Riiid_AI_Tutor-Answer_Correctness_Predictions/blob/main/reports/StudentPredictions_ppt.pdf.pdf)

### Notebooks
- [Final Notebook](https://github.com/SinShady/Riiid_AI_Tutor-Answer_Correctness_Predictions/blob/main/notebooks/final/report.ipynb)
- [Create SQL Database notebook](https://github.com/SinShady/Riiid_AI_Tutor-Answer_Correctness_Predictions/blob/main/notebooks/create_SQL_database.ipynb)

### Helpful Resources
- [Riiid AIEd Challenge 2020 Kaggle](https://www.kaggle.com/c/riiid-test-answer-prediction)

- [Riiid Labs Website](https://riiidlabs.ai/)

- [UNESCO Institute for Education Statistics](http://uis.unesco.org/)

# Project Overview

## Issues in Education
First, I’d like to talk about some issues in education today. According to data gathered by the [UNESCO Institute](http://uis.unesco.org/), in 2018, 260 million children weren’t attending school. Of the children that we’re attending school, more than half of young students around the globe did not meet minimum reading and math standards. This is in part due to the fact that many students don’t have access to personalized learning.

Education was already in a tough place before COVID forced many schools to shutdown and switch to remote learning. I created this map in Tableau with data from [UNESCO Institute](http://uis.unesco.org/).

<b>School Closure Due to COVID-19 May 2020</b>
![COVID MAP](/reports/figures/COVID_map_no_labels.png)

## Education with Artificial Intelligence
 Aiming to rethink traditional ways of learning, [Riiid Labs](https://riiidlabs.ai/) developed Artificial Intelligent tutors. Artificial Intelligent solutions can change the current education system in terms of attendance, engagement, and individualized attention. It could potentially provide equal opportunity in education to anyone with an internet connection. 

In efforts to improve upon the performance of AI tutors, [Riiid Labs](https://riiidlabs.ai/) launched EdNet this year, the world’s largest open database for AI education. The database, which is hosted on [Kaggle](https://www.kaggle.com/c/riiid-test-answer-prediction), contains data on more than 100 million student interactions across almost 400 thousand students for over 13,000 questions.

## Student Performance Predictions on AI tutor
I will be predicting whether the student will answer incorrectly, or correctly for future questions. The purpose of these predictions is to help evaluate and guide the success of the AI tutors. The AI tutor can become more individualized to a student’s needs if they know the predicted performance. For example, it could provide more questions and lectures on topics it sees the student is predicted to be weak in.

## Setup Instructions in case you would like to work in this repository

If you are missing required software (e.g. Anaconda, PostgreSQL), please run the following command in Bash (designed for Mac computers):
```bash
# installs necessary requirements
# note: this may take anywhere from 10-20 minutes
sh src/requirements/install.sh
```

For Windows computers, you may need to manually ensure that you have installed [Anaconda](https://docs.anaconda.com/anaconda/install/) and [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads).

### `riiid-env` conda Environment

This project relies on you using the [`environment.yml`](environment.yml) file to recreate the `riiid-env` conda environment. To do so, please run the following commands *in your terminal*:

```bash
# create the riiid-env conda environment
conda env create -f environment.yml

# activate the riiid-env conda environment
conda activate riiid-env

# if needed, make riiid-env available to you as a kernel in jupyter
python -m ipykernel install --user --name riiid-env --display-name "Python 3 (riiid-env)"
```

Note that this may take 10 or more minutes depending on internet speed.

**Windows Note:** The same versions of these packages are not available for Windows computers, so all Windows users should use the `windows.yml` file instead of `environment.yml` (this file was generated on Windows 10)

**Catalina Note:** You may need to modify the `prefix` at the very bottom of `environment.yml` if you are on macOS Catalina.  Run `conda env list` in your terminal to determine the appropriate path by looking at the paths of your existing conda environment(s).  Modify `environment.yml` then try running the installation commands listed above again.

# The Data

## Data Download

To download the relevant data and import it into a SQL database, run the [Create SQL Database notebook](https://github.com/SinShady/Riiid_AI_Tutor-Answer_Correctness_Predictions/blob/main/notebooks/create_SQL_database.ipynb). Using PostreSQL saves space for data storage and reading, which is useful as the data is large, containing over 100 million rows.

The data is hosted on [Kaggle](https://www.kaggle.com/c/riiid-test-answer-prediction) as part of an active competition and can be downloaded [here](https://www.kaggle.com/c/riiid-test-answer-prediction) .

## Data Understanding

Our data contains 3 relevant tables for our project - train, questions, and lectures

<b>Description of Features in Train</b>

`row_id` - ID for the row.

`timestamp` - the time between this user interaction and the first event from that user.

`user_id` - ID for the user.

`content_id` - ID for the user interaction

`content_type_id` - 0 if the event was a question being posed to the user, 1 if the event was the user watching a lecture. Every row with 1 has an answered_correctly value of not answered(-1). Filtering out all rows with content id 1 filters out all the unanswered questions. This is the culprit of our 100% predictions on unanswered.

`task_container_id` - ID for the batch of questions or lectures. For example, a user might see three questions in a row before seeing the explanations for any of them. Those three would all share a task_container_id. Monotonically increasing for each user.

`user_answer` - the user's answer to the question, if any. Read -1 as null, for lectures.

`answered_correctly` - if the user responded correctly. Read -1 as null, for lectures.

`prior_question_elapsed_time` - How long it took a user to answer their previous question bundle, ignoring any lectures in between. The value is shared across a single question bundle, and is null for a user's first question bundle or lecture. Note that the time is the total time a user took to solve all the questions in the previous bundle.

`prior_question_had_explanation` - Whether or not the user saw an explanation and the correct response(s) after answering the previous question bundle, ignoring any lectures in between. The value is shared across a single question bundle, and is null for a user's first question bundle or lecture. Typically the first several questions a user sees were part of an onboarding diagnostic test where they did not get any feedback.

Count of unique values in each column:
- `row_id`: 101230332
- `timestamp`: 72821015
- `user_id`: 393656
- `content_id`: 13782
- `content_type_id`: 2
- `task_container_id`: 10000
- `user_answer`: 5
- `answered_correctly`: 3
- `prior_question_elapsed_time`: 3258
- `prior_question_had_explanation`: 2

Categorical Features: `content_type_id`, `user_answer`, `answered_correctly`, `prior_question_had_explanation`

<b>Description of Features in Questions</b>

`question` - foreign key for the train/test content_id column, when the content type is question (0).

`bundle_id` - code for which questions are served together.

`correct_answer` - the answer to the question. Can be compared with the train user_answer column to check if the user was right.

`part` - top level category code for the question.

`tags` - one or more detailed tag codes for the question. The meaning of the tags will not be provided, but these codes are sufficient for clustering the questions together.

Count of unique values in each column
- `question`: 13523
- `bundle_id`: 9765
- `correct_answer`: 4
- `part`: 7
- `tags`: 1519

Categorical Features: `correct_answer`, `part`

<b>Description of Features in Lectures</b>

Note - Wont be using this table for our model

`lecture_id` - foreign key for the train/test content_id column, when the content type is lecture (1).

`part` - top level category code for the lecture.

`tag` - one tag codes for the lecture. The meaning of the tags will not be provided, but these codes are sufficient for clustering the lectures together.

`type_of` - brief description of the core purpose of the lecture

Count of unique values in each column
- `lecture_id`: 418
- `tag`: 151
- `part`: 7
- `type_of`: 4

## Data Engineering

A I am only predicting student answers on questions, there was no need for the lectures data. I joined the train and questions tables on the `content_id` and `question` columns and dropped the columns `user_answer` (since real training data could not have this column), `tags`, and `content_id`.

Since the original features were not enough for my model to make accurate predictions, I engineered the following features.
- `user_question_count` - the cumulative count of questions each user has answered
- `avg_time_per_question` - the cumulative average time spent per question per user
- `question_difficulty` - the ratio of wrong answers to total answers per question

## Data Visualization

This is the distribution of our target variable - answers - in the Ednet Database. We can see students are getting over twice as many answers correct than incorrect.

![Class Distribution](/reports/figures/class_imbalance.png)

Features in the dataset include cumulative timestamps per user, and prior question elapsed time, which is shown here as a violin plot. The widest part shows how long most questions took to answer, which is around 18 seconds. The next wide part is at 0 since the prior question elapsed time for the first question for every user is 0. We can see that most users tend to get the first question wrong. The small white dot shows the average time per question – 20 seconds. Overall, the shapes of both violins are very similar which suggests that this feature will only help a little in predicting student answers.

![Prior Question Elapsed Time](/reports/figures/prior_question_time_violin.png)

Another feature in the dataset was topics numbered from 1-7 shown by this plot. Ednet has not provided the information for which number belongs to which topic, but that’s understandable given consideration of student privacy. Here we can see some topics have a greater class imbalance than others, which means this feature will help our model more accurately predict student outcomes. For example, students on average seem to be performing better on topic 1 than on topic 4. Topic 5 seems to be very popular.

![Parts](/reports/figures/parts.png)

Another feature was if the prior qestion had an explanation or not. As it looks like most prior questions did not have an explantion, this feature doesnt seem immensly helpful for my model.

![Prior Explanations](/reports/figures/prior_q_explanation.png)

To improve my model performance, I also engineered features such as the cumulative question count per user, cumulative average time per question per user, and question difficulty which we can see represented here on a scale of 0 to 10 as a right skewed normal distribution. This new feature significantly increased my model performance. I calculated this by dividing the number of incorrect answers by the amount of total answers per unique question in the database. For all the questions with a difficulty of 0, every student answered correctly, while for all the questions with a difficulty of 10, nobody answered correctly. The average question, has a difficulty around 2, meaning about 80% of students answered those questions correctly.

![Prior Explanations](/reports/figures/Question_difficulty.png)

# Modeling
 As the dataset of over 100 million student interactions was too big for my sole computer to handle, I used a subset - 1 million interactions to train my models. After trying numerous types of models such as Logistic Regression and K Nearest Neighbors as well as a few boosting ensembles, my best performing model is a Random Forest Classifier from the Scikit-learn library with an overall accuracy of 68%

Here is a confusion matrix representing the results of my first simple model. We can see that it is over predicting correctly answered but underpredicting incorrect answers. This was due to the class imbalance of having many more correct than incorrect answers in the dataset. To address the issue, I used the SMOTE method from imblearn library to resample the training data.

  ![FSM Confusion Matrix](/reports/figures/fsm_matrix.png)

Here is a confusion matrix of the final model, providing more details on how the model is performing. We are getting 64% accuracy on the correct answer predictions and 65% accuracy on the incorrect answer predictions

 ![RF Confusion Matrix](/reports/figures/random_forest_matrix.png)

# Conclusion
In conclusion, we can use these predictions to improve and prove the success of AI tutors. Knowing how the student is likely to perform in the future can give better insight for the AI to individualize education and personalize the learning experience for each student to achieve the best results. I strongly believe that if features about student demographics were included in the database, the model accuracy would greatly improve and student success in underprivileged areas could be addressed and improved by the AI tutor as well.

AI tutors could be a much needed change in our education system to provide equal opportunity and improve the success of students around the globe.

# Next Steps
- As engineering new features is what improved my model the most in the end, in the futures, I would like to brainstorm more creative ideas for features to add.
- With the limitations of my computer, I was only able to use 1% of the dataset for my current model, even after using the dask package for parallel computing. Being able to fit the entire dataset of 100 million student interactions could improve my model.
- I want to try a neural network model and see how it does with this database.
- I would also like to create a deployable web app for my model using flask.
