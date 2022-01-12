# Name: Matthew Gader
# OSU Email: gaderm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 12/3/21
# Description: Implementation of a HashMap class built from a DynamicArray with each
# bucket (index) made up of a LinkedList. It includes methods to clear, get or put
# a value based on a key, and remove a key. It also has a method to determine if a
# given key is in the hash table, a method which returns the number of empty buckets,
# and a method to determine the table's load factor. Lastly, it has a method to resize
# the hash table, and one which returns a DynamicArray of all of the table's keys.


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Remove all content from hash map
        """

        # set each bucket to empty LinkedList
        for i in range(self.capacity):
            self.buckets.set_at_index(i, LinkedList())
        self.size = 0

    def get(self, key: str) -> object:
        """
        Return value associated with key if
        key is found, None otherwise
        """

        # determine which bucket to search for key
        hash = self.hash_function(key)
        index = hash % self.capacity
        bucket = self.buckets[index]

        # search for key in bucket
        if bucket.contains(key):
            val = bucket.contains(key).value
            return val

    def put(self, key: str, value: object) -> None:
        """
        Update key's value if key is found,
        add new key/value pair otherwise
        """

        # determine which bucket to search for key
        hash = self.hash_function(key)
        index = hash % self.capacity
        bucket = self.buckets[index]

        # if key is found, replace with given value
        if bucket.contains(key):
            bucket.remove(key)
            bucket.insert(key, value)
        # otherwise insert key/value pair
        else:
            bucket.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Remove from hash map if key is found
        """

        # determine which bucket to search for key
        hash = self.hash_function(key)
        index = hash % self.capacity
        bucket = self.buckets[index]

        # remove key if found
        if bucket.contains(key):
            bucket.remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Return True if key is found, False otherwise
        """

        # determine which bucket to search for key
        hash = self.hash_function(key)
        index = hash % self.capacity
        bucket = self.buckets[index]

        # search for key
        if bucket.contains(key):
            return True
        return False

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table
        """

        count = 0
        for i in range(self.capacity):
            bucket = self.buckets[i]
            # add to count if bucket is empty
            if bucket.length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Calculate and return the hash table's load factor
        """

        num_elements = self.size
        num_buckets = self.capacity

        return num_elements/num_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the hash table's capacity and rehash existing content
        """

        if new_capacity < 1:
            return

        # create new hash table
        new_table = HashMap(new_capacity, self.hash_function)
        # rehash all content and add to new table
        for i in range(self.capacity):
            for node in self.buckets[i]:
                new_table.put(node.key, node.value)

        # assign new table attributes to self
        self.size = new_table.size
        self.buckets = new_table.buckets
        self.capacity = new_capacity

    def get_keys(self) -> DynamicArray:
        """
        Return a DynamicArray of all keys in hash map
        """

        array = DynamicArray()
        # append keys from buckets to array
        for i in range(self.capacity):
            for node in self.buckets[i]:
                array.append(node.key)
        return array


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
