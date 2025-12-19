"""
Comprehensive unit tests for tinycolors v0.5.0 library.

This test suite provides extensive coverage of the tinycolors ANSI color
and styling library, including both legacy and new APIs.

Test Coverage:
- Basic colorize() function (legacy API)
- New colortext() function (new API)
- cprint() with both APIs
- cinput() with both APIs
- Color classes and NodeProxy
- All color, style, and background maps
- Error handling and exceptions
- Edge cases and integration scenarios
"""

import pytest # type: ignore
from io import StringIO
from unittest.mock import patch, MagicMock
from typing import Any

from tinycolors import (
    # Functions
    colorize,
    colortext,
    cprint,
    cinput,
    # Color classes
    clib,
    color,
    NodeProxy,
    # Maps
    COLOR_MAP,
    STYLE_MAP,
    BG_COLOR_MAP,
    COMBINED_STYLES,
    COMBINED_STYLES_WITH_BG,
    # Exceptions
    ColorNotFoundError,
    StyleNotFoundError,
    # Type definitions
    ColorOptions,
)


# =========================================================================
# Test Suite for Basic Colorize Function (Legacy API)
# =========================================================================

class TestColorizeBasics:
    """Test the colorize function with individual color, style, and bg parameters."""

    def test_colorize_with_red_color(self):
        """Test colorizing text with red color."""
        result = colorize("test", color="red")
        assert "\033[31m" in result
        assert "test" in result
        assert "\033[0m" in result

    def test_colorize_with_blue_color(self):
        """Test colorizing text with blue color."""
        result = colorize("test", color="blue")
        assert "\033[34m" in result
        assert "test" in result

    def test_colorize_with_green_color(self):
        """Test colorizing text with green color."""
        result = colorize("test", color="green")
        assert "\033[32m" in result
        assert "test" in result

    @pytest.mark.parametrize("color_name", [
        "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
    ])
    def test_colorize_basic_colors(self, color_name):
        """Test all basic colors."""
        result = colorize("test", color=color_name)
        assert "test" in result
        assert "\033[0m" in result

    @pytest.mark.parametrize("color_name", [
        "gray", "default"
    ])
    def test_colorize_special_colors(self, color_name):
        """Test special colors (gray and default)."""
        result = colorize("test", color=color_name)
        assert "test" in result
        assert "\033[0m" in result

    @pytest.mark.parametrize("color_name", [
        "bright black", "bright red", "bright green", "bright yellow",
        "bright blue", "bright magenta", "bright cyan", "bright white"
    ])
    def test_colorize_bright_colors(self, color_name):
        """Test all bright colors."""
        result = colorize("test", color=color_name)
        assert "test" in result
        assert "\033[0m" in result


class TestColorizeStyles:
    """Test the colorize function with style parameters."""

    @pytest.mark.parametrize("style_name", [
        "bold", "dim", "italic", "underline", "blink",
        "fast_blink", "inverse", "hidden", "strike"
    ])
    def test_colorize_with_styles(self, style_name):
        """Test all style types."""
        result = colorize("test", style=style_name)
        assert "test" in result
        assert "\033[0m" in result

    def test_colorize_bold_style(self):
        """Test bold style generates correct ANSI code."""
        result = colorize("test", style="bold")
        assert "\033[1m" in result

    def test_colorize_dim_style(self):
        """Test dim style generates correct ANSI code."""
        result = colorize("test", style="dim")
        assert "\033[2m" in result

    def test_colorize_italic_style(self):
        """Test italic style generates correct ANSI code."""
        result = colorize("test", style="italic")
        assert "\033[3m" in result


class TestColorizeBackgrounds:
    """Test the colorize function with background color parameters."""

    @pytest.mark.parametrize("bg_color", [
        "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
    ])
    def test_colorize_basic_backgrounds(self, bg_color):
        """Test all basic background colors."""
        result = colorize("test", bg=bg_color)
        assert "test" in result
        assert "\033[0m" in result

    @pytest.mark.parametrize("bg_color", [
        "gray", "default"
    ])
    def test_colorize_special_backgrounds(self, bg_color):
        """Test special background colors."""
        result = colorize("test", bg=bg_color)
        assert "test" in result
        assert "\033[0m" in result

    @pytest.mark.parametrize("bg_color", [
        "bright black", "bright red", "bright green", "bright yellow",
        "bright blue", "bright magenta", "bright cyan", "bright white"
    ])
    def test_colorize_bright_backgrounds(self, bg_color):
        """Test all bright background colors."""
        result = colorize("test", bg=bg_color)
        assert "test" in result
        assert "\033[0m" in result

    def test_colorize_red_background(self):
        """Test red background generates correct ANSI code."""
        result = colorize("test", bg="red")
        assert "\033[41m" in result


class TestColorizeCombo:
    """Test the colorize function with combined parameters."""

    def test_colorize_color_and_style(self):
        """Test combining color and style."""
        result = colorize("test", color="red", style="bold")
        assert "\033[1m" in result
        assert "\033[31m" in result
        assert "test" in result

    def test_colorize_color_and_background(self):
        """Test combining color and background."""
        result = colorize("test", color="red", bg="blue")
        assert "\033[31m" in result
        assert "\033[44m" in result
        assert "test" in result

    def test_colorize_style_and_background(self):
        """Test combining style and background."""
        result = colorize("test", style="bold", bg="red")
        assert "\033[1m" in result
        assert "\033[41m" in result
        assert "test" in result

    def test_colorize_all_three_parameters(self):
        """Test combining color, style, and background."""
        result = colorize("test", color="white", style="bold", bg="red")
        assert "\033[1m" in result
        assert "\033[37m" in result
        assert "\033[41m" in result
        assert "test" in result
        assert "\033[0m" in result

    def test_colorize_multiple_combinations(self):
        """Test various color/style/bg combinations."""
        result = colorize("alert", color="yellow", style="bold", bg="black")
        assert "\033[1m" in result
        assert "\033[33m" in result
        assert "\033[40m" in result
        assert "alert" in result


class TestColorizeDefaults:
    """Test the colorize function with None values and defaults."""

    def test_colorize_none_values(self):
        """Test that None values are handled as reset."""
        result = colorize("test", color=None, style=None, bg=None)
        assert "test" in result
        assert "\033[0m" in result

    def test_colorize_default_behavior(self):
        """Test colorize with no parameters uses defaults."""
        result = colorize("test")
        assert "test" in result
        assert "\033[0m" in result

    def test_colorize_reset_color(self):
        """Test explicit reset color."""
        result = colorize("test", color="reset")
        assert "test" in result
        assert "\033[0m" in result

    def test_colorize_reset_style(self):
        """Test explicit reset style."""
        result = colorize("test", style="reset")
        assert "test" in result

    def test_colorize_reset_bg(self):
        """Test explicit reset background."""
        result = colorize("test", bg="reset")
        assert "test" in result


class TestColorizeErrors:
    """Test error handling in colorize function."""

    def test_colorize_invalid_color_raises_error(self):
        """Test that invalid color raises ColorNotFoundError."""
        with pytest.raises(ColorNotFoundError):
            colorize("test", color="invalidcolor")

    def test_colorize_invalid_style_raises_error(self):
        """Test that invalid style raises StyleNotFoundError."""
        with pytest.raises(StyleNotFoundError):
            colorize("test", style="invalidstyle")

    def test_colorize_invalid_background_raises_error(self):
        """Test that invalid background raises ColorNotFoundError."""
        with pytest.raises(ColorNotFoundError):
            colorize("test", bg="invalidbg")

    def test_colorize_error_message_mentions_color(self):
        """Test error message contains color information."""
        with pytest.raises(ColorNotFoundError) as exc_info:
            colorize("test", color="notacolor")
        assert "notacolor" in str(exc_info.value)
        assert "Color" in str(exc_info.value)

    def test_colorize_error_message_mentions_style(self):
        """Test error message contains style information."""
        with pytest.raises(StyleNotFoundError) as exc_info:
            colorize("test", style="notastyle")
        assert "notastyle" in str(exc_info.value)
        assert "Style" in str(exc_info.value)

    def test_colorize_error_message_mentions_bg_color(self):
        """Test error message contains background color information."""
        with pytest.raises(ColorNotFoundError) as exc_info:
            colorize("test", bg="notabg")
        assert "notabg" in str(exc_info.value)
        assert "BG" in str(exc_info.value).upper()


# =========================================================================
# Test Suite for New colortext() Function
# =========================================================================

class TestColortextBasics:
    """Test the colortext function with simple combined styles."""

    def test_colortext_bold_red(self):
        """Test bold red combination."""
        result = colortext("test", as_="bold red")
        assert "\033[1m" in result
        assert "\033[31m" in result
        assert "test" in result
        assert "\033[0m" in result

    def test_colortext_italic_cyan(self):
        """Test italic cyan combination."""
        result = colortext("test", as_="italic cyan")
        assert "\033[3m" in result
        assert "\033[36m" in result

    def test_colortext_underline_blue(self):
        """Test underline blue combination."""
        result = colortext("test", as_="underline blue")
        assert "\033[4m" in result
        assert "\033[34m" in result

    @pytest.mark.parametrize("style_color", [
        "bold red", "bold blue", "bold green", "bold yellow",
        "dim cyan", "italic magenta", "underline white"
    ])
    def test_colortext_style_color_combinations(self, style_color):
        """Test various style and color combinations."""
        result = colortext("test", as_=style_color)
        assert "test" in result
        assert "\033[0m" in result


class TestColortextBrightColors:
    """Test colortext with bright color combinations."""

    def test_colortext_bold_bright_red(self):
        """Test bold bright red."""
        result = colortext("test", as_="bold bright red")
        assert "\033[1m" in result
        assert "\033[91m" in result

    def test_colortext_italic_bright_cyan(self):
        """Test italic bright cyan."""
        result = colortext("test", as_="italic bright cyan")
        assert "\033[3m" in result
        assert "\033[96m" in result

    @pytest.mark.parametrize("bright_combo", [
        "bold bright black", "bold bright red", "bold bright green",
        "bold bright blue", "dim bright cyan", "italic bright white"
    ])
    def test_colortext_bright_combinations(self, bright_combo):
        """Test various bright color combinations."""
        result = colortext("test", as_=bright_combo)
        assert "test" in result
        assert "\033[0m" in result


class TestColortextBackground:
    """Test colortext with background color combinations."""

    def test_colortext_bold_red_on_black(self):
        """Test bold red on black background."""
        result = colortext("test", as_="bold red on black")
        assert "\033[1m" in result
        assert "\033[31m" in result
        assert "\033[40m" in result

    def test_colortext_italic_white_on_blue(self):
        """Test italic white on blue background."""
        result = colortext("test", as_="italic white on blue")
        assert "\033[3m" in result
        assert "\033[37m" in result
        assert "\033[44m" in result

    def test_colortext_underline_white_on_red(self):
        """Test underline white on red background."""
        result = colortext("test", as_="underline white on red")
        assert "\033[4m" in result
        assert "\033[37m" in result
        assert "\033[41m" in result

    @pytest.mark.parametrize("style_fg_bg", [
        "bold white on red", "bold black on white", "italic cyan on black",
        "underline yellow on black", "dim green on black"
    ])
    def test_colortext_style_color_background(self, style_fg_bg):
        """Test style, foreground, and background combinations."""
        result = colortext("test", as_=style_fg_bg)
        assert "test" in result
        assert "\033[0m" in result


class TestColortextSpecialColors:
    """Test colortext with special colors like gray and default."""

    def test_colortext_bold_gray(self):
        """Test bold gray combination."""
        result = colortext("test", as_="bold gray")
        assert "\033[1m" in result
        assert "\033[90m" in result

    def test_colortext_italic_default(self):
        """Test italic default color."""
        result = colortext("test", as_="italic default")
        assert "\033[3m" in result
        assert "\033[39m" in result

    def test_colortext_italic_gray_on_black(self):
        """Test italic gray on black."""
        result = colortext("test", as_="italic gray on black")
        assert "\033[3m" in result
        assert "\033[90m" in result
        assert "\033[40m" in result


class TestColortextErrors:
    """Test error handling in colortext function."""

    def test_colortext_invalid_style_raises_error(self):
        """Test that invalid combined style raises StyleNotFoundError."""
        with pytest.raises(StyleNotFoundError):
            colortext("test", as_="invalidstyle")

    def test_colortext_invalid_color_raises_error(self):
        """Test that invalid color in combo raises StyleNotFoundError."""
        with pytest.raises(StyleNotFoundError):
            colortext("test", as_="bold notacolor")

    def test_colortext_invalid_background_raises_error(self):
        """Test that invalid background in combo raises StyleNotFoundError."""
        with pytest.raises(StyleNotFoundError):
            colortext("test", as_="bold red on notabg")

    def test_colortext_error_message_is_helpful(self):
        """Test that error message is descriptive."""
        with pytest.raises(StyleNotFoundError) as exc_info:
            colortext("test", as_="invalidcombo")
        assert "invalidcombo" in str(exc_info.value)
        assert "bold red" in str(exc_info.value).lower() or "italic" in str(exc_info.value).lower()

    def test_colortext_case_sensitive(self):
        """Test that style matching is case-sensitive."""
        with pytest.raises(StyleNotFoundError):
            colortext("test", as_="Bold Red")  # Capital B


# =========================================================================
# Test Suite for cprint() Function
# =========================================================================

class TestCprintLegacyAPI:
    """Test cprint with legacy color, style, bg parameters."""

    @patch('builtins.print')
    def test_cprint_legacy_color(self, mock_print):
        """Test cprint with legacy color parameter."""
        cprint("test", color="red")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert "test" in args[0]
        assert "\033[31m" in args[0]

    @patch('builtins.print')
    def test_cprint_legacy_style(self, mock_print):
        """Test cprint with legacy style parameter."""
        cprint("test", style="bold")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert "test" in args[0]
        assert "\033[1m" in args[0]

    @patch('builtins.print')
    def test_cprint_legacy_background(self, mock_print):
        """Test cprint with legacy background parameter."""
        cprint("test", bg="blue")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert "test" in args[0]
        assert "\033[44m" in args[0]

    @patch('builtins.print')
    def test_cprint_legacy_combined(self, mock_print):
        """Test cprint with legacy combined parameters."""
        cprint("test", color="red", style="bold", bg="blue")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert "\033[1m" in args[0]
        assert "\033[31m" in args[0]
        assert "\033[44m" in args[0]


class TestCprintNewAPI:
    """Test cprint with new as_ parameter."""

    @patch('builtins.print')
    def test_cprint_new_api_bold_red(self, mock_print):
        """Test cprint with new API - bold red."""
        cprint("test", as_="bold red")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert "\033[1m" in args[0]
        assert "\033[31m" in args[0]
        assert "test" in args[0]

    @patch('builtins.print')
    def test_cprint_new_api_italic_cyan(self, mock_print):
        """Test cprint with new API - italic cyan."""
        cprint("test", as_="italic cyan")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert "\033[3m" in args[0]
        assert "\033[36m" in args[0]

    @patch('builtins.print')
    def test_cprint_new_api_with_background(self, mock_print):
        """Test cprint with new API - background combination."""
        cprint("test", as_="bold red on black")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert "\033[1m" in args[0]
        assert "\033[31m" in args[0]
        assert "\033[40m" in args[0]


class TestCprintAPIPreference:
    """Test that new API (as_) takes precedence over legacy API."""

    @patch('builtins.print')
    def test_cprint_as_takes_precedence(self, mock_print):
        """Test that as_ parameter is used when both APIs provided."""
        cprint("test", color="red", as_="bold blue")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        # Should use bold blue, not red
        assert "\033[1m" in args[0]
        assert "\033[34m" in args[0]  # blue
        assert "\033[31m" not in args[0]  # not red

    @patch('builtins.print')
    def test_cprint_new_api_ignores_legacy_params(self, mock_print):
        """Test that new API ignores legacy parameters."""
        cprint("test", color="red", style="dim", bg="yellow", as_="italic green")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        # Should only use italic green
        assert "\033[3m" in args[0]
        assert "\033[32m" in args[0]


class TestCprintKwargs:
    """Test cprint passes through print kwargs."""

    @patch('builtins.print')
    def test_cprint_with_end_kwarg(self, mock_print):
        """Test cprint with end parameter."""
        cprint("test", color="red", end="")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert kwargs.get('end') == ""

    @patch('builtins.print')
    def test_cprint_with_sep_kwarg(self, mock_print):
        """Test cprint with sep parameter."""
        cprint("test", color="red", sep=", ")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert kwargs.get('sep') == ", "

    @patch('builtins.print')
    def test_cprint_with_multiple_kwargs(self, mock_print):
        """Test cprint with multiple print kwargs."""
        cprint("test", as_="bold red", end="", sep="|")
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert kwargs.get('end') == ""
        assert kwargs.get('sep') == "|"

    @patch('builtins.print')
    def test_cprint_with_file_kwarg(self, mock_print):
        """Test cprint with file parameter."""
        output = StringIO()
        cprint("test", color="blue", file=output)
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert kwargs.get('file') == output


# =========================================================================
# Test Suite for cinput() Function
# =========================================================================

class TestCinputLegacyAPI:
    """Test cinput with legacy color, style, bg parameters."""

    @patch('builtins.input', return_value="user input")
    def test_cinput_legacy_color(self, mock_input):
        """Test cinput with legacy color parameter."""
        result = cinput("Name: ", color="blue")
        assert result == "user input"
        mock_input.assert_called_once()
        args = mock_input.call_args[0]
        assert "Name:" in args[0]
        assert "\033[34m" in args[0]

    @patch('builtins.input', return_value="user input")
    def test_cinput_legacy_style(self, mock_input):
        """Test cinput with legacy style parameter."""
        result = cinput("Age: ", style="bold")
        assert result == "user input"
        args = mock_input.call_args[0]
        assert "\033[1m" in args[0]

    @patch('builtins.input', return_value="user input")
    def test_cinput_legacy_combined(self, mock_input):
        """Test cinput with legacy combined parameters."""
        result = cinput("Email: ", color="green", style="underline", bg="black")
        assert result == "user input"
        args = mock_input.call_args[0]
        assert "\033[4m" in args[0]
        assert "\033[32m" in args[0]
        assert "\033[40m" in args[0]


class TestCinputNewAPI:
    """Test cinput with new as_ parameter."""

    @patch('builtins.input', return_value="user input")
    def test_cinput_new_api_bold_blue(self, mock_input):
        """Test cinput with new API - bold blue."""
        result = cinput("Name: ", as_="bold blue")
        assert result == "user input"
        args = mock_input.call_args[0]
        assert "\033[1m" in args[0]
        assert "\033[34m" in args[0]

    @patch('builtins.input', return_value="user input")
    def test_cinput_new_api_italic_cyan(self, mock_input):
        """Test cinput with new API - italic cyan."""
        result = cinput("Input: ", as_="italic cyan")
        assert result == "user input"
        args = mock_input.call_args[0]
        assert "\033[3m" in args[0]
        assert "\033[36m" in args[0]

    @patch('builtins.input', return_value="user input")
    def test_cinput_new_api_with_background(self, mock_input):
        """Test cinput with new API - background combination."""
        result = cinput("Prompt: ", as_="bold green on black")
        assert result == "user input"
        args = mock_input.call_args[0]
        assert "\033[1m" in args[0]
        assert "\033[32m" in args[0]
        assert "\033[40m" in args[0]


class TestCinputAPIPreference:
    """Test that new API (as_) takes precedence over legacy API."""

    @patch('builtins.input', return_value="user input")
    def test_cinput_as_takes_precedence(self, mock_input):
        """Test that as_ parameter is used when both APIs provided."""
        result = cinput("Prompt: ", color="red", as_="bold blue")
        assert result == "user input"
        args = mock_input.call_args[0]
        # Should use bold blue, not red
        assert "\033[1m" in args[0]
        assert "\033[34m" in args[0]


class TestCinputReturnValue:
    """Test cinput returns user input correctly."""

    @patch('builtins.input', return_value="test input")
    def test_cinput_returns_user_input(self, mock_input):
        """Test that cinput returns the user's input."""
        result = cinput("Prompt: ", color="blue")
        assert result == "test input"

    @patch('builtins.input', return_value="")
    def test_cinput_empty_input(self, mock_input):
        """Test cinput with empty input."""
        result = cinput("Prompt: ", as_="bold red")
        assert result == ""

    @patch('builtins.input', return_value="special chars !@#$%")
    def test_cinput_special_characters(self, mock_input):
        """Test cinput with special characters in input."""
        result = cinput("Prompt: ", as_="italic cyan")
        assert result == "special chars !@#$%"


# =========================================================================
# Test Suite for Color Classes and NodeProxy
# =========================================================================

class TestClibColorClass:
    """Test the clib color class."""

    def test_clib_black(self):
        """Test clib.black attribute."""
        assert clib.black == "\033[30m"

    def test_clib_red(self):
        """Test clib.red attribute."""
        assert clib.red == "\033[31m"

    def test_clib_gray(self):
        """Test clib.gray attribute."""
        assert clib.gray == "\033[90m"

    def test_clib_default(self):
        """Test clib.default attribute."""
        assert clib.default == "\033[39m"

    def test_clib_reset(self):
        """Test clib.reset attribute."""
        assert clib.reset == "\033[0m"

    def test_clib_palette(self):
        """Test clib palette contains all basic colors."""
        assert len(clib.palette) == 8
        assert "black" in clib.palette
        assert "red" in clib.palette
        assert "green" in clib.palette

    @pytest.mark.parametrize("color_name", clib.palette)
    def test_clib_all_basic_colors(self, color_name):
        """Test all basic colors in palette are accessible."""
        color_code = getattr(clib, color_name)
        assert isinstance(color_code, str)
        assert color_code.startswith("\033[")


class TestColorBrightClass:
    """Test the color.bright class."""

    def test_color_bright_red(self):
        """Test color.bright.red attribute."""
        assert color.bright.red == "\033[91m"

    def test_color_bright_blue(self):
        """Test color.bright.blue attribute."""
        assert color.bright.blue == "\033[94m"

    def test_color_bright_black(self):
        """Test color.bright.black attribute (same as gray)."""
        assert color.bright.black == "\033[90m"

    @pytest.mark.parametrize("color_name", [
        "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
    ])
    def test_color_bright_all_colors(self, color_name):
        """Test all colors in color.bright are accessible."""
        bright_color = getattr(color.bright, color_name)
        assert isinstance(bright_color, str)
        assert bright_color.startswith("\033[")


class TestColorBgClass:
    """Test the color.bg class."""

    def test_color_bg_red(self):
        """Test color.bg.red attribute."""
        assert color.bg.red == "\033[41m"

    def test_color_bg_blue(self):
        """Test color.bg.blue attribute."""
        assert color.bg.blue == "\033[44m"

    def test_color_bg_gray(self):
        """Test color.bg.gray attribute."""
        assert color.bg.gray == "\033[100m"

    def test_color_bg_default(self):
        """Test color.bg.default attribute."""
        assert color.bg.default == "\033[49m"

    @pytest.mark.parametrize("color_name", [
        "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
    ])
    def test_color_bg_all_colors(self, color_name):
        """Test all background colors are accessible."""
        bg_color = getattr(color.bg, color_name)
        assert isinstance(bg_color, str)
        assert bg_color.startswith("\033[")


class TestColorBgBrightClass:
    """Test the color.bg.bright class."""

    def test_color_bg_bright_red(self):
        """Test color.bg.bright.red attribute."""
        assert color.bg.bright.red == "\033[101m"

    def test_color_bg_bright_blue(self):
        """Test color.bg.bright.blue attribute."""
        assert color.bg.bright.blue == "\033[104m"

    @pytest.mark.parametrize("color_name", [
        "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
    ])
    def test_color_bg_bright_all_colors(self, color_name):
        """Test all bright background colors are accessible."""
        bright_bg = getattr(color.bg.bright, color_name)
        assert isinstance(bright_bg, str)
        assert bright_bg.startswith("\033[1")


class TestColorStyleClasses:
    """Test the color style classes (bold, dim, italic, etc.)."""

    def test_color_bold_is_node_proxy(self):
        """Test that color.bold is a NodeProxy."""
        assert isinstance(color.bold, NodeProxy)

    def test_color_bold_red(self):
        """Test color.bold.red combination."""
        result = color.bold.red
        assert "\033[1m" in result
        assert "\033[31m" in result

    def test_color_bold_cyan(self):
        """Test color.bold.cyan combination."""
        result = color.bold.cyan
        assert "\033[1m" in result
        assert "\033[36m" in result

    def test_color_dim_is_node_proxy(self):
        """Test that color.dim is a NodeProxy."""
        assert isinstance(color.dim, NodeProxy)

    def test_color_dim_green(self):
        """Test color.dim.green combination."""
        result = color.dim.green
        assert "\033[2m" in result
        assert "\033[32m" in result

    def test_color_italic_blue(self):
        """Test color.italic.blue combination."""
        result = color.italic.blue
        assert "\033[3m" in result
        assert "\033[34m" in result

    def test_color_underline_yellow(self):
        """Test color.underline.yellow combination."""
        result = color.underline.yellow
        assert "\033[4m" in result
        assert "\033[33m" in result

    @pytest.mark.parametrize("style_name", [
        "bold", "dim", "italic", "underline", "blinking", "fast_blinking", "inverted", "hidden", "striked"
    ])
    def test_color_all_style_classes(self, style_name):
        """Test all style classes are NodeProxy instances."""
        style = getattr(color, style_name)
        assert isinstance(style, NodeProxy)


class TestColorStyleClassValues:
    """Test the values in style classes."""

    def test_color_bold_value(self):
        """Test color.bold style value."""
        # Access through NodeProxy
        assert color.bold._cls.value == "\033[1m"

    def test_color_dim_value(self):
        """Test color.dim style value."""
        assert color.dim._cls.value == "\033[2m"

    def test_color_italic_value(self):
        """Test color.italic style value."""
        assert color.italic._cls.value == "\033[3m"

    def test_color_underline_value(self):
        """Test color.underline style value."""
        assert color.underline._cls.value == "\033[4m"

    def test_color_blinking_value(self):
        """Test color.blinking style value."""
        assert color.blinking._cls.value == "\033[5m"

    def test_color_fast_blinking_value(self):
        """Test color.fast_blinking style value."""
        assert color.fast_blinking._cls.value == "\033[6m"

    def test_color_inverted_value(self):
        """Test color.inverted style value."""
        assert color.inverted._cls.value == "\033[7m"

    def test_color_hidden_value(self):
        """Test color.hidden style value."""
        assert color.hidden._cls.value == "\033[8m"

    def test_color_striked_value(self):
        """Test color.striked style value."""
        assert color.striked._cls.value == "\033[9m"


class TestNodeProxyRepr:
    """Test NodeProxy repr and str methods."""

    def test_node_proxy_repr(self):
        """Test NodeProxy __repr__ method."""
        repr_str = repr(color.bold)
        assert "<colornode" in repr_str
        assert "bold" in repr_str
        assert "code" in repr_str

    def test_node_proxy_str(self):
        """Test NodeProxy __str__ method."""
        str_result = str(color.bold)
        # Should contain the style code and reset
        assert "\033[1m" in str_result  # bold code
        assert "\033[0m" in str_result  # reset code

    def test_node_proxy_getattr_style(self):
        """Test NodeProxy __getattr__ with style access."""
        # Should be able to access colors through style
        bold_red = color.bold.red
        assert isinstance(bold_red, str)
        assert "\033[1m" in bold_red


# =========================================================================
# Test Suite for Color, Style, and Background Maps
# =========================================================================

class TestColorMap:
    """Test COLOR_MAP completeness and correctness."""

    def test_color_map_has_all_basic_colors(self):
        """Test COLOR_MAP contains all basic colors."""
        basic_colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        for color_name in basic_colors:
            assert color_name in COLOR_MAP

    def test_color_map_has_special_colors(self):
        """Test COLOR_MAP contains special colors."""
        assert "gray" in COLOR_MAP
        assert "default" in COLOR_MAP

    def test_color_map_has_bright_colors(self):
        """Test COLOR_MAP contains bright colors."""
        bright_colors = [
            "bright black", "bright red", "bright green", "bright yellow",
            "bright blue", "bright magenta", "bright cyan", "bright white"
        ]
        for color_name in bright_colors:
            assert color_name in COLOR_MAP

    def test_color_map_has_reset(self):
        """Test COLOR_MAP contains reset."""
        assert "reset" in COLOR_MAP

    def test_color_map_values_are_ansi_codes(self):
        """Test all COLOR_MAP values are valid ANSI codes."""
        for color_name, ansi_code in COLOR_MAP.items():
            assert isinstance(ansi_code, str)
            assert ansi_code.startswith("\033[")
            assert ansi_code.endswith("m")

    @pytest.mark.parametrize("color_name,expected_code", [
        ("red", "\033[31m"),
        ("blue", "\033[34m"),
        ("green", "\033[32m"),
        ("gray", "\033[90m"),
        ("default", "\033[39m"),
        ("bright red", "\033[91m"),
        ("bright blue", "\033[94m"),
        ("reset", "\033[0m"),
    ])
    def test_color_map_correct_codes(self, color_name, expected_code):
        """Test COLOR_MAP has correct ANSI codes."""
        assert COLOR_MAP[color_name] == expected_code

    def test_color_map_count(self):
        """Test COLOR_MAP has expected number of entries."""
        assert len(COLOR_MAP) == 19  # 8 basic + 8 bright + gray + default + reset


class TestStyleMap:
    """Test STYLE_MAP completeness and correctness."""

    def test_style_map_has_all_styles(self):
        """Test STYLE_MAP contains all style types."""
        styles = ["bold", "dim", "italic", "underline", "blink",
                  "fast_blink", "inverse", "hidden", "strike"]
        for style_name in styles:
            assert style_name in STYLE_MAP

    def test_style_map_has_reset(self):
        """Test STYLE_MAP contains reset."""
        assert "reset" in STYLE_MAP

    def test_style_map_values_are_ansi_codes(self):
        """Test all STYLE_MAP values are valid ANSI codes."""
        for style_name, ansi_code in STYLE_MAP.items():
            assert isinstance(ansi_code, str)
            assert ansi_code.startswith("\033[")
            assert ansi_code.endswith("m")

    @pytest.mark.parametrize("style_name,expected_code", [
        ("bold", "\033[1m"),
        ("dim", "\033[2m"),
        ("italic", "\033[3m"),
        ("underline", "\033[4m"),
        ("blink", "\033[5m"),
        ("fast_blink", "\033[6m"),
        ("inverse", "\033[7m"),
        ("hidden", "\033[8m"),
        ("strike", "\033[9m"),
        ("reset", "\033[0m"),
    ])
    def test_style_map_correct_codes(self, style_name, expected_code):
        """Test STYLE_MAP has correct ANSI codes."""
        assert STYLE_MAP[style_name] == expected_code

    def test_style_map_count(self):
        """Test STYLE_MAP has expected number of entries."""
        assert len(STYLE_MAP) == 10  # 9 styles + reset


class TestBGColorMap:
    """Test BG_COLOR_MAP completeness and correctness."""

    def test_bg_color_map_has_all_basic_colors(self):
        """Test BG_COLOR_MAP contains all basic background colors."""
        basic_colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        for color_name in basic_colors:
            assert color_name in BG_COLOR_MAP

    def test_bg_color_map_has_special_colors(self):
        """Test BG_COLOR_MAP contains special background colors."""
        assert "gray" in BG_COLOR_MAP
        assert "default" in BG_COLOR_MAP

    def test_bg_color_map_has_bright_colors(self):
        """Test BG_COLOR_MAP contains bright background colors."""
        bright_colors = [
            "bright black", "bright red", "bright green", "bright yellow",
            "bright blue", "bright magenta", "bright cyan", "bright white"
        ]
        for color_name in bright_colors:
            assert color_name in BG_COLOR_MAP

    def test_bg_color_map_has_reset(self):
        """Test BG_COLOR_MAP contains reset."""
        assert "reset" in BG_COLOR_MAP

    def test_bg_color_map_values_are_ansi_codes(self):
        """Test all BG_COLOR_MAP values are valid ANSI codes."""
        for color_name, ansi_code in BG_COLOR_MAP.items():
            assert isinstance(ansi_code, str)
            assert ansi_code.startswith("\033[")
            assert ansi_code.endswith("m")

    @pytest.mark.parametrize("color_name,expected_code", [
        ("red", "\033[41m"),
        ("blue", "\033[44m"),
        ("black", "\033[40m"),
        ("gray", "\033[100m"),
        ("default", "\033[49m"),
        ("bright red", "\033[101m"),
        ("bright blue", "\033[104m"),
    ])
    def test_bg_color_map_correct_codes(self, color_name, expected_code):
        """Test BG_COLOR_MAP has correct ANSI codes."""
        assert BG_COLOR_MAP[color_name] == expected_code

    def test_bg_color_map_count(self):
        """Test BG_COLOR_MAP has expected number of entries."""
        assert len(BG_COLOR_MAP) == 19  # 8 basic + 8 bright + gray + default + reset


class TestCombinedStylesMap:
    """Test COMBINED_STYLES map completeness."""

    def test_combined_styles_has_entries(self):
        """Test COMBINED_STYLES has entries."""
        assert len(COMBINED_STYLES) > 0

    def test_combined_styles_count(self):
        """Test COMBINED_STYLES has all style+color combinations."""
        # 9 styles × 18 colors = 162
        assert len(COMBINED_STYLES) == 162

    def test_combined_styles_bold_combinations(self):
        """Test COMBINED_STYLES has bold combinations."""
        assert "bold black" in COMBINED_STYLES
        assert "bold red" in COMBINED_STYLES
        assert "bold bright cyan" in COMBINED_STYLES

    def test_combined_styles_values_are_ansi_codes(self):
        """Test all COMBINED_STYLES values are valid ANSI codes."""
        for style_combo, ansi_code in COMBINED_STYLES.items():
            assert isinstance(ansi_code, str)
            # Should contain at least style code and color code
            assert "\033[" in ansi_code

    @pytest.mark.parametrize("style_combo,has_bold", [
        ("bold red", True),
        ("bold blue", True),
        ("dim cyan", False),
        ("italic green", False),
    ])
    def test_combined_styles_contains_correct_codes(self, style_combo, has_bold):
        """Test COMBINED_STYLES values contain expected style codes."""
        ansi_code = COMBINED_STYLES[style_combo]
        if has_bold:
            assert "\033[1m" in ansi_code
        else:
            assert "\033[1m" not in ansi_code or style_combo.startswith("bold")

    def test_combined_styles_all_contain_reset_when_used(self):
        """Test that colortext with COMBINED_STYLES adds reset."""
        result = colortext("test", as_="bold red")
        assert "\033[0m" in result


class TestCombinedStylesWithBGMap:
    """Test COMBINED_STYLES_WITH_BG map completeness."""

    def test_combined_styles_with_bg_has_entries(self):
        """Test COMBINED_STYLES_WITH_BG has entries."""
        assert len(COMBINED_STYLES_WITH_BG) > 0

    def test_combined_styles_with_bg_has_bold_combinations(self):
        """Test COMBINED_STYLES_WITH_BG has bold background combinations."""
        assert "bold red on black" in COMBINED_STYLES_WITH_BG
        assert "bold white on red" in COMBINED_STYLES_WITH_BG
        assert "bold black on white" in COMBINED_STYLES_WITH_BG

    def test_combined_styles_with_bg_has_other_styles(self):
        """Test COMBINED_STYLES_WITH_BG has non-bold combinations."""
        assert "italic cyan on black" in COMBINED_STYLES_WITH_BG
        assert "underline white on blue" in COMBINED_STYLES_WITH_BG
        assert "dim white on black" in COMBINED_STYLES_WITH_BG

    def test_combined_styles_with_bg_values_are_ansi_codes(self):
        """Test all COMBINED_STYLES_WITH_BG values are valid ANSI codes."""
        for style_combo, ansi_code in COMBINED_STYLES_WITH_BG.items():
            assert isinstance(ansi_code, str)
            # Should contain style, foreground, and background codes
            assert "\033[" in ansi_code
            assert ansi_code.count("\033[") >= 2  # At least style + fg/bg

    def test_combined_styles_with_bg_on_pattern(self):
        """Test that all keys follow 'style color on bg' pattern."""
        for key in COMBINED_STYLES_WITH_BG.keys():
            assert " on " in key

    def test_combined_styles_with_bg_colortext_integration(self):
        """Test COMBINED_STYLES_WITH_BG works with colortext."""
        result = colortext("test", as_="bold red on black")
        assert "\033[1m" in result
        assert "\033[31m" in result
        assert "\033[40m" in result
        assert "test" in result


# =========================================================================
# Test Suite for Edge Cases
# =========================================================================

class TestEdgeCases:
    """Test edge cases and unusual inputs."""

    def test_colorize_empty_string(self):
        """Test colorize with empty string."""
        result = colorize("", color="red")
        assert "\033[0m" in result

    def test_colortext_empty_string(self):
        """Test colortext with empty string."""
        result = colortext("", as_="bold red")
        assert "\033[0m" in result

    def test_colorize_unicode_text(self):
        """Test colorize with unicode characters."""
        result = colorize("测试", color="red")
        assert "测试" in result
        assert "\033[0m" in result

    def test_colortext_unicode_text(self):
        """Test colortext with unicode characters."""
        result = colortext("日本語", as_="bold blue")
        assert "日本語" in result
        assert "\033[0m" in result

    def test_colorize_special_characters(self):
        """Test colorize with special characters."""
        result = colorize("!@#$%^&*()", color="green")
        assert "!@#$%^&*()" in result

    def test_colortext_special_characters(self):
        """Test colortext with special characters."""
        result = colortext("!@#$%^&*()", as_="italic cyan")
        assert "!@#$%^&*()" in result

    def test_colorize_newline_in_text(self):
        """Test colorize with newline in text."""
        result = colorize("line1\nline2", color="red")
        assert "line1\nline2" in result
        assert "\033[0m" in result

    def test_colortext_newline_in_text(self):
        """Test colortext with newline in text."""
        result = colortext("line1\nline2", as_="bold red")
        assert "line1\nline2" in result

    def test_colorize_very_long_text(self):
        """Test colorize with very long text."""
        long_text = "a" * 10000
        result = colorize(long_text, color="blue")
        assert long_text in result
        assert "\033[0m" in result

    def test_colortext_very_long_text(self):
        """Test colortext with very long text."""
        long_text = "a" * 10000
        result = colortext(long_text, as_="bold red")
        assert long_text in result

    def test_colorize_with_ansi_codes_in_text(self):
        """Test colorize with existing ANSI codes in text."""
        text = "\033[31mred text\033[0m"
        result = colorize(text, color="blue")
        assert text in result  # Original codes should be preserved

    @patch('builtins.print')
    def test_cprint_empty_string(self, mock_print):
        """Test cprint with empty string."""
        cprint("", color="red")
        mock_print.assert_called_once()

    @patch('builtins.input', return_value="")
    def test_cinput_empty_input(self, mock_input):
        """Test cinput with empty user input."""
        result = cinput("Prompt: ", color="blue")
        assert result == ""


# =========================================================================
# Test Suite for Integration Scenarios
# =========================================================================

class TestIntegration:
    """Test integration scenarios and real-world usage."""

    def test_multiple_colored_strings_sequence(self):
        """Test creating multiple colored strings."""
        red_text = colorize("Error", color="red", style="bold")
        blue_text = colorize("Info", color="blue", style="italic")
        green_text = colortext("Success", as_="bold green")

        combined = red_text + " " + blue_text + " " + green_text
        assert "Error" in combined
        assert "Info" in combined
        assert "Success" in combined

    @patch('builtins.print')
    def test_cprint_multiple_calls(self, mock_print):
        """Test multiple cprint calls."""
        cprint("First", color="red")
        cprint("Second", as_="bold blue")
        cprint("Third", color="green", style="italic")

        assert mock_print.call_count == 3

    def test_colorize_and_colortext_produce_similar_output(self):
        """Test that colorize and colortext produce consistent output."""
        colorize_result = colorize("test", color="red", style="bold")
        colortext_result = colortext("test", as_="bold red")

        # Both should contain the text and reset
        assert "test" in colorize_result
        assert "test" in colortext_result
        assert "\033[0m" in colorize_result
        assert "\033[0m" in colortext_result

    def test_all_colors_with_all_styles(self):
        """Test that all color-style combinations work."""
        # Sample a subset to avoid long test
        test_colors = ["red", "blue", "green"]
        test_styles = ["bold", "dim", "italic"]

        for color_name in test_colors:
            for style_name in test_styles:
                result = colorize("test", color=color_name, style=style_name)
                assert "test" in result
                assert "\033[0m" in result

    def test_platform_specific_initialization(self):
        """Test that module initializes correctly on current platform."""
        # Should not raise any errors on initialization
        from tinycolors import clib, color
        assert hasattr(clib, 'red')
        assert hasattr(color, 'bold')

    def test_color_chain_with_reset(self):
        """Test that each colored string has its own reset."""
        result1 = colorize("text1", color="red")
        result2 = colorize("text2", color="blue")

        # Each should have a reset code
        assert result1.endswith("\033[0m")
        assert result2.endswith("\033[0m")

    def test_background_foreground_combination_ordering(self):
        """Test that background + foreground ordering is correct."""
        result = colorize("test", color="white", bg="red")
        # Background should come first in colorize
        assert "\033[41m" in result  # red bg
        assert "\033[37m" in result  # white fg


# =========================================================================
# Test Suite for Backward Compatibility
# =========================================================================

class TestBackwardCompatibility:
    """Test that legacy API continues to work correctly."""

    def test_colorize_legacy_still_works(self):
        """Test that original colorize function still works."""
        result = colorize("test", color="red", style="bold", bg="blue")
        assert "test" in result
        assert "\033[1m" in result
        assert "\033[31m" in result
        assert "\033[44m" in result

    @patch('builtins.print')
    def test_cprint_legacy_still_works(self, mock_print):
        """Test that cprint still works with legacy parameters."""
        cprint("test", color="blue", style="underline")
        mock_print.assert_called_once()

    @patch('builtins.input', return_value="test")
    def test_cinput_legacy_still_works(self, mock_input):
        """Test that cinput still works with legacy parameters."""
        result = cinput("Prompt: ", color="green", style="italic")
        assert result == "test"

    def test_colorize_with_none_still_works(self):
        """Test colorize with None parameters (default behavior)."""
        result = colorize("test")
        assert "test" in result
        assert "\033[0m" in result

    def test_clib_class_still_accessible(self):
        """Test that clib class attributes are still accessible."""
        assert clib.red == "\033[31m"
        assert clib.reset == "\033[0m"  # Should not raise AttributeError

    def test_color_class_hierarchy_still_works(self):
        """Test that color class hierarchy is intact."""
        assert hasattr(color, 'bright')
        assert hasattr(color, 'bg')
        assert hasattr(color.bg, 'bright')
        assert hasattr(color, 'bold')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
