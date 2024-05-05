import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('C:/Users/shwet/FoodProject/balanced_output.csv')

# Convert 'cteDate' to datetime format for time series analysis
data['cteDate'] = pd.to_datetime(data['cteDate'])

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Time series plot of contamination events over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='cteDate', y='contaminated', estimator='mean', ci=None)
plt.title('Trend of Contamination Over Time')
plt.xlabel('Date')
plt.ylabel('Average Contamination Status')
plt.show()

# Histogram for comparison of Quantity by contamination status
plt.figure(figsize=(10, 6))
sns.histplot(data[data['contaminated'] == 1]['quantity'], color='red', bins=50, kde=True, label='Contaminated')
sns.histplot(data[data['contaminated'] == 0]['quantity'], color='blue', bins=50, kde=True, label='Not Contaminated')
plt.title('Comparison of Quantity Distribution by Contamination Status')
plt.xlabel('Quantity')
plt.ylabel('Frequency')
plt.legend()
plt.show()


#Bar graph for count of contamination by units of measure
plt.figure(figsize=(10, 6))
sns.countplot(x='unitOfMeasure', hue='contaminated', data=data, palette={0: 'lightgreen', 1: 'darkred'})
plt.title('Count of Contaminated Items by Unit of Measure')
plt.xlabel('Unit of Measure')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Contaminated')
plt.show()

# Histogram of the contamination status
plt.figure(figsize=(8, 6))
sns.countplot(x='contaminated', data=data)
plt.title('Distribution of Contamination Status')
plt.xlabel('Contaminated (1 = Yes, 0 = No)')
plt.ylabel('Count')
plt.show()

# Boxplot of quantity by contamination status
plt.figure(figsize=(10, 6))
sns.boxplot(x='contaminated', y='quantity', data=data)
plt.title('Quantity Distribution by Contamination Status')
plt.xlabel('Contaminated (1 = Yes, 0 = No)')
plt.ylabel('Quantity')
plt.yscale('log')  # Using logarithmic scale for better visualization of wide range values
plt.show()

# Scatter plot for quantity and quantity received with contamination
plt.figure(figsize=(10, 6))
# Create a scatter plot
scatter = sns.scatterplot(x='quantity', y='quantityReceived', hue='contaminated', data=data, style='contaminated', palette={0: 'green', 1: 'red'})

plt.title('Correlation of Quantity and Quantity Received with Contamination')
plt.xlabel('Quantity')
plt.ylabel('Quantity Received')
# Handle the legend: explicitly defining the labels and colors
handles, labels = scatter.get_legend_handles_labels()
# Update the labels as necessary
plt.legend(handles=handles, labels=['Not Contaminated', 'Contaminated'], title='Contamination status')
plt.show()


# Bar graph showing contamination over various commodities
if data['commodity'].dtype == 'object' and pd.api.types.is_numeric_dtype(data['contaminated']):
    # Drop rows with missing values
    data.dropna(subset=['commodity', 'contaminated'], inplace=True)

    # Calculate the mean of 'contaminated' for each 'commodity'
    contamination_means = data.groupby('commodity')['contaminated'].mean()

    # Get the top 10 commodities with the highest mean contamination
    top_contaminated = contamination_means.nlargest(40)

    # Create a horizontal bar chart
    plt.figure(figsize=(10, 8))
    top_contaminated.plot(kind='barh', color='orange', edgecolor='black')
    plt.title('Commodities by Contamination')
    plt.xlabel('Contamination Level')
    plt.ylabel('Commodity')
    plt.gca().invert_yaxis()  # Invert the y-axis to show the highest value on top
    plt.tight_layout()  # Adjust layout to fit labels
    plt.show()
else:
    print("Please ensure that 'commodity' is a string and 'contaminated' is numeric.")