import pandas as pd
import numpy as np

def calculate_slope(X, Y):
    """
    Returns:
        float: Absolute value of the slope
    """
    SlopeDF = pd.DataFrame({
        'X': X,
        'Y': Y
    })
    SlopeA = np.polyfit(SlopeDF['X'], SlopeDF['Y'], 1)
    Slope = abs(SlopeA[0])
    return Slope