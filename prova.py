print("Hello world")

def somma(a, b):
    return a+b

def sottrazione (a,b):
    return a-b

def moltiplicazione (a,b):
    return a*b

def rad_quad (a):
    if(a<0):
        return "Impossibile"
    return a**0.5

print(f"La somma di 6 e 4 e'{somma(6,4)}")
print(f"La sottrazione tra 10 e 5 e' {sottrazione(10,5)}")
print(f"La moltiplicazione tra 3 e 5 e' {moltiplicazione(3, 5)}")
print(f"La radice quadrata di 1 e' {rad_quad(1)}")
