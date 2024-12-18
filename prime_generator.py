"""
Prime Number Generator for Dynamic Hash Table Resizing

This module provides a mechanism to generate and manage prime numbers
for dynamic hash table resizing operations.
"""

# primes in descending order
prime_sizes = [29]

def set_primes(list_of_primes):
    """
    Set the global list of prime sizes for hash table resizing.
    
    Args:
        list_of_primes (list): A list of prime numbers in descending order
    """
    global prime_sizes
    prime_sizes = list_of_primes
    
def get_next_size():
    """
    Get the next prime size for hash table resizing.
    
    Returns:
        int: The next prime size from the predefined list
    """
    return prime_sizes.pop()
