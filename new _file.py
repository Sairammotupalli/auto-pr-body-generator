#creating new python file for a test 
def fibonacci_iterative(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

# Get the nth Fibonacci number
n = 10
result = fibonacci_iterative(n)
print("The", n, "th Fibonacci number is:", result)
