def time_log(warning_threshold_ms: float=1000):
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start = time.time()
            result = func(*args, **kwargs)
            print('\n', '#' * 19, ' BENCHMARKS ', '#' * 19, '\n', sep='')
            end = time.time()
            execution_time_ms = (end - start) * 1000

            if execution_time_ms > warning_threshold_ms:
                print(f"WARNING: {func.__name__} executed in %.3f ms\n" % execution_time_ms)
            else:
                print(f"{func.__name__} executed in %.3f ms\n" % execution_time_ms)

            print('#' * 50, '\n', sep='')
            return result

        return wrapper

    return decorator