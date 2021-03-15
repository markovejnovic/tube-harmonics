#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

tube_lengths = np.array([313, 296, 275, 255, 235, 215, 195, 175, 155, 135, 115, 95, 75]) * 1e-3
tube_length_err = 0.5 * 1e-3
tube_length_linspace = np.linspace(75e-3, 313e-3)
def tube_freq(l, n=1, v=343.00):
    return (2*n - 1)*v/(4*l)

harmonics1 = np.array([263.93, 279.08, 299.76, 323.66, 353.6, 379.46, 417.28, 463.01, 516.09, 579.79, 681.76, 804.82, 1010.84])
harmonics2 = np.array([791.94, 837.23, 400.41, 973.6, 1095.3, 1133.93, 1231.62, 1376.02, 1231.28, 1384.31, 2078.03, 2443.65, np.NaN])
harmonics3 = np.array([1321.57, 1413.22, 1504.67, 1627.58, 1755.71, 1909.43, 2096.49, 2335.92, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN])
harmonics4 = np.array([1863.69, 1976.29, 2124.29, np.NaN, 2467.44, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN])

finv1 = 1 / harmonics1
finv2 = 1 / harmonics2
finv3 = 1 / harmonics3
finv4 = 1 / harmonics4

# We have to cleanup NaN values
cond = np.isfinite(finv1) & np.isfinite(tube_lengths)
finv1 = finv1[cond]
tube_lengths1 = tube_lengths[cond]
cond = np.isfinite(finv2) & np.isfinite(tube_lengths)
finv2 = finv2[cond]
tube_lengths2 = tube_lengths[cond]
cond = np.isfinite(finv3) & np.isfinite(tube_lengths)
finv3 = finv3[cond]
tube_lengths3 = tube_lengths[cond]
cond = np.isfinite(finv4) & np.isfinite(tube_lengths)
finv4 = finv4[cond]
tube_lengths4 = tube_lengths[cond]

finv1fit, finv1fitcov = np.polyfit(tube_lengths1, finv1, 1, cov=True)
finv1fitf = np.poly1d(finv1fit)
finv2fit, finv2fitcov = np.polyfit(tube_lengths2, finv2, 1, cov=True)
finv2fitf = np.poly1d(finv2fit)
finv3fit, finv3fitcov = np.polyfit(tube_lengths3, finv3, 1, cov=True)
finv3fitf = np.poly1d(finv3fit)
finv4fit, finv4fitcov = np.polyfit(tube_lengths4, finv4, 1, cov=True)
finv4fitf = np.poly1d(finv4fit)

print(1)
print(finv1fit)
finv1fitu = np.sqrt(np.diag(finv1fitcov))
print(finv1fitu)

print(2)
print(finv2fit)
finv2fitu = np.sqrt(np.diag(finv2fitcov))
print(finv2fitu)

print(3)
print(finv3fit)
finv3fitu = np.sqrt(np.diag(finv3fitcov))
print(finv3fitu)

print(4)
print(finv4fit)
finv4fitu = np.sqrt(np.diag(finv4fitcov))
print(finv4fitu)

plt.errorbar(tube_lengths1, finv1, xerr=tube_length_err, fmt='kd', label='n=1')
plt.plot(tube_length_linspace, finv1fitf(tube_length_linspace), 'b--', linewidth=1)

plt.errorbar(tube_lengths2, finv2, xerr=tube_length_err, fmt='k^', label='n=2')
plt.plot(tube_length_linspace, finv2fitf(tube_length_linspace), 'r--', linewidth=1)

plt.errorbar(tube_lengths3, finv3, xerr=tube_length_err, fmt='kx', label='n=3')
plt.plot(tube_length_linspace, finv3fitf(tube_length_linspace), 'g--', linewidth=1)

plt.errorbar(tube_lengths4, finv4, xerr=tube_length_err, fmt='k+', label='n=4')
plt.plot(tube_length_linspace, finv4fitf(tube_length_linspace), 'm--', linewidth=1)

plt.legend()
plt.grid()
plt.xlabel('Length $[m]$')
plt.ylabel(r'Inverse Frequency $\frac{1}{f} [s]$')

tikzplotlib.clean_figure()
tikzplotlib.save('report/graphs/l-1f-rel.tex')

def nuf(k, n):
    return 4 / (k * (2*n - 1))
def nufu(k, delk, n):
    return nuf(k, n) * delk / k
nus = np.array([nuf(finv1fit[0], 1), nuf(finv2fit[0], 2), nuf(finv3fit[0], 3), nuf(finv4fit[0], 4)])
nusu = np.array([nufu(finv1fit[0], finv1fitu[0], 1), nufu(finv2fit[0], finv2fitu[0], 2), nufu(finv3fit[0], finv3fitu[0], 3), nufu(finv4fit[0], finv4fitu[0], 4)])
print(nus, nusu)
