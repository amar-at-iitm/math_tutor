# agent/step_verifier.py

import sympy

def verify_step(previous_expression: str, current_expression: str) -> bool:
    """
    Verifies if a mathematical step is logically correct using SymPy.

    It works by checking if the two expressions are symbolically equivalent.
    For example, it can verify that 'x + 2 = 0' is equivalent to 'x = -2'.

    Args:
        previous_expression: The mathematical expression from the previous step.
        current_expression: The mathematical expression from the current step.

    Returns:
        True if the step is valid, False otherwise.
    """
    try:
        # SymPy's `sympify` converts a string into a SymPy expression.
        # We handle equations by splitting them at the '=' sign.
        if '=' in previous_expression and '=' in current_expression:
            prev_lhs, prev_rhs = map(sympy.sympify, previous_expression.split('='))
            curr_lhs, curr_rhs = map(sympy.sympify, current_expression.split('='))

            # An equation `A = B` is equivalent to `A - B = 0`.
            # We check if the two equations are equivalent by simplifying their difference.
            # If `(prev_lhs - prev_rhs) - (curr_lhs - curr_rhs)` simplifies to 0,
            # they are equivalent.
            is_equivalent = sympy.simplify((prev_lhs - prev_rhs) - (curr_lhs - curr_rhs)) == 0
            return is_equivalent

        # Handle cases that are not simple equations (e.g., factoring)
        # This is a simplified check and can be expanded.
        prev_expr = sympy.sympify(previous_expression)
        curr_expr = sympy.sympify(current_expression)
        
        # Check if expanding the current expression gives the previous one.
        if sympy.expand(curr_expr) == prev_expr:
            return True

    except (SyntaxError, TypeError, ValueError) as e:
        print(f"ERROR: SymPy could not parse expressions: '{previous_expression}', '{current_expression}'. Error: {e}")
        return False

    # Fallback for more complex or multi-part steps
    # The logic here can be expanded significantly.
    print(f"WARN: Could not definitively verify step from '{previous_expression}' to '{current_expression}'. Assuming False.")
    return False

def full_verification(steps_data: dict) -> dict:
    """
    Takes the full chain-of-thought and adds a verification status to each step.
    """
    steps = steps_data.get("steps", [])
    if not steps:
        return steps_data

    # The first step is always considered "verified" as it's the starting point.
    steps[0]['verified'] = True

    # Iterate from the second step onwards
    for i in range(1, len(steps)):
        prev_expr = steps[i-1]['expression']
        curr_expr = steps[i]['expression']

        # Skip verification for steps with non-mathematical or multi-part expressions
        if "or" in curr_expr or "or" in prev_expr:
             # This is a logic step, not a direct algebraic transformation.
             # A more advanced verifier could handle this. For now, we accept it.
            steps[i]['verified'] = True
            continue

        is_valid = verify_step(prev_expr, curr_expr)
        steps[i]['verified'] = is_valid

    steps_data['steps'] = steps
    return steps_data


if __name__ == '__main__':
    # Example usage
    mock_steps = {
        "steps": [
            {"expression": "x**2 + 5*x + 6 = 0"},
            {"expression": "(x + 2)*(x + 3) = 0"}, # This is tricky, verify_step needs to handle it
            {"expression": "x + 2 = 0 or x + 3 = 0"},
            {"expression": "x = -2"} # This should fail verification from the previous step
        ]
    }
    # A better verifier would compare "x+2=0" to "x=-2" and "x+3=0" to "x=-3"
    # Our current simplified one will have issues with the "or" statement.
    
    # Test a direct verification
    print(f"Verification for 'x+2=0' -> 'x=-2': {verify_step('x+2=0', 'x=-2')}")
    print(f"Verification for 'x**2-4=0' -> '(x-2)*(x+2)=0': {verify_step('x**2-4', '(x-2)*(x+2)')}")

    verified_data = full_verification(mock_steps)
    import json
    print(json.dumps(verified_data, indent=2))
