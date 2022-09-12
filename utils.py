numbers_to_emoji = {
        0: u'0️⃣',
        1: u'1️⃣',
        2: u'2️⃣',
        3: u'3️⃣',
        4: u'4️⃣',
        5: u'5️⃣',
        6: u'6️⃣',
        7: u'7️⃣',
        8: u'8️⃣',
        9: u'9️⃣',
    }
        

MINUS = u'➖'
PLUS = u'➕'


def i2e(num: int) -> str:
    if num < 0:
        result = MINUS
    else:
        result = ''

    digits = [d for d in str(abs(num))]
    for d in digits:
        result += numbers_to_emoji[int(d)]
    return result
