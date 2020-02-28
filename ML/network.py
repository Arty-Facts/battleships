import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
class ConvSkip(nn.Module):
    def __init__(self, n_in, n_out, kernel_size=3, stride=1, padding=1, bias=False):
        super(ConvSkip, self).__init__()
        self.layer = nn.Sequential(
                        nn.Conv2d(n_in, n_in, kernel_size=kernel_size, stride=stride, padding=padding, bias=bias),
                        nn.BatchNorm2d(n_out),
                        nn.ReLU(inplace=True),
                        nn.Conv2d(n_in, n_out, kernel_size=kernel_size, stride=stride, padding=padding, bias=bias),
                        nn.BatchNorm2d(n_out),
                        nn.ReLU(inplace=True),
                        )
        self.mp = nn.MaxPool2d(kernel_size=(3, 3), stride=1 , padding=1)
    def forward(self, inputs):
        return self.mp(inputs) + self.layer(inputs)

class Conv(nn.Module):
    def __init__(self, n_in, n_out, kernel_size=3, stride=2, padding=1, bias=False):
        super(Conv, self).__init__()
        self.layer = nn.Sequential(
                        nn.Conv2d(n_in, n_out, kernel_size=kernel_size, stride=stride, padding=padding, bias=bias),
                        nn.BatchNorm2d(n_out),
                        nn.ReLU(inplace=True),
                        )
    def forward(self, inputs):
        return self.layer(inputs)

class Network(nn.Module):   
    def __init__(self, depth=1):
        super(Network, self).__init__()
        self.mask_step = lambda x: x.to(
                            dtype=torch.long,
                            device=next(self.parameters()).device.type
                            )
        self.step_0 = lambda x: x.to( 
                            dtype=next(self.parameters()).dtype, 
                            device=next(self.parameters()).device.type
                            )

        self.step_1 = nn.Sequential(
                    Conv(3, 16, kernel_size=3, padding=1, stride=1), #10
                    nn.Sequential(*[
                        nn.Sequential(*[
                            ConvSkip(16,16)
                        ]) for _ in range(depth)]
                        ),
                )
        self.step_2 = nn.Sequential(
                    nn.MaxPool2d(kernel_size=(3, 3), stride=1 , padding=1),
                    Conv(16, 32), #5
                    nn.Sequential(*[
                        nn.Sequential(*[
                            ConvSkip(32,32)
                        ]) for _ in range(depth)]
                        ),
                )


        self.step_3 = nn.Sequential(
                    nn.MaxPool2d(kernel_size=(3, 3), stride=1 , padding=1),
                    Conv(32, 64), #3
                    nn.Sequential(*[
                        nn.Sequential(*[
                            ConvSkip(64,64)
                        ]) for _ in range(depth)]
                        ),
                )

        self.step_4 = nn.Sequential(
                    nn.MaxPool2d(kernel_size=(3, 3), stride=1 , padding=1),
                    Conv(64, 128), #2
                    nn.Sequential(*[
                        nn.Sequential(*[
                            ConvSkip(128,128)
                        ]) for _ in range(depth)]
                        ),
                    nn.ConvTranspose2d(128, 64, kernel_size=(3, 3), stride=2, padding=1, bias=True), #3
                    nn.ReLU(inplace=True) 
                )

        # torch.cat([out3,out4])
        self.step_5 = nn.Sequential(
                    nn.ConvTranspose2d(128, 32, kernel_size=(3, 3), stride=2, padding=1, bias=True), #5
                    nn.ReLU(inplace=True)
                )

        # torch.cat([out2,out5]) 
        self.step_6 = nn.Sequential(
                    nn.ConvTranspose2d(64, 16, kernel_size=(4, 4), stride=2, padding=1, bias=True), #10
                    nn.ReLU(inplace=True) 
                )
        # torch.cat([out1,out6]) 
        self.step_7 = nn.Sequential(
                    ConvSkip(32,32, kernel_size=(3, 3), padding=1),
                    nn.Conv2d(32, 2,  kernel_size=(3, 3), stride=1, padding=1, bias=True), #
                    nn.Softmax(dim=1)
                )

    def forward(self, inputs):
        out1 = self.step_1(inputs)
        out2 = self.step_2(out1)
        out3 = self.step_3(out2)
        out4 = self.step_4(out3)
        inp5 = torch.cat([out3,out4], dim=1)
        out5 = self.step_5(inp5)
        inp6 = torch.cat([out2,out5], dim=1)
        out6 = self.step_6(inp6)
        inp7 = torch.cat([out1,out6], dim=1)
        out7 = self.step_7(inp7)
        return out7

    def predict(self, inputs):
        return self.forward(inputs) 

    def fitt_and_predict(self, inputs):
        return self.forward(self.step_0(inputs))