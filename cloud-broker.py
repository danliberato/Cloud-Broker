import socket 
from threading import Thread
import threading 
import boto3
import os
import sys
import json
import ast
from boto3.dynamodb.conditions import Key, Attr
from classes.DecimalEncoder import DecimalEncoder
from classes.ProviderTable import ProviderTable

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Provider')
client = boto3.client('dynamodb')
provider = boto3.client
option = ''
address = {}
print_lock = threading.Lock()
max_buffer_size = 5120
vmInUse = []

#	comunica com o banco na AWS e selecina a Vm com menor preco
def selectCheaperVM(vm):
	
	if table.table_status == 'ACTIVE':
	
		response = table.scan(
			Select='ALL_ATTRIBUTES',
			Limit=50,
			FilterExpression=Attr('vCPUs').gte(int(vm['vCPUs'])) & Attr('RAM').gte(int(vm['RAM'])) & Attr('capStorage').gte(int(vm['capStorage']))
		)
		
		item = {}
		print('count =', response['Count'])
		if response['Count'] > 0: #check if search returned at least 1 register
			items = response["Items"]
			items.sort(key=sortVms)
			item = items[0]
		
		return json.dumps(item,indent=4, cls=DecimalEncoder)

def sortVms(vmList):
	return vmList['price']
	
# thread client
def clientThread(connection, ip, port):
	is_active = True

	while is_active:
		#try:
		rcv_in = receive_input(connection, max_buffer_size)
		if (not rcv_in) or (rcv_in == 'x'): #		QUIT
			print('Client is requesting to quit')
			is_active = False
			connection.close()
			print("Connection " + ip + ":" + port + " closed")
			is_active = False
			break
		elif rcv_in == 'r': #						Realease VM
			answer = 'VM deallocated!'
			vm = json.loads(receive_input(connection, max_buffer_size))
			changeStatusVM(vm, 1)
		else:	#									Select cheap VM
			print('Matching VM for '+ ip + ':' + port)
			answer = selectCheaperVM(json.loads(rcv_in))
			print(answer)
			
		connection.send(str(answer).encode('utf8'))
		#except:
			#print("Client " + ip + ":" + port + " suddenly disconnected!")
			#is_active = False

# provider thread
def providerThread(connection, ip, port):
	is_active = True
	providerName = ''
	
	items = json.loads(receive_input(connection, max_buffer_size)) 
	
	with table.batch_writer() as batch: # receives all items from provider and insert into the table
		for item in items:
			providerName = item['providerName']
			batch.put_item(Item=item)

	while True:
		m = receive_input(connection, max_buffer_size)
		if m == 'x':
			print(providerName+ ' wants to disconnect')
			removeProviderVMs(providerName)
			break
		elif m == 'r':
			print('Removing VMs from ' +providerName+ ' ['+ ip + ":" + port+']')
			removeProviderVMs(providerName)
			m = 'All VMs were removed!'
		elif m == 'u':
			vm = json.loads(receive_input(connection, max_buffer_size))
			print('Updating VM '+vm['id']+' from ' + ip + ":" + port)
			updateVM(vm)
			m = 'VM was updated!'

		connection.send(m.encode('utf8'))

#	remove all VMs from provider
def removeProviderVMs(providerName):
	response = table.scan(
		FilterExpression=Attr('providerName').eq(providerName)
	)
	for item in response['Items']:
		table.delete_item(Key={'id' : int(item['id'])})
	
		
#	update VM from provider
def updateVM(vm):
	table.update_item(
		Key={'id':int(vm['id'])},
		UpdateExpression="SET RAM = :ram, isAvaliable = :is, price = :price, capStorage = :st, vCPUs = :cpus",
		ExpressionAttributeValues={
            ':ram': int(vm['RAM']),
            ':is': int(vm['isAvaliable']),
            ':price': int(vm['price']),
            ':st': int(vm['capStorage']),
            ':cpus': int(vm['vCPUs'])
            }
	)

def changeStatusVM(vm, flag):
	table.update_item(
		Key={"id":int(vm['id'])},
		UpdateExpression="SET isAvaliable = :is",
		ExpressionAttributeValues={
            ":is": flag
            }
	)


def receive_input(connection, max_buffer_size):
	client_input = connection.recv(max_buffer_size)
	client_input_size = sys.getsizeof(client_input)

	if client_input_size > max_buffer_size:
		print("The input size is greater than expected {}".format(client_input_size))

	result = client_input.decode("utf8").rstrip()  # decode and strip end of line

	return result

def receiveProviderData(m):
	print(m)

#	MAIN
def Main(): 
	host = "localhost"
	port = 8888         # arbitrary non-privileged port
	
	try:
		response = client.describe_table(TableName='Provider')
	except client.exceptions.ResourceNotFoundException:
		table = ProviderTable.createTable(client)
	
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
	print("Socket created at ", host, ':', port)

	try:
		soc.bind((host, port))
	except:
		print("Bind failed. Error : " + str(sys.exc_info()))
		sys.exit()

	soc.listen(5)       # queue up to 5 requests
	print("Socket now listening")

	# infinite loop- do not reset for every requests
	while True:
		connection, address = soc.accept()
		ip, port = str(address[0]), str(address[1])
		print("Connected with " + ip + ":" + port)
		m = json.loads(receive_input(connection, max_buffer_size))

		try:
			if m['type'] == 'p':
				Thread(target=providerThread, args=(connection, ip, port)).start()
			elif m['type'] == 'c':
				Thread(target=clientThread, args=(connection, ip, port)).start()
			else:
				print('Client or Provider connection not found!')
		except:
			print("Thread did not start.")
			traceback.print_exc()

	soc.close()

if __name__ == '__main__': 
	Main() 
