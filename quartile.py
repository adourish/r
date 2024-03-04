import pandas as pd
import numpy as np
import statsmodels.api as sm

# Provided data
np.random.seed(42)
health_centers = ['Health Center {}'.format(i) for i in range(1, 41)]
percent_uninsured = np.random.uniform(0, 40, 40)
percent_minority = np.random.uniform(0, 50, 40)
percent_homeless = np.random.uniform(0, 10, 40)
percent_agricultural_worker = np.random.uniform(0, 15, 40)
ehr_status = np.random.choice(['non-EHR', 'EHR'], 40)
outcome = 1
data = {
    'Health Center': health_centers,
    'Percent Uninsured': percent_uninsured,
    'Percent Minority': percent_minority,
    'Percent Homeless': percent_homeless,
    'Percent Agricultural Worker': percent_agricultural_worker,
    'Outcome': outcome
}

df = pd.DataFrame(data)
print(df)

# Add eCQM columns to the DataFrame
eCQMs = ['eCQM {}'.format(i) for i in range(1, 10)]
for eCQM in eCQMs:
    df[eCQM] = np.random.uniform(0, 100, 40)

# Define the independent variables (predictors) and the dependent variable
X = df[['Percent Uninsured', 'Percent Minority', 'Percent Homeless', 'Percent Agricultural Worker'] + eCQMs]
y = df['Outcome']


# Proceed with model fitting

# Add a constant to the independent variables
X = sm.add_constant(X)

# Fit the multiple linear regression model
model = sm.OLS(y, X).fit()

# Get the beta coefficients
betas = model.params

print(betas)