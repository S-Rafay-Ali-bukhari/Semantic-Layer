Semantic Layer Generator for FM Framework

This repository contains the proof-of-concept Python script (semantic_results_gen.py) used to demonstrate the L2 Semantic Layer of the proposed Neuro-Symbolic Facility Management Framework.

📌 Overview

The script simulates the "Semantic Lifting" process where heterogeneous data sources are ingested, normalized, and unified into a single Knowledge Graph. It specifically demonstrates:

Topological Ingestion: Creating spatial nodes (Building, Storey, Room) using the BOT ontology.

Asset Ingestion: Creating mechanical assets (VAVs, Sensors) using the Brick Schema.

Data Fusion: Linking assets to spaces and sensor streams to assets.

Reasoning: Executing a SPARQL query to find critical faults that cross-reference operational data (Temperature) with historical data (Maintenance Dates).

🛠️ Prerequisites

You need Python 3.x installed on your system.
The script relies on the following semantic web and data handling libraries:

rdflib: For creating the RDF Graph, managing namespaces, and running SPARQL queries.

pandas: For formatting the query results into a readable table.

📦 Installation

Open your terminal or command prompt and run the following command to install the dependencies:

pip install rdflib pandas


🚀 How to Run

Save the Python script as semantic_results_gen.py.

Navigate to the directory containing the file.

Run the script:

python semantic_results_gen.py


📄 Output Artifacts

When executed, the script generates two outputs:

Console Output (The Evidence):
A Pandas dataframe table printed to the terminal showing the result of the SPARQL query.

Use Case: Take a screenshot of this table for your "Results" slide.

Example Output:

   Room URI   Asset URI Temperature  Last Maint
0  Room_101     VAV_101      26.5°C  2023-01-15


knowledge_graph.ttl (The Graph File):
A Turtle syntax file containing the generated RDF triples.

Use Case: You can open this file in any text editor (Notepad, VS Code) or load it into a Graph Database (like GraphDB or Protégé) to visualize the structure.

