a = '34 sd'

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


d = [n for n in a.split(' ') if isfloat(n)]
print(d)
