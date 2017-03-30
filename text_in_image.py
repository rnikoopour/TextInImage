import argparse
import sys
import re

from PIL import Image

string_length_start_pixel = 0
string_text_start_pixel = 11
int_size = 32

def num_bits_in_string(string):
    return 8 * len(string)

def bit_string_to_32bits(bit_string):
    preceding_zeroes = '0' * (32 - len(bit_string))
    full_string = preceding_zeroes + bit_string
    return full_string

def change_last_bit(byte, bit_val):
    rep_as_bit = list(format(byte, 'b'))
    rep_as_bit[-1] = bit_val
    rep_as_bit = ''.join(rep_as_bit)
    return rep_as_bit

def bit_string_to_8bits(bit_string):
    preceding_zeroes = '0' * (8 - len(bit_string))
    full_string = preceding_zeroes + bit_string
    return full_string

def embed_binary_in_image(image_data, binary, index=0):
    binary = list(binary)
    new_image_data = []
    
    while binary:
        red, green, blue = image_data[index]
        index += 1

        new_red = change_last_bit(red, binary[0])
        red = int(new_red, 2)
        binary.pop(0)
        if not binary:
            new_image_data.append((red, green, blue))
            break
        new_green = change_last_bit(green, binary[0])
        green = int(new_green, 2)
        binary.pop(0)
        if not binary:
            new_image_data.append((red, green, blue))
            break
        new_blue = change_last_bit(blue, binary[0])
        blue = int(new_blue, 2)
        binary.pop(0)
        new_image_data.append((red, green, blue))
    return (new_image_data, index)

def extract_last_bit(byte):
    rep_as_bit = list(format(byte, 'b'))
    return rep_as_bit[-1]
        
def string_to_binary(text):
    binary_string = ''
    for letter in text:
        letter_as_int = ord(letter)
        letter_as_binary = format(letter_as_int, 'b')
        letter_as_binary = bit_string_to_8bits(letter_as_binary)
        binary_string += letter_as_binary
    return binary_string

def embed_in_image(image_data, text):
    string_length_in_binary = format(num_bits_in_string(text), 'b')
    string_length_in_binary = bit_string_to_32bits(string_length_in_binary)
    text_as_binary = string_to_binary(text)

    new_image_data = []
    (transformed_image_data,_) = embed_binary_in_image(image_data, string_length_in_binary, string_length_start_pixel)
    new_image_data += transformed_image_data
    (transformed_image_data, last_pixel_written) = embed_binary_in_image(image_data, text_as_binary, string_text_start_pixel)
    new_image_data += transformed_image_data
    new_image_data += image_data[last_pixel_written:]
    return new_image_data

def extract_from_image(image_data, num_bits, index=0):
    bit_string = ''
    end_at = index + num_bits
    while index <= end_at:
        red, green, blue = image_data[index]
        index += 1
        bit_string += extract_last_bit(red)
        bit_string += extract_last_bit(green)
        bit_string += extract_last_bit(blue)
    return bit_string[:num_bits]

def extract_text_length(image_data):
    length_in_binary = extract_from_image(image_data, int_size, string_length_start_pixel)
    length = int(length_in_binary, 2)
    return length

def extract_text(image_data, num_bits_to_extract):
    string_in_binary = extract_from_image(image_data, num_bits_to_extract, string_text_start_pixel)
    letters = re.findall('........', string_in_binary)
    text = ''
    for letter in letters:
        int_val = int(letter, 2)
        text += chr(int_val)
    return text
    
def extract_hidden_text(image_data):
    num_bits_to_extract = extract_text_length(image_data)
    text = extract_text(image_data, num_bits_to_extract)
    print(text)

    
def main(image_path, output_file, text, should_encrypt):
    image = Image.open(image_path)
    image_data = list(image.getdata())

    if should_encrypt:
        new_image = embed_in_image(image_data, text)
        image.putdata(new_image)
        image.save(output_file, 'PNG')
    else:
        text = extract_hidden_text(image_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hides text inside image.')
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument('--encrypt', '-e', action='store_true', default=False)
    group.add_argument('--decrypt', '-d', action='store_true', default=False)

    parser.add_argument('image_path', help='Image to hide text in')


    parser.add_argument('--text', '-t', help='Text to hide')
    parser.add_argument('--output_file', '-o', help='Name of output file', default=None)

    args = parser.parse_args()

    if args.encrypt and not args.text and not args.output_file:
        print('If encrypting text is required')
        sys.exit(0)
            
    main(args.image_path, args.output_file,  args.text, args.encrypt)
