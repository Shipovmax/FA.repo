YELLOW_COLOR = '\033[93m'
RESET_COLOR = '\033[0m'

def print_ended():
    line = f'{YELLOW_COLOR}Спасибо за игру{RESET_COLOR}'
    divider_line = '-' * 40
    
    print(divider_line)
    print(line)
    print(divider_line)
