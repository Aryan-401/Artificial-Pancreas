from static.constants import Constants

c = Constants()

def kidney(G):
    Ke1 = 0.003
    Ke2 = 162
    
    if G >= Ke2:
        y = Ke1 * (G - Ke2)
    else:
        y = 0
    
    return y