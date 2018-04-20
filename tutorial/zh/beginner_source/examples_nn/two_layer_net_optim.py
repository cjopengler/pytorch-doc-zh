# -*- coding: utf-8 -*-
"""
PyTorch: optim
--------------

A fully-connected ReLU network with one hidden layer, trained to predict y from x
by minimizing squared Euclidean distance.

This implementation uses the nn package from PyTorch to build the network.

Rather than manually updating the weights of the model as we have been doing,
we use the optim package to define an Optimizer that will update the weights
for us. The optim package defines many optimization algorithms that are commonly
used for deep learning, including SGD+momentum, RMSProp, Adam, etc.
"""
import torch
from torch.autograd import Variable

# N 批量大小; D_in是输入尺寸;
# H是隐藏尺寸; D_out是输出尺寸.
N, D_in, H, D_out = 64, 1000, 100, 10

# 创建随机张量来保存输入和输出,并将它们包装在变量中.
x = Variable(torch.randn(N, D_in))
y = Variable(torch.randn(N, D_out), requires_grad=False)

# 使用nn包来定义我们的模型和损失函数.
model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
    torch.nn.ReLU(),
    torch.nn.Linear(H, D_out),
)
loss_fn = torch.nn.MSELoss(size_average=False)

# 使用优化包来定义一个优化器,它将为我们更新模型的权重.
# 在这里,我们将使用 Adam;这个 optim 包包含许多其他优化算法.
# Adam构造函数的第一个参数告诉优化器应该更新哪个Variables.
learning_rate = 1e-4
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
for t in range(500):
    # 正向传递:通过将x传递给模型来计算预测的y.
    y_pred = model(x)

    # 计算和打印损失函数.
    loss = loss_fn(y_pred, y)
    print(t, loss.data[0])

    # 在向后传递之前,使用优化器对象为其要更新的变量（这是模型的可学习权重）的所有梯度归零.
    # 这是因为默认情况下,只要调用.backward(),渐变就会在缓冲区中累积(即不会被覆盖).
    # 查看torch.autograd.backward的文档以获取更多详细信息.
    optimizer.zero_grad()

    # 向后传递:计算相对于模型参数的损失梯度
    loss.backward()

    # 在优化器上调用step功能会更新其参数
    optimizer.step()
