# 📊 Code Line Counter

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
[![GitHub stars](https://img.shields.io/github/stars/SNO7E-G/Code-Line-Counter.svg)](https://github.com/SNO7E-G/Code-Line-Counter/stargazers)

A versatile and efficient Python tool for counting code lines, comments, and blank lines in source files across multiple programming languages.

**Author:** Mahmoud Ashraf (SNO7E)  
**License:** MIT  
**Copyright:** © 2025 Mahmoud Ashraf

## ✨ Features

- **Advanced Code Analysis**: Counts total lines, code lines, comment lines, and blank lines
- **Multi-Language Support**: Over 25 programming languages with automatic comment detection
- **Colorized Output**: Beautiful terminal output with syntax highlighting
- **Data Visualization**: Simple ASCII charts to visualize code distribution
- **Customizable Analysis**: Filter by file extensions, directories, or specific files
- **Export Capability**: Export results to CSV for further analysis
- **Performance Optimized**: Fast analysis with progress indication for large codebases
- **Smart Extension Detection**: Automatically detects file types even without extensions
- **Hidden File Handling**: Option to include or exclude hidden files
- **Symbolic Link Support**: Option to follow symbolic links for complete analysis
- **Depth Control**: Limit recursive analysis depth to focus on specific directories
- **Sorting Options**: Sort results by different metrics
- **Percentage View**: See the proportion of code, comments, and blank lines (with option to hide)
- **Zero Division Protection**: Handles empty files without errors

## 🔍 Supported Languages

| Language | Extensions | Language | Extensions |
|----------|------------|----------|------------|
| Python | .py | JavaScript | .js |
| TypeScript | .ts | React (JSX/TSX) | .jsx, .tsx |
| HTML | .html | CSS | .css |
| Java | .java | C/C++ | .c, .cpp |
| PHP | .php | Ruby | .rb |
| Swift | .swift | Go | .go |
| Rust | .rs | Kotlin | .kt |
| Shell/Bash | .sh, .bash | JSON | .json |
| XML | .xml | YAML | .yml, .yaml |
| Markdown | .md | Lua | .lua |
| PowerShell | .ps1 | SQL | .sql |
| Scala | .scala | Dart | .dart |
| R | .r | Perl | .pl |

## 🚀 Installation

### From PyPI (coming soon)

```bash
pip install code-line-counter
```

### From Source

```bash
git clone https://github.com/SNO7E-G/code-line-counter.git
cd code-line-counter
pip install -e .
```

## 📖 Usage

### Command Line Interface

```bash
# Analyze a single file
python code_counter.py path/to/your/file.py

# Analyze a directory
python code_counter.py path/to/your/project

# Analyze only specific file extensions
python code_counter.py -e .py .js .ts path/to/your/project

# Exclude directories
python code_counter.py -x node_modules vendor build path/to/your/project

# Generate ASCII bar chart visualization
python code_counter.py --chart path/to/your/project

# Export results to CSV
python code_counter.py --csv report.csv path/to/your/project

# Sort results by code lines
python code_counter.py -s code path/to/your/project

# Include hidden files and directories
python code_counter.py --hidden path/to/your/project

# Hide percentage columns in output
python code_counter.py --no-percentage path/to/your/project

# Show detailed help
python code_counter.py --help
```

### As a Python Module

```python
from code_counter import count_lines, analyze_directory, print_results

# Analyze a single file
total, code, comment, blank = count_lines('path/to/your/file.py')
print(f"Total: {total}, Code: {code}, Comments: {comment}, Blank: {blank}")

# Analyze a directory
results, total_results, skipped, elapsed = analyze_directory(
    'path/to/your/project',
    extensions=['.py', '.js'],
    exclude=['node_modules', 'venv']
)

# Print formatted results
print_results(results, total_results, elapsed_time=elapsed)
```

## 📋 Sample Output

```
Analyzing directory: ./my-project

Extension  Language    Files    Total      Code       Comments   Blank     Code%      Comments%  Blank%    
--------------------------------------------------------------------------------------------------
.py        Python      12       1458       942        286        230       64.6%      19.6%      15.8%    
.js        JavaScript  8        952        723        98         131       75.9%      10.3%      13.8%    
.tsx       React TSX   5        687        495        102        90        72.1%      14.8%      13.1%    
.html      HTML        3        324        285        12         27        88.0%      3.7%       8.3%     
.css       CSS         2        198        158        23         17        79.8%      11.6%      8.6%     
--------------------------------------------------------------------------------------------------
Total                  30       3619       2603       521        495       71.9%      14.4%      13.7%    

Analysis completed in: 0.45 seconds

Distribution of code lines by language:

Python (.py)           ████████████████████████ 942    (36.2%)
JavaScript (.js)       ██████████████████ 723        (27.8%)
React TSX (.tsx)       █████████████ 495             (19.0%)
HTML (.html)           ███████ 285                   (10.9%)
CSS (.css)             ████ 158                      (6.1%)
```

## 📈 CSV Export Format

When using the `--csv` option, the tool exports results in the following format:

```csv
Extension,Language,Files,Total Lines,Code Lines,Comment Lines,Blank Lines,Code %,Comment %,Blank %
.py,Python,12,1458,942,286,230,64.6,19.6,15.8
.js,JavaScript,8,952,723,98,131,75.9,10.3,13.8
...
TOTAL,,30,3619,2603,521,495,71.9,14.4,13.7
```

## 🔧 Advanced Usage

### Using as a Python Module

You can use Code Line Counter as a module in your own Python scripts:

```python
from code_counter import count_lines, analyze_directory, print_results

# Analyze a single file
total, code, comment, blank = count_lines("myfile.py")
print(f"Code lines: {code}")

# Analyze a directory
results, total_results, skipped_files, elapsed_time = analyze_directory(
    ".", extensions=[".py", ".js"], exclude=["venv"]
)
print_results(results, total_results)
```

### Integration with Build Systems

You can integrate Code Line Counter into your build process to track code metrics over time:

```bash
# Example for CI/CD pipeline
python code_counter.py . --csv metrics.csv
python analyze_metrics.py metrics.csv # Your custom analysis script
```

## 🛠️ Error Handling

Code Line Counter is built with robust error handling:

- Gracefully handles files with encoding issues
- Skips files that can't be accessed or read
- Reports files that were skipped during analysis
- Prevents division by zero errors with empty files
- Safely processes large codebases with memory efficiency

## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📜 License

MIT License

Copyright (c) 2025 Mahmoud Ashraf (SNO7E)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 