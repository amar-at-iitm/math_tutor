# tutor.py

import argparse
import json

# Import the core agent modules
from agent.step_generator import generate_steps
from agent.step_verifier import full_verification
from agent.latex_renderer import render_latex_to_pdf
from agent.practice_generator import generate_practice_problems

def main():
    """
    Main function for the Command-Line Interface (CLI).
    """
    parser = argparse.ArgumentParser(description="AI Math Tutor CLI")
    parser.add_argument("--problem", type=str, required=True, help="The math problem to solve.")
    parser.add_argument("--topic", type=str, default="algebra", help="The topic of the problem.")
    
    args = parser.parse_args()

    print("--- Starting AI Math Tutor ---")
    
    # 1. Generate Steps (Simulated LLM call)
    print("\n[1/4] Generating initial steps...")
    steps_data = generate_steps(args.problem, args.topic)
    print("...Steps generated.")
    
    # 2. Verify Steps (SymPy)
    print("\n[2/4] Verifying steps for correctness...")
    verified_data = full_verification(steps_data)
    print("...Verification complete.")
    print("--- Verified Steps ---")
    print(json.dumps(verified_data, indent=2))
    print("----------------------")

    # 3. Render Solution to LaTeX/PDF
    print("\n[3/4] Rendering final solution to PDF...")
    pdf_path = render_latex_to_pdf(verified_data, output_filename="cli_solution")
    if pdf_path:
        print(f"...PDF successfully created at: {pdf_path}")
    else:
        print("...Failed to create PDF.")

    # 4. Generate Practice Problems (Simulated LLM call)
    print("\n[4/4] Generating practice problems...")
    practice_problems = generate_practice_problems(verified_data.get("topic", "general math"))
    print("...Practice problems generated.")
    
    print("\n--- Suggested Practice Problems ---")
    for i, prob in enumerate(practice_problems):
        print(f"{i+1}. {prob}")
    print("---------------------------------")
    
    print("\n--- Tutor session finished ---")

if __name__ == "__main__":
    main()
