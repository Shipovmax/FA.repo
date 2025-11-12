BLUE_COLOR = '\033[93m'
RESET_COLOR = '\033[0m'

def print_header():
    line = f'{BLUE_COLOR}Добро пожаловать в Симулятор футбола{RESET_COLOR}'
    divider_line = '-' * 40
    
    print(divider_line)
    print(line)
    print(divider_line)