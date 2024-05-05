import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

from neo4j import GraphDatabase
import pandas as pd

# Replace these variables with your actual credentials and URI
uri = "neo4j+s://28967cf5.databases.neo4j.io"
username = "neo4j"
password = "2bhqnK5X1iQwVIWEJs7Hrw4vDlPBKJvU0cReyIyARvc"

# Initialize the Neo4j connection
driver = GraphDatabase.driver(uri, auth=(username, password))

cypher_query = """MATCH (n) 
OPTIONAL MATCH (n)-[r]->(m) 
RETURN n, r, m"""

with driver.session() as session:
    result = session.run(cypher_query)

    # Extract properties and relationships from nodes
    data = []
    for record in result:
        node = record['n']
        properties = dict(node.items())
        relationship = record['r']
        if relationship is not None:
            relationship_properties = dict(relationship.items())
        else:
            relationship_properties = {}
        data.append({**properties, **relationship_properties})


# Optional: Remove duplicates to clean up the data
data.drop_duplicates(inplace=True)

# Separate features and target
X = data.drop('contaminated', axis=1)
y = data['contaminated']

# Identify numeric and categorical columns
newnf = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
newcf = X.select_dtypes (include=['object']).columns.tolist()

# Preprocessing for numerical data: imputation + scaling
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Preprocessing for categorical data: imputation + one-hot encoding
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, newnf),
        ('cat', categorical_transformer, newcf)
    ])

# Create a preprocessing and modeling pipeline with Decision Tree
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', DecisionTreeClassifier(random_state=42))
])

# Perform k-fold cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

# Fit the model
model.fit(X, y)

# Predict using the model
y_pred = model.predict(X)

# Output results
print("Cross-validated accuracy scores:", scores)
print("Mean cross-validated accuracy score: {:.2f}".format(scores.mean()))
print("Classification Report:\n", classification_report(y,y_pred))
