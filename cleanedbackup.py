
from math import log
import numpy as np
import matplotlib.pyplot as plt

fh = open("data.txt", "r")
lines = fh.readlines()
fh.close()
temp = True

def f(U): # This is the function which calculates the conductivity from the voltage assuming other variables remain constant.
	poikkipinta_ala = 0.001*0.01 # in meters**2 == 1mm * 10mm
	virta = 0.006 # in amps
	l = 0.020 # in meters
	return (l/(poikkipinta_ala)*virta/(U))

temps = []
voltages = []
for line in lines:
	if len(line) < 2:
		continue
	if temp:
		temps.append(float(line))
	else:
		voltages.append(float(line))
	temp = not temp # The temperatures and voltages are on alternating lines in the text file.

temp_inverse = [1.0 / (x+257.0) for x in temps]
sigmat_val = [log(f(x)) for x in voltages] # This is basically ln(sigma) where sigma is the result of the function. The log function is imported from the math library
s = [f(x) for x in voltages]
sigmat = [str(x) for x in sigmat_val] # This is a list of the sigma values meaning conductivity.
coefficients = np.polyfit(temp_inverse, sigmat_val, 1)
# Print the slope and intercept
slope, intercept = coefficients
print(f"Slope: {slope}, Intercept: {intercept}")
# Create a fitted line using the coefficients
fitted_line = np.polyval(coefficients, temp_inverse)
k_B = 1.380649*(10**(-23)) # Boltzmanns constant
# Calculate E_g...
E_g = -2*k_B*slope
eV = 1.60217663*(10**(-19)) # Electron volt in joules
E_g_as_electron_volts = E_g/(eV)
print("Value for E_g: "+str(E_g))
print("Value for E_g as electron volts: "+str(E_g_as_electron_volts))
# Plot the data and the fitted line

plt.scatter(temp_inverse, sigmat_val, label="Data points")
plt.plot(temp_inverse, fitted_line, color="red", label="Fitted line")
plt.xlabel("Lämpötilan käänteisluku 1/T (C^(-1))")
plt.ylabel("Luonnollinen logaritmi johtavuudesta ln(σ) ()")
plt.legend()
plt.show()