# Import necessary libraries
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data frame from csv
df = pd.read_csv('data\immunization.csv')

# Convert the 'ID' column to a numerical data type
df['ID'] = pd.to_numeric(df['ID'], errors='coerce')

# Fill any resulting NaNs with 0 and change the data type to int
df['ID'] = df['ID'].fillna(0).astype(int)

# Create a new incremental ID column
df['new_ID'] = range(1, len(df) + 1)

# Convert the 'MINORITY' column to int
df['MINORITY'] = df['MINORITY'].astype(int)

# Calculate the beta coefficients using the new_ID
model = smf.ols(formula='MINORITY ~ new_ID', data=df).fit()
beta_coefficients = model.params

# Print the beta coefficients
print(beta_coefficients)

# Plot a scatter graph using the new_ID
plt.figure(figsize=(10,6))
sns.scatterplot(x='new_ID', y='MINORITY', data=df)

# Get the x values for the line
x_values = np.array(df['new_ID'])

# Calculate the y values for the line
y_values = beta_coefficients.iloc[0] + beta_coefficients.iloc[1] * x_values  # changed here

# Plot the line
sns.lineplot(x=x_values, y=y_values, color='red')  # changed here

# Set plot title and labels
plt.title('Scatter plot with beta line')
plt.xlabel('New ID')
plt.ylabel('Minority')

# Display the plot
plt.show()