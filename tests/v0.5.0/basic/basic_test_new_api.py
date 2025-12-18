#!/usr/bin/env python3
"""Test script for the new combined styles API."""

import sys
sys.path.insert(0, '/')

from tinycolors import colortext, cprint, COMBINED_STYLES, COMBINED_STYLES_WITH_BG

print("=" * 60)
print("Testing tinycolors new simplified API")
print("=" * 60)
print()

# Test 1: Verify COMBINED_STYLES count
print("Test 1: COMBINED_STYLES dictionary")
print(f"  Total combinations: {len(COMBINED_STYLES)}")
print(f"  Expected: 162 (9 styles × 18 colors)")
print(f"  Status: {'PASS' if len(COMBINED_STYLES) == 162 else 'FAIL'}")
print()

# Test 2: Verify COMBINED_STYLES_WITH_BG count
print("Test 2: COMBINED_STYLES_WITH_BG dictionary")
print(f"  Total combinations: {len(COMBINED_STYLES_WITH_BG)}")
print(f"  Expected: 50-100 practical combinations")
print(f"  Status: {'PASS' if 50 <= len(COMBINED_STYLES_WITH_BG) <= 100 else 'FAIL'}")
print()

# Test 3: Sample COMBINED_STYLES entries
print("Test 3: Sample COMBINED_STYLES entries")
sample_styles = ["bold red", "dim green", "italic bright cyan", "underline default"]
for style in sample_styles:
    if style in COMBINED_STYLES:
        result = colortext("Sample", as_=style)
        print(f"  {style}: {result}")
    else:
        print(f"  {style}: MISSING!")
print()

# Test 4: Sample COMBINED_STYLES_WITH_BG entries
print("Test 4: Sample COMBINED_STYLES_WITH_BG entries")
sample_bg_styles = [
    "bold red on black",
    "bold white on red",
    "italic cyan on black",
    "dim green on black"
]
for style in sample_bg_styles:
    if style in COMBINED_STYLES_WITH_BG:
        result = colortext("Sample", as_=style)
        print(f"  {style}: {result}")
    else:
        print(f"  {style}: MISSING!")
print()

# Test 5: colortext() function with various styles
print("Test 5: colortext() function tests")
print("  " + colortext("Error!", as_="bold red"))
print("  " + colortext("Success!", as_="bold green"))
print("  " + colortext("Warning!", as_="bold yellow"))
print("  " + colortext("Info", as_="italic cyan"))
print("  " + colortext("Bright text", as_="bold bright white"))
print()

# Test 6: colortext() function with backgrounds
print("Test 6: colortext() function with backgrounds")
print("  " + colortext("Critical Error!", as_="bold white on red"))
print("  " + colortext("Success Message", as_="bold green on black"))
print("  " + colortext("Highlighted", as_="bold black on yellow"))
print("  " + colortext("Notification", as_="italic white on blue"))
print()

# Test 7: cprint() function with new API
print("Test 7: cprint() function with new API")
cprint("  Bold red text", as_="bold red")
cprint("  Italic cyan text", as_="italic cyan")
cprint("  Underline blue text", as_="underline blue")
cprint("  Bold white on red", as_="bold white on red")
print()

# Test 8: cprint() function with legacy API (backward compatibility)
print("Test 8: cprint() function with legacy API (backward compatibility)")
cprint("  Legacy: red + bold", color="red", style="bold")
cprint("  Legacy: green + italic", color="green", style="italic")
cprint("  Legacy: blue + underline", color="blue", style="underline")
print()

# Test 9: All 9 styles
print("Test 9: All 9 styles with red color")
styles = ["bold", "dim", "italic", "underline", "blink", "fast_blink", "inverse", "hidden", "strike"]
for style in styles:
    try:
        result = colortext(f"{style} red", as_=f"{style} red")
        print(f"  {result}")
    except Exception as e:
        print(f"  {style} red: FAILED - {e}")
print()

# Test 10: All 18 colors with bold style
print("Test 10: All 18 colors with bold style")
colors = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "gray", "default",
    "bright black", "bright red", "bright green", "bright yellow",
    "bright blue", "bright magenta", "bright cyan", "bright white"
]
for clr in colors:
    try:
        result = colortext(f"bold {clr}", as_=f"bold {clr}")
        print(f"  {result}")
    except Exception as e:
        print(f"  bold {clr}: FAILED - {e}")
print()

# Test 11: Error handling
print("Test 11: Error handling")
try:
    colortext("test", as_="invalid style")
    print("  ERROR: Should have raised StyleNotFoundError!")
except Exception as e:
    print(f"  Correctly raised: {type(e).__name__}")
print()

# Test 12: Visual comparison
print("Test 12: Visual comparison of common patterns")
print("  Errors:")
print("    " + colortext("ERROR", as_="bold red"))
print("    " + colortext("ERROR", as_="bold white on red"))
print("    " + colortext("CRITICAL", as_="bold bright white on red"))
print()
print("  Success:")
print("    " + colortext("SUCCESS", as_="bold green"))
print("    " + colortext("SUCCESS", as_="bold green on black"))
print("    " + colortext("PASSED", as_="bold bright green on black"))
print()
print("  Warnings:")
print("    " + colortext("WARNING", as_="bold yellow"))
print("    " + colortext("WARNING", as_="bold yellow on black"))
print("    " + colortext("CAUTION", as_="bold black on yellow"))
print()
print("  Info:")
print("    " + colortext("INFO", as_="italic cyan"))
print("    " + colortext("INFO", as_="italic bright cyan on black"))
print("    " + colortext("NOTE", as_="dim cyan on black"))
print()

print("=" * 60)
print("All tests completed!")
print("=" * 60)
