import sys
from resumate import driver, config

def main():
    args = sys.argv
    if '-d' in args:
        config.DEBUG = True
    driver.run()

main()
