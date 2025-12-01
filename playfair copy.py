import numpy as np

def make_matrix(key):
    key = key.upper().replace("J", "I")
    alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    s = "".join(dict.fromkeys(key + alpha))  # remove duplicates while preserving order
    return np.array(list(s)).reshape(5,5)

def prep(text):
    t = "".join(ch for ch in text.upper().replace("J","I") if ch.isalpha())
    out = []
    i = 0
    while i < len(t):
        a = t[i]
        b = t[i+1] if i+1 < len(t) else "X"
        if a == b:
            out.append(a + "X")
            i += 1
        else:
            out.append(a + b)
            i += 2
    return out

def pos(m, c):
    x, y = np.where(m == c)
    return int(x[0]), int(y[0])

def process(pairs, m, dec=False):
    s = -1 if dec else 1
    out = []
    for a,b in pairs:
        x1,y1 = pos(m,a)
        x2,y2 = pos(m,b)

        if x1 == x2:  # row
            out.append(m[x1,(y1+s)%5] + m[x2,(y2+s)%5])
        elif y1 == y2:  # column
            out.append(m[(x1+s)%5,y1] + m[(x2+s)%5,y2])
        else:  # rectangle
            out.append(m[x1,y2] + m[x2,y1])
    return "".join(out)

def encrypt(pt, key):
    m = make_matrix(key)
    return process(prep(pt), m)

def decrypt(ct, key):
    m = make_matrix(key)
    pairs = [ct[i:i+2] for i in range(0, len(ct), 2)]
    return process(pairs, m, dec=True)


# Example
if __name__ == "__main__":
    c = encrypt("HIDE THE GOLD", "keyword")
    print("Cipher:", c)
    print("Plain :", decrypt(c, "keyword"))