from __future__ import annotations
from typing import Optional, Callable, Iterator


class Node:
    def __init__(self, key: str, value: int, next: Optional["Node"] = None) -> None:
        self.key = key
        self.value = value
        self.next = next


# ------------------------------------------------------------
# Hash functions 
# ------------------------------------------------------------

def hash_function1(table: "HashTable", key: str) -> int:
    return ord(key[0]) % table.size

def hash_function2(table: "HashTable", key: str) -> int:
    salt = 1
    hash_value = 0
    modulus = table.size
    for i in range(len(key)):
        hash_value += ord(key[i]) * i * salt
        hash_value = hash_value % modulus + hash_value // modulus
    hash_value = hash_value % modulus
    return hash_value


# ------------------------------------------------------------
# Hash Table Class
# ------------------------------------------------------------

class HashTable:
    def __init__(self, size: int) -> None:
        self.size = size
        self.total = 0
        self.buckets: list[Optional[Node]] = [None] * size

    # --------------------------------------------------------
    # Core operations
    # --------------------------------------------------------

    def add(self, key: str, value: int, hf: Callable[["HashTable", str], int]) -> None:
        index = hf(self, key)
        head = self.buckets[index]

        # Replace existing key
        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # Insert new node at head
        new_node = Node(key, value, head)
        self.buckets[index] = new_node
        self.total += 1

    def remove(self, key: str, hf: Callable[["HashTable", str], int]) -> bool:
        index = hf(self, key)
        curr_node = self.buckets[index]

        # Check certain edge cases
        if curr_node is None:
            return False
        elif curr_node.key == key:
            self.buckets[index] = curr_node.next
            return True
        
        # Start iterating
        prev_node: Node = curr_node
        while True:
            if curr_node.key == key:
                prev_node.next = curr_node.next
                return True
            elif curr_node.next is None:
                return False
            else:
                # Proceed to the next node
                prev_node = curr_node
                curr_node = curr_node.next

    def get(self, key: str, hf: Callable[["HashTable", str], int]) -> Optional[int]:
        index = hf(self, key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    # --------------------------------------------------------
    # dunder methods for easy interface
    # --------------------------------------------------------

    def __setitem__(self, key: str, value: int) -> None:
        self.add(key, value, hash_function1)

    def __getitem__(self, key: str) -> int:
        value = self.get(key, hash_function1)
        if value is None:
            raise KeyError(key)
        return value

    def __delitem__(self, key: str) -> None:
        if not self.remove(key, hash_function1):
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return self.get(key, hash_function1) is not None

    def __iter__(self) -> Iterator[str]:
        for bucket in self.buckets:
            current = bucket
            while current:
                yield current.key
                current = current.next

    # --------------------------------------------------------
    # Utility methods
    # --------------------------------------------------------

    def reset(self) -> None:
        self.buckets = [None] * self.size
        self.total = 0

    def collisions(self) -> int:
        num = 0
        for bucket in self.buckets:
            if bucket is not None:
                curr_bucket: Node = bucket
                while curr_bucket.next is not None:
                    num += 1
                    curr_bucket = curr_bucket.next
        return num

    def display(self) -> None:
        # print out the hash table in a readable format.
        # best not alter the display function as it is used in evaluating the output.
        print(f"HashTable(size={self.size}, total={self.total})")
        for i, bucket in enumerate(self.buckets):
            print(f"bucket[{i}]", end="")
            current = bucket
            if not current:
                print(" -|")
                continue
            while current:
                print(f" -> (key={current.key}, value={current.value})", end="")
                current = current.next
            print(" -|")
        print()
