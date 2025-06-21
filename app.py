import streamlit as st 
from joblib import load 
import pandas as pd

model= load("employee_retention_prediction.joblib")

st.title("🌟 Employee Retention Prediction Website")

st.header("Enter Employee Info")

st.markdown("Predict if an employee is likely to change their job.")

gender_map = {'Male': 0, 'Female': 1, 'Other': 2} 
relevent_experience_map = {'Has relevant experience': 0, 'No relevant experience': 1} 
enrolled_university_map = {'no_enrollment': 0, 'Full time course': 1, 'Part time course': 2} 
education_level_map = {'Primary School': 0, 'High School': 1, 'Graduate': 2, 'Masters': 3, 'Phd': 4} 
major_discipline_map = {'STEM': 0, 'Business Degree': 1, 'Arts': 2, 'Humanities': 3, 'Other': 4, 'No Major': 5}
experience_map = {'<1': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                  '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11-20': 15, '>20': 21} 
company_size_map = {'<10': 0, '10-49': 1, '50-99': 2, '100-500': 3, '500-999': 4, '1000-4999': 5, '5000-9999': 6, '10000+': 7} 
company_type_map = {'Pvt Ltd': 0, 'Funded Startup': 1, 'Early Stage Startup': 2, 'Public Sector': 3, 'NGO': 4, 'Other': 5} 
last_new_job_map = {'never': 0, '1': 1, '2': 2, '3': 3, '4': 4, '>4': 5} 

with st.form("prediction_form"):
    gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
    relevant_experience = st.selectbox('Relevant Experience', ['Has relevant experience', 'No relevant experience'])
    enrolled_university = st.selectbox('Enrolled in University', ['no_enrollment', 'Full time course', 'Part time course'])
    education_level = st.selectbox('Education Level', ['Primary School', 'High School', 'Graduate', 'Masters', 'Phd'])
    major_discipline = st.selectbox('Major Discipline', ['STEM', 'Business Degree', 'Arts', 'Humanities', 'Other', 'No Major'])
    experience = st.selectbox('Experience (Years)', ['<1', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11-20', '>20'])
    company_size = st.selectbox('Company Size', ['<10', '10-49', '50-99', '100-500', '500-999', '1000-4999', '5000-9999', '10000+'])
    company_type = st.selectbox('Company Type', ['Pvt Ltd', 'Funded Startup', 'Early Stage Startup', 'Public Sector', 'NGO', 'Other'])
    last_new_job = st.selectbox('Last New Job (Years)', ['never', '1', '2', '3', '4', '>4'])
    city_development_index = st.slider('City Development Index', 0.0, 1.0, 0.5)
    training_hours = st.slider('Training Hours', 0, 400, 20)
    submitted = st.form_submit_button("Predict")

if submitted:
    input_df = pd.DataFrame({
        'gender': [gender],
        'relevent_experience': [relevant_experience],
        'enrolled_university': [enrolled_university],
        'education_level': [education_level],
        'major_discipline': [major_discipline],
        'experience': [experience_map[experience]],
        'company_size': [company_size],
        'company_type': [company_type],
        'last_new_job': [last_new_job_map[last_new_job]],
        'city_development_index': [city_development_index],
        'training_hours': [training_hours]})
        
    input_df['gender'] = input_df['gender'].map(gender_map)
    input_df['relevent_experience'] = input_df['relevent_experience'].map(relevent_experience_map)
    input_df['enrolled_university'] = input_df['enrolled_university'].map(enrolled_university_map)
    input_df['education_level'] = input_df['education_level'].map(education_level_map)
    input_df['major_discipline'] = input_df['major_discipline'].map(major_discipline_map)
    input_df['company_size'] = input_df['company_size'].map(company_size_map)
    input_df['company_type'] = input_df['company_type'].map(company_type_map)
    input_df['last_new_job'] = input_df['last_new_job'].map(last_new_job_map)

try:
    columns = [
    'gender', 'relevent_experience', 'enrolled_university',
    'education_level', 'major_discipline', 'experience',
    'company_size', 'company_type', 'last_new_job','city_development_index','training_hours']
    input_df = input_df.reindex(columns=columns)    
    prediction= model.predict(input_df)    
    st.header("Prediction Result")
    
    if prediction[0]==0:
        st.success("Data Scientist is not looking for a job change.")
    else:
        st.error("Data Scientist is looking for a job change.")

except Exception as e:
    st.error(f"Prediction failed: {e}")