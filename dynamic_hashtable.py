"""
Dynamic Hash Table Implementation

This module provides dynamic hash table classes (Set and Map) with 
automatic resizing when load factor exceeds 50%.
"""

from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        """
        Initialize a dynamic hash set.
        
        Args:
            collision_type (str): Type of collision handling
            params (tuple): Parameters for hash table initialization
        """
        super().__init__(collision_type, params)
        
    def rehash(self):
        """
        Rehash the hash set when load factor exceeds 50%.
        Allocate a new table with a prime size just over double the old size.
        """
        # Get new table size
        new_size = get_next_size()
        
        # Create a temporary list to store current elements
        current_elements = []
        
        # Collect all elements from the current table
        for slot in self.table:
            if self.collision_type == "Chain":
                # For chaining, collect elements from lists
                if slot:
                    current_elements.extend(slot)
            elif slot is not None:
                # For probing methods, collect non-empty slots
                current_elements.append(slot)
        
        # Reset table with new size and collision type
        self.__init__(self.collision_type, (self.z, new_size))
        
        # Reinsert all elements
        for element in current_elements:
            self.insert(element)
            
    def insert(self, x):
        """
        Insert an element and trigger rehashing if load factor exceeds 50%.
        
        Args:
            x: Element to insert
        """
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        """
        Initialize a dynamic hash map.
        
        Args:
            collision_type (str): Type of collision handling
            params (tuple): Parameters for hash table initialization
        """
        super().__init__(collision_type, params)
        
    def rehash(self):
        """
        Rehash the hash map when load factor exceeds 50%.
        Allocate a new table with a prime size just over double the old size.
        """
        # Get new table size
        new_size = get_next_size()
        
        # Create a temporary list to store current elements
        current_elements = []
        
        # Collect all elements from the current table
        for slot in self.table:
            if self.collision_type == "Chain":
                # For chaining, collect elements from lists
                if slot:
                    current_elements.extend(slot)
            elif slot is not None:
                # For probing methods, collect non-empty slots
                current_elements.append(slot)
        
        # Reset table with new size and collision type
        self.__init__(self.collision_type, self.params[:2] + (new_size,))
        
        # Reinsert all elements
        for element in current_elements:
            self.insert(element)
            
    def insert(self, key):
        """
        Insert an element and trigger rehashing if load factor exceeds 50%.
        
        Args:
            key: Key-value pair to insert
        """
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()
