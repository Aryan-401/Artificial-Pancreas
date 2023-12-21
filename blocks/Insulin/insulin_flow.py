from Insulin import Insulin
from blocks.static.type_check import InsulinModel
from blocks.static.constants import Constants
from blocks.static.common_funciton import mul_div, add_sub, MulDivModel, AddSubModel

c = Constants()
foo_bar = 0  # TODO: foo_bar is Integrator in Simulink

# LEFTMOST BLOCK
TmaxI = c.TmaxI
d = InsulinModel(t=0)
insulin_output = Insulin(d)
mul_result_1 = mul_div(MulDivModel(inputs=[foo_bar, TmaxI], symbols='*/'))  # FooBar1
add_result_1 = add_sub(AddSubModel(inputs=[insulin_output, mul_result_1], symbols='+-'))  # To Integrator
mul_result_2 = mul_div(MulDivModel(inputs=[foo_bar, c.TmaxI], symbols='*/'))  # FooBar2
add_result_2 = add_sub(AddSubModel(inputs=[mul_result_1, mul_result_2], symbols='+-'))  # To Integrator
# LEFTMOST BLOCK END

# SECOND BLOCK FROM LEFT
VI = c.VI
Ke = c.Ke
mul_result_3 = mul_div(MulDivModel(inputs=[mul_result_2, VI], symbols='*/'))
mul_result_4 = mul_div(MulDivModel(inputs=[Ke, foo_bar], symbols='**'))  # FooBar3
add_result_3 = add_sub(AddSubModel(inputs=[mul_result_3, mul_result_4], symbols='+-'))  # To Integrator
# SECOND BLOCK FROM LEFT END

# RIGHTMOST BLOCK
KB3 = c.KB3
KA3 = c.KA3
mul_result_5 = mul_div(MulDivModel(inputs=[KB3, foo_bar], symbols='**'))  # FooBar3
mul_result_6 = mul_div(MulDivModel(inputs=[foo_bar, KA3], symbols='**'))  # FooBar4
add_result_4 = add_sub(AddSubModel(inputs=[mul_result_6, mul_result_5], symbols='-+'))  # To Integrator
# RIGHTMOST BLOCK END
