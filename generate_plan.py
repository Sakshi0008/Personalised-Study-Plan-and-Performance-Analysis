
def load_models():
    with open('dvcp\student_cluster_model.pkl', 'rb') as f:
        cluster_model = pickle.load(f)
    with open('dvcp\student_score_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return cluster_model, scaler


import plotly.express as px
import pandas as pd
import plotly.io as pio

def generate_cluster_based_study_plan(student_row, subjects, data):
    # Extract the subject scores
    subject_scores = student_row[subjects]
    average_score = subject_scores.mean()

    # Identify the strongest and weakest subjects
    strongest_subject = subject_scores.idxmax()
    weakest_subject = subject_scores.idxmin()

    # Get cluster number
    cluster = student_row['Cluster']
    
    # Get all students in the same cluster
    cluster_data = data[data['Cluster'] == cluster]
    cluster_avg = cluster_data[subjects].mean()

    # Define cluster label based on average score
    if average_score > cluster_avg.mean():
        cluster_label = "Good Performance"
    elif average_score < cluster_avg.mean():
        cluster_label = "Moderate Performance"
    else:
        cluster_label = "Needs Improvement"

    # Subject-specific tips
    subject_recommendations = {
    'Maths': {
        'strong': (
            "You're excelling in Mathematics, which is fantastic! To maintain and elevate your performance:\n"
            "- Practice 2–3 advanced problems daily from RD Sharma, RS Aggarwal, or Olympiad-level books.\n"
            "- Participate in online math quizzes or challenges.\n"
            "- Help classmates with math problems—it strengthens your own fundamentals.\n"
            "- Spend at least 30 minutes weekly reviewing chapters from earlier terms to keep them fresh."
        ),
        'weak': (
            "Math can be challenging, but consistent effort brings improvement. Here's your personalized plan:\n"
            "- Start with revising core concepts from NCERT and take notes on important formulas.\n"
            "- Dedicate 1 hour daily: 30 minutes for concept learning and 30 minutes for solving basic examples.\n"
            "- Use platforms like Khan Academy or Doubtnut to visualize problem-solving steps.\n"
            "- Create a formula chart and stick it near your study area for daily revision.\n"
            "- Practice mental math and small calculations during breaks to build confidence."
        )
    },
    'English': {
        'strong': (
            "Your command over English is impressive! Here's how to keep improving:\n"
            "- Read newspapers or books to have a daily habit of english reading.\n"
            "- Write a short essay, summary, or diary entry twice a week to develop expression.\n"
            "- Engage in speaking activities like debates or storytelling with peers or family.\n"
            "- Solve sample comprehension and grammar papers every weekend to stay sharp."
        ),
        'weak': (
            "Improving in English is all about consistency and exposure. Follow this routine:\n"
            "- Dedicate 20–30 minutes daily for grammar exercises from Wren & Martin or BBC Grammar.\n"
            "- Practice comprehension passages twice a week and underline key points.\n"
            "- Watch English-language cartoons or shows with subtitles to enhance listening and vocabulary.\n"
            "- Start a personal journal in English—writing helps solidify sentence structure.\n"
            "- Learn 5 new words a day and use them in sentences to retain better."
        )
    },
    'Science': {
        'strong': (
            "Science suits you well! To go deeper and stay ahead:\n"
            "- Watch topic-wise animated videos or experiments on YouTube (e.g., by ‘LearnNext’ or ‘Byju's’).\n"
            "- Regularly revise diagrams, labeling, and definitions using flashcards or mind maps.\n"
            "- Take part in science fairs, quizzes, or online Olympiads for exposure.\n"
            "- Spend 15 minutes daily on NCERT textbook back questions and HOTS (Higher Order Thinking Skills).\n"
        ),
        'weak': (
            "Let’s work on building your confidence in Science. Follow this structured plan:\n"
            "- Spend 1 hour daily: 20 mins for watching topic videos, 20 mins for reading NCERT, 20 mins for practice.\n"
            "- Use colorful notes, flowcharts, and diagrams to make difficult topics easy to recall.\n"
            "- Revise only 1 chapter every 3 days to avoid overload.\n"
            "- Practice 2 previous year questions every evening and analyze your answers.\n"
            "- If stuck, make a ‘doubt diary’ and clarify questions weekly with a teacher or mentor."
        )
    },
    'History': {
        'strong': (
            "You're doing very well in History. Let's enhance your retention and critical thinking:\n"
            "- Create and revise a timeline of major events every week—add visuals or symbols.\n"
            "- Prepare flashcards for important dates, leaders, and acts.\n"
            "- Read historical fiction or biographies to deepen contextual understanding.\n"
            "- Use mind-mapping techniques to connect events, causes, and effects.\n"
            "- Discuss what you learn with peers or family to reinforce memory and interest."
        ),
        'weak': (
            "History becomes easier when approached like a story. Here's your personalized action plan:\n"
            "- Convert chapters into storylines and retell them aloud in your own words.\n"
            "- Prepare event timelines with images and color codes for better visual memory.\n"
            "- Revise one topic daily and summarize it on a single flashcard or sticky note.\n"
            "- Watch short animated history videos to understand the context and sequence.\n"
            "- Do a weekly self-test: write down everything you remember from a chapter without looking."
        )
    },
    'Geography': {
        'strong': (
            "Great going in Geography! To keep acing it:\n"
            "- Practice blank maps every 2–3 days to test your memory.\n"
            "- Use Google Earth or interactive map tools to visualize geographical features.\n"
            "- Create a glossary of important terms with diagrams and definitions.\n"
            "- Read the newspaper for real-world examples of concepts like natural disasters or agriculture.\n"
            "- Quiz yourself every Sunday on location names, landforms, and climate types."
        ),
        'weak': (
            "To strengthen your Geography skills, follow this routine:\n"
            "- Spend 15–20 minutes daily practicing one type of map (rivers, states, minerals, etc.).\n"
            "- Make a visual glossary with definitions, symbols, and short explanations.\n"
            "- Break down long answers into points using diagrams or flowcharts.\n"
            "- Watch animated lessons or use 3D map apps to visualize terrain.\n"
            "- Every Friday, revise the week's topics and mark the ones you still find difficult."
        )
    },
    'Marathi': {
        'strong': (
            "Your fluency in Marathi is commendable!\n"
            "- Read Marathi newspapers like 'Loksatta' or children’s magazines for vocabulary.\n"
            "- Listen to Marathi podcasts or audio books for better pronunciation and fluency.\n"
            "- Practice writing essays, applications, and letters every week.\n"
            "- Learn one new idiom or proverb daily and try using it in writing.\n"
            "- Participate in school elocution or poetry recitations for confidence."
        ),
        'weak': (
            "To get better in Marathi, immerse yourself in the language regularly:\n"
            "- Focus on grammar for 15 minutes daily using school textbooks and exercises.\n"
            "- Practice writing short paragraphs or essays on familiar topics.\n"
            "- Watch children’s Marathi shows or listen to rhymes for fun and fluency.\n"
            "- Maintain a notebook for difficult words and revise them weekly.\n"
            "- Speak Marathi at home during casual conversation to build comfort and accuracy."
        )
    }
}

    # Fallback in case subject not in dict
    default_strong = "Keep practicing to maintain performance."
    default_weak = "Study this subject more with regular revision and practice."

    plan = {
        "registration_number": int(student_row['Registration Number']),
        "average_score": round(average_score, 2),
        "strongest_subject": strongest_subject,
        "weakest_subject": weakest_subject,
        "cluster_label": cluster_label,
        "cluster_average": cluster_avg.to_dict(),
        "suggested_plan": {
            weakest_subject: subject_recommendations.get(weakest_subject, {}).get('weak', default_weak),
            strongest_subject: subject_recommendations.get(strongest_subject, {}).get('strong', default_strong),
            "General Tip": "Focus more on subjects where your score is below the cluster average."
        }
    }
    return plan


