from prime_generator import get_next_size

class HashTable:
    """
    A flexible hash table implementation supporting different collision resolution strategies.
    
    Supports three collision handling methods:
    - Chaining: Uses linked lists to handle collisions
    - Linear Probing: Finds next available slot when collision occurs
    - Double Hashing: Uses a secondary hash function for probe sequence
    """
    def __init__(self, collision_type, params):
        """
        Initialize hash table with specified collision resolution strategy.
        
        Args:
            collision_type (str): Type of collision handling 
                - "Chain": Chaining method
                - "Linear": Linear probing
                - "Double": Double hashing
            params (list): Configuration parameters for hash table
        """
        self.collision_type = collision_type
        self.total_elements = 0
        
        # Setup parameters based on collision type
        if collision_type == "Double": 
            self.z, self.z2, self.c2, self.table_size = params[0], params[1], params[2], params[3]
        else: 
            self.z, self.table_size = params[0], params[1]
        
        # Initialize table based on collision type
        if collision_type == "Chain":
            self.table = [[] for i in range(self.table_size)] 
        else:
            self.table = [None] * self.table_size

    def insert(self, x):
        """
        Insert an element into the hash table, handling collisions based on strategy.
        
        Args:
            x: Element to insert (can be a key or key-value pair)
        """
        # Extract key, skip if already exists
        key = x[0] if isinstance(x, tuple) else x
        if self.find(key):
            return
        
        # Get initial slot
        idx = self.get_slot(key)
        
        # Insert based on collision resolution method
        if self.collision_type == "Chain":
            self.table[idx].append(x)
        elif self.collision_type == "Linear":                           
            orig_idx = idx
            while self.table[idx] is not None:
                idx = (idx + 1) % self.table_size
                if idx == orig_idx:
                    return 
            self.table[idx] = x
        else:  # Double Hashing
            # Calculate secondary hash for probe sequence
            step = 0
            for i in range(len(key)-1, -1, -1):
                char = key[i]
                if char.islower():  value = ord(char) - ord('a')
                else:   value = ord(char) - ord('A') + 26
                step = (step * self.z2 + value)
            step = self.c2 - (step%self.c2)
            
            # Find available slot
            orig_idx = idx
            while self.table[idx] is not None:
                idx = (idx + step) % self.table_size
                if idx == orig_idx: return
            self.table[idx] = x
        
        self.total_elements += 1
        
    def find(self, key):
        """
        Search for a key in the hash table.
        
        Args:
            key: Key to search for
        
        Returns:
            Value associated with key or boolean indicating presence
        """
        # Get initial slot and handle search based on collision strategy
        idx = self.get_slot(key)
        orig_idx  = idx
        
        if self.collision_type == "Chain":
            for item in self.table[idx]:
                if (isinstance(item, tuple) and item[0] == key) or item == key:
                        return item[1] if isinstance(item, tuple) else True
            return None if isinstance(self, HashMap) else False 
        
        elif self.collision_type == "Linear":
            while self.table[idx]:                        
                item = self.table[idx]
                if (isinstance(item, tuple) and item[0] == key) or item == key:
                    return item[1] if isinstance(item, tuple) else True
                idx = (idx + 1) % self.table_size                 
                if orig_idx == idx: 
                    break
            return None if isinstance(self, HashMap) else False
        
        else:  # Double Hashing
            # Calculate secondary hash for probe sequence
            step = 0
            for i in range(len(key)-1, -1, -1):
                char = key[i]
                if char.islower():  value = ord(char) - ord('a')
                else:   value = ord(char) - ord('A') + 26
                step = (step * self.z2 + value)
            step = self.c2 - (step%self.c2)
            
            while self.table[idx]:
                item = self.table[idx]
                if (isinstance(item, tuple) and item[0] == key) or item == key:
                    return item[1] if isinstance(item, tuple) else True
                idx = (idx + step) % self.table_size                
                if orig_idx == idx: break
            return None if isinstance(self, HashMap) else False
            
    def get_slot(self, key):
        """
        Calculate the hash slot for a given key using polynomial accumulation.
        
        Args:
            key: Key to hash
        
        Returns:
            int: Calculated slot index
        """
        poly = 0
        for i in range(len(key)-1, -1, -1):
            char = key[i]
            if char.islower():  value = ord(char) - ord('a')
            else:   value = ord(char) - ord('A') + 26
            poly = (poly *self.z + value) % self.table_size
        return poly % self.table_size
    
    def get_load(self):
        """
        Calculate the current load factor of the hash table.
        
        Returns:
            float: Ratio of total elements to table size
        """
        return self.total_elements / self.table_size
    
    def __str__(self):
        """
        Generate a string representation of the hash table.
        
        Returns:
            str: Formatted string showing table contents
        """
        result = ""
        for slot in self.table:
            if slot:
                if self.collision_type == "Chain":
                    result += ' ; '.join(str(x) for x in slot) + " | "
                else:
                    result += str(slot) + " | "
            else:
                result += "<EMPTY> | "
        return result.rstrip(" | ")  
    
    def rehash(self):
        """
        Resize the hash table to a new prime size and reinsert existing elements.
        Useful for maintaining performance as load factor increases.
        """
        new_size = get_next_size()
        old_table = self.table
        self.table_size = new_size
        self.total_elements = 0
        
        if self.collision_type == "Chain":
            self.table = [[] for i in range(self.table_size)]
            for slot in old_table:
                for item in slot:
                    self.insert(item)
        else:
            self.table = [None] * self.table_size
            for item in old_table:
                if item is not None:
                    self.insert(item)

class HashSet(HashTable):
    """
    Implements a HashSet using inheritance from HashTable.
    Provides a set-like data structure with unique elements.
    """
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    # Inherit all methods from HashTable with no modifications

class HashMap(HashTable):
    """
    Implements a HashMap using inheritance from HashTable.
    Provides key-value pair storage with unique keys.
    """
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    # Inherit all methods from HashTable with no modifications
