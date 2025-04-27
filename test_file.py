#!/usr/bin/env python3
"""
Test file for Code Line Counter
Copyright (c) 2025 Mahmoud Ashraf (SNO7E)
MIT License
"""
# This is a test file to verify code counter functionality
# It contains comments, code, and blank lines

"""
This is a multi-line comment
that spans multiple lines
and should be counted correctly
"""

import sys
import os

# Define a sample function
def hello_world():
    print("Hello, World!")  # This is an inline comment
    
    # This is another comment
    return True

# Empty lines below

class TestClass:
    '''
    This is a class docstring
    which is also a comment
    '''
    def __init__(self):
        self.value = 42
        
    def get_value(self):
        # Return the value
        return self.value

# Main execution
if __name__ == "__main__":
    hello_world()
    
    test = TestClass()
    print(f"The value is: {test.get_value()}")
    
    # End of file 