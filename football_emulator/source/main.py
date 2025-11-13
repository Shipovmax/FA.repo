import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from football_emulator.templates.ended import print_ended

print_ended()