#!/usr/bin/env python
# vim:set ft=python fileencoding=utf-8 sr et ts=4 sw=4 : See help 'modeline'

'''
    == A few notes about color ==
    Color   Wavelength(nm) Frequency(THz)
    Red     620-750        484-400
    Orange  590-620        508-484
    Yellow  570-590        526-508
    Green   495-570        606-526
    Blue    450-495        668-606
    Violet  380-450        789-668
    f is frequency (cycles per second)
    l (lambda) is wavelength (meters per cycle)
    e is energy (Joules)
    h (Plank's constant) = 6.6260695729 x 10^-34 Joule*seconds
                         = 6.6260695729 x 10^-34 m^2*kg/seconds
    c = 299792458 meters per second
    f = c/l
    l = c/f
    e = h*f
    e = c*h/l
    List of peak frequency responses for each type of 
    photoreceptor cell in the human eye:
        S cone: 437 nm
        M cone: 533 nm
        L cone: 564 nm
        rod:    550 nm in bright daylight, 498 nm when dark adapted. 
                Rods adapt to low light conditions by becoming more sensitive.
                Peak frequency response shifts to 498 nm.
'''
import csv
import sys
import os
import traceback
import optparse
import time
import logging
import time
import datetime
from win10toast import ToastNotifier


def wavelength_to_rgb(wavelength, gamma=0.8):
    """
    Description:
    Given a wavelength in the range of (380nm, 750nm), visible light range.
    a tuple of intergers for (R,G,B) is returned.
    The integers are scaled to the range (0, 1).

    Based on code: http://www.noah.org/wiki/Wavelength_to_RGB_in_Python

    Parameters:
        Wavelength: the given wavelength range in (380, 750)
    Returns:
        (R,G,B): color range in (0,1)
    """
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    return (R, G, B)

def pc_toast(text):
    toaster = ToastNotifier()
    header = "测试完成"  # 通知的标题
    time_min = float(0.2)
    time.sleep(1)
    time.sleep(time_min)
    toaster.show_toast(title=f"{header}", msg=f"{text}", duration=10, threaded=True)
    while toaster.notification_active():
        time.sleep(0.001)


log_root = 'log.csv'


def write_log(label, argmax, theta, conf_before, conf_after, times):
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open('adv/' + log_root, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(
            [time_str, label, argmax, conf_before, conf_after, theta.phi, theta.l, theta.b, theta.w, theta.alpha,
             times])


def write_log_error(label):
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open('adv/' + log_root, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([time_str, label, 'error'])
