import numpy as np

class Derr:
    
    value: float
    error: float

    def __init__(self, value, error) -> None:
        self.value = value
        self.error = error

    def __str__(self):
        return sci_err(self.value, self.error)
    
    def __format__(self):
        return sci_err(self.value, self.error)
    
    def __repr__(self):
        return sci_err(self.value, self.error)



def ld_to_dl( list_of_dicts ):
    return {k: [dic[k] for dic in list_of_dicts] for k in list_of_dicts[0]}


def dl_to_ld( dict_of_lists ):
    return [dict(zip(dict_of_lists,t)) for t in zip(*dict_of_lists.values())]


def weighted_mean_with_errors( data, errors ):

    weights = np.array(errors) ** -2
    
    w_mean  = np.average(data, weights= weights)
    w_err   = np.sqrt(1 / sum( weights ))

    return Derr(w_mean, w_err)


def weighted_mean_derr( list_of_derr: list[Derr] ):

    values, errors = [], []

    for obj in list_of_derr:
        values.append(obj.value)
        errors.append(obj.error)

    return weighted_mean_with_errors(values, errors)


def __get_mag__( number: float ) -> int:
    """
    `get_mag( a * 10^2 )` = 2
    con 1 <= a <= 9.99
    
    `get_mag( 1 )` = 0
    
    `get_mag( 0.99 )` = -1
    """
    return int(np.floor(np.log10(abs(number))))


def __exponent__(exp: int) -> str:

    ret_str: str = ""
    str_index = "⁰¹²³⁴⁵⁶⁷⁸⁹"

    if exp == 0:
        return "⁰"

    if exp < 0: 
        ret_str += "⁻"
        exp = -exp
    
    magnitude: int = __get_mag__(exp)

    digit: int

    for mag in range(magnitude, -1, -1):

        digit = int((exp // 10**mag)%10)

        ret_str += str_index[digit]

    return ret_str


def __get_n_dig__( number: float, n: int ) -> int:
    """
    with n = 987654
    
    `get_n_dig(n, 0) = 9`
    
    `get_n_dig(n, 2) = 7`
    
    get the n-th digit of the number, dont try to extact digits too far off, float math... 
    """

    number = abs(number)

    mag = __get_mag__(number)

    return (number // 10**(mag-n)) % 10


def __dsci_not__ ( value:float, digits: int ) -> tuple[str, str, int]:
    
    sign_str: str = ""

    if value < 0:
        sign_str = f"-"
        value = -value

    magnitude: int = __get_mag__(value)

    real_part: float = value / 10**magnitude

    if real_part >= 5:
        real_part /= 10
        magnitude += 1

    real_part = round(real_part, digits)

    return sign_str + f"{real_part}", f"10{__exponent__(magnitude)}", magnitude 


def sci_not( value: float, digits: int = 4) -> str:

    real_part, mag_str, _= __dsci_not__(value, digits)

    return real_part + " × " + mag_str


def sci_err( value: float, err: float, min_digits: float = 4 ):

    err = abs(err)

    digits : int = __get_mag__(value) - __get_mag__(err)
    digits = max(digits, min_digits)
    
    if __get_n_dig__(value, 0) >= 3:
        digits += 1

    real_part, mag_str, mag = __dsci_not__(value, digits)

    err += 10**mag
    err_part, _, _ = __dsci_not__(err, digits)
    err_part = err_part.replace("1", "0", 1)

    # return ret_str + f"{real_part} × 10{__exponent__(magnitude)}" 
    return f"[{real_part} ± {err_part}] × {mag_str}"


def __bdsci_not__ ( value:float, digits: int ) -> tuple[str, str, int]:
    
    sign_str: str = ""

    if value < 0:
        sign_str = f"-"
        value = -value

    magnitude: int = __get_mag__(value)

    base: float = value / 10**magnitude

    base = round(base, digits)

    return sign_str + f"{base}", f"10{__exponent__(magnitude)}", magnitude 


def bsci_err(value: float, err: float ) -> str :
    
    err = abs(err)
    
    value_mag = __get_mag__(value)
    err_mag   = __get_mag__(err)
    
    digits : int = value_mag - err_mag
        
    error = round(err, -err_mag)             # arrotonda alla prima cifra
    if __get_mag__(error) > err_mag:       # se c'è un 0.0099 => 0.01 non 0.010
        digits -= 1
    
    real_part, mag_str, mag = __dsci_not__(value, digits)
    
    if digits-1 == -1:
        error_displ = str(int(__get_n_dig__(error,0)))
        
    elif digits - 1 < -1:
        error_displ = str(int(__get_n_dig__(error,digits)))
        return f"[0.0 ± {error_displ}] × {mag_str}"
    
    else:
        error_displ = "0." + "0"*(digits-1) + str(int(__get_n_dig__(error,0)))
        
    return f"[{real_part} ± {error_displ}] × {mag_str}"
    


def nhypot(pos_value: float, *neg_values: float) -> float:

    result : float = pos_value**2

    for value in neg_values:

        result -= value**2

    return np.sqrt(result)

def phypot( *values: float ) -> float:

    result : float = 0

    for value in values:

        result += value**2

    return np.sqrt(result)

