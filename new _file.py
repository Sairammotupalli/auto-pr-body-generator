#creating new python file for a test 
def is_fibonacci(n):
  """
  Checks if a number is a Fibonacci number.
  """

  # A number is Fibonacci if and only if one of the following is a perfect square
  return is_perfect_square(5 * n**2 + 4) or is_perfect_square(5 * n**2 - 4)

def is_perfect_square(x):
  """
  Checks if a number is a perfect square.
  """

  if x < 0:
    return False

  sqrt = int(x**0.5)
  return sqrt**2 == x

# Example usage
print(is_fibonacci(8))  # True
print(is_fibonacci(10)) # False
