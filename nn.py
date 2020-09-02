import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 56 input
        self.fc1 = nn.Linear(56, 16)
        self.fc2 = nn.Linear(16, 3)

    def forward(self, x: Tensor) -> Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return F.softmax(x, dim=0)
