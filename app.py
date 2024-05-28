from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import pickle
import os
import numpy as np
import joblib  # To load your logistic regression model
from gensim.models.fasttext import FastText

import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)


app = Flask(__name__)

global jobs
global option_save
jobs = []


def docvecs(embeddings, docs):
    vecs = np.zeros((len(docs), embeddings.vector_size))
    for i, doc in enumerate(docs):
        valid_keys = [term for term in doc if term in embeddings.key_to_index]
        docvec = np.vstack([embeddings[term] for term in valid_keys])
        docvec = np.sum(docvec, axis=0)
        vecs[i,:] = docvec
    return vecs



@app.route('/')
def homepage():
    # print('Jobs', jobs)
    return render_template('index.html', jobs=get_jobs())

# @app.route('/categories/<category>')
# def category(category):
#     filtered_jobs = [job for job in jobs if job['category'] == category]
#     print(filtered_jobs)
#     return render_template('category.html', category = category, jobs = filtered_jobs)

@app.route('/job/<int:job_id>')
def job(job_id):
    job = next((job for job in jobs if job['id'] == job_id), None)

    if job:
        return render_template('job.html', job=job)
    else:
        return "Job not found."


@app.route('/categories', methods=['GET'])
def select_category():
    category = request.args.get('category')
    if category:
        filtered_jobs = [job for job in jobs if job['category'] == category]
        return render_template('index.html', jobs = filtered_jobs)
    else:
        return redirect(url_for('homepage'))

def predict_job_category(job_description):
    # Tokenize the content of the .txt file so as to input to the saved model
    # Here, as an example,  we just do a very simple tokenization
    tokenized_data = job_description.split(' ')
    

    # Load your language model (FastText)
    jobFT = FastText.load("/Users/sunitaverma/Desktop/Flask/JobFlask/models/desc_FT.model")

    jobFT_wv = jobFT.wv

    # Generate vector representation of the tokenized data
    jobFT_dvs = docvecs(jobFT_wv, [tokenized_data])
    # Load the LR model
    pkl_filename = ("/Users/sunitaverma/Desktop/Flask/JobFlask/models/descFT_LR.pkl")
    with open(pkl_filename, 'rb') as file:
        model = pickle.load(file)

    # Predict the label of tokenized_data
    y_pred = model.predict(jobFT_dvs)
    y_pred = y_pred[0]

    # Set the predicted message
    predicted_message = y_pred
    print(predicted_message)
    return predicted_message


@app.route('/create_job', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        category_new = ""
        # Retrieve job creation form data
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        job_category = request.form.get('job_category')
        company = request.form.get('company')
        location = request.form.get('location')
        salary = request.form.get('salary')
        # Get the action value to determine if "Classify Job" or "Save Job" is clicked
        action = request.form.get('action')
        print(request.form.get('action'))
        print("-------------------------")
        print(action)

        # If "Classify Job" is clicked, predict category and update dropdown
        if action == "classify":

            predicted_category = predict_job_category(job_description)
            # print("upper: ", predicted_category)
            return render_template('create_job.html', predicted_category = predicted_category,job_title = job_title, job_description = job_description, job_category = job_category,
                                   company=company,location=location,salary=salary)
        
        # If "Save Job" is clicked, add the job to the list
        if action == "save":

            if job_category == "":
                print("idhar", category_new)
                new_job = {
                    'title': job_title,
                    'description': job_description,
                    'category': predict_job_category(job_description),
                    'company': company,
                    'location': location,
                    'salary': salary,
                    'id': len(jobs) + 1  # Assign a unique ID
                }
                print(new_job)
                jobs.append(new_job)
                print(jobs)

            else:
                # job_category = predicted_category
                print("udhar")
                new_job = {
                    'title': job_title,
                    'description': job_description,
                    'category': job_category,
                    'company': company,
                    'location': location,
                    'salary': salary,
                    'id': len(jobs) + 1  # Assign a unique ID
                }
                print(new_job)
                jobs.append(new_job)
                print(jobs)


                # option_save = True

                # get_jobs(new_job)

                # return render_template('create_job.html', predicted_category = job_category,job_title = job_title, job_description = job_description, job_category=job_category,
                #                    company=company,location=location,salary=salary)
            return redirect(url_for('homepage'))
        
        return render_template('create_job.html')
    
    return render_template('create_job.html')

           

# def get_category_recommendations(job_title, job_description):
#     # Use your language model to generate category recommendations based on job title and description
#     # You may use your logistic regression model for classification
#     # Implement your logic to predict categories based on job_title and job_description
#     predicted_categories = lr_model.predict([job_description])  # Example, replace with your own logic
#     return predicted_categories 


def parse_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Initialize a dictionary to store the job data
            job_data = {
                'id': len(jobs) + 1,  # Assign a unique ID for each job
                'title': '',
                'company': '',
                'description': '',
                'salary': '',
                'category': '',
                'location': ''
            }

            # Split the content by lines
            lines = content.split('\n')
            # print(lines)

            # Loop through the lines to extract the fields
            for line in lines:
                if line.startswith('Title: '):
                    job_data['title'] = line[7:]  # Remove the "Title: " prefix
                elif line.startswith('Company: '):
                    job_data['company'] = line[9:]  # Remove the "Company: " prefix
                elif line.startswith('Description: '):
                    job_data['description'] = line[13:]  # Remove the "Description: " prefix
                elif line.startswith('Salary: '):
                    job_data['salary'] = line[8:]  # Remove the "Salary: " prefix
                elif line.startswith('Category: '):
                    job_data['category'] = line[10:]  # Remove the "Category: " prefix
                elif line.startswith('Location: '):
                    job_data['location'] = line[10:]  # Remove the "Location: " prefix

            # Check if all required fields have been found
            if all(job_data.values()):
                jobs.append(job_data)  # Append the job data to the jobs list
                print(f"Processed: {file_path}")
                # print(jobs)
            else:
                print(f"Skipped: {file_path} (Missing fields)")
    except Exception as e:
        print(f"Error parsing {file_path}: {str(e)}")


# if __name__ == '__main__':
    
def get_jobs(new_job = ""):
    text_files_directory = os.path.join(os.getcwd(), 'jobdata')

    for filename in os.listdir(text_files_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(text_files_directory, filename)
            parse_text_file(file_path)
    # print('here', jobs)
    return jobs

    
app.run(debug=False)

