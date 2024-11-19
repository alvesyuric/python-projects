# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Chart setting and display function
def plot_extraction_ph(df):
    plt.figure(figsize=(8, 6))
    plot_styles = {'marker': 'o', 'linestyle': '-'}
    
    plt.plot(df['Month'], df['Extraction'], color='blue', label='Extraction', **plot_styles)
    plt.plot(df['Month'], df['PH'], color='red', label='PH', **plot_styles)
    
    plt.title('Extraction and PH Values')
    plt.xlabel('Month (2023)')
    plt.ylabel('Values')
    plt.legend()
    plt.show()

# Statistical Operations Function
def calculate_statistics(df):
    # Calculating Pearson correlation
    correlation = df['Extraction'].corr(df['PH'])
    print("Pearson coefficient: ", round(correlation, 4))
    
    # Linear regression for PH and Extraction
    slope, intercept, r_value, p_value, std_err = linregress(df['PH'], df['Extraction'])
    print(f"Line equation: Extraction = {slope:.4f} * PH + {intercept:.4f}")
    
    return slope, intercept

# Main Code
# Data setup
data = {
    'Month': ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
    'Extraction': [76.5, 77.1, 76.1, 76.5, 77.2, 75.4, 76.3, 76.5, 77.2, 75.4, 77.3, 76.5],
    'PH': [78.2, 79.1, 77.6, 78.7, 78.3, 76.1, 77.3, 78.0, 77.0, 76.3, 79.5, 77.5]
}

# Creating DataFrame
extraction_ph = pd.DataFrame(data)
print(extraction_ph)

# Plotting the data
plot_extraction_ph(extraction_ph)

# Calculating statistics
slope, intercept = calculate_statistics(extraction_ph)

# Function to predict Extraction given a PH value
def predict_extraction(ph_value):
    return slope * ph_value + intercept

# Request PH value and predict Extraction
try:
    ph_value = float(input("Enter a value for PH: "))
    predicted_extraction = predict_extraction(ph_value)
    print(f"For PH = {ph_value}, the predicted Extraction value is: {predicted_extraction:.1f}")
except ValueError:
    print("Please enter a valid numeric value for PH.")

# Calculation of effective production
daily_production = 1100
production_forecast = int(input("Enter the production forecast in days: "))
effective_production = int(round(daily_production * production_forecast * predicted_extraction / 100, 0))
print("For a production of " + str(production_forecast) + " days, we will obtain a volume of " + str(effective_production) + " tons.")
print()