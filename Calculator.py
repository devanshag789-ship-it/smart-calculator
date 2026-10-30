
import ast
import operator

print("===== SMART CALCULATOR =====")
print("Enter any mathematical expression.")
print("Use +, -, *, /, %, ** and brackets ().")
print("Type 'exit' to close the calculator.")

# Only allow these mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = calculate(node.left)
        right = calculate(node.right)

        # Prevent excessively large exponent calculations
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("Exponent is too large!")

        return OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](calculate(node.operand))

    raise ValueError("Only mathematical expressions are allowed!")


def evaluate_expression(expression):
    tree = ast.parse(expression, mode="eval")
    return calculate(tree.body)



if __name__ == "__main__":
    while True:
        expression = input("\nEnter expression: ").strip()

        if expression.lower() == "exit":
            print("Calculator closed!")
            break

        try:
            result = evaluate_expression(expression)
            print("Result =", result)

        except ZeroDivisionError:
            print("Error: Division by zero!")

        except (
            SyntaxError,
            ValueError,
            TypeError,
            OverflowError,
        ):
            print("Invalid expression or unsupported operation!")

        except Exception:
            print("Something went wrong!")
