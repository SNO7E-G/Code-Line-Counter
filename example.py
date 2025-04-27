#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of Code Line Counter

This is a sample file to demonstrate the code counter functionality.
It contains a mix of code, comments, and blank lines that can be analyzed.
"""

# Import standard libraries
import os
import sys

# Define a sample function with comments
def hello_world():
    """
    A simple function that prints a greeting
    This is a multi-line docstring comment
    """
    # This is a single line comment
    print("Hello, World!")  # This is an inline comment
    
    # Return success
    return True

# Define a sample class
class Example:
    """Example class for demonstration"""
    
    def __init__(self, name="Example"):
        self.name = name
    
    def get_name(self):
        # Return the name
        return self.name

# Main execution
if __name__ == "__main__":
    # Call the hello_world function
    hello_world()
    
    # Create an instance of Example
    example = Example("Code Counter")
    
    # Print information about using the Code Line Counter
    print("\nTo use the Code Line Counter tool:")
    print("python code_counter.py path/to/file/or/directory")
    print("python code_counter.py --chart -e .py .js .ts project_directory")
    print("python code_counter.py -s files -x node_modules vendor project_directory")
    print("python code_counter.py --csv report.csv project_directory") 