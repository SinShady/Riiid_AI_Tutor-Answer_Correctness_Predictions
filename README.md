# Riiid---Answer-Correctness-Prediction
Predicting Student Performance on future interactions with an AI tutor

## Table of Contents

### Reports
- [Presentation PowerPoint](https://github.com/SinShady/Riiid_AI_Tutor-Answer_Correctness_Predictions/blob/main/reports/StudentPredictions_ppt.pdf.pdf)

### Notebooks
- [Final Notebook](https://github.com/SinShady/Riiid_AI_Tutor-Answer_Correctness_Predictions/blob/main/notebooks/final/report.ipynb)

### Helpful Resources
 - [Riiid AIEd Challenge 2020 Kaggle](https://www.kaggle.com/c/riiid-test-answer-prediction)

- [UNESCO Institute for Education Statistics](http://uis.unesco.org/)

## Issues in Education
First, I’d like to talk about some issues in education today. According to data gathered by the UNESCO Institute, in 2018, 260 million children weren’t attending school. Of the children that we’re attending school, more than half of young students around the globe did not meet minimum reading and math standards. This is in part due to the fact that many students don’t have access to personalized learning.

Education was already in a tough place before COVID forced many schools to shutdown and switch to remote learning. I created this map in Tableau with data from UNESCO Institute.

<b>School Closure Due to COVID-19 May 2020</b>
![COVID MAP](/reports/figures/COVID_map.png)

## Education with Artificial Intelligence
 Artificial Intelligent solutions can change the current education system in terms of attendance, engagement, and individualized attention. It could potentially provide equal opportunity in education to anyone with an internet connection. With these goals in mind, RIIID Labs developed AI tutors.

Aiming to rethink traditional ways of learning, RIID Labs launched EdNet this year, the world’s largest open database for AI education. The database, which is hosted on Kaggle.com, contains data on more than 100 million student interactions across almost 400 thousand students for over 13,000 questions.

## Student Performance Predictions on AI tutor
I will be predicting whether the student will answer incorrect, or correct for future questions. The purpose of these predictions is to help evaluate and guide the success of the AI tutors. The AI tutor can become more individualized to a student’s needs if they know the predicted performance. For example, it could provide more questions and lectures on topics it sees the student is predicted to be weak in.

# The Data

This is the distribution of our target variable - answers - in the Ednet Database. We can see students are getting over twice as many answers correct than incorrect.

![Class Distribution](/reports/figures/class_imbalance.png)

Also included in the database are topics numbered from 1-7. Ednet has not provided the information for which number belongs to which topic, but that’s understandable given consideration of student privacy. Here we can see some topics have a greater class imbalance than others. For example, students on average seem to be performing better on topic 1 than on topic 4. Topic 5 seems to be very popular.

![Parts](/reports/figures/parts.png)

Other Features in the dataset included cumulative timestamps per user, prior question elapsed time, and if the prior question had an explanation. We can see here that most times, there were no explanations on the prior questions

![Prior Explanations](/reports/figures/prior_q_explanation.png)

I also engineered features such as the cumulative question count per user and cumulative average time per question per user, which we can see here. On average, students spent longer on questions they answered correctly.

![Prior Explanations](/reports/figures/Average_Time_Per_Question.png)

# Modeling
 As the dataset of over 100 million student interactions was too big for my sole computer to handle, I used a subset - 1 million interactions to train my models. After trying numerous types of models such as Logistic Regression and K Nearest Neighbors as well as a few boosting ensembles, my best performing model is a Random Forest Classifier from the Scikit-learn library with an accuracy of 60%

 A confusion matrix provides us with more details on how the model is performing. We are getting 63% accuracy on the correct answer predictions and 56% accuracy on the incorrect answer predictions

 ![RF Confusion Matrix](/reports/figures/rf_matrix.png)

 While 60% isn’t the greatest accuracy, on the brightside it is doing much better than my first simple linear regression model, which just predicted almost everything as correct but achieved an overall accuracy of 64%. This was due to the class imbalance of having many more correct than incorrect answers in the dataset, which I then used the SMOTE method from imblearn library to resample and address the issue.

  ![FSM Confusion Matrix](/reports/figures/fsm_matrix.png)

# Conclusion
We can use these predictions to improve and prove the success of AI tutors. Knowing how the student is likely to perform in the future and give better insight for the AI to individualize education and personalize the learning experience for each student to achieve the best results.

AI tutors could be a much needed change in our education system to provide equal opportunity and improve the success of students around the globe.
