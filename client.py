# Import socket module 
import socket 
import sys
import json
from classes.DecimalEncoder import DecimalEncoder

VMNOTFOUND = "\tNo VM allocated was found!"
max_buffer_size = 5120
vm = {}
connectedTo = 'c' # [c] cloudBroker | [p] provider

def Main(): 
	# Define the host and port
	host = "localhost"
	port = 8888
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		soc.connect((host, port))
		message = json.dumps({"type" : 'c'}) #presentation message
		soc.send(message.encode("utf8"))
	except Exception as err:
		print("Connection error: ", err)
		sys.exit()
		
	print('[ Options ]')
	options()

	opt = ''
	while opt != 'x':
		message = ''
		opt = input('Select an option\n>')
		if opt.lower() != 'x': # client wants to disconnect
			try:
				if opt == 's': 		#client wants a VM
					message = json.dumps(mountVM())
					soc.send(message.encode("utf8"))
					vm = json.loads(soc.recv(max_buffer_size).decode("utf8"))
					message = 'Best VM:\n'+ formatVM(vm) + '\n'
					if(input('Do you accept this VM? (you will be redirect to this Provider) ') == 'Y'):
						message = json.dumps({"redirect": "Y"})
						consumesVM(json.loads(soc.recv(max_buffer_size).decode("utf8")))
						
				elif opt == 'r': 	#client wants get rid of VM
					print('VM = ',vm)
					message = opt
					soc.send(message.encode("utf8"))
					message = json.dumps(vm)
					soc.send(message.encode("utf8"))
					message = soc.recv(max_buffer_size).decode("utf8")
				elif opt == 'p': 	#client wants get rid of VM
						message = formatVM(vm)
				else:				#default
					print('Please select an option...')
					options()
			except UnboundLocalError as error:
				message = VMNOTFOUND
			print(message)
		else:
			soc.close()
			sys.exit()
			
def consumesVM(ap):
	connectedTo = 'p'
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		soc.connect((ap, port))
	except Exception as err:
		print("Connection error: ", err)
		
	while True:
		opt

# mounts client demand
def mountVM():
	print('Describe the server:')
	vcpus = input('vCPUs:')
	ram = input('RAM:')
	storage = input('Storage:')
	vm = {
		"vCPUs": int(vcpus),
		"RAM": int(ram),
		"capStorage": int(storage),
		"isAvaliable": 1,
		}
	return vm

def formatVM(vm):
	return ("----- VM -----"+
		"\n\t-vCPUs: " + str(vm['vCPUs'])+
		"\n\t-RAM: " + str(vm['RAM'])+"GB"+
		"\n\t-Storage: " + str(vm['capStorage'])+"GB"+
		"\n\t-Provider: " + str(vm['providerName'])+
		"\n\t-Price: U$ " + str(vm['price']))

def options():
	print('  p : Print current VM configuration')
	print('  r : Deallocate resources')
	print('  s : Select cheaper VM')
	print('  x : Exit')

if __name__ == '__main__': 
	Main()
