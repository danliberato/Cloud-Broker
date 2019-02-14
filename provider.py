# Import socket module 
import socket 
import sys
import json
import csv
from classes.DecimalEncoder import DecimalEncoder

HOST = "localhost"
PORT = 8888
max_buffer_size = 5120
items = []

def Main(): 
	
	csv_file = sys.argv[1]  # receive provider file
	# Define the host and port
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	try:
		soc.connect((HOST, PORT))
	except Exception as err:
		print("Connection error: ", err)
		sys.exit()
	
	message = json.dumps({'type' : 'p'}) #presentation message
	soc.send(message.encode("utf8"))
	convert_csv_to_json_list(csv_file)
	message = json.dumps(items, cls=DecimalEncoder)
	soc.send(message.encode("utf8"))
	
	options()
	message = input('Selecione uma opcao > ')
	while True:
		if message != 'x':
			if message == 's':
				message = json.dumps(m)
			if message == 'u':
				soc.send(message.encode("utf8"))
				message = json.dumps(updateVM(),cls=DecimalEncoder)
				print(message)
			soc.send(message.encode("utf8"))
			data = soc.recv(max_buffer_size).decode("utf8")
			print('Received from the server :',data) 
			message = input(' > ') 
		else:
			soc.close()
			sys.exit()


def convert_csv_to_json_list(file):
	with open(file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			data = {}
			data['id'] = int(row['id (N)'])
			data['price'] = int(row['price (N)'])
			data['RAM'] = int(row['RAM (N)'])
			data['isAvaliable'] = int(row['isAvaliable (N)'])
			data['vCPUs'] = int(row['vCPUs (N)'])
			data['capStorage'] = int(row['capStorage (N)'])
			data['providerName'] = row['providerName (S)'],
			data['host'] = HOST
			items.append(data)
	return items

def updateVM():
	print('Describe the server:')
	vm = {
		"id": input('ID:'),
		"vCPUs": input('vCPUs:'),
		"RAM": input('RAM:'),
		"capStorage": input('capStorage:'),
		"price": input('Price:'),
		"isAvaliable": 1,
		"host": HOST,
		}
	return vm	

def options():
	print('[ Options ]')
	print('r : remove VMs')
	print('u : update a VM (by id)')
	print('x : Exit')

if __name__ == '__main__': 
	Main()
