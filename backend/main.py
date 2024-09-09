from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
import os
from dotenv import load_dotenv
import psycopg2

app = Flask(__name__)
CORS(app)

load_dotenv()

current_dir = os.path.dirname(__file__)

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)

DATABASE_URL = os.getenv('DATABASE_URL')


def read_text_from_file(file_path):
    """Reads the HR data from the saved file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as text_file:
            text = text_file.read()
        return text
    except Exception as e:
        print(f"Error reading text from file: {e}")
        return ""


def get_file_from_email(email):
    """Return the company HR file from the email of the user"""
    cur = None
    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='disable')
        cur = conn.cursor()

        cur.execute("SELECT company_file_path FROM details WHERE email = %s", (email,))

        result = cur.fetchone()

        if result:
            return result[0]
        else:
            return None
    
    except Exception as e:
        print(f"Error getting file from email: {e}")
        return None
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/get-company', methods=['POST'])
def get_company_from_email():
    """Return the company name from the email of the user"""
    cur = None
    conn = None

    try:
        data = request.get_json()
        email = data['email']

        conn = psycopg2.connect(DATABASE_URL, sslmode='disable')
        cur = conn.cursor()

        cur.execute("SELECT company FROM details WHERE email = %s", (email,))

        result = cur.fetchone()

        if result:
            return jsonify({'companyName': result[0]})
        else:
            return jsonify({'companyName': 'Error getting company name'})
    
    except Exception as e:
        print(f"Error getting company name: {e}")
        return jsonify({'companyName': 'Error getting company name'})
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

            
def company_to_path(company):
    """Converts the company name to the respective file path"""
    return os.path.join(current_dir, 'extracted_data', f'{company.replace(' ', '_')}.txt')


def apply_for_leave(email):
    """Apply for leave and update the number of leaves taken"""
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='disable')
        cur = conn.cursor()

        cur.execute("UPDATE details SET leaves = leaves + 1 WHERE email = %s", (email,))
        conn.commit()
        
        cur.execute("SELECT leaves FROM details WHERE email = %s", (email,))
        result = cur.fetchone()

        return(f"Successfully applied for leave. You have taken {result[0]} leaves")
    
    except Exception as e:
        print(f"Error applying for leave: {e}")
        return "Error applying for leave"
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route('/get-answer', methods=['POST'])
def get_answer():
    """Get the answer to the question and decide whether it is a leave request or not"""
    data = request.get_json()
    question = data['question']
    currEmail = data['email']
    
    wants_to_take_leave = generate_answer("Based on the sentence in the context, just give me an answer saying 'Yes' or 'No' on whether the user wishes to take a leave. If he is just asking about the leave policy, say 'No'.", 
                                        question)
        
    if (wants_to_take_leave.strip().lower() == 'yes'):
        return jsonify({'answer': apply_for_leave(currEmail)})

    curr_file = get_file_from_email(currEmail)

    if curr_file:
        context = read_text_from_file(curr_file)
        answer = generate_answer(question, context)
    else:
        answer = "Error getting company files"

    return jsonify({'answer': answer})


@app.route('/signup', methods=['POST'])
def signup():
    """Sign up the user and store the details in the database"""
    cur = None
    conn = None

    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        company = data['company']

        conn = psycopg2.connect(DATABASE_URL, sslmode='disable')
        cur = conn.cursor()

        cur.execute("INSERT INTO details (email, password, company, company_file_path) VALUES (%s, %s, %s, %s)", (email, password, company, company_to_path(company)))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'success': True})
    
    except Exception as e:
        print(f"Error signing up: {e}")

        if conn:
            conn.rollback()
        if cur:
            cur.close()
        if conn:
            conn.close()

        return jsonify({'success': False})


@app.route('/login', methods=['POST'])
def login():
    """Login the user and check if the details are correct"""
    cur = None
    conn = None

    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        conn = psycopg2.connect(DATABASE_URL, sslmode='disable')
        cur = conn.cursor()
        
        cur.execute("SELECT password FROM details WHERE email = %s", (email,))

        result = cur.fetchone()

        if result and result[0] == password:
            return jsonify({'success': True, 'details': True})
        else:
            return jsonify({'success': True, 'details': False})
    
    except Exception as e:
        print(f"Error logging in: {e}")
        return jsonify({'success': False, 'details': False})
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route('/logout', methods=['POST'])
def logout():
    """Logout the user"""
    return jsonify({'success': True})


def generate_answer(question, context, model='command-xlarge-nightly'):
    """Generate the answer to the question based on the context using Cohere"""

    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = co.generate(
        model=model,
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        k=0,
        p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop_sequences=["\n"]
    )
    return response.generations[0].text.strip()


@app.route('/')
def index():
    """Return the backend message to check if backend is working"""
    return 'This is the backend'


if __name__ == '__main__':
    app.run(debug=True)
