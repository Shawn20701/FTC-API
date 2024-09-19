from imports import *
from classes import APIcalls, misc, main
colorama.init()

misc.clear()
if __name__ == "__main__":
  option = input("1. Read team numbers from file" "\n" "2. Input team number manually" "\n" "3. Retrieve Averages" "\n" "4. Exit" "\n""Enter an option: ")
  if option == "1":
    APIcalls.read_from_file()
  elif option == "2":
    APIcalls.input_data()
  elif option == "3":
    APIcalls.retrieve_averages()
  else:
    exit()