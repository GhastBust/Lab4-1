
def green( text: str ) -> str :
    return '\x1b[92m' + text +  '\x1b[0m'

def azure( text: str ) -> str : 
    return '\x1b[94m' + text + '\x1b[0m'

def red( text: str ) -> str : 
    return '\x1b[91m' + text + '\x1b[0m'