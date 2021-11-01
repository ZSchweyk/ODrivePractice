def count_partitions(n, k):
    if n == 0:
        return 1
    if k <= 0 or n < 0:
        return 0

    return count_partitions(n - k, k) + count_partitions(n, k - 1)


n = 100
k = 10
print(f"{n} with max size {k}:", count_partitions(100, 10))
