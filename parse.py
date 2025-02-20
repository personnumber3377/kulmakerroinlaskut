

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

temp_inverse = [1.0 / (x+257.0) for x in temps]

sigmat_val = [math.log(f(x)) for x in voltages]
s = [f(x) for x in voltages]
#print(sigmat)
sigmat = [str(x) for x in sigmat_val]

print("\n".join(sigmat), end="")






coefficients = np.polyfit(temp_inverse, sigmat_val, 1)

# Print the slope and intercept
slope, intercept = coefficients
print(f"Slope: {slope}, Intercept: {intercept}")

# Create a fitted line using the coefficients
fitted_line = np.polyval(coefficients, temp_inverse)



# Plot the data and the fitted line

plt.scatter(temp_inverse, sigmat_val, label="Data points")
plt.plot(temp_inverse, fitted_line, color="red", label="Fitted line")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()



'''


coefficients = np.polyfit(sigmat_val, temp_inverse, 1)

# Print the slope and intercept
slope, intercept = coefficients
print(f"Slope: {slope}, Intercept: {intercept}")

# Create a fitted line using the coefficients
fitted_line = np.polyval(coefficients, sigmat_val)



# Plot the data and the fitted line
plt.scatter(sigmat_val, temp_inverse, label="Data points")
plt.plot(sigmat_val, fitted_line, color="red", label="Fitted line")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()


'''




# Now add a linear fit.


'''
136.36363636363635
129.0322580645161
109.09090909090908
85.7142857142857
70.58823529411764
61.538461538461526
54.05405405405404
47.99999999999999
42.85714285714285
33.89830508474576
29.999999999999993
26.315789473684205
23.999999999999996
20.68965517241379
18.749999999999996
16.43835616438356
15.384615384615381
15.384615384615381
12.12121212121212
11.009174311926603
9.756097560975608
8.888888888888888
8.21917808219178
7.692307692307691
7.058823529411764
6.779661016949151
6.31578947368421
4.838709677419354
4.0677966101694905


'''