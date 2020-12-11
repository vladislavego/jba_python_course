""" The program is number system converter

    To run program enter in consel folowing command:

    'program_name.py decimal_digit number_system' to convert decimal_digit from decimal system to number_system
    
    'program_name.py value source_base target_base' to convert value from source_base system to target_base system
    (value must correspond base_system)
    
    Note: the value to convert must be non-negative
"""


def i_to_base(nb:int, base:str):
    """ Function converts number from decimal system to any other """
    
    digits_in_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    try:
        base = int(base)
    except:
        return f'"{base}"'
    else:
        if base >= 37 or base < 1:
            return f'"{base}"'
        if base == 0:
            return f'"0"'
        if base == 1:
            return '|' * nb
        if nb < base:
            return str(nb)
        
        based = [];
        while (nb >= base):
            digit = nb % base
            nb //= base
            if digit >= 10:          
                based.append(digits_in_letters[digit - 10])
            else:
                based.append(str(digit))
                
        if nb >= 10:          
            based.append(digits_in_letters[nb - 10])
        else:
            based.append(str(nb))
        return ''.join(based[::-1])

def i_to_base_all(nb:str, base_src:str, base_dst:str):
    """ Function converts nb from base_srs to base_dst """

    allow_dictionary = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    try:
        base_src = int(base_src)
        base_dst = int(base_dst)
    except:
        return f'{nb} from "{base_src}" to "{base_dst}"'
    else:
        if base_src >= 37 or base_dst >= 37 or base_src < 1 or base_dst < 1:
            return f'{nb} from "{base_src}" to "{base_dst}"'
        if base_src == 1:
            return i_to_base(len(nb), base_dst)
        
        if nb.isdigit():
            for digit in nb:
                if int(digit) >= base_src:
                    return 'Wrong base number system'
        else:
            for char in nb:
                if not char.isdigit() and char.upper() not in allow_dictionary:
                    if char == '-' and nb.index(char) == 0:
                        return 'The value to convert must be non-negative'
                    return 'Wrong value to convert. The value to convert must be non-negative number'
            for char in nb:       
                char = int(char) if char.isdigit() else allow_dictionary.index(char.upper()) + 10
                if char >= base_src:
                    return 'Wrong base number system'
                
        nb = list(nb)
        in_decimal = 0;
        power = 0
        while(nb):
            digit = nb.pop()
            digit = int(digit) if digit.isdigit() else allow_dictionary.index(digit.upper()) + 10
            in_decimal += digit * base_src **  power
            power += 1        
        return i_to_base(in_decimal, base_dst)
            

def main():

    usage = '\nTo convert from the decimal system:\n\n enter the program file name, decimal number, and target number system as command-line arguments, for example: main.py 15 5\n\nFor translation from an arbitrary number system:\n\n enter the program file name, number, source and target number system as command-line arguments, for example: main.py 15 5 2\n\nNote: the value to convert must be non-negative\n'
    
    if 2 < len(sys.argv) < 5:
        if len(sys.argv) < 4:
            try:
                nb = int(sys.argv[1])
                if nb < 0:
                    raise TypeError
            except TypeError:
                print('The value to convert must be non-negative')
            except IndexError:
                print(usage)
            except:
                print('Wrong value to convert. The value to convert must be non-negative decimal number')
            else:
                base = sys.argv[2]
                print(i_to_base(nb, base))
        else:
            value = sys.argv[1]
            source_base = sys.argv[2]
            target_base = sys.argv[3]

            print(i_to_base_all(value, source_base, target_base))
    else:
        print(usage)

        
            
            
if __name__ == '__main__':
    
    import sys
    
    main()
    
