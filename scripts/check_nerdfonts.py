#!/usr/bin/env python3
"""Script to check for Nerd Font installation."""

from cli_utils.utils.nerd_font_check import check_nerd_fonts, get_nerd_fonts_list

# ANSI color codes
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
NC = '\033[0m'  # No Color

result = check_nerd_fonts()
fonts = get_nerd_fonts_list()

print()

if result == 1:
    print(f'{GREEN}✓ Nerd Fonts detected!{NC}')
    print()
    print(f'{YELLOW}Installed Nerd Fonts:{NC}')
    if fonts:
        for font in fonts[:5]:
            print(f'  - {font}')
        if len(fonts) > 5:
            print('  ...')
else:
    print(f'{YELLOW}✗ No Nerd Fonts found{NC}')
    print()
    print(f'{YELLOW}To install Nerd Fonts:{NC}')
    print('  1. Visit: https://www.nerdfonts.com/font-downloads')
    print('  2. Download and install your preferred font')
    print('  3. Restart your terminal')
    print('  4. Run: make check-nerdfonts')

print()
print('Icon support will fall back to emoji or text automatically.')
