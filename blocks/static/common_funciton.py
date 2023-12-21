from typing import List
from pydantic import BaseModel, validator
import warnings

warnings.filterwarnings("ignore")


class MulDivModel(BaseModel):
    '''
    # Example usage:
    data = {
        "inputs": [1, 2, 3],
        "symbols": "***"
    }

    MulDivModel(**data)
    '''
    inputs: List[float]
    symbols: str

    @validator('symbols')
    def check_length(cls, v, values, **kwargs):
        if 'inputs' in values and len(v) != len(values['inputs']):
            raise ValueError(f'Inputs and Symbols must have the same length\nGot {len(values["inputs"])} inputs and '
                             f'{len(v)} symbols')
        return v

    @validator('symbols')
    def check_symbols(cls, v, values, **kwargs):
        for symbol in v:
            if symbol not in ['*', '/']:
                raise ValueError(f'Invalid symbol: Expected "*" or "/" got "{symbol}"')
        return v


class AddSubModel(BaseModel):
    """
    # Example usage:
    data = {
        "inputs": [1, 5, 3],
        "symbols": "+++"
    }

    print(add_sub(AddSubModel(**data)))
    """
    inputs: List[float]
    symbols: str

    @validator('symbols')
    def check_length(cls, v, values, **kwargs):
        if 'inputs' in values and len(v) != len(values['inputs']):
            raise ValueError(f'Inputs and Symbols must have the same length\nGot {len(values["inputs"])} inputs and '
                             f'{len(v)} symbols')
        return v

    @validator('symbols')
    def check_symbols(cls, v, values, **kwargs):
        for symbol in v:
            if symbol not in ['+', '-']:
                raise ValueError(f'Invalid symbol: Expected "+" or "-" got "{symbol}"')
        return v


def mul_div(data: MulDivModel) -> float:
    result = data.inputs[0]
    for i in range(1, len(data.inputs)):
        if data.symbols[i - 1] == '*':
            result *= data.inputs[i]
        elif data.symbols[i - 1] == '/':
            result /= data.inputs[i]
    return result


def add_sub(data: AddSubModel) -> float:
    result = data.inputs[0]
    for i in range(1, len(data.inputs)):
        if data.symbols[i - 1] == '+':
            result += data.inputs[i]
        elif data.symbols[i - 1] == '-':
            result -= data.inputs[i]
    return result



