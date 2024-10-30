#creating new python file for a test 
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Get the nth Fibonacci number
n = 10
result = fibonacci(n)
print("The", n, "th Fibonacci number is:", result)
