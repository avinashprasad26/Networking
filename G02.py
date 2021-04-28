from socket import *
import sys
import getopt
port = 25
def main(argv):
	clients = socket(AF_INET,SOCK_STREAM)
	try:
		opts,args = getopt.getopt(argv,"f:d:i:s:",["mailfrom=","rcptto=","files=","srvipadd="])
		for opt,arg in opts:
			if opt in ('-h'):
				print('assign.py -f <from email address> -d <recipent-1 email address> .... -i <file1> .... -s <server ip address>')
				sys.exit()
			elif opt in ('-f'):
				mailfrom=arg
			elif opt in ('-d'):
				rcptto=""
				rcptto=arg[0:]	
				x=rcptto.split(",")
			elif opt in ('-i'):
				files=''
				files=arg[0:]
				a=files.split(",")
			elif opt in ('-s'):
				srvipadd=''
				srvipadd = arg
	except getopt.GetoptError:
		print(' given error arguments in command ')
	
	
	clients.connect((srvipadd,port))
	recv = clients.recv(1024)
	recv=recv.decode('utf-8')
	print("\nMessage after connection request: "+ recv+'\n')
	if recv[:3] != '220':
		print('\n 220 reply not recieved from server.\n')
		
	
	print('---------------------------------------------------------------')
		
	ehlocommand = 'EHLO ksit.ac.in\r\n'
	clients.send(ehlocommand.encode())
	recv2 = clients.recv(1024)
	recv2=recv2.decode()
	print("\nMessage after EHLO command: "+ recv2+'\n')
	if recv2[:3] != '250':
		print('\n 250 reply not recieved from server.\n')
		
	print('---------------------------------------------------------------')
		
	m_from = "MAIL FROM: "+ mailfrom +"\r\n"
	clients.send(m_from.encode())
	recv3 = clients.recv(1024)
	recv3=recv3.decode()
	print("\nMessage after MAIL FROM command: "+ recv3+'\n')
	
	print('---------------------------------------------------------------')
	
	ii=0
	for ii in x:
		rcptto1=ii
		r_to = "RCPT TO: "+ rcptto1 +"\r\n"
		clients.send(r_to.encode())
		recv4 = clients.recv(1024)
		recv4=recv4.decode()
		print("\nMessage after RCPT TO command: "+ recv4+'\n')


	print('---------------------------------------------------------------')
	
	data='DATA\r\n'
	clients.send(data.encode())
	recv5=clients.recv(1024)
	recv5=recv5.decode()
	print("After DATA command: "+recv5)
	
	jj=0
	for jj in a:
		files1=jj
		f = open(files1)
		print('******************************************************************************\n\n')
		for line in f:
    			print(line)
    			clients.send(line.encode())
	dot='\r\n.\r\n'
	clients.send(dot.encode())
	recv_msg= clients.recv(1024)
	print("Response after sending message body: "+recv_msg.decode())
	
	print('---------------------------------------------------------------')
	
	
	quit="QUIT\r\n"
	clients.send(quit.encode())
	recv6=clients.recv(1024)
	print(recv6.decode())	
	clients.close()
	
	print('---------------------------------------------------------------')
main(sys.argv[1:])


