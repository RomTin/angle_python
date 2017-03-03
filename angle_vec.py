import numpy as np
import itertools as itt
from random import random
from sys import float_info

DIGITS = 3
ACCURACY = 0.001
UP_MAX = 30

class AngleInfo(object):

    def __init__(self, information):
        # 0 <= spin <= 360
        # 0 <= up <= UP_MAX
        # -1 <= sin, cos <= 1
        if len(information) == 2:
            # initialize with angles
            spin = round(information[0] % 360, DIGITS)
            up = round(information[1], DIGITS)
            #print "\tangle - spin:%f, up:%f" % (spin, up)
            if spin < 0 or 360 < spin or up < 0 or UP_MAX < up:
                # invalid angles
                up = None
                spin = None
        elif len(information) == 3:
            # initialized with trigon. function
            sin_s = information[0]
            cos_s = information[1]
            sin_u = information[2]
            #print "\ttrigo - ss:%f, cs:%f, su:%f" % (sin_s, cos_s, sin_u)
            if reduce(
                    lambda acc, item:
                    acc & (-1 <= item and item <= 1),
                    [sin_s, cos_s, sin_u],
                    True):
                # denormalization
                sin_u_org = sin_u * (np.sin(np.radians(UP_MAX)) / 1.0)
                up = np.rad2deg(np.arcsin(sin_u_org))
                spin = AngleInfo.calculateSpinAngle(sin_s, cos_s)
            else:
                # invalid trigon. func values
                up = None
                spin = None
        if spin != float_info.max:
            self.spin = round(spin, DIGITS)
            self.up = round(up, DIGITS)
        else:
            self.spin = None
            self.up = None

    def getAngles(self):
        return (self.spin, self.up)

    def getVectors(self):
        if self.spin is None or self.up is None:
            return (None, None, None)
        else:
            return (np.sin(np.radians(self.spin)),
                np.cos(np.radians(self.spin)),
                np.sin(np.radians(self.up)) / np.sin(np.radians(UP_MAX)))

    @staticmethod
    def calculateSpinAngle(sin_s, cos_s):

        spin_fsin = np.rad2deg(np.arcsin(sin_s))
        if spin_fsin < 0:
            spin_fsin = spin_fsin + 360

        spin_fcos = np.rad2deg(np.arccos(cos_s))
        if spin_fcos < 0:
            spin_focs = spin_fcos + 360
        
        angles_fsin = set([spin_fsin % 360, (540 - spin_fsin) % 360])
        angles_fcos = set([spin_fcos % 360, (360 - spin_fcos) % 360])
        angles = list(itt.product(angles_fsin, angles_fcos))
        res = None
        for i in angles:
            if abs(i[0] - i[1]) < ACCURACY:
                res = (i[0] + i[1]) / 2.0
        return (res if res is not None else float_info.max)

    @staticmethod
    def getRandomVector():
        spin = random() * 360
        up = random() * 30
        return (np.sin(np.radians(spin)), np.cos(np.radians(spin)), np.sin(np.radians(up)) / np.sin(np.radians(UP_MAX)))

def main():
    s = 100
    u = 100
    for i in range(s):
        for j in range(u):
            a = AngleInfo(AngleInfo.getRandomVector())
            b = AngleInfo(a.getVectors())
            print a.getAngles(), b.getAngles(), a.getVectors(), b.getVectors()
            if not a.getAngles() == b.getAngles() or not a.getVectors() == b.getVectors():
                print "check failed at %d %d" % (i, j)

if __name__ == '__main__':
    main()
