# -*- coding:utf-8 -*-
"""
@Time:    2023/11/27 19:36
@Author:  Evan Wong
@File:    angle_interpolation.py
@Project: NAOGolf
@Description: The file to store some angle interpolations
"""


def soft_hit():
    """
    Softly hit the ball.

    :return:
        angle interpolations: names, times, keys
        :rtype: tuple[list, list, list]
    """
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([1.28])
    keys.append([[-0.993989, [3, -0.44, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([1.28])
    keys.append([[-1.37604, [3, -0.44, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([1.28])
    keys.append([[0.264, [3, -0.44, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([1.28])
    keys.append([[1.42965, [3, -0.44, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([1.28])
    keys.append([[0.27301, [3, -0.44, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([1.28])
    keys.append([[0.0413762, [3, -0.44, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([1.28])
    keys.append([[0.598302, [3, -0.44, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([1.28])
    keys.append([[1.27625, [3, -0.44, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([1.28])
    keys.append([[0.2572, [3, -0.44, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([1.28])
    keys.append([[0.441834, [3, -0.44, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([1.28])
    keys.append([[0.115008, [3, -0.44, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([0.8, 1.28])
    keys.append([[0.767945, [3, -0.28, 0], [3, 0.16, 0]], [-0.0314159, [3, -0.16, 0], [3, 0, 0]]])

    return names, times, keys


def medium_hit():
    """
    Hit the ball with medium force.

    :return:
        angle interpolations: names, times, keys
        :rtype: tuple[list, list, list]
    """
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([1.16])
    keys.append([[-0.993989, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([1.16])
    keys.append([[-1.37604, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([1.16])
    keys.append([[0.264, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([1.16])
    keys.append([[1.42965, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([1.16])
    keys.append([[0.27301, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([1.16])
    keys.append([[0.0413762, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([1.16])
    keys.append([[0.598302, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([1.16])
    keys.append([[1.27625, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([1.16])
    keys.append([[0.2572, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([1.16])
    keys.append([[0.441834, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([1.16])
    keys.append([[0.115008, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([0.64, 1.16])
    keys.append([[0.767945, [3, -0.226667, 0], [3, 0.173333, 0]], [-0.228638, [3, -0.173333, 0], [3, 0, 0]]])

    return names, times, keys


def hard_hit():
    """
    Hardly hit the ball.

    :return:
        angle interpolations: names, times, keys
        :rtype: tuple[list, list, list]
    """
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([1.32])
    keys.append([[-0.993989, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([1.32])
    keys.append([[-1.37604, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([1.32])
    keys.append([[0.264, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([1.32])
    keys.append([[1.42965, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([1.32])
    keys.append([[0.27301, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([1.32])
    keys.append([[0.0413762, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([1.32])
    keys.append([[0.598302, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([1.32])
    keys.append([[1.27625, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([1.32])
    keys.append([[0.2572, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([1.32])
    keys.append([[0.441834, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([1.32])
    keys.append([[0.115008, [3, -0.453333, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([0.92, 1.32])
    keys.append([[0.767945, [3, -0.32, 0], [3, 0.133333, 0]], [-0.228638, [3, -0.133333, 0], [3, 0, 0]]])

    return names, times, keys


def strong_hit():
    """
    Hit the ball with strong force.

    :return:
        angle interpolations: names, times, keys
        :rtype: tuple[list, list, list]
    """
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([1.16])
    keys.append([[-0.993989, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([1.16])
    keys.append([[-1.37604, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([1.16])
    keys.append([[0.264, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([1.16])
    keys.append([[1.42965, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([1.16])
    keys.append([[0.27301, [3, -0.4, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([1.16])
    keys.append([[0.0413762, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([1.16])
    keys.append([[0.598302, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([1.16])
    keys.append([[1.27625, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([1.16])
    keys.append([[0.2572, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([1.16])
    keys.append([[0.441834, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([1.16])
    keys.append([[0.115008, [3, -0.4, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([0.88, 1.0])
    keys.append([[0.767945, [3, -0.306667, 0], [3, 0.0933333, 0]], [-0.563741, [3, -0.0933333, 0], [3, 0, 0]]])
    return names, times, keys


def hand_ready():
    """
    Lift the hand out of the init and Put it up.
    The initial location needs to be based on golf_init.

    :return:
        angle interpolations: names, times, keys
        :rtype: tuple[list, list, list]
    """
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append([[-0.970981, [3, -0.226667, 0], [3, 0.226667, 0]],
                 [-0.960242, [3, -0.226667, -0.0031803], [3, 0.32, 0.00448983]],
                 [-0.94797, [3, -0.32, 0], [3, 0.266667, 0]], [-0.94797, [3, -0.266667, 0], [3, 0.266667, 0]],
                 [-0.972514, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append([[-1.37604, [3, -0.226667, 0], [3, 0.226667, 0]], [-1.37604, [3, -0.226667, 0], [3, 0.32, 0]],
                 [-1.35917, [3, -0.32, 0], [3, 0.266667, 0]], [-1.35917, [3, -0.266667, 0], [3, 0.266667, 0]],
                 [-1.36684, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append([[0.264, [3, -0.226667, 0], [3, 0.226667, 0]], [0.264, [3, -0.226667, 0], [3, 0.32, 0]],
                 [0.2528, [3, -0.32, 0], [3, 0.266667, 0]], [0.2528, [3, -0.266667, 0], [3, 0.266667, 0]],
                 [0.256, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append([[1.46186, [3, -0.226667, 0], [3, 0.226667, 0]], [1.46186, [3, -0.226667, 0], [3, 0.32, 0]],
                 [1.47106, [3, -0.32, 0], [3, 0.266667, 0]], [1.47106, [3, -0.266667, 0], [3, 0.266667, 0]],
                 [1.47567, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append([[0.239262, [3, -0.226667, 0], [3, 0.226667, 0]], [0.239262, [3, -0.226667, 0], [3, 0.32, 0]],
                 [0.240796, [3, -0.32, 0], [3, 0.266667, 0]], [0.240796, [3, -0.266667, 0], [3, 0.266667, 0]],
                 [0.245398, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append([[0.030638, [3, -0.226667, 0], [3, 0.226667, 0]], [0.030638, [3, -0.226667, 0], [3, 0.32, 0]],
                 [0.05825, [3, -0.32, 0], [3, 0.266667, 0]], [0.05825, [3, -0.266667, 0], [3, 0.266667, 0]],
                 [0.032172, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append([[0.07214, [3, -0.226667, 0], [3, 0.226667, 0]],
                 [0.200996, [3, -0.226667, -0.0485517], [3, 0.32, 0.0685435]],
                 [0.423426, [3, -0.32, 0], [3, 0.266667, 0]], [0.342125, [3, -0.266667, 0], [3, 0.266667, 0]],
                 [0.566088, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append(
        [[1.4051, [3, -0.226667, 0], [3, 0.226667, 0]], [1.36062, [3, -0.226667, 0.0192934], [3, 0.32, -0.0272377]],
         [1.26551, [3, -0.32, 0.025102], [3, 0.266667, -0.0209183]], [1.22256, [3, -0.266667, 0], [3, 0.266667, 0]],
         [1.25477, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append(
        [[0.3088, [3, -0.226667, 0], [3, 0.226667, 0]], [0.25, [3, -0.226667, 0.0136553], [3, 0.32, -0.0192781]],
         [0.21, [3, -0.32, 0], [3, 0.266667, 0]], [0.23, [3, -0.266667, -0.00873333], [3, 0.266667, 0.00873333]],
         [0.2624, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append(
        [[1.53864, [3, -0.226667, 0], [3, 0.226667, 0]], [0.277696, [3, -0.226667, 0.228554], [3, 0.32, -0.322664]],
         [-0.115008, [3, -0.32, 0.0257713], [3, 0.266667, -0.0214761]],
         [-0.136484, [3, -0.266667, 0], [3, 0.266667, 0]], [0.452572, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append([[-0.378941, [3, -0.226667, 0], [3, 0.226667, 0]], [-1.22111, [3, -0.226667, 0], [3, 0.32, 0]],
                 [0.00149202, [3, -0.32, -0.0128855], [3, 0.266667, 0.0107379]],
                 [0.0122299, [3, -0.266667, -0.0107379], [3, 0.266667, 0.0107379]],
                 [0.0950661, [3, -0.266667, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([0.64, 1.32, 2.28, 3.08, 3.88])
    keys.append([[-0.154976, [3, -0.226667, 0], [3, 0.226667, 0]],
                 [-0.986404, [3, -0.226667, 0.0119523], [3, 0.32, -0.0168739]],
                 [-1.00328, [3, -0.32, 0], [3, 0.266667, 0]],
                 [0.561996, [3, -0.266667, -0.104311], [3, 0.266667, 0.104311]],
                 [0.391128, [3, -0.266667, 0], [3, 0, 0]]])

    return names, times, keys


def hang_down():
    """
    Have the NAO robot's hands hanged down.

    :return:
        angle interpolations: names, times, keys
        :rtype: tuple[list, list, list]
    """
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[-0.94797, [3, -0.32, 0], [3, 0.28, 0]], [-0.94797, [3, -0.28, 0], [3, 0.36, 0]],
                 [-0.960242, [3, -0.36, 0.0036981], [3, 0.386667, -0.00397203]],
                 [-0.970981, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[-1.35917, [3, -0.32, 0], [3, 0.28, 0]], [-1.35917, [3, -0.28, 0], [3, 0.36, 0]],
                 [-1.37604, [3, -0.36, 0], [3, 0.386667, 0]], [-1.37604, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[0.2528, [3, -0.32, 0], [3, 0.28, 0]], [0.2528, [3, -0.28, 0], [3, 0.36, 0]],
                 [0.264, [3, -0.36, 0], [3, 0.386667, 0]], [0.264, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[1.47106, [3, -0.32, 0], [3, 0.28, 0]], [1.47106, [3, -0.28, 0], [3, 0.36, 0]],
                 [1.46186, [3, -0.36, 0], [3, 0.386667, 0]], [1.46186, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[0.240796, [3, -0.32, 0], [3, 0.28, 0]], [0.240796, [3, -0.28, 0], [3, 0.36, 0]],
                 [0.239262, [3, -0.36, 0], [3, 0.386667, 0]], [0.239262, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[0.05825, [3, -0.32, 0], [3, 0.28, 0]], [0.05825, [3, -0.28, 0], [3, 0.36, 0]],
                 [0.030638, [3, -0.36, 0], [3, 0.386667, 0]], [0.030638, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[0.342125, [3, -0.32, 0], [3, 0.28, 0]], [0.423426, [3, -0.28, 0], [3, 0.36, 0]],
                 [0.200996, [3, -0.36, 0.0564566], [3, 0.386667, -0.0606386]],
                 [0.07214, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[1.22256, [3, -0.32, 0], [3, 0.28, 0]], [1.26551, [3, -0.28, -0.0201339], [3, 0.36, 0.0258864]],
                 [1.36062, [3, -0.36, -0.0224346], [3, 0.386667, 0.0240964]],
                 [1.4051, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[0.22, [3, -0.32, 0], [3, 0.28, 0]], [0.21, [3, -0.28, 0], [3, 0.36, 0]],
                 [0.24, [3, -0.36, 0], [3, 0.386667, 0]], [0.21, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append(
        [[-0.136484, [3, -0.32, 0], [3, 0.28, 0]], [-0.115008, [3, -0.28, -0.0214761], [3, 0.36, 0.0276121]],
         [0.277696, [3, -0.36, -0.265765], [3, 0.386667, 0.285452]], [1.53864, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append(
        [[0.0122299, [3, -0.32, 0], [3, 0.28, 0]], [0.00149202, [3, -0.28, 0.0107379], [3, 0.36, -0.0138059]],
         [-1.22111, [3, -0.36, 0], [3, 0.386667, 0]], [-0.378941, [3, -0.386667, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([0.92, 1.76, 2.84, 4])
    keys.append([[0.286817, [3, -0.32, 0], [3, 0.28, 0]], [-1.00328, [3, -0.28, 0], [3, 0.36, 0]],
                 [-0.986404, [3, -0.36, -0.0168739], [3, 0.386667, 0.0181238]],
                 [-0.154976, [3, -0.386667, 0], [3, 0, 0]]])

    return names, times, keys


def setup_movement():
    """
    Initialization movement for golf competition.

    :return:
        angle interpolations: names, times, keys
        :rtype: tuple[list, list, list]
    """
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([0.92])
    keys.append([[-0.970981, [3, -0.32, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([0.92])
    keys.append([[-1.37604, [3, -0.32, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([0.92])
    keys.append([[0.264, [3, -0.32, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([0.92])
    keys.append([[1.46186, [3, -0.32, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([0.92])
    keys.append([[0.239262, [3, -0.32, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([0.92])
    keys.append([[0.030638, [3, -0.32, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([0.92])
    keys.append([[0.07214, [3, -0.32, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([0.92])
    keys.append([[1.4051, [3, -0.32, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([0.92])
    keys.append([[0.3088, [3, -0.32, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([0.92])
    keys.append([[1.53864, [3, -0.32, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([0.92])
    keys.append([[-0.378941, [3, -0.32, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([0.92])
    keys.append([[-0.154976, [3, -0.32, 0], [3, 0, 0]]])

    return names, times, keys
