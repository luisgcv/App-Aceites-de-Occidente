# utils/threading_utils.py
from concurrent.futures import ThreadPoolExecutor

# Reutilizable para toda la app
executor = ThreadPoolExecutor(max_workers=5)

def run_async(func, *args, **kwargs):
    def wrapper():
        func(*args, **kwargs)
    executor.submit(wrapper)
