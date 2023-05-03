from opcua import Client

# Connect to OPC-UA Server
url = "opc.tcp://localhost:4840"
client = Client(url)
client.connect()
print(f"Connected to OPC-UA Server at {url}")

# Get node for 'thomas' variable and read its value
node = client.get_node("ns=1;s=Variable.thomas")
print(node)
#value = node.get_value()

#print(f"Current value of 'thomas': {value}")

# Disconnect from server
client.disconnect()
