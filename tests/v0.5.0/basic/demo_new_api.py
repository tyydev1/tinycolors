#!/usr/bin/env python3
"""
Demo script showcasing the new simplified color API for tinycolors.
"""

import sys
sys.path.insert(0, '/')

from tinycolors import colortext, cprint

print("=" * 70)
print("              tinycolors - New Simplified API Demo")
print("=" * 70)
print()

# Example 1: Basic colortext() usage
print("1. Using colortext() function:")
print()
print("   Simple styles:")
print("   " + colortext("Bold red text", as_="bold red"))
print("   " + colortext("Italic cyan text", as_="italic cyan"))
print("   " + colortext("Underline yellow text", as_="underline yellow"))
print("   " + colortext("Dim magenta text", as_="dim magenta"))
print()

# Example 2: With backgrounds
print("2. Using backgrounds:")
print()
print("   " + colortext(" ERROR ", as_="bold white on red") + " Critical failure occurred")
print("   " + colortext(" SUCCESS ", as_="bold white on green") + " Operation completed")
print("   " + colortext(" WARNING ", as_="bold black on yellow") + " Potential issue detected")
print("   " + colortext(" INFO ", as_="bold white on blue") + " System information")
print()

# Example 3: Bright colors
print("3. Using bright colors:")
print()
print("   " + colortext("Bright red", as_="bold bright red"))
print("   " + colortext("Bright green", as_="bold bright green"))
print("   " + colortext("Bright cyan", as_="bold bright cyan"))
print("   " + colortext("Bright yellow", as_="bold bright yellow"))
print()

# Example 4: Using cprint() with new API
print("4. Using cprint() with new API:")
print()
cprint("   This is bold magenta", as_="bold magenta")
cprint("   This is italic green", as_="italic green")
cprint("   This is strike red", as_="strike red")
cprint("   This is inverse white", as_="inverse white")
print()

# Example 5: Common UI patterns
print("5. Common UI patterns:")
print()
print("   Terminal prompts:")
print("   " + colortext("user@host", as_="bold green") + ":" + colortext("~/project", as_="bold blue") + "$ ls")
print()
print("   Status messages:")
print("   [" + colortext("OK", as_="bold green") + "] Service started successfully")
print("   [" + colortext("FAIL", as_="bold red") + "] Connection timeout")
print("   [" + colortext("WARN", as_="bold yellow") + "] Deprecated API usage")
print()

# Example 6: Comparison with old API
print("6. API Comparison:")
print()
print("   Old API (still works):")
cprint("   Red bold text", color="red", style="bold")
print()
print("   New API (cleaner):")
cprint("   Red bold text", as_="bold red")
print()

# Example 7: Error severity levels
print("7. Error severity visualization:")
print()
print("   " + colortext("DEBUG", as_="dim gray") + "   - Debug information")
print("   " + colortext("INFO", as_="italic cyan") + "    - General information")
print("   " + colortext("WARNING", as_="bold yellow") + " - Warning message")
print("   " + colortext("ERROR", as_="bold red") + "   - Error occurred")
print("   " + colortext("CRITICAL", as_="bold white on red") + " - Critical failure")
print()

# Example 8: Code highlighting
print("8. Code-like output:")
print()
print("   " + colortext("def", as_="bold magenta") + " " +
      colortext("my_function", as_="bold blue") + "(" +
      colortext("param", as_="italic cyan") + "):")
print("       " + colortext("return", as_="bold magenta") + " " +
      colortext("param", as_="italic cyan") + " * " +
      colortext("2", as_="bold yellow"))
print()

# Example 9: Table-like output
print("9. Formatted table:")
print()
print("   " + colortext("Name", as_="bold white on black") + "        " +
      colortext("Status", as_="bold white on black") + "     " +
      colortext("Duration", as_="bold white on black"))
print("   " + "-" * 50)
print("   test_login    " + colortext("PASSED", as_="bold green") + "    0.5s")
print("   test_auth     " + colortext("FAILED", as_="bold red") + "    1.2s")
print("   test_api      " + colortext("SKIPPED", as_="bold yellow") + "   0.0s")
print()

print("=" * 70)
print("Demo completed!")
print("=" * 70)
