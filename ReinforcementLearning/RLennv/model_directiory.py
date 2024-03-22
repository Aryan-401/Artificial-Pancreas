import torch
import torch.nn as nn
# from environment import Bergman
from RLennv.Constants import Constants
from RLennv.environment import Bergman
import matplotlib.pyplot as plt


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
class NeuralNetwork_v6(nn.Module):
    def __init__(self, input_size, output_size):
        super(NeuralNetwork_v6, self).__init__()
        self.l1 = nn.Linear(input_size, 128)
        self.l2 = nn.Linear(128, 256)
        self.l3 = nn.Linear(256, 512)
        self.l4 = nn.Linear(512, 256)
        self.l5 = nn.Linear(256, 128)
        self.l6 = nn.Linear(128, 64)
        self.fc = nn.Linear(64, output_size)
        self.relu = nn.ReLU()
        self.sig = nn.Sigmoid()

    def forward(self, x):
        x = self.l1(x)
        x = self.l2(x)
        x = self.relu(x)
        x = self.l3(x)
        x = self.l4(x)
        x = self.relu(x)
        x = self.l5(x)
        x = self.l6(x)
        x = self.relu(x)
        x = self.fc(x)
        x = torch.abs(self.sig(x)*50)
        x = torch.clamp(x, min=0, max=50)
        # print(f"At C1: {x}")
        return x

## Include in Paper
## New Model Iter. 1

class NeuralNetwork_v7(nn.Module):
    def __init__(self, input_size, output_size, n_check=20, num_layers_lstm=5):
        super(NeuralNetwork_v7, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.num_layers_lstm = num_layers_lstm
        self.n_check = n_check
        self.lstm = nn.LSTM(input_size, hidden_size=n_check, num_layers=num_layers_lstm, batch_first=True)
        self.h1 = nn.Linear(n_check, 32)
        self.h2 = nn.Linear(32, 16)
        self.h3 = nn.Linear(16, 8)
        self.fc = nn.Linear(8, output_size)
        self.fc2 = nn.Linear(num_layers_lstm, 1)
        self.relu = nn.ReLU()
        self.sig = nn.Sigmoid()
        self.tanh = nn.Tanh()
        self.c = True
        self.p  = 0.5

    def forward(self, x):
        x, (h0, c0) = self.lstm(x)
        x = h0
        x = self.h1(x)
        x = self.relu(x)
        x = self.h2(x)
        x = self.relu(x)
        x = self.h3(x)
        x = self.relu(x)
        x = self.fc(x)
        x = self.fc2(x.T)
        x = self.sig(x)
        if self.c:
            self.c = False
            self.p = x
            print(x)
        x = (((x )/self.p) - 1) * 12500 * 45 # To increase range from (1.000 to 1.0020) t0 (0 to 50ish)
        return torch.clamp(x, min=0, max=50)

## Include in Paper
## Iter. 2 on v7. Added Batch Normalisation after every linear layer
## We notice that v7 would often alternate between 0 and `n` to maintain a low average Insulin dosage
## This model can Intuitively set insulin to 0 when no meals are fed (Which was a rare site in v7
## and not seen at all in the other version that we replicated)


class NeuralNetwork_v8(nn.Module):
    def __init__(self, input_size, output_size, n_check=20, num_layers_lstm=5):
        super(NeuralNetwork_v8, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.num_layers_lstm = num_layers_lstm
        self.n_check = n_check
        self.lstm = nn.LSTM(input_size, hidden_size=n_check, num_layers=num_layers_lstm, batch_first=True)
        self.h1 = nn.Linear(n_check, 32)
        self.bn1 = nn.BatchNorm1d(32)  # Batch normalization layer after first linear layer
        self.h2 = nn.Linear(32, 16)
        self.bn2 = nn.BatchNorm1d(16)  # Batch normalization layer after second linear layer
        self.h3 = nn.Linear(16, 8)
        self.bn3 = nn.BatchNorm1d(8)  # Batch normalization layer after third linear layer
        self.fc = nn.Linear(8, output_size)
        self.fc2 = nn.Linear(num_layers_lstm, 1)
        self.relu = nn.ReLU()
        self.sig = nn.Sigmoid()
        self.tanh = nn.Tanh()
        self.c = True
        self.p = 0.5

    def forward(self, x):
        x, (h0, c0) = self.lstm(x)
        x = h0
        x = self.h1(x)
        x = self.bn1(x)  # Batch normalization
        x = self.relu(x)
        x = self.h2(x)
        x = self.bn2(x)  # Batch normalization
        x = self.relu(x)
        x = self.h3(x)
        x = self.bn3(x)  # Batch normalization
        x = self.relu(x)
        x = self.fc(x)
        x = self.fc2(x.T)
        x = self.sig(x)
        if self.c:
            self.c = False
            self.p = x
            print(x)
        x = (((x) / self.p) - 1) * 1000 * 2 # To increase range from (1.000 to 1.0020) to (0 to 50ish)
        # return x
        return torch.clamp(x, min=0, max=50)


def inference_model(model_name, meta_data):
    c = Constants()
    c.set_values(dict_=meta_data['parameters'])
    meal_info = meta_data['grid_data']
    meal_gram = [meal_info[i] for i in range(len(meal_info)) if i % 2 == 0]
    meal_time = [meal_info[i] for i in range(len(meal_info)) if i % 2 == 1]
    env = Bergman(params=c, meal_gram=meal_gram, meal_time=meal_time)
    if model_name == "Previous Paper":
        model = NeuralNetwork_v6(3, 1)
        file_name = 'NeuralNetwork_v6_1708672087_2000.pth'
    elif model_name == "LSTM wo BN":
        model = NeuralNetwork_v7(3, 1)
        file_name = 'NeuralNetwork_v7_1709879593_1000.pth'
    elif model_name == "LSTM w BN":
        model = NeuralNetwork_v8(3, 1)
        file_name = 'NeuralNetwork_v8_1710154328_1000.pth'
    else:
        raise ValueError("Model not found")
    model.load_state_dict(torch.load(f"ReinforcementLearning/Models/{file_name}", map_location=device))

    model.eval()
    with torch.no_grad():
        state = env.reset()
        while env.cur_time <= c.MAX_TIME:
            state_tensor = torch.tensor(state, dtype= torch.float32).to(device)
            state_tensor = state_tensor.unsqueeze(0)
            action = model(state_tensor)
            n_state, _, __, ___ = env.step([action.item()])
            state = n_state

    plt.plot(env.t_graph_list, env.g_graph_list, color='blue', label='Glucose Plot')
    plt.savefig('ReinforcementLearning/graph_gt.png')
    plt.close()
    plt.plot(env.t_graph_list, env.i_graph_list, color='blue', label="Insulin Plot")
    plt.savefig('ReinforcementLearning/graph_it.png')
    plt.close()
