# Import necessary libraries
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('data\immunization.csv')
df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
df['ID'] = df['ID'].fillna(0).astype(int)
df['new_ID'] = range(1, len(df) + 1)
df['MINORITY'] = df['MINORITY'].astype(int)
model = smf.ols(formula='MINORITY ~ new_ID', data=df).fit()
beta_coefficients = model.params
print(beta_coefficients)
plt.figure(figsize=(10,6))
sns.scatterplot(x='new_ID', y='MINORITY', data=df)
x_values = np.array(df['new_ID'])
y_values = beta_coefficients.iloc[0] + beta_coefficients.iloc[1] * x_values  # changed here
sns.lineplot(x=x_values, y=y_values, color='red')  # changed here
plt.title('Scatter plot with beta line')
plt.xlabel('New ID')
plt.ylabel('Minority')
quartiles = df['ID'].quantile([0.25, 0.5, 0.75]).values
quartile_names = ['25th', '50th', '75th']
df['quartile'] = pd.cut(df['ID'], bins=np.append(quartiles, df['ID'].max()), labels=quartile_names, include_lowest=True)
print(df[['ID', 'MINORITY', 'quartile']])
plt.show()