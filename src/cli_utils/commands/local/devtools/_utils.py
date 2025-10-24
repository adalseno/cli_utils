"""Utility functions for code analysis."""

import ast
import json
from pathlib import Path

from colorama import Fore, Style, init

init(autoreset=True)


def analyze_file(filepath: Path):
    """
    Analyze a single file and return a dictionary with file metrics.

    The returned dictionary will have the following keys:
    - 'file': the name of the file
    - 'path': the path to the file
    - 'lines': the number of meaningful lines (excluding blank lines and comments)
    - 'classes': the number of classes found
    - 'functions': the number of standalone functions found
    - 'methods': the total number of methods found
    - 'class_methods': a dictionary with class names as keys and the number of methods found in each class as values

    If there is an error reading the file, the function will return None.
    If there is a syntax error when parsing the file, the function will return a dictionary with default values for the metrics.
    """
    try:
        source = filepath.read_text(encoding='utf-8')
    except Exception:
        return None

    lines = source.splitlines()
    meaningful_lines = [
        line for line in lines if line.strip() and not line.strip().startswith('#')
    ]

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {
            'file': filepath.name,
            'path': str(filepath),
            'lines': len(meaningful_lines),
            'classes': 0,
            'functions': 0,
            'methods': 0,
            'class_methods': {}
        }

    class_count = 0
    function_count = 0
    method_names = set()
    class_methods = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_count += 1
            method_count = 0
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_count += 1
                    method_names.add(item.name)
            class_methods[node.name] = method_count
        elif isinstance(node, ast.FunctionDef):
            if node.name not in method_names:
                function_count += 1

    return {
        'file': filepath.name,
        'path': str(filepath),
        'lines': len(meaningful_lines),
        'classes': class_count,
        'functions': function_count,
        'methods': sum(class_methods.values()),
        'class_methods': class_methods
    }


def gather_reports(base: Path, recursive: bool = False):
    """
    Gather code reports for all .py files in the given directory.

    Parameters
    ----------
    base : Path
        The directory to search for .py files.
    recursive : bool, optional
        Whether to search recursively in subdirectories. Defaults to False.

    Returns
    -------
    reports : list of dict
        A list of dictionaries with code metrics for each file.
    total_lines : int
        The total number of meaningful lines in all files.
    """
    pattern = "**/*.py" if recursive else "*.py"
    files = sorted(base.glob(pattern))
    reports = []

    for f in files:
        result = analyze_file(f)
        if result:
            reports.append(result)

    total_lines = sum(r['lines'] for r in reports)
    for r in reports:
        r['percent'] = (r['lines'] / total_lines * 100) if total_lines > 0 else 0

    return reports, total_lines


def print_text_report(reports, total_lines):
    """
    Print a text-based code report.

    Parameters
    ----------
    reports : list of dict
        A list of dictionaries with code metrics for each file.
    total_lines : int
        The total number of meaningful lines in all files.
    """
    for i, r in enumerate(reports):
        prefix = "└──" if i == len(reports) - 1 else "├──"
        print(
            f"{Fore.YELLOW}{prefix} {r['file']:<28} "
            f"{Style.DIM}({r['lines']:>5} lines, "
            f"{Fore.CYAN}{r['classes']} classes, "
            f"{Fore.GREEN}{r['functions']} functions, "
            f"{Fore.MAGENTA}{r['methods']} methods, "
            f"{Fore.BLUE}{r['percent']:.1f}% of total)"
        )
        for cname, mcount in sorted(r['class_methods'].items()):
            print(f"    {Style.DIM}- {Fore.CYAN}{cname}{Style.RESET_ALL}: {Fore.MAGENTA}{mcount} methods")

    print(f"\n{Style.BRIGHT}{Fore.BLUE}Total:")
    print(f"  Files     : {len(reports)}")
    print(f"  Lines     : {total_lines}")
    print(f"  Classes   : {sum(r['classes'] for r in reports)}")
    print(f"  Functions : {sum(r['functions'] for r in reports)}")
    print(f"  Methods   : {sum(r['methods'] for r in reports)}")


def print_json_report(reports, total_lines):
    """
    Print a JSON-based code report.

    Parameters
    ----------
    reports : list of dict
        A list of dictionaries with code metrics for each file.
    total_lines : int
        The total number of meaningful lines in all files.
    """
    summary = {
        'total_files': len(reports),
        'total_lines': total_lines,
        'total_classes': sum(r['classes'] for r in reports),
        'total_functions': sum(r['functions'] for r in reports),
        'total_methods': sum(r['methods'] for r in reports),
        'files': reports
    }
    print(json.dumps(summary, indent=2))


def print_markdown_report(reports, total_lines):
    """
    Print a markdown-based code report.

    Parameters
    ----------
    reports : list of dict
        A list of dictionaries with code metrics for each file.
    total_lines : int
        The total number of meaningful lines in all files.

    Prints a markdown table with columns for file name, lines, classes, functions, methods, and percentage of total lines.

    Also prints a markdown section for total metrics.
    """
    print("| File | Lines | Classes | Functions | Methods | % of Total |")
    print("|------|-------|---------|-----------|---------|------------|")
    for r in reports:
        print(f"| `{r['file']}` | {r['lines']} | {r['classes']} | {r['functions']} | {r['methods']} | {r['percent']:.1f}% |")

    print("\n**Total:**")
    print(f"- Files: {len(reports)}")
    print(f"- Lines: {total_lines}")
    print(f"- Classes: {sum(r['classes'] for r in reports)}")
    print(f"- Functions: {sum(r['functions'] for r in reports)}")
    print(f"- Methods: {sum(r['methods'] for r in reports)}")


def generate_text_report(reports, total_lines):
    """
    Generate a text-based code report as a string.

    Parameters
    ----------
    reports : list of dict
        A list of dictionaries with code metrics for each file.
    total_lines : int
        The total number of meaningful lines in all files.

    Returns
    -------
    str
        The formatted text report.
    """
    lines = []
    for i, r in enumerate(reports):
        prefix = "└──" if i == len(reports) - 1 else "├──"
        lines.append(
            f"{prefix} {r['file']:<28} "
            f"({r['lines']:>5} lines, "
            f"{r['classes']} classes, "
            f"{r['functions']} functions, "
            f"{r['methods']} methods, "
            f"{r['percent']:.1f}% of total)"
        )
        for cname, mcount in sorted(r['class_methods'].items()):
            lines.append(f"    - {cname}: {mcount} methods")

    lines.append(f"\nTotal:")
    lines.append(f"  Files     : {len(reports)}")
    lines.append(f"  Lines     : {total_lines}")
    lines.append(f"  Classes   : {sum(r['classes'] for r in reports)}")
    lines.append(f"  Functions : {sum(r['functions'] for r in reports)}")
    lines.append(f"  Methods   : {sum(r['methods'] for r in reports)}")

    return "\n".join(lines)


def generate_json_report(reports, total_lines):
    """
    Generate a JSON-based code report as a string.

    Parameters
    ----------
    reports : list of dict
        A list of dictionaries with code metrics for each file.
    total_lines : int
        The total number of meaningful lines in all files.

    Returns
    -------
    str
        The formatted JSON report.
    """
    summary = {
        'total_files': len(reports),
        'total_lines': total_lines,
        'total_classes': sum(r['classes'] for r in reports),
        'total_functions': sum(r['functions'] for r in reports),
        'total_methods': sum(r['methods'] for r in reports),
        'files': reports
    }
    return json.dumps(summary, indent=2)


def generate_markdown_report(reports, total_lines):
    """
    Generate a markdown-based code report as a string.

    Parameters
    ----------
    reports : list of dict
        A list of dictionaries with code metrics for each file.
    total_lines : int
        The total number of meaningful lines in all files.

    Returns
    -------
    str
        The formatted markdown report.
    """
    lines = []
    lines.append("| File | Lines | Classes | Functions | Methods | % of Total |")
    lines.append("|------|-------|---------|-----------|---------|------------|")
    for r in reports:
        lines.append(f"| `{r['file']}` | {r['lines']} | {r['classes']} | {r['functions']} | {r['methods']} | {r['percent']:.1f}% |")

    lines.append("\n**Total:**")
    lines.append(f"- Files: {len(reports)}")
    lines.append(f"- Lines: {total_lines}")
    lines.append(f"- Classes: {sum(r['classes'] for r in reports)}")
    lines.append(f"- Functions: {sum(r['functions'] for r in reports)}")
    lines.append(f"- Methods: {sum(r['methods'] for r in reports)}")

    return "\n".join(lines)
