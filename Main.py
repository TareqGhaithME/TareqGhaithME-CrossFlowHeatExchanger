import numpy as np
import pandas as pd
from SlopeFunc import calculate_slope
import matplotlib.pyplot as plt


#loading experiment data
data = pd.read_excel("Data/Edata.xlsx", sheet_name = "Sheet1")

###Constants
Patm = 9000 #pa
Tair = 20 #C
m = 0.1093 #kg
Cp = 380 #J/kg.oC
A1 = 0.00404 #m2
d = 0.01242 #m
density = 1.225 #kg/m3
mew = 0.00001806 #N.s/m2 
Ka = 0.0256 #W/m.K
#

H1m = pd.DataFrame({'H1':[0.02, 0.0085, 0.002]})
###


###calculations
Results = pd.DataFrame(
    {
        "log(T-Ta 100%)": np.log10(data['Te (100%)'] - Tair),
        "log(T-Ta 70%)":  np.log10(data['Te (70%)'] - Tair),
        "log(T-Ta 40%)":  np.log10(data['Te (40%)'] - Tair),
    }
)
V1= pd.DataFrame({'V1': 237.7 * (np.sqrt((H1m['H1']*(Tair+273))/Patm))})
V = pd.DataFrame({'V': V1['V1']*2})


######h calculation of Slope log(T-Ta) vs Time
S100 = calculate_slope(data['Time'], Results['log(T-Ta 100%)'])
S70 = calculate_slope(data['Time'], Results['log(T-Ta 70%)'])
S40 = calculate_slope(data['Time'], Results['log(T-Ta 40%)'])
Sdf = pd.DataFrame({ 'Slope': (S100, S70, S40)
    })
######

###h,Re,Nu
h = pd.DataFrame(
    {
     'h': (2.3026 * (m * Cp)/A1) * Sdf['Slope']}
      )
Re = pd.DataFrame({
    'Re': (V['V']*d*density)/mew
    })
Nu = pd.DataFrame({
    'Nu': (h['h'] * d) / Ka
    })
###

#resultsofCalculations
CResults = pd.DataFrame(
    {
     'Throttle Opens': ['100%', '70%', '40%'],
     'H1': H1m['H1'],
     'V1': V1['V1'],
     'V': V['V'],
     'h': h['h'],
     'Re':Re['Re'],
     'Nu':Nu['Nu']
    }
)

#Visualization

plt.plot(data['Time'], Results['log(T-Ta 100%)'], label='log(T-Ta 100%)', color='blue', linestyle='-', marker='o')
plt.plot(data['Time'], Results['log(T-Ta 70%)'], label='log(T-Ta 70%)', color='red', linestyle='--', marker='s')
plt.plot(data['Time'], Results['log(T-Ta 40%)'], label='log(T-Ta 40%)', color='green', linestyle=':', marker='^')


plt.xlabel("Time")
plt.ylabel("log(T-Ta)")
plt.title("Time vs. log(T-Ta)")
plt.legend()
plt.grid(True)  # Add grid


#ExportingResults
plt.savefig('Graphs/Time vs. log(T-Ta).png', dpi=300, bbox_inches='tight')
Results.to_excel("Results/log(T-Ta).xlsx", index=False)
CResults.to_excel("Results/CResults.xlsx", index=False)
