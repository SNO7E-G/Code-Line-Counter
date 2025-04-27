#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code Line Counter - A tool to count lines of code while ignoring comments and empty lines
Copyright (c) 2025 Mahmoud Ashraf (SNO7E)
MIT License
"""
import os
import re
import argparse
import sys
from collections import defaultdict
from datetime import datetime

# ANSI color codes for colorized terminal output
COLORS = {
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'CYAN': '\033[96m',
    'WHITE': '\033[97m',
    'GRAY': '\033[90m',
}

# Dictionary of language-specific comment patterns
COMMENT_PATTERNS = {
    '.py': [r'#.*', r'""".*?"""', r"'''.*?'''"],
    '.js': [r'//.*', r'/\*.*?\*/', r'<!--.*?-->'],
    '.jsx': [r'//.*', r'/\*.*?\*/', r'<!--.*?-->'],
    '.ts': [r'//.*', r'/\*.*?\*/'],
    '.tsx': [r'//.*', r'/\*.*?\*/', r'<!--.*?-->'],
    '.html': [r'<!--.*?-->'],
    '.css': [r'/\*.*?\*/'],
    '.java': [r'//.*', r'/\*.*?\*/'],
    '.c': [r'//.*', r'/\*.*?\*/'],
    '.cpp': [r'//.*', r'/\*.*?\*/'],
    '.php': [r'//.*', r'/\*.*?\*/', r'#.*'],
    '.rb': [r'#.*', r'=begin.*?=end'],
    '.swift': [r'//.*', r'/\*.*?\*/'],
    '.go': [r'//.*', r'/\*.*?\*/'],
    '.rs': [r'//.*', r'/\*.*?\*/'],
    '.kt': [r'//.*', r'/\*.*?\*/'],
    '.sh': [r'#.*'],
    '.bash': [r'#.*'],
    '.json': [],
    '.xml': [r'<!--.*?-->', r'<\?.*?\?>'],
    '.yml': [r'#.*'],
    '.yaml': [r'#.*'],
    '.md': [],
    '.lua': [r'--.*', r'--\[\[.*?\]\]'],
    '.ps1': [r'#.*', r'<#.*?#>'],
    '.sql': [r'--.*', r'/\*.*?\*/'],
    '.scala': [r'//.*', r'/\*.*?\*/'],
    '.dart': [r'//.*', r'/\*.*?\*/'],
    '.r': [r'#.*'],
    '.pl': [r'#.*'],
}

FILE_EXTENSIONS = list(COMMENT_PATTERNS.keys())

# Language names for pretty output
LANGUAGE_NAMES = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.jsx': 'React JSX',
    '.ts': 'TypeScript',
    '.tsx': 'React TSX',
    '.html': 'HTML',
    '.css': 'CSS',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.php': 'PHP',
    '.rb': 'Ruby',
    '.swift': 'Swift',
    '.go': 'Go',
    '.rs': 'Rust',
    '.kt': 'Kotlin',
    '.sh': 'Shell',
    '.bash': 'Bash',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yml': 'YAML',
    '.yaml': 'YAML',
    '.md': 'Markdown',
    '.lua': 'Lua',
    '.ps1': 'PowerShell',
    '.sql': 'SQL',
    '.scala': 'Scala',
    '.dart': 'Dart',
    '.r': 'R',
    '.pl': 'Perl',
}

def is_windows():
    """Check if running on Windows"""
    return sys.platform.startswith('win')

def enable_windows_color():
    """Enable ANSI color codes in Windows console"""
    if is_windows():
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except:
            return False
    return True

def colorize(text, color):
    """Add color to text if supported"""
    global support_color
    if support_color:
        return f"{COLORS.get(color, '')}{text}{COLORS['RESET']}"
    return text

def count_lines(file_path):
    """
    Count lines of code, ignoring comments and empty lines.
    
    Args:
        file_path: Path to the file to analyze
        
    Returns:
        tuple: (total_lines, code_lines, comment_lines, blank_lines)
    """
    _, ext = os.path.splitext(file_path)
    
    # Handle files with no extension by trying to guess from content
    if not ext and os.path.isfile(file_path):
        ext = guess_file_extension(file_path)
    
    if ext not in COMMENT_PATTERNS:
        return 0, 0, 0, 0
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        try:
            content = file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return 0, 0, 0, 0
    
    # Count total lines
    lines = content.split('\n')
    total_lines = len(lines)
    
    # Count blank lines
    blank_lines = len(re.findall(r'^\s*$', content, re.MULTILINE))
    
    # Remove multi-line comments first (non-greedy matching)
    content_no_multiline = content
    for pattern in COMMENT_PATTERNS[ext]:
        if '.*?' in pattern:  # Multi-line comment patterns contain non-greedy matching
            content_no_multiline = re.sub(pattern, '', content_no_multiline, flags=re.DOTALL)
    
    # Count single-line comments 
    comment_lines = 0
    for pattern in COMMENT_PATTERNS[ext]:
        if '.*?' not in pattern:  # Single-line comment patterns don't have non-greedy matching
            comment_lines += len(re.findall(pattern, content_no_multiline))
    
    # Calculate code lines
    code_lines = total_lines - blank_lines - comment_lines
    
    return total_lines, code_lines, comment_lines, blank_lines

def guess_file_extension(file_path):
    """Try to guess file type by examining file content"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        try:
            first_lines = ''.join([file.readline() for _ in range(10)])
        except:
            return ''
    
    # Check for shebang line
    if re.search(r'^#!.*python', first_lines):
        return '.py'
    elif re.search(r'^#!.*node', first_lines) or re.search(r'^#!.*javascript', first_lines):
        return '.js'
    elif re.search(r'^#!.*(bash|sh)', first_lines):
        return '.sh'
    elif re.search(r'^#!.*perl', first_lines):
        return '.pl'
    elif re.search(r'^#!.*ruby', first_lines):
        return '.rb'
    elif re.search(r'^<!DOCTYPE html>', first_lines, re.IGNORECASE) or re.search(r'^<html', first_lines, re.IGNORECASE):
        return '.html'
    elif re.search(r'^<\?xml', first_lines):
        return '.xml'
    elif first_lines.strip().startswith('{') or first_lines.strip().startswith('['):
        return '.json'
    
    return ''  # Unable to determine file type

def analyze_directory(directory, extensions=None, exclude=None, follow_symlinks=False, max_depth=None, include_hidden=False):
    """
    Analyze all files in a directory recursively.
    
    Args:
        directory: Root directory to analyze
        extensions: List of file extensions to include
        exclude: List of directories or files to exclude
        follow_symlinks: Whether to follow symbolic links
        max_depth: Maximum depth to recurse into directories
        include_hidden: Whether to include hidden files and directories
        
    Returns:
        dict: Statistics per file extension
    """
    if extensions is None:
        extensions = FILE_EXTENSIONS
    
    if exclude is None:
        exclude = []
    
    results = defaultdict(lambda: {'files': 0, 'total': 0, 'code': 0, 'comments': 0, 'blank': 0})
    total_results = {'files': 0, 'total': 0, 'code': 0, 'comments': 0, 'blank': 0}
    
    # Track files with issues
    skipped_files = []
    
    start_time = datetime.now()
    file_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Check recursion depth
        if max_depth is not None:
            # Get relative path depth from the starting directory
            current_depth = root[len(directory):].count(os.sep)
            if current_depth >= max_depth:
                dirs.clear()  # Skip processing subdirectories
        
        # Skip hidden directories if not included
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
        # Skip excluded directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude and d not in exclude]
        
        # Skip symlink directories if not following symlinks
        if not follow_symlinks:
            dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip excluded files
            if file_path in exclude or file in exclude:
                continue
                
            # Skip hidden files if not included
            if not include_hidden and file.startswith('.'):
                continue
                
            # Skip symlinks if not following symlinks
            if not follow_symlinks and os.path.islink(file_path):
                continue

            _, ext = os.path.splitext(file)
            
            # Try to determine file type for files without extension
            if not ext:
                ext = guess_file_extension(file_path)

            if ext in extensions:
                try:
                    total, code, comment, blank = count_lines(file_path)
                    
                    results[ext]['files'] += 1
                    results[ext]['total'] += total
                    results[ext]['code'] += code
                    results[ext]['comments'] += comment
                    results[ext]['blank'] += blank
                    
                    total_results['files'] += 1
                    total_results['total'] += total
                    total_results['code'] += code
                    total_results['comments'] += comment
                    total_results['blank'] += blank
                    
                    file_count += 1
                    
                    # Print progress indicator for large directories
                    if file_count % 50 == 0:
                        sys.stdout.write(f"\rProcessing files... {file_count}")
                        sys.stdout.flush()
                except Exception as e:
                    skipped_files.append((file_path, str(e)))
    
    # Clear progress indicator
    if file_count >= 50:
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()
    
    elapsed_time = (datetime.now() - start_time).total_seconds()
    
    return results, total_results, skipped_files, elapsed_time

def print_results(results, total_results, elapsed_time=None, show_percentage=True, sort_by='code'):
    """Print analysis results in a formatted table"""
    headers = ["Extension", "Language", "Files", "Total", "Code", "Comments", "Blank"]
    
    if show_percentage:
        headers.extend(["Code%", "Comments%", "Blank%"])
    
    # Sort results by the specified column
    sorted_results = []
    for ext, data in results.items():
        if sort_by == 'code':
            sort_value = data['code']
        elif sort_by == 'files':
            sort_value = data['files']
        elif sort_by == 'total':
            sort_value = data['total']
        elif sort_by == 'ext':
            sort_value = ext
        else:
            sort_value = data['code']  # Default
        
        sorted_results.append((ext, data, sort_value))
    
    sorted_results.sort(key=lambda x: x[2], reverse=(sort_by != 'ext'))
    
    # Determine column widths
    widths = [10, 12, 8, 10, 10, 10, 10, 10, 10, 10]
    
    # Print headers
    header_row = "".join(f"{colorize(headers[i], 'BOLD'):{widths[i]}}" for i in range(len(headers)))
    print(f"\n{header_row}")
    print("-" * (sum(widths[:len(headers)])))
    
    # Print data rows
    for ext, data in sorted_results:
        lang_name = LANGUAGE_NAMES.get(ext, ext)
        row = [
            colorize(ext, 'CYAN'),
            colorize(lang_name, 'YELLOW'),
            str(data['files']),
            str(data['total']),
            colorize(str(data['code']), 'GREEN'),
            colorize(str(data['comments']), 'BLUE'),
            str(data['blank'])
        ]
        
        if show_percentage and data['total'] > 0:
            code_pct = data['code'] / data['total'] * 100
            comment_pct = data['comments'] / data['total'] * 100
            blank_pct = data['blank'] / data['total'] * 100
            
            row.extend([
                f"{code_pct:.1f}%",
                f"{comment_pct:.1f}%",
                f"{blank_pct:.1f}%"
            ])
        
        row_str = "".join(f"{col:{widths[i]}}" for i, col in enumerate(row))
        print(row_str)
    
    # Print total row
    print("-" * (sum(widths[:len(headers)])))
    
    total_row = [
        colorize("Total", 'BOLD'),
        "",
        colorize(str(total_results['files']), 'BOLD'),
        colorize(str(total_results['total']), 'BOLD'),
        colorize(str(total_results['code']), 'BOLD'),
        colorize(str(total_results['comments']), 'BOLD'),
        colorize(str(total_results['blank']), 'BOLD')
    ]
    
    if show_percentage and total_results['total'] > 0:
        code_pct = total_results['code'] / total_results['total'] * 100
        comment_pct = total_results['comments'] / total_results['total'] * 100
        blank_pct = total_results['blank'] / total_results['total'] * 100
        
        total_row.extend([
            colorize(f"{code_pct:.1f}%", 'BOLD'),
            colorize(f"{comment_pct:.1f}%", 'BOLD'),
            colorize(f"{blank_pct:.1f}%", 'BOLD')
        ])
    
    total_row_str = "".join(f"{col:{widths[i]}}" for i, col in enumerate(total_row))
    print(total_row_str)
    
    # Print elapsed time if provided
    if elapsed_time is not None:
        print(f"\n{colorize('Analysis completed in:', 'GRAY')} {colorize(f'{elapsed_time:.2f} seconds', 'GREEN')}")

def print_file_analysis(file_path, total, code, comment, blank):
    """Print analysis results for a single file with color"""
    print(f"\n{colorize('Analysis of:', 'BOLD')} {colorize(file_path, 'CYAN')}")
    print(f"{colorize('Total lines:', 'GRAY')} {total}")
    
    if total > 0:
        print(f"{colorize('Code lines:', 'GREEN')} {code} ({code/total*100:.1f}% of total)")
        print(f"{colorize('Comment lines:', 'BLUE')} {comment} ({comment/total*100:.1f}% of total)")
        print(f"{colorize('Blank lines:', 'YELLOW')} {blank} ({blank/total*100:.1f}% of total)")
    else:
        print(f"{colorize('Code lines:', 'GREEN')} {code} (0.0% of total)")
        print(f"{colorize('Comment lines:', 'BLUE')} {comment} (0.0% of total)")
        print(f"{colorize('Blank lines:', 'YELLOW')} {blank} (0.0% of total)")

def generate_ascii_bar_chart(results, total_results, metric='code'):
    """Generate a simple ASCII bar chart for a specified metric"""
    sorted_results = sorted(results.items(), key=lambda x: x[1][metric], reverse=True)
    max_value = max(data[metric] for _, data in sorted_results) if sorted_results else 0
    max_bar_length = 40
    
    if max_value == 0:
        return
    
    print(f"\n{colorize('Distribution of', 'BOLD')} {colorize(metric, 'CYAN')} {colorize('lines by language:', 'BOLD')}")
    print()
    
    for ext, data in sorted_results[:10]:  # Show top 10
        bar_length = int((data[metric] / max_value) * max_bar_length)
        percentage = (data[metric] / total_results[metric]) * 100 if total_results[metric] > 0 else 0
        lang_name = LANGUAGE_NAMES.get(ext, ext)
        lang_display = f"{lang_name} ({ext})"
        
        # Define bar color based on extension
        if ext in ['.py', '.rb', '.pl']:
            bar_color = 'BLUE'
        elif ext in ['.js', '.ts', '.jsx', '.tsx']:
            bar_color = 'YELLOW'
        elif ext in ['.java', '.kt', '.scala']:
            bar_color = 'RED'
        elif ext in ['.c', '.cpp', '.h']:
            bar_color = 'MAGENTA'
        elif ext in ['.html', '.xml', '.css']:
            bar_color = 'CYAN'
        else:
            bar_color = 'GREEN'
        
        bar = colorize('#' * bar_length, bar_color)
        print(f"{lang_display:20} {bar} {data[metric]:6} ({percentage:5.1f}%)")
    
    if len(sorted_results) > 10:
        print(f"\n{colorize('Note:', 'GRAY')} Showing top 10 of {len(sorted_results)} languages.")

def export_csv(results, total_results, filename):
    """Export results to a CSV file"""
    try:
        with open(filename, 'w', newline='') as csvfile:
            headers = ['Extension', 'Language', 'Files', 'Total Lines', 'Code Lines', 'Comment Lines', 'Blank Lines', 
                       'Code %', 'Comment %', 'Blank %']
            
            csvfile.write(','.join(headers) + '\n')
            
            for ext, data in sorted(results.items()):
                lang_name = LANGUAGE_NAMES.get(ext, ext)
                
                code_pct = data['code'] / data['total'] * 100 if data['total'] > 0 else 0
                comment_pct = data['comments'] / data['total'] * 100 if data['total'] > 0 else 0
                blank_pct = data['blank'] / data['total'] * 100 if data['total'] > 0 else 0
                
                row = [
                    ext,
                    lang_name,
                    str(data['files']),
                    str(data['total']),
                    str(data['code']),
                    str(data['comments']),
                    str(data['blank']),
                    f"{code_pct:.1f}",
                    f"{comment_pct:.1f}",
                    f"{blank_pct:.1f}"
                ]
                
                csvfile.write(','.join([f'"{item}"' if ',' in item else item for item in row]) + '\n')
            
            # Write total row
            if total_results['total'] > 0:
                code_pct = total_results['code'] / total_results['total'] * 100
                comment_pct = total_results['comments'] / total_results['total'] * 100
                blank_pct = total_results['blank'] / total_results['total'] * 100
            else:
                code_pct = comment_pct = blank_pct = 0
                
            total_row = [
                'TOTAL',
                '',
                str(total_results['files']),
                str(total_results['total']),
                str(total_results['code']),
                str(total_results['comments']),
                str(total_results['blank']),
                f"{code_pct:.1f}",
                f"{comment_pct:.1f}",
                f"{blank_pct:.1f}"
            ]
            
            csvfile.write(','.join([f'"{item}"' if ',' in item else item for item in total_row]) + '\n')
        
        print(f"\n{colorize('Results exported to:', 'BOLD')} {colorize(filename, 'GREEN')}")
        return True
    except Exception as e:
        print(f"\n{colorize('Error exporting to CSV:', 'RED')} {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Count lines of code, ignoring comments and empty lines.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('path', help='File or directory to analyze')
    parser.add_argument('-e', '--extensions', nargs='+', help='File extensions to include (e.g., .py .js)')
    parser.add_argument('-x', '--exclude', nargs='+', help='Directories or files to exclude')
    parser.add_argument('-s', '--sort', choices=['code', 'files', 'total', 'ext'], default='code',
                       help='Sort results by specified column')
    parser.add_argument('-l', '--follow-links', action='store_true', help='Follow symbolic links')
    parser.add_argument('--no-color', action='store_true', help='Disable colorized output')
    parser.add_argument('--no-percentage', action='store_true', help='Hide percentage columns')
    parser.add_argument('-d', '--max-depth', type=int, help='Maximum directory recursion depth')
    parser.add_argument('--hidden', action='store_true', help='Include hidden files and directories')
    parser.add_argument('--chart', action='store_true', help='Show ASCII bar chart visualization')
    parser.add_argument('--csv', help='Export results to a CSV file')
    
    args = parser.parse_args()
    
    # Set up color support
    global support_color
    support_color = not args.no_color and enable_windows_color()
    
    path = args.path
    extensions = args.extensions if args.extensions else FILE_EXTENSIONS
    exclude = args.exclude if args.exclude else []
    show_percentage = not args.no_percentage
    max_depth = args.max_depth
    
    if os.path.isfile(path):
        start_time = datetime.now()
        total, code, comment, blank = count_lines(path)
        elapsed_time = (datetime.now() - start_time).total_seconds()
        if total > 0:  # Only print if the file had content
            print_file_analysis(path, total, code, comment, blank)
            print(f"\n{colorize('Analysis completed in:', 'GRAY')} {colorize(f'{elapsed_time:.2f} seconds', 'GREEN')}")
    else:
        print(f"\n{colorize('Analyzing directory:', 'BOLD')} {colorize(path, 'CYAN')}")
        try:
            results, total_results, skipped_files, elapsed_time = analyze_directory(
                path, extensions, exclude, args.follow_links, max_depth, args.hidden
            )
            
            if total_results['files'] > 0:
                print_results(results, total_results, elapsed_time, show_percentage, args.sort)
                
                if args.chart and total_results['code'] > 0:
                    generate_ascii_bar_chart(results, total_results, 'code')
                    
                if args.csv:
                    export_csv(results, total_results, args.csv)
                
                # Report skipped files if any
                if skipped_files:
                    print(f"\n{colorize('Warning:', 'YELLOW')} {len(skipped_files)} files skipped due to errors")
                    for file_path, error in skipped_files[:5]:  # Show only first 5 errors
                        print(f"  - {file_path}: {error}")
                    if len(skipped_files) > 5:
                        print(f"  ... and {len(skipped_files) - 5} more")
            else:
                print(f"\n{colorize('No files were analyzed.', 'RED')} Check your path and file extensions.")
        except Exception as e:
            print(f"\n{colorize('Error during analysis:', 'RED')} {str(e)}")
            print("Please check that the directory exists and is accessible.")

if __name__ == '__main__':
    support_color = True  # Global variable for color support
    main() 