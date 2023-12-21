from blocks.static.constants import Constants
from blocks.static.type_check import InsulinModel

c = Constants()


def Insulin(data: InsulinModel) -> float:
    if 210 < data.t < 215:
        i = 700
    elif 450 < data.t < 455:
        i = 250
    elif 690 < data.t < 695:
        i = 200
    else:
        i = 12.9127
    return i


"""
Formula used to calculate insulin
body_weight =70;
TDD = 0.55*body_weight;

ICR= 500/TDD;

ISF = 1800/TDD

Breakfast_m1 = 30;
Lunch_m2 = 60;
Dinner_m3 = 40;

m1_bolus = Breakfast_m1 / ICR;
m2_bolus = Lunch_m2/ICR;
m3_bolus = Dinner_m3/ICR;

Average_m = (m1_bolus+m2_bolus+m3_bolus)/3;

Active_insulin = (Average_m)/body_weight;
Active_insulin = 6/body_weight;

BG_target1 = 100;
BG_current1 = 96.7;

Correction_bolus1 = (BG_current1 - BG_target1)/ISF;
i= ((m1_bolus +Correction_bolus1 -Active_insulin) *10^6)/10;

"""
