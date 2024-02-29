import statsmodels.api as sm
import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(123)

# Create a dataset with 40 people
data = pd.DataFrame({
    'person_id': range(1, 41),
    'BMI': np.random.normal(25, 3, 40) # Generate random BMI values
})

# Assign high BMI values to a few people
high_bmi_people = np.random.choice(range(1, 41), 5, replace=False)
data.loc[data['person_id'].isin(high_bmi_people), 'BMI'] = np.random.normal(30, 3, 5)

# Add a constant term for the intercept
data['constant'] = 1

# Perform linear regression
model = sm.OLS(data['BMI'], data[['constant']])
results = model.fit()

# Get the beta coefficient
beta = results.params['constant']


# Print the dataset
print(data)
print("Beta coefficient for BMI:", beta)