from static.constants import Constants

c = Constants()

def insulin_independent(G):
    F01 = 18 * ((0.00097 * 70) / (0.12 * 70))
    
    if G >= 81:
        y = F01
    else:
        y = F01 * (G / 81)
    
    return y