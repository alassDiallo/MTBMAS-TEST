import requests
#import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.tools.rdf2dot import rdf2dot
import sys
from systems import *

#pip install rdflib
g = Graph()
g.parse("ontoF.ttl", format="ttl")
#onto = get_ontology("ontology.ttl")

agent = "<http://mtbmas#RDCN_ServiceHeatingAgentManager>"
space = "<http://mtbmas#ground_north>"
service = "<http://mtbmas#heatingService>"
simulation = "<http://mtbmas#simRDCN>"
simModel = "<http://mtbmas#simModRDCN>"
# Définir les namespaces
mtbmas = Namespace("http://www.owl-ontologies.com/mtbmas#")
saref = Namespace("https://saref.etsi.org/core/v3.2.1/")
saref4bldg = Namespace("https://saref.etsi.org/saref4bldg/")

urlapi = "http://127.0.0.1:8000"
# response = requests.get(f"{urlapi}/donnees")
# print(response.json())"""
#sync_reasoner()

#retrieve the 
cq1 = """
            PREFIX mtbmas: <http://mtbmas#>
            PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
            SELECT ?agent
            WHERE {
                {?agent a mtbmas:ServiceHeatingAgentManager}
                UNION
                {?agent a mtbmas:ServiceCoolingAgentManager }
                UNION
                {?agent a mtbmas:ServiceLightingAgentManager }
                UNION
                {?agent a mtbmas:ServiceVentilationAgentManager }
                UNION
                {?agent a mtbmas:ServiceAirQualityAgentManager }
              
            }
            
            
        """

#CQ2 In which space of the building is a given agent located?
cq2 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?space WHERE {{
?space mtbmas:containsAgent ?agent .
FILTER(?agent = {agent})
}}""".format(agent=agent)

#print(cq2)

#CQ3 What service is offered by an agent?
cq3 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?service WHERE {{
?agent mtbmas:offersSpecificService ?service .
?service a mtbmas:Service .
FILTER(?agent = {agent})
}}""".format(agent=agent)

#CQ4 What devices are linked to an agent?
cq4 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?device ?agent WHERE {
{?agent a mtbmas:ServiceAgentManager }
UNION
{?agent a mtbmas:ServiceHeatingAgentManager}
UNION
{?agent a mtbmas:ServiceCoolingAgentManager }
UNION
{?agent a mtbmas:ServiceLightingAgentManager }
UNION
{?agent a mtbmas:ServiceVentilationAgentManager }
UNION
{?agent a mtbmas:ServiceAirQualityAgentManager }
?device a mtbmas:Device .
{?device mtbmas:isControledBy ?agent }
UNION
{?agent mtbmas:controlsDevice ?device}
}"""

#CQ5 What is the type of agents in a given space of the building?
cq5 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?agent WHERE {{
?space mtbmas:containsAgent ?agent .
FILTER(?space = {space})
}}""".format(space=space)
#?agent a ?ServiceAgentManager .
#CQ6 Who is the agent managing a given service (heating, ventilation, lighting, air quality) in a space of the building?
cq6 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?agent WHERE {{
?service a mtbmas:Service .
?agent mtbmas:offersSpecificService ?service .
FILTER(?service = {service})
}}""".format(service=service)

#CQ7 What simulations are associated with a specific agent?
cq7 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?simulation ?input_val ?weather WHERE {{
{{ ?agent a mtbmas:ServiceAgentManager }}
UNION
{{?agent a mtbmas:ServiceHeatingAgentManager}}
UNION
{{?agent a mtbmas:ServiceCoolingAgentManager }}
UNION
{{?agent a mtbmas:ServiceLightingAgentManager }}
UNION
{{?agent a mtbmas:ServiceVentilationAgentManager }}
UNION
{{?agent a mtbmas:ServiceAirQualityAgentManager }}
?simulation a mtbmas:Simulation .
?agent mtbmas:providesInputDataSimulation ?simulation .
?simulation mtbmas:input_val ?input_val .
?simulation mtbmas:weather ?weather .
FILTER(?agent = {agent})
}}""".format(agent=agent)

#CQ8 What simulation results is used by a specific agent?
cq8 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?result ?predictValue WHERE {{
{{ ?agent a mtbmas:ServiceAgentManager }}
UNION
{{?agent a mtbmas:ServiceHeatingAgentManager}}
UNION
{{?agent a mtbmas:ServiceCoolingAgentManager }}
UNION
{{?agent a mtbmas:ServiceLightingAgentManager }}
UNION
{{?agent a mtbmas:ServiceVentilationAgentManager }}
UNION
{{?agent a mtbmas:ServiceAirQualityAgentManager }}
?result a mtbmas:SimulationResult .
?result mtbmas:predictValue ?predictValue .
?agent mtbmas:useResult ?result .
FILTER(?agent = {agent})
}}""".format(agent=agent)

#CQ9 What are the results of a specific simulation?
cq9 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?result ?predictValue WHERE {{
?result a mtbmas:SimulationResult .
?simulation a mtbmas:Simulation .
?simulation mtbmas:hasResult ?result .
?result mtbmas:predictValue ?predictValue .
FILTER(?simulation = {simulation})
}}""".format(simulation=simulation)
#CQ10 What simulations are produced by a specific Space simulation model?
cq10 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?simulation ?input_val ?weather WHERE {{
?spaceSimulationModel a mtbmas:SpaceSimulationModel .
?simulation a mtbmas:Simulation .
?spaceSimulationModel mtbmas:producesSim ?simulation .
?simulation mtbmas:input_val ?input_val .
?simulation mtbmas:weather ?weather .
FILTER(?spaceSimulationModel = {simModel})
}}""".format(simModel=simModel)
#CQ11 Who occupies a space in the building?
cq11 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?tenant ?space WHERE {
{?space a mtbmas:Space}
UNION
{?space a mtbmas:Zone}
UNION
{?space a mtbmas:Floor}
UNION
{?space a mtbmas:Room}
?tenant a mtbmas:Tenant .
?tenant mtbmas:occupies ?space .
}"""

#CQ12 What spaces are available in the building?
cq12 = """
PREFIX mtbmas: <http://mtbmas#>
PREFIX saref4bldg: <https://saref.etsi.org/saref4bldg#>
SELECT ?space WHERE {
{?space a mtbmas:Space}
UNION
{?space a mtbmas:Zone}
UNION
{?space a mtbmas:Floor}
UNION
{?space a mtbmas:Room}
}"""


resultCq1 = g.query(cq1)
print("########################################## CQ1 ################################################" )
for a in resultCq1:
    print("#  ",a.agent.split("#")[1])
print("########################################## end CQ1 ################################################" )

resultCq2 = g.query(cq2)
print("########################################## CQ2 ################################################" )
for s in resultCq2:
    print("# the {} agent is located in the {}".format(agent.split("#")[1].replace(">",""), s.space.split("#")[1])," space")
print("########################################## end CQ2 ################################################" )


resultCq3 = g.query(cq3)
print("########################################## CQ3 ################################################" )
for service in resultCq3:
    print("#  ",service.service.split("#")[1])
print("########################################## end CQ3 ################################################" )

resultCq4 = g.query(cq4)
print("########################################## CQ4 ################################################" )
for r in resultCq4:
    print("#  ",r.agent.split("#")[1]," ", r.device.split("#")[1])
print("########################################## end CQ4 ################################################" )
resultCq5 = g.query(cq5)
print("########################################## CQ5 ################################################" )
print("#   agents contained in {} space".format(space))
for a in resultCq5:
    print("#  ",a.agent.split("#")[1])
print("########################################## end CQ5 ################################################" )

resultCq6 = g.query(cq6)
print("########################################## CQ6 ################################################" )
print("#  Liste of agents who offer a {} service in the building ".format(service.service.split("#")[1]))
for a in resultCq6:
    print("#  ",a.agent.split("#")[1])
print("########################################## end CQ6 ################################################" )


resultCq7 = g.query(cq7)
print("########################################## CQ7 ################################################" )
for sim in resultCq7:
    print("#  simulation: ",sim.simulation.split('#')[1]," input value: ",sim.input_val," weather: ",sim.weather)
print("########################################## end CQ7 ################################################" )

resultCq8 = g.query(cq8)
print("########################################## CQ8 ################################################" )
for r in resultCq8:
    print("#  simulation result: ",r.result.split("#")[1]," predict value : ",r.predictValue)
print("########################################## end CQ8 ################################################" )


resultCq9 = g.query(cq9)
print("########################################## CQ9 ################################################" )
for r in resultCq9:
     print("#  simulation result: ",r.result.split("#")[1]," predict value : ",r.predictValue)
print("########################################## end CQ9 ################################################" )

resultCq10 = g.query(cq10)
print("########################################## CQ10 ################################################" )
for sim in resultCq10:
    print("#  simulation: ",sim.simulation.split('#')[1]," input value: ",sim.input_val," weather: ",sim.weather)
print("########################################## end CQ10 ################################################" )

resultCq11 = g.query(cq11)
print("########################################## CQ11 ################################################" )
for tenant in resultCq11:
    print("#  ",tenant.tenant.split("#")[1]," occupies ",tenant.space.split("#")[1]," space")
print("########################################## end CQ11 ################################################" )

resultCq12 = g.query(cq12)
print("########################################## CQ12 ################################################" )
for space in resultCq12:
    print("#  ",space.space.split("#")[1])
print("########################################## end CQ12 ################################################" )
