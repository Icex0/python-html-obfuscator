import argparse
import base64
import random
import string

def read_html_from_file(filename, debug=False):
    # Read HTML content, return only content within body tags
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        body_tag = soup.find('body')
        if body_tag:
            body_content = body_tag.decode_contents()
        else:
            #If no body tag found, return entire content of file
            body_content = html_content

        if debug:
            print(f"\n{GREEN}HTML read:{RESET}\n {body_content}")

        return body_content

def generate_random_key(length):
    #Generate a random key of a x length.
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def obfuscate_html(html_code):
    key_length = 5
    key = generate_random_key(key_length)
    print("Key:", key)

    # XOR encryption
    def xor_encrypt(text, key):
        encrypted = []
        for i in range(len(text)):
            encrypted.append(chr(ord(text[i]) ^ ord(key[i % len(key)])))
        return ''.join(encrypted)

    xored_html = xor_encrypt(html_code, key)
    print("\nXOR encrypted HTML:\n", xored_html)

    # Base64 encoding
    base64_encoded = base64.b64encode(xored_html.encode()).decode()
    print("\nBase64 encoded HTML:\n", base64_encoded)

    # Reverse Base64
    reversed_base64 = base64_encoded[::-1]
    print("\nReversed Base64:\n", reversed_base64)

    # Generate random chunk size
    min_chunk_size = 5
    max_chunk_size = 20
    chunk_size = random.randint(min_chunk_size, max_chunk_size)
    print("\nChunk Size:\n", chunk_size)

    # Chunking
    chunked_base64 = [reversed_base64[i:i+chunk_size] for i in range(0, len(reversed_base64), chunk_size)]
    print("\nChunked Base64:\n", chunked_base64)

    # Shuffle order for all chunks except the last one
    shuffle_order = list(range(len(chunked_base64) - 1))
    random.shuffle(shuffle_order)
    # Convert shuffle order to double-digit string
    shuffle_order_str = ''.join([f"{i:02}" for i in shuffle_order])
    print("\nShuffle Order:\n", shuffle_order)

    # Shuffle the chunks based on the shuffle order
    shuffled_chunks = [chunked_base64[i] for i in shuffle_order]
    print("\nShuffled:\n", shuffled_chunks)

    # Extract and append the last chunk
    last_chunk = chunked_base64[-1]
    shuffled_chunks.append(last_chunk)

    # Calculate the length of the last chunk
    last_chunk_length = len(last_chunk)
    last_chunk_length_str = '{:02}'.format(last_chunk_length)

    # Combine chunks in the obfuscated content
    obfuscated_content = shuffle_order_str + ''.join(shuffled_chunks) + last_chunk_length_str +'{:02x}'.format(chunk_size) 

    return key + obfuscated_content

def parse_arguments():
    parser = argparse.ArgumentParser(description="Obfuscate HTML content, generate JavaScript, and minify it")
    parser.add_argument("-f", "--file", help="Path to the HTML file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()

def main():
    print(BANNER)
    args = parse_arguments()

    if args.file:
        html_code = read_html_from_file(args.file)
        obfuscated_html = obfuscate_html(html_code)
        print("\nFinal Obfuscated HTML:", obfuscated_html)
    else:
        print("Provide the path to the HTML file using -f or --file option.")

if __name__ == "__main__":
    main()