from opcua import Client

url = "opc.tcp://192.168.0.155:4840/"
client = Client(url)
client.connect()

testinteger_node = client.get_node("ns=2;i=2")
#attributes = testinteger_node.get_value()

print("Available attributes for TestInteger node:",testinteger_node.get_display_name())
#for attr in attributes:
#    print(attr)

client.disconnect()
