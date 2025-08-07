# agent/latex_renderer.py

import subprocess
import sympy
import os

def _generate_latex_string(verified_data: dict) -> str:
    """
    Generates a LaTeX document string from the verified solution data.
    
    This function simulates an LLM call to get a polished explanation
    and then formats it into a LaTeX template.
    """
    problem = verified_data.get("problem", "")
    steps = verified_data.get("steps", [])

    # --- LLM Simulation for Polished Explanation ---
    # In a real implementation, you'd send the verified steps to the LLM
    # and ask for a beautiful, cohesive explanation.
    print("INFO: [LLM Simulation] Generating polished explanation for LaTeX output.")
    polished_explanation = "To solve the quadratic equation, we first factor it. By finding two numbers that multiply to 6 and add to 5, we get the factors (x+2) and (x+3). Setting each factor to zero gives us the final solutions."
    # --- End of LLM Simulation ---

    # Build the LaTeX steps string
    latex_steps = []
    for step in steps:
        # Use SymPy to convert the expression to LaTeX format
        try:
            # We need to handle equations and simple expressions differently
            if '=' in step['expression']:
                lhs, rhs = step['expression'].split('=', 1)
                latex_expr = f"{sympy.latex(sympy.sympify(lhs))} = {sympy.latex(sympy.sympify(rhs))}"
            else:
                latex_expr = sympy.latex(sympy.sympify(step['expression']))
        except (SyntaxError, TypeError, ValueError):
            latex_expr = step['expression'] # Fallback to raw string

        reasoning = step.get('reasoning', '').replace('#', r'\#') # Escape special chars
        verified_status = " Verified" if step.get('verified', False) else " Error"
        
        latex_steps.append(f"\\item \\textbf{{{reasoning}}} \\\\ \n ${latex_expr}$ \\hfill \\textit{{{verified_status}}}")

    steps_string = "\n".join(latex_steps)

    # The LaTeX document template
    latex_template = f"""
\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}
\\usepackage[margin=1in]{{geometry}}
\\title{{Math Problem Solution}}
\\author{{AI Math Tutor}}
\\date{{\\today}}
\\begin{document}
\\maketitle

\\section*{{Problem}}
${sympy.latex(sympy.sympify(problem))}$

\\section*{{Summary of Solution}}
{polished_explanation}

\\section*{{Step-by-Step Solution}}
\\begin{{enumerate}}
{steps_string}
\\end{{enumerate}}

\\end{{document}}
"""
    return latex_template

def render_latex_to_pdf(verified_data: dict, output_filename: str = "solution") -> str:
    """
    Renders the solution data to a PDF file using a LaTeX installation.

    Args:
        verified_data: The dictionary containing the problem and verified steps.
        output_filename: The base name for the output files (e.g., 'solution').

    Returns:
        The path to the generated PDF file, or an empty string on failure.
    """
    import sympy # Required for latex conversion
    
    latex_content = _generate_latex_string(verified_data)
    
    tex_filepath = f"{output_filename}.tex"
    pdf_filepath = f"{output_filename}.pdf"
    
    with open(tex_filepath, 'w') as f:
        f.write(latex_content)
        
    print(f"INFO: Generated LaTeX file: {tex_filepath}")

    # Compile the .tex file to a .pdf using pdflatex
    # This requires a LaTeX distribution (like MiKTeX or TeX Live) to be installed.
    command = [
        "pdflatex",
        "-interaction=nonstopmode", # Continue on errors
        tex_filepath
    ]
    
    try:
        print("INFO: Compiling LaTeX to PDF...")
        # We run it twice to ensure cross-references (like table of contents) are correct.
        subprocess.run(command, check=True, capture_output=True, text=True)
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"SUCCESS: PDF generated at {pdf_filepath}")
        return os.path.abspath(pdf_filepath)
    except FileNotFoundError:
        print("ERROR: `pdflatex` command not found. Is a LaTeX distribution installed and in your PATH?")
        return ""
    except subprocess.CalledProcessError as e:
        print(f"ERROR: LaTeX compilation failed. Check the log file: {output_filename}.log")
        print(f"--- LaTeX Compiler Output ---\n{e.stdout}\n{e.stderr}\n--- End of Output ---")
        return ""
    finally:
        # Clean up auxiliary files
        for ext in ['.aux', '.log']:
            if os.path.exists(output_filename + ext):
                os.remove(output_filename + ext)

if __name__ == '__main__':
    # Example usage
    mock_verified_data = {
        "problem": "x**2 + 5*x + 6 = 0",
        "steps": [
            {"reasoning": "Initial equation", "expression": "x**2 + 5*x + 6 = 0", "verified": True},
            {"reasoning": "Factor the quadratic", "expression": "(x + 2)*(x + 3) = 0", "verified": True},
            {"reasoning": "Set factors to zero", "expression": "x + 2 = 0", "verified": True},
            {"reasoning": "Solve for x", "expression": "x = -2", "verified": True}
        ]
    }
    render_latex_to_pdf(mock_verified_data)
