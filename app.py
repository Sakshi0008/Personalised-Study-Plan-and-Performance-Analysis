

from flask import Flask, render_template, request
import pandas as pd
import joblib
import plotly.express as px
import plotly.io as pio
from generate_plan import generate_cluster_based_study_plan

app = Flask(__name__)

# Load model and dataset
model = joblib.load("student_cluster_model.pkl")
data = pd.read_csv("All_Translated_Student_Data_With_Gender.csv")
subjects = ['English', 'Maths', 'Marathi', 'History', 'Geography', 'Science']
data['Cluster'] = model.predict(data[subjects])

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            reg_no = int(request.form["reg_no"])
            student_row = data[data['Registration Number'] == reg_no]
            
            if student_row.empty:
                return render_template("index.html", error="Student not found.")
            
            student_row = student_row.iloc[0]
            study_plan = generate_cluster_based_study_plan(student_row, subjects, data)
            

            # Prepare data for visualization
            student_marks = student_row[subjects].to_dict()
            performance_analysis = {
                "average_score": round(student_row[subjects].mean(), 2),
                "strongest_subject": study_plan['strongest_subject'],
                "weakest_subject": study_plan['weakest_subject'],
                "cluster_avg": study_plan['cluster_average']
            }

            # Create the bar chart for subject scores
            fig_scores = px.bar(
                x=subjects,
                y=student_marks.values(),
                labels={'x': 'Subjects', 'y': 'Scores'},
                title="Student's Subject Scores"
            )
            scores_chart = pio.to_html(fig_scores, full_html=False)

            # Create pie chart for performance breakdown
            performance_labels = ['Good Performance', 'Moderate Performance', 'Needs Improvement']
            performance_values = [
                sum(data[data['Cluster'] == 0]['Total Marks'] > performance_analysis['average_score']),  # Example values
                sum(data[data['Cluster'] == 1]['Total Marks'] <= performance_analysis['average_score']),
                sum(data[data['Cluster'] == 2]['Total Marks'] == performance_analysis['average_score'])
            ]
            fig_performance = px.pie(
                names=performance_labels,
                values=performance_values,
                title="Cluster Performance Distribution"
            )
            performance_pie_chart = pio.to_html(fig_performance, full_html=False)

            # Pass the student's name here
            student_name = student_row['Student Name']  # Assuming 'Name' is the column for the student's name

            return render_template(
                "student_dashboard.html", 
                student_name=student_name,
                student_marks=student_marks,
                study_plan=study_plan,
                performance_analysis=performance_analysis,
                scores_chart=scores_chart,
                performance_pie_chart=performance_pie_chart
            )

        except ValueError:
            return render_template("index2.html", error="Invalid registration number format.")
    
    return render_template("index2.html")


if __name__ == "__main__":
    app.run(debug=True)
