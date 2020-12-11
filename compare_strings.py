""" The program compares two strings and prints 'OK' if they are equal and 'KO' otherwise 
    
    the * character in the second line means any combination of any characters
"""

def is_equal_strings(first_string:str, second_string:str):

    first_length = len(first_string)
    second_length = len(second_string)

    length = min(first_length, second_length)
    
    for i in range(length):
        first_char = first_string[i]
        second_char = second_string[i]
        if first_char != second_char or second_char == '*':
            if second_char == '*':
                i += 1
                k = i
                while (i < second_length and second_char == '*' ):
                    second_char = second_string[i]
                    i += 1
                if i == second_length and second_char == '*':
                    return 'OK'
                if first_char == second_char:
                    return is_equal_strings(first_string[k - 1:], second_string[i - 1:])
                while (k < first_length and first_char != second_char):
                    first_char = first_string[k]
                    k += 1
                if k != first_length or first_char == second_char:
                    return is_equal_strings(first_string[k - 1:], second_string[i - 1:])
                return 'KO'
            second_char = second_string[0]
            if first_char != '*' and second_char == '*':
                k = i + 1
                while (k < first_length and first_char != second_char):
                    first_char = first_string[k]
                    k += 1
                if k != first_length:
                    return is_equal_strings(first_string[k - 1:], second_string)
                return 'KO'
            return 'KO'

    if second_length > length:
        for char in second_string[length:]:
            if char != '*':
                return 'KO'

    if first_length > length:
        return 'KO'

    return 'OK'


def main():

    if len(sys.argv) != 3:
        print()
        print("Enter two lines for comparison as command-line arguments, for example: main.py 'a' 'a*'\n\nthe * character in the second line means any combination of any characters")
        print()
    else:
        print(is_equal_strings(sys.argv[1], sys.argv[2]))
    



if __name__ == '__main__':
    import sys

    main()
    
    
