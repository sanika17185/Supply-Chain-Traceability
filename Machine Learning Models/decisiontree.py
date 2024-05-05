import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
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
        
# Preprocessing 
X = data.drop('contaminated', axis=1)
y = data['contaminated']
newnf = X.select_dtypes(include=['object']).columns
newcf = X.select_dtypes(exclude=['object']).columns

preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ]), newnf),
        ('cat', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), newcf)
    ])

# Define the Decision Tree model
dt_model = DecisionTreeClassifier(random_state=42)

# Create a pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', dt_model)
])

# Split, train, and evaluate as before
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model_pipeline.fit(X_train, y_train)
y_pred = model_pipeline.predict(X_test)
report = classification_report(y_test, y_pred)
print(report)
