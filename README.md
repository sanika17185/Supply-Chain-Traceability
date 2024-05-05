# Supply-Chain-Traceability
The U.S Food and Drug Administration (FDA) is the primary regulatory authority overseeing food safety and its purpose is to protect public health and maintain an approach to addressing foodborne outbreaks. The FDA holds the responsibility for safeguarding food safety within the United States, employing a range of strategies to manage outbreaks effectively. Through the utilization of systems such as FORS, they conduct thorough investigations to ascertain the origins of contamination, swiftly implementing measures such as recalls or inspections to mitigate associated risks. Additionally, the FDA prioritizes preventative actions by enforcing rigorous standards and promoting cooperation with the food industry to ensure adherence to regulations. This proactive stance, combined with collaboration between agencies, highlights their dedication to upholding the integrity of the food supply chain.

In conjunction with the Food and Drug Administration's (FDA) existing system Foodborne Outbreaks Response and Surveillance Network (FORS), the regulatory landscape is further fortified by the FSMA Final Rule Requirements for Additional Traceability Records for Certain Foods, thereby guaranteeing traceability across the supply chain. This regulation along with FDA existing systems establish protocols ensuring traceability both forward and backward within the food supply chain. The primary purpose behind these requirements is to prepare for and respond effectively in the event of a foodborne outbreak, underscoring the FDA's commitment to enhancing traceability measures for the protection of public health.

The presence of contaminated food presents a significant hazard, often resulting in illness. The occurrence of multiple illnesses stemming from the consumption of the same tainted food constitutes an outbreak. Statistics reveal that approximately one in six individuals falls victim to illness in such outbreaks, leading to an estimated 3,000 deaths annually. Our project endeavors to enhance public health by closely monitoring supply chain data associated with these outbreaks.

# Neo4J 
To work with Neo4j, follow these steps:

1. Set up Neo4j Instance: Begin by creating a Neo4j instance in Neo4j Aura. This instance will be used to create nodes and relationships.
2. Store CSV Files: Store your CSV files containing the data in a cloud storage service such as AWS or Azure.
3. Create Nodes: Define nodes for each stage of your supply chain process. For example, nodes could include harvesting, receiving, cooling, initial packaging, first land-based packaging, transformation, and shipping.
4. Establish Relationships: Create relationships between these nodes based on the properties of the relationship required for your supply chain model.
5. Establish Data Connection: Use a Python package to connect to your Neo4j server and retrieve the newly created dataset. Provide the necessary credentials for authentication.
6. Perform Analysis: Utilize visualization tools and perform machine learning modeling to gain insights into the established supply chain connections and optimize your supply chain process.

For sample code: see Neo4j_cypher.txt file 

