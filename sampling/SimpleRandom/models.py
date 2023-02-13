from django.db import models
import math

#confidence interval -> ci
#margin of error -> moe
#population size -> ps
#sample size -> ss

def zscorecalculator(ci):
    match ci:
        case 80:
            return 1.28
        case 85:
            return 1.44
        case 90:
            return 1.65
        case 95:
            return 1.96
        case 99:
            return 2.58

class SimpleRandom(models.Model):
    ps = models.FloatField()
    moe = models.FloatField()
    ci = models.FloatField()

    def calc(self):
        ps = self.ps
        moe = self.moe
        ci = self.ci
        z = zscorecalculator(ci)

        numerator = (z*z*0.5*0.5)/moe*moe
        denominator = 1 + (numerator/ps)
        s = numerator/denominator
        return math.ceil(s)

