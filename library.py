import hash_table as ht

class DigitalLibrary:
    """
    Abstract base class defining interface for digital library management.
    Provides placeholder methods for book and word management.
    """
    def __init__(self):
        """Initialize base library with no specific implementation."""
        pass
    
    def distinct_words(self, book_title):
        """
        Retrieve distinct words in a book.
        
        Args:
            book_title (str): Title of the book
        """
        pass
    
    def count_distinct_words(self, book_title):
        """
        Count number of distinct words in a book.
        
        Args:
            book_title (str): Title of the book
        """
        pass
    
    def search_keyword(self, keyword):
        """
        Search for books containing a specific keyword.
        
        Args:
            keyword (str): Word to search for
        """
        pass

    def print_books(self):
        """Print details of all books in the library."""
        pass

class MuskLibrary(DigitalLibrary):
    """
    Digital library implementation using merge sort for word management.
    Optimizes word storage and retrieval using sorted distinct words.
    """
    def __init__(self, book_titles, texts):
        """
        Initialize library with books and their texts.
        
        Args:
            book_titles (list): Titles of books
            texts (list): Corresponding book texts
        """
        super().__init__()
        self.unsorted_books = book_titles.copy()
        self.texts = [None]*len(book_titles)      
        self.distincts = [None]*len(book_titles)
        
        # Sort book titles
        self.book_titles = self.mergesort_words(book_titles)
        
        # Process each book
        for i in range(len(book_titles)):
            text = texts[i]                
            orig_title = self.unsorted_books[i]
            
            # Binary search to find correct index
            s, e = 0, len(self.book_titles) - 1
            while s <= e:
                mid = (s+e)//2
                if self.book_titles[mid] == orig_title:   
                    break
                elif self.book_titles[mid] < orig_title:
                    s = mid +1
                else:
                    e = mid-1
            
            # Store text and distinct words
            self.texts[mid] = text
            sorted_dist = self.mergesort_words(text)
            self.distincts[mid] = sorted_dist

    def mergesort_words(self, lst):
        """
        Merge sort implementation that removes duplicate words.
        
        Args:
            lst (list): List of words to sort
        
        Returns:
            list: Sorted list of unique words
        """
        if len(lst) <= 1:
            return lst
        mid = len(lst) //2
        lst1 = self.mergesort_words(lst[:mid])
        lst2 = self.mergesort_words(lst[mid:])
        distinct_words = self.merge(lst1, lst2)
        return distinct_words

    def merge(self, left, right):
        """
        Merge two sorted lists, removing duplicates.
        
        Args:
            left (list): First sorted list
            right (list): Second sorted list
        
        Returns:
            list: Merged sorted list with unique elements
        """
        i, j = 0, 0
        merged = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]: 
                if not merged or merged[-1] != left[i]:
                    merged.append(left[i])
                    if left[i] == right[j] : j += 1
                i += 1
            else:
                if not merged or merged[-1] != right[j]:
                    merged.append(right[j])
                j += 1
        
        # Handle remaining elements
        while i < len(left):
            if not merged or merged[-1] != left[i]:
                    merged.append(left[i])
            i += 1
        while j < len(right):
            if not merged or merged[-1] != right[j]:
                    merged.append(right[j])
            j += 1

        return merged

    def distinct_words(self, book_title):
        """
        Retrieve distinct words for a specific book using binary search.
        
        Args:
            book_title (str): Title of the book
        
        Returns:
            list: Sorted list of distinct words in the book
        """
        s, e = 0, len(self.book_titles) - 1
        while s <= e:
            mid = (s+e)//2
            if self.book_titles[mid] == book_title:   
                break
            elif self.book_titles[mid] < book_title:
                s = mid +1
            else:
                e = mid-1
        return self.distincts[mid]
    
    def count_distinct_words(self, book_title):
        """
        Count distinct words in a book.
        
        Args:
            book_title (str): Title of the book
        
        Returns:
            int: Number of distinct words
        """
        temp = self.distinct_words(book_title)
        return len(temp)
    
    def search_keyword(self, keyword):
        """
        Find books containing a specific keyword.
        
        Args:
            keyword (str): Word to search for
        
        Returns:
            list: Titles of books containing the keyword
        """
        ans = []
        for i in range(len(self.distincts)):
            words = self.distincts[i]
            s, e = 0, len(words) - 1
            while s <= e:
                mid = (s+e)//2
                if words[mid] == keyword:   
                    ans.append(self.book_titles[i])
                    break
                elif words[mid] < keyword:
                    s = mid +1
                else:
                    e = mid-1
        return ans
    
    def print_books(self):
        """Print details of books with their distinct words."""
        for i in range(len(self.book_titles)):
            distinctwords = " | ".join(self.distincts[i])
            print(f"{self.book_titles[i]}: {distinctwords}")

class JGBLibrary(DigitalLibrary):
    """
    Digital library implementation using hash tables for word management.
    Supports different hash table collision resolution strategies.
    """
    def __init__(self, name, params):
        """
        Initialize library with specific hash table configuration.
        
        Args:
            name (str): Library name/type ("Jobs", "Gates", or "Bezos")
            params (tuple): Hash table configuration parameters
        """
        super().__init__()
        self.name = name
        self.params = params
        
        # Select collision resolution strategy
        if name == "Jobs":
            self.collision_type = "Chain"
        elif name == "Gates":
            self.collision_type = "Linear"
        elif name == "Bezos":
            self.collision_type = "Double"
        
        # Initialize main book storage hash map
        self.books = ht.HashMap(self.collision_type, self.params)
        self.appended_books = []

    def add_book(self, book_title, text):
        """
        Add a book to the library with its unique words.
        
        Args:
            book_title (str): Title of the book
            text (list): Words in the book
        """
        # Create a hash set to store unique words
        hashy = ht.HashSet(self.collision_type, self.params)
        self.appended_books.append(book_title)
