# app.py

import os
from flask import Flask, request, render_template, url_for, send_from_directory

# Import the core agent modules
from agent.step_generator import generate_steps
from agent.step_verifier import full_verification
from agent.latex_renderer import render_latex_to_pdf
from agent.practice_generator import generate_practice_problems

# Initialize the Flask app
app = Flask(__name__)

# Ensure a directory for static files (like PDFs) exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    """Handles the problem submission and returns the solution."""
    problem_text = request.form.get('problem')
    if not problem_text:
        return render_template('index.html', error="Please enter a problem.")

    # --- Full Tutor Pipeline ---
    # 1. Generate Steps
    steps_data = generate_steps(problem_text)
    
    # 2. Verify Steps
    verified_data = full_verification(steps_data)
    
    # 3. Render PDF
    # We use a unique filename to avoid browser caching issues
    output_filename = f"static/solution_{hash(problem_text)}"
    pdf_path = render_latex_to_pdf(verified_data, output_filename=output_filename)
    
    # 4. Generate Practice Problems
    practice_problems = generate_practice_problems(verified_data.get("topic", "general math"))
    
    # Pass results to the template
    return render_template(
        'index.html',
        problem_text=problem_text,
        solution_pdf=os.path.basename(pdf_path) if pdf_path else None,
        practice_problems=practice_problems
    )

# This route is necessary for the browser to be able to download the PDF
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Use port 5001 to avoid conflicts
