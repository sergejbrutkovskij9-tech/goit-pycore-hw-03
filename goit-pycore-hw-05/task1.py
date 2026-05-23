def caching_fibonacci():
    """
    Повертає функцію fibonacci з власним кешем через замикання.
    """
    cache = {}

    def fibonacci(n):
        """
        Обчислює n-е число Фібоначчі з використанням кешування.
        """
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


# Приклад використання
fib = caching_fibonacci()

print(fib(10))  # 55
print(fib(15))  # 610