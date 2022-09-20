import sys
from expressionParser import parser

if __name__ == '__main__':
    expressions = [
        ("1 + 1", 1 + 1),
        ("2 * 3", 2 * 3),
        ("5 / 4", 5 / 4),
        ("2 * 3 + 1", 2 * 3 + 1),
        ("1 + 2 * 3", 1 + 2 * 3),
        ("(2 * 3) + 1", (2 * 3) + 1),
        ("2 * (3 + 1)", 2 * (3 + 1)),
        ("(2 + 1) * 3", (2 + 1) * 3),
        ("-2 + 3", -2 + 3),
        ("5 + (-2)", 5 + (-2)),
        ("5 * -2", 5 * -2),
        ("-1 - -2", -1 - -2),
        ("-1 - 2", -1 - 2),
        ("4 - 5", 4 - 5),
        ("1 - 2", 1 - 2),
        ("3 - ((8 + 3) * -2)", 3 - ((8 + 3) * -2)),
        ("2.01e2 - 200", 2.01e2 - 200),
        ("2*3*4", 2 * 3 * 4),
        ("2 + 3 + 4 * 3 * 2 + 2", 2 + 3 + 4 * 3 * 2 + 2),
        ("10 + 11", 10 + 11),
        ("sqrt(9)", 3),
        ("d=2", 2),
        ("b=4 b + 3", 7),
        ("b=4 (3 + b)", 7),
        ("b=4 3 + b", 7),
        ("a = 1 a + 3", 4),
        ("a = 1 b = 2 a + b + 3", 6),
        ("a = 2 2 * a * 1", 4),
        ("a = 2 2 * a", 4),
        ("a = 2 a * 2", 4),
        ("a = 2 b = 3 a * b", 6),
        ("a = 2 b = 3 a * b * 2", 12),
        ("a = 2 10 / a", 5),
        ("a = 2\nb = 3\nc = a * b * 2\nc + 1", 13),
        # ("sqrt(9) * 3", 9),
    ]

    errors = []
    for expression, expected in expressions:
        try:
            response = parser(expression)
            result = "PASS" if response == expected else "FAIL"

            print(f"Expression: \"{expression}\" - {result}  => expected: {expected} / response: {response}")

            if (result == "FAIL"):
                errors.append({
                    'expression': expression,
                    'expected': expected,
                    'result': response
                })
        except Exception as e:
            errors.append({
                'expression': expression,
                'expected': expected,
                'result': f"[THROWS EXCEPTION]: {str(e)}"
            })

    if (len(errors) == 0):
        print("\n\nAll expressions executed with success")

        sys.exit(0)
    else:
        print(f"\n\n{len(errors)} expressions was executed with error:")

        for error in errors: 
            print(f"\nexpression: \"{error['expression']}\"")
            print(f"    expect: {error['expected']}")
            print(f"    result: {error['result']}")

        sys.exit(1)
