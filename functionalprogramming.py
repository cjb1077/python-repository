floor_number = int(input("Which number? "))

match floor_number:
    case 4:
        print("Unlucky in Japan")
    case 13:
        print("Unlucky in America")
    case _:
        print("No issues found.")
