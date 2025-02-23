
from math import log
import numpy as np
import matplotlib.pyplot as plt

fh = open("data.txt", "r")
lines = fh.readlines()
fh.close()
temp = True

def f_err(U): # This basically calculates the errors in the ln(sigma) calculations. This is basically the height of the errorbar up and down from the measurement point.
	return 0.12 # The sum of dl, dI, dU and dA

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

# Get the errors for the Y values. This is actually constant in our case (0.12)

y_error = [f_err(U) for U in voltages] # Get the errors. Again this doesn't depend on voltage, but we pass the voltage anyway because the error could depend on the voltage in other cases.

# Calculate the virhesuorat

x_coords = [temp_inverse[0], temp_inverse[-1]]
y_coords_1 = [sigmat_val[0]+y_error[0], sigmat_val[-1]-y_error[0]]
y_coords_2 = [sigmat_val[0]-y_error[0], sigmat_val[-1]+y_error[0]]

# Now calculate the slopes of the error lines...

dy_dx_1 = (y_coords_1[1] - y_coords_1[0]) / (x_coords[1] - x_coords[0])
dy_dx_2 = (y_coords_2[1] - y_coords_2[0]) / (x_coords[1] - x_coords[0])

# Print out the slopes of the dashed lines

print("Virhesuora 1:en kulmakerroin: "+str(dy_dx_1))
print("Virhesuora 2:en kulmakerroin: "+str(dy_dx_2))

# Now calculate the differences between the actual slope and the slopes of the error lines

diff_k_1 = abs(slope - dy_dx_1)
diff_k_2 = abs(slope - dy_dx_2)

# Now the actual error is the average of these two:

err_k = (diff_k_1 + diff_k_2) / 2

# Print it out

print("Error in the slope of the graph: "+str(err_k))

# Calculate the error for E_g

err_E_g = 2*k_B*err_k

# Convert to eV

err_E_g_as_eV = err_E_g / eV

# Print it out

print("Error in the final value for E_g: "+str(err_E_g_as_eV))

# Plot the data and the fitted line

plt.errorbar(temp_inverse, sigmat_val, yerr=y_error, fmt='o', capsize=5, ecolor='red', elinewidth=1.0, label="Mittauspisteet virheiden kanssa")
plt.plot(temp_inverse, fitted_line, color="red", label="Sovitettu suora")
plt.plot(x_coords, y_coords_1, linestyle='--', color='gray', label='Virhesuora 1')
plt.plot(x_coords, y_coords_2, linestyle='--', color='gray', label='Virhesuora 2')
plt.xlabel("Lämpötilan käänteisluku 1/T (°K^(-1))")
plt.ylabel("Luonnollinen logaritmi johtavuudesta ln(σ) (ei yksikköä)")
plt.legend()

# Save the plot as vector graphics:

plt.savefig('plot.eps', format='eps', bbox_inches='tight')  # Save as EPS

plt.show()
