import argparse
import base64
import random
import string
from jsmin import jsmin
from bs4 import BeautifulSoup

GREEN = '\033[92m'
RESET = '\033[0m'

BANNER = f"""
=================================================================================
{GREEN}HTML Obfuscator{RESET} by {GREEN}Icex0{RESET}
---------------------------------------------------------------------------------
{GREEN}HTML file > XOR with random key > Base64 > Base64 reverse > JS > Minify JS{RESET}
=================================================================================
"""

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

def xor_encrypt(text, key):
    #Encrypt content using XOR encryption. Fix for Unicode chars
    text_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')
    encrypted_bytes = bytes([text_byte ^ key_bytes[i % len(key_bytes)] for i, text_byte in enumerate(text_bytes)])
    return encrypted_bytes

def obfuscate_html(html_code, debug=False):
    #Obfuscate HTML content
    key_length = 5
    key = generate_random_key(key_length)
    if debug:
        print(f"{GREEN}Key:{RESET} {key}")

    xored_html = xor_encrypt(html_code, key)
    if debug:
        print(f"\n{GREEN}XOR encrypted HTML:{RESET}\n {xored_html}")

    base64_encoded = base64.b64encode(xored_html).decode('utf-8')
    if debug:
        print(f"\n{GREEN}Base64 encoded HTML:{RESET}\n {base64_encoded}")

    reversed_base64 = base64_encoded[::-1]
    if debug:
        print(f"\n{GREEN}Reversed Base64:{RESET}\n {reversed_base64}")

    obfuscated_content = key + reversed_base64
    if debug:
        print(f"\n{GREEN}With key:{RESET}\n {obfuscated_content}")
    return obfuscated_content

def generate_javascript(obfuscated_content):
    #Generate JS code with obfuscated HTML
    javascript_code = f"""
<script>
    var image = "{obfuscated_content}";
    var content_type = image.substring(0, 5), image_content = image.substring(5);
    var image_result = atob(image_content.split('').reverse().join(''));

    function image_decompress(content, type) {{
        return Array.from(content, (c, i) => String.fromCharCode(c.charCodeAt() ^ type.charCodeAt(i % type.length))).join('');
    }}
    document.write(image_decompress(image_result, content_type));
</script>
"""
    return javascript_code

def minify_js(js_code):
    return jsmin(js_code)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Obfuscate HTML content, generate JavaScript, and minify it")
    parser.add_argument("-f", "--file", help="Path to the HTML file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()

def main():
    print(BANNER)
    args = parse_arguments()

    if args.file:
        html_code = read_html_from_file(args.file, args.debug)
        obfuscated_html = obfuscate_html(html_code, args.debug)
        javascript_code = generate_javascript(obfuscated_html)
        
        minified_js_code = minify_js(javascript_code)
        print(f"\n{GREEN}Minified Javascript:{RESET}\n {minified_js_code}")
    else:
        print("Provide the path to the HTML file using -f or --file option.")

if __name__ == "__main__":
    main()