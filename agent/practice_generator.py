# agent/practice_generator.py

import json

def generate_practice_problems(topic: str, difficulty: str = "medium"):
    """
    Simulates calling a local LLM to generate related practice problems.

    Args:
        topic: The topic for the practice problems (e.g., 'quadratic equations').
        difficulty: The desired difficulty level.

    Returns:
        A list of practice problems.
    """
    print(f"INFO: [LLM Simulation] Generating practice problems for topic: '{topic}'")

    # This is a simulated response from the LLM.
    mock_llm_response = {
        "practice_problems": [
            "Solve for x: x**2 - 4*x + 4 = 0",
            "Find the roots of the equation: 2*x**2 - 3*x - 2 = 0",
            "Factor and solve: x**2 + x - 12 = 0"
        ]
    }
    
    return mock_llm_response.get("practice_problems", [])

if __name__ == '__main__':
    # Example usage
    topic = "quadratic equations"
    problems = generate_practice_problems(topic)
    print(f"Practice Problems for '{topic}':")
    for prob in problems:
        print(f"- {prob}")
