# tinycolors New API - Quick Reference

## Import

```python
from tinycolors import colortext, cprint, cinput
```

## colortext() Function

Returns colorized text with ANSI codes.

```python
# Style + color
colortext("text", as_="bold red")
colortext("text", as_="italic cyan")
colortext("text", as_="underline yellow")

# Style + color + background
colortext("text", as_="bold white on red")
colortext("text", as_="italic cyan on black")
colortext("text", as_="bold black on yellow")
```

## cprint() Function

Prints colorized text directly.

```python
# New API
cprint("Error!", as_="bold red")
cprint("Success!", as_="bold green on black")

# Old API (still works)
cprint("Error!", color="red", style="bold")
```

## cinput() Function

Gets user input with colorized prompt.

```python
# New API
name = cinput("Name: ", as_="bold blue")
email = cinput("Email: ", as_="italic cyan")

# Old API (still works)
name = cinput("Name: ", color="blue", style="bold")
```

## Available Styles (9)

- `bold` - Bold text
- `dim` - Dimmed/faint text
- `italic` - Italic text
- `underline` - Underlined text
- `blink` - Blinking text
- `fast_blink` - Fast blinking text
- `inverse` - Inverted foreground/background
- `hidden` - Hidden text
- `strike` - Strikethrough text

## Available Colors (18)

**Standard colors:**
- `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, `gray`, `default`

**Bright colors:**
- `bright black`, `bright red`, `bright green`, `bright yellow`
- `bright blue`, `bright magenta`, `bright cyan`, `bright white`

## Common UI Patterns

```python
# Error messages
colortext(" ERROR ", as_="bold white on red")
colortext("Error: ", as_="bold red")

# Success messages
colortext(" SUCCESS ", as_="bold white on green")
colortext("Success: ", as_="bold green")

# Warnings
colortext(" WARNING ", as_="bold black on yellow")
colortext("Warning: ", as_="bold yellow")

# Info messages
colortext(" INFO ", as_="bold white on blue")
colortext("Info: ", as_="italic cyan")

# Debug messages
colortext("Debug: ", as_="dim gray")
```

## Log Severity Levels

```python
cprint("DEBUG   ", as_="dim gray")
cprint("INFO    ", as_="italic cyan")
cprint("WARNING ", as_="bold yellow")
cprint("ERROR   ", as_="bold red")
cprint("CRITICAL", as_="bold white on red")
```

## Terminal Prompts

```python
user = colortext("user@host", as_="bold green")
path = colortext("~/project", as_="bold blue")
print(f"{user}:{path}$ ", end="")
```

## Status Indicators

```python
print("[" + colortext("OK", as_="bold green") + "] Service started")
print("[" + colortext("FAIL", as_="bold red") + "] Connection failed")
print("[" + colortext("SKIP", as_="bold yellow") + "] Test skipped")
```

## Syntax Highlighting

```python
keyword = colortext("def", as_="bold magenta")
function = colortext("my_function", as_="bold blue")
param = colortext("x", as_="italic cyan")
number = colortext("42", as_="bold yellow")

print(f"{keyword} {function}({param}): return {number}")
```

## Tips

1. **Use IDE autocomplete**: The `as_` parameter has type hints for all valid styles
2. **Prefer new API**: More concise and readable than separate parameters
3. **Legacy compatibility**: Old API still works, no need to update existing code
4. **Background colors**: Use "X on Y" format for backgrounds
5. **High contrast**: Choose contrasting colors for readability
6. **Error handling**: Invalid styles raise `StyleNotFoundError`

## Total Combinations Available

- **162** style + color combinations (e.g., "bold red")
- **78** practical style + color + background combinations (e.g., "bold white on red")
- **240** total pre-defined combinations

## Example Application

```python
from tinycolors import colortext, cprint

# Application header
cprint("=" * 60, as_="bold cyan")
cprint("  My Application v1.0", as_="bold bright white")
cprint("=" * 60, as_="bold cyan")
print()

# Process steps
cprint("1. Loading configuration...", as_="dim cyan")
cprint("   " + colortext("✓", as_="bold green") + " Configuration loaded", as_="dim white")
print()

cprint("2. Connecting to database...", as_="dim cyan")
cprint("   " + colortext("✓", as_="bold green") + " Connected successfully", as_="dim white")
print()

cprint("3. Processing data...", as_="dim cyan")
cprint("   " + colortext("✗", as_="bold red") + " Error: Invalid data format", as_="dim white")
print()

# Summary
print()
cprint("Summary:", as_="bold white")
print("  Passed: " + colortext("2", as_="bold green"))
print("  Failed: " + colortext("1", as_="bold red"))
```

## More Information

See `ENHANCEMENT_SUMMARY.md` for complete implementation details.
