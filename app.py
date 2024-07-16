from flask import Flask, request, render_template
import re
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

# Load the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to load legal data from a text file
def load_legal_data(file_path):
    legal_data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Use regular expression to split by two or more newline characters
        sections = re.split(r'\n\n+', content)
        
        for section in sections:
            if section.strip():
                title_match = re.search(r'[Ss]ection (\d+):', section)
                title = title_match.group(0).strip() if title_match else "Unknown Section"
                
                about_match = re.search(r'[Aa]bout:(.*)', section, re.DOTALL)
                about = about_match.group(1).strip() if about_match else ""
                
                combined_text = f"{title}. {about}"
                legal_data[title] = combined_text
    return legal_data

# Load both IPC and CrPC data
ipc_data = load_legal_data('IPC sections 1 to 62.txt')  # Replace with your IPC data file path
crpc_data = load_legal_data('CrPC Sections dataset(complete).txt')  # Replace with your CrPC data file path

def query_legal_data(query, legal_data):
    query_embedding = model.encode(query, convert_to_tensor=True)
    legal_sections = list(legal_data.keys())
    combined_texts = list(legal_data.values())  # Use combined texts for similarity search
    
    # Encode legal texts
    legal_embeddings = model.encode(combined_texts, convert_to_tensor=True)
    
    # Compute cosine similarity
    cosine_scores = util.pytorch_cos_sim(query_embedding, legal_embeddings)[0]
    
    # Find the most similar sections
    top_results = cosine_scores.topk(5)  # Get top 5 results
    matched_sections = []
    for idx in top_results.indices:
        matched_sections.append(f"{legal_sections[idx]}\n")
    
    if matched_sections:
        return "".join(matched_sections)
    else:
        return "Sorry, no relevant legal information found for the provided keyword."


@app.route('/')
def landing_page():
    return render_template('landingpage.html')

@app.route('/chatbot')
def chatbot():
    return render_template('index2.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    if not question:
        return render_template('result.html', question=question, response="Please provide a valid input.")

    ipc_response = query_legal_data(question, ipc_data)
    crpc_response = query_legal_data(question, crpc_data)
    combined_response = f"IPC Sections:\n{ipc_response}\n\nCrPC Sections:\n{crpc_response}"
    
    return render_template('result.html', question=question, response=combined_response)

@app.route('/helpline')
def helpline():
    return render_template('helpline.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.errorhandler(500)
def internal_error(error):
    return "500 error: Internal Server Error. Please try again later.", 500

@app.errorhandler(404)
def not_found_error(error):
    return "404 error: Page Not Found. Please check the URL.", 404

# if __name__ == "__main__":
#     app.run(debug=True)
