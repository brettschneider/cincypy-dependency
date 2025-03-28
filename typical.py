"""
Illustration of typical decorators
"""
from functools import wraps


def log_it(func: callable):
    @wraps(func)
    def logger_func(*args, **kwargs):
        print(f"DEBUG: {func.__name__} called with {args}, {kwargs}")
        return func(*args, **kwargs)

    return logger_func

@log_it
def reverse(msg: str) -> str:
    return msg[::-1]

#equivilent to reverse = log_it(reverse)

if __name__ == '__main__':
    print("Result", reverse("Steve Was Here"))
