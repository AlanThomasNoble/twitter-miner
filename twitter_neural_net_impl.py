import re

# Alternative/Merged Implementation of Clean Text
'''This implementation entirely removes hashtags and mentions'''
'''pythex.org'''
def cleanTextNN(text, cleanEmoticons=False):
    # Conversions
    text = text.lower() # Convert to lowercase
    
    # Removals
    text = re.sub(r'@[A-Za-z0-9]+','',text) # Removes mentions
    text = re.sub(r'#[A-Za-z0-9_]+','',text) # Removes hashtags
    text = re.sub(r'(https?)://[-a-zA-Z0-9@:%_\+.~#?&//=]*','',text) # Removes hyperlink

    # Cleanup
    text = re.sub('[\s]+',' ',text) # Removes additional white spaces
    text = text.strip('\'"').lstrip().rstrip() # Trim (Removes '' and Trailing and Leading Spaces)

    if cleanEmoticons:
        pass    # :\)|:-\)|:\(|:-\(|;\);-\)|:-O|8-|:P|:D|:\||:S|:\$|:@|8o\||\+o\(|\(H\)|\(C\)|\(\?\)

    return text

def main():
    print(cleanTextNN("Hello 8342938@jhgjh #jhb $@#$     world"))

if __name__ == "__main__":
    main()