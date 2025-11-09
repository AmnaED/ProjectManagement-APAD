# encryption_script.py

def encrypt(inputText, N, D):
    """
    Encrypts a string by reversing it and shifting ASCII characters.

    Parameters:
    inputText (str): The text to encrypt.
    N (int): Number of spaces to shift.
    D (int): Direction of shift, either -1 or +1.

    Returns:
    str: The encrypted text.
    """
    valid_ASCII = [chr(i) for i in range (34,127)]                 # list of printable ASCII minut space and '!'
    valid_range = len(valid_ASCII)                                 # range of valid ascii characters

    # input validation for all 3 parameters
    for char in inputText:
        if char not in valid_ASCII:
            raise ValueError("Input Text is invalid.")

    if N < 1:
        raise ValueError("N must be an integer greater than or equal to 1.")
    
    if D not in [1, -1]:
        raise ValueError("D must be 1 or -1.")
    
    # reverse input
    reversed_input = inputText[::-1]

    # shift
    encryptedText = ''

    for char in reversed_input:
        # get ascii value using ord, subtracts 34, adds step*direction, gets remainder and adds to starting point 34
        new_value = (((ord(char)-34) + (N*D))%valid_range) + 34
        new_char = chr(new_value)                                   # turns value into ascii character
        encryptedText += new_char                                   # concatenates shifted char to new string

    return encryptedText


def decrypt(encryptedInput, N, D):
    """
    Decrypts an encrypted string by reversing the shifting process.

    Parameters:
    encryptedInput (str): The text to decrypt.
    N (int): Number of spaces used for shifting during encryption.
    D (int): Direction of shift used during encryption, either -1 or +1.

    Returns:
    str: The decrypted original text.
    """
    valid_ASCII = [chr(i) for i in range (34,127)]                  # list of printable ASCII minut space and '!'
    valid_range = len(valid_ASCII)                                  # range of valid ascii characters
    
    # shift
    shifted_text = ''

    for char in encryptedInput:
        # same as encryption but subtracts step*direction to shift back to original
        new_value = (((ord(char)-34) - (N*D))%valid_range) + 34
        new_char = chr(new_value)
        shifted_text += new_char                                    # concatenates shifted char to new string
    
    # reverse text after shift
    decryptedText = shifted_text[::-1]

    return decryptedText