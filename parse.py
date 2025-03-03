
# These next two functions are for printing a table which is easily copy-pasteable to latex. These are not necessary for the calculations

def read_file_as_string(fn: str) -> str:
	fh = open(fn, "r")
	out = fh.read()
	fh.close()
	return out

template_start = read_file_as_string("template_start.txt")
template_end = read_file_as_string("template_end.txt")

def create_table(x,y):
	# This creates the table string which you can paste to the report
	# 143.0 & 0.088 \\
	out = template_start + "\n"
	for x_val, y_val in zip(x,y):
		x_val = round(x_val, 5)
		y_val = round(y_val, 5)
		out += f"{str(x_val)} & {str(y_val)} \\\\" + "\n"
	return out + template_end


fh = open("data.txt", "r")
lines = fh.readlines()
fh.close()
temp = True


def f(U):
	poikkipinta_ala = 0.001*0.01 # in meters**2 == 1mm * 10mm
	virta = 0.006 # in amps
	l = 0.02 # in meters
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
	temp = not temp

#print(temps)
#print(voltages)

sigmat = [f(x) for x in voltages]
#print(sigmat)
# sigmat = [str(x).replace(".", ",") for x in sigmat]

#print("\n".join(sigmat), end="")

import math

import numpy as np
import matplotlib.pyplot as plt



print("Temperatures: "+str(temps))
print("Voltages: "+str(voltages))


temp_inverse = [1.0 / (x+257.0) for x in temps]
sigmat_val = [math.log(f(x)) for x in voltages] # This is basically ln(sigma) where sigma is the result of the function
s = [f(x) for x in voltages]
sigmat = [str(x) for x in sigmat_val] # This is a list of the sigma values meaning conductivity.
print("Here is the scaled table: ")
print(create_table(temp_inverse, sigmat_val))
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
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()