import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
# pip install pandas
# pip install statsmodels
# python quartile-ecqm.py
# Load data
df = pd.read_csv('data/ecqm-data.csv')
df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)
df['newID'] = range(1, len(df) + 1)
df['MINORITY'] = df['MINORITY'].astype(int)

# Define performance measures and control variables
performance_measures = [
    'prenatal', 'lbw', 'immunization', 'childbmi', 'adultbmi',
    'tobacco', 'coloncscreen', 'paptest', 'asthmatreat',
    'sealant', 'lipid', 'aspirin', 'hivlink',
    'depressionsc', 'htn', 'hba1c8', 'hba1c9'
]
controlvars = ['MINORITY', 'UNINSURED', 'HOMELESS', 'MIGRANT']

# Initialize results storage
results = {}

# Loop through each performance measure
for measure in performance_measures:
    formula = f'{measure} ~ ' + ' + '.join(controlvars) + ' + newID'  
    model = smf.ols(formula=formula, data=df).fit()
    
    # Set non-significant coefficients to zero
    params = model.params.copy()
    pvalues = model.pvalues
    params[pvalues > 0.05] = 0
    
    # Predict and calculate residuals
    prediction = params.get('Intercept', 0)
    for var in controlvars + ['newID']:  
        prediction += params.get(var, 0) * df[var]
    df[f'pred_{measure}'] = prediction
    residuals = df[measure] - df[f'pred_{measure}']
    
    # Assign quartiles
    if measure == 'lbw':
        df[f'rank_{measure}'] = pd.qcut(residuals, 4, labels=[4, 3, 2, 1])
    else:
        df[f'rank_{measure}'] = pd.qcut(residuals, 4, labels=[1, 2, 3, 4])
    
    # Store model parameters
    results[measure] = params

# Print coefficients
for measure, params in results.items():
    print(f'Coefficients for {measure}:')
    print(params)
    print()

# Print rankings
# rankcols = [f'rank{m}' for m in performance_measures]
# print(df[rankcols].head())

# Save the updated dataframe
df.to_csv('data/ecqm-data-out.csv', index=False)