# agent/step_generator.py

import json

def generate_steps(problem_statement: str, topic: str = "algebra"):
    """
    Simulates calling a local LLM to break down a math problem into steps.

    In a real implementation, this function would make a request to the
    GPT-OSS-20B model API. For this prototype, we return a hardcoded
    JSON structure that mimics the expected output.

    Args:
        problem_statement: The math problem from the user.
        topic: The topic of the math problem (e.g., algebra, calculus).

    Returns:
        A dictionary containing the chain-of-thought steps.
    """
    print(f"INFO: [LLM Simulation] Generating steps for problem: '{problem_statement}'")

    # This is a simulated response from the LLM.
    # The structure includes the original problem, the topic, and a list of steps.
    # Each step has a 'reasoning' part (the explanation) and an 'expression'
    # part (the mathematical formula).
    mock_llm_response = {
        "problem": problem_statement,
        "topic": topic,
        "solution_summary": "The solutions are x = -2 and x = -3.",
        "steps": [
            {
                "reasoning": "The initial quadratic equation to solve.",
                "expression": "x**2 + 5*x + 6 = 0"
            },
            {
                "reasoning": "We need to find two numbers that multiply to 6 and add to 5. These numbers are 2 and 3. We can use this to factor the quadratic expression.",
                "expression": "(x + 2)*(x + 3) = 0"
            },
            {
                "reasoning": "For the product of two factors to be zero, at least one of the factors must be zero. So, we set each factor equal to zero.",
                "expression": "x + 2 = 0 or x + 3 = 0"
            },
            {
                "reasoning": "Solving the first equation for x.",
                "expression": "x = -2"
            },
            {
                "reasoning": "Solving the second equation for x.",
                "expression": "x = -3"
            }
        ]
    }

    # In a real scenario, you would parse the JSON string from the LLM.
    # Here, we just return the Python dict.
    return mock_llm_response

if __name__ == '__main__':
    # Example usage
    problem = "Solve the equation x**2 + 5*x + 6 = 0 for x."
    steps_data = generate_steps(problem)
    print(json.dumps(steps_data, indent=2))
