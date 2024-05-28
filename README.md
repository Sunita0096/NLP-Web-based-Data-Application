# NLP-Web-based-Data-Application

---

## Overview:

Welcome to our NLP-based job search website developed using the Flask web framework. This website serves as a platform for job seekers to explore existing job advertisements and for employers to create new job listings. One of the key features of this website is the integration of a machine learning model trained in Milestone I, which recommends job categories for newly created job adverts. By leveraging natural language processing (NLP) techniques, we aim to reduce human error, increase job exposure to relevant candidates, and enhance the overall user experience of the job seeking website.

---

## Model Training:

For the job category recommendation task, we employed a machine learning model trained on job descriptions and titles. The model was developed using the FastText algorithm with a vector size of 200. Additionally, we utilized a logistic regression model for classification purposes. These models were trained to accurately categorize job advertisements and provide relevant recommendations to employers during the job creation process.

---

### Functionality for Job Seekers:
- **Job Display:** Users can browse open job adverts displayed on the homepage and view full job details by clicking on a job summary. They can also view jobs listed by category and access full job details within selected categories.

### Functionality for Employers:
- **Create New Job Listing:** Employers can create new job listings by providing information such as title, description, and salary. Upon job creation, the website recommends a list of categories based on the job description/title. Employers have the flexibility to override these recommendations and select their own categories.

---

## Website Layout and Design:

The layout and design of the website are flexible, allowing for easy navigation and intuitive user experience. We drew inspiration from industry examples such as the Job Browsing Page and Employer site of seek.com.au, ensuring a visually appealing and functional interface.

---
## Getting Started:

To run the JobSeeker website locally, follow these steps:

1. Install Flask and any required dependencies.
2. Clone the repository to your local machine.
3. Navigate to the project directory and run the Flask application.
4. Access the website through the provided URL.
   
---
## Conclusion:

Our NLP-based job search website offers a seamless experience for both job seekers and employers, powered by machine learning for job category recommendations. By combining advanced NLP techniques with web development, we aim to revolutionize the job search process and connect candidates with relevant opportunities effectively.

