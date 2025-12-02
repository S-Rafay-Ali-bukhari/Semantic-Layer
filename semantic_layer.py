import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, XSD
import pandas as pd

# 1. SETUP: Define Namespaces
BRICK = Namespace("https://brickschema.org/schema/Brick#")
BOT = Namespace("https://w3id.org/bot#")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
EX = Namespace("http://example.org/fm/")

g = Graph()
g.bind("brick", BRICK)
g.bind("bot", BOT)
g.bind("sosa", SOSA)
g.bind("ex", EX)

# 2. DATA GENERATION: Simulating the Ingestion Process
print("--- GENERATING KNOWLEDGE GRAPH ---")

# Create a Building and a Storey (from BOT/IFC)
building = EX["Building_A"]
level_1 = EX["Level_1"]
room_101 = EX["Room_101"]

g.add((building, RDF.type, BOT.Building))
g.add((level_1, RDF.type, BOT.Storey))
g.add((room_101, RDF.type, BOT.Space))
g.add((building, BOT.hasStorey, level_1))
g.add((level_1, BOT.hasSpace, room_101))

# Create Assets (from Brick/BMS)
vav_box = EX["VAV_101"]
temp_sensor = EX["Sensor_T_101"]

g.add((vav_box, RDF.type, BRICK.VAV))
g.add((temp_sensor, RDF.type, BRICK.Temperature_Sensor))

# 3. LINKING: The Semantic "Bridge"
# Connect the Mechanical Asset to the Spatial Room
g.add((vav_box, BRICK.feeds, room_101))
g.add((vav_box, BRICK.hasPoint, temp_sensor))

# Add Operational Data (Simulating IoT Stream)
g.add((temp_sensor, BRICK.hasValue, Literal(26.5, datatype=XSD.float))) # Too hot!
g.add((vav_box, EX.lastMaintenanceDate, Literal("2023-01-15", datatype=XSD.date)))

print(f"Graph Generated with {len(g)} triples.")

# 4. EXPORT: Save the Turtle file (Artifact 1)
# You can show this file snippet on your slide to prove 'Structure'
rdf_output = g.serialize(format="turtle")
print("\n--- ARTIFACT 1: TURTLE SNIPPET ---")
print(rdf_output[:500] + "...") # Printing first 500 chars

# 5. REASONING: The SPARQL Query (Artifact 2)
# "Find rooms fed by VAVs where Temp > 25 AND Maintenance was > 1 year ago"
query = """
PREFIX brick: <https://brickschema.org/schema/Brick#>
PREFIX bot: <https://w3id.org/bot#>
PREFIX ex: <http://example.org/fm/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema>

SELECT ?room ?asset ?temp ?date
WHERE {
    ?asset a brick:VAV .
    ?asset brick:feeds ?room .
    ?asset brick:hasPoint ?sensor .
    ?sensor a brick:Temperature_Sensor .
    ?sensor brick:hasValue ?temp .
    ?asset ex:lastMaintenanceDate ?date .
    
    FILTER(?temp > 24.0)
    FILTER(?date < "2024-01-01"^^xsd:date)
}
"""

print("\n--- ARTIFACT 2: SPARQL QUERY RESULTS ---")
qres = g.query(query)

results = []
for row in qres:
    results.append({
        "Room URI": row.room.split('/')[-1],
        "Asset URI": row.asset.split('/')[-1],
        "Temperature": f"{row.temp}°C",
        "Last Maint": row.date
    })

# Display as a clean table
df = pd.DataFrame(results)
print(df.to_string(index=False))

# Optional: Save to file
df.to_csv("sparql_results.csv", index=False)
g.serialize(destination="knowledge_graph.ttl", format="turtle")