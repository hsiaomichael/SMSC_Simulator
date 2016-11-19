
import sys, time,string
from select import select
import socket
import PCA_GenLib
import PCA_XMLParser

class Acceptor:
	ConnectionLoginState = {}
	########################################################		
	## Init Socket Environment and set socket option      ##
	##						      ##
	########################################################
	def __init__(self,XMLCFG):		
		try:	
			Msg = "Acceptor Init ..."
			PCA_GenLib.WriteLog(Msg,9)
			self.XMLCFG = XMLCFG
			
			Tag = "LISTEN_HOST"
			host = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
			self.host = host
			
			
			Tag = "LISTEN_PORT"
			port = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
			self.port = string.atoi(port)
			
			Msg = "Listen Host=<%s>,Port=<%s>" % (self.host,self.port)
			PCA_GenLib.WriteLog(Msg,1)
			
			
			
			
			# make main sockets for accepting new client requests
			self.SocketConnectionPool, self.ReadSet, self.WriteSet = [], [], []
	
			
			
			SocketDescriptor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # make a TCP/IP spocket object
	    			
	    		# you should add "setsockopt(level, optname, value)"  here
	    		#  /* Set SO_REUSEADDR socket option to allow socket reuse */
	    		SocketDescriptor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    		Msg = "setsockopt..SO_REUSEADDR."
			PCA_GenLib.WriteLog(Msg,9)
				
	    		#   /* Set SO_KEEPALIVE socket option */
      			SocketDescriptor.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE,1 )
      			Msg = "setsockopt...SO_KEEPALIVE"
			PCA_GenLib.WriteLog(Msg,9)
				
      			#   /* Set SO_LINGER socket option setup whether discard data on close */
    			#SocketDescriptor.setsockopt( socket.SOL_SOCKET, socket.SO_LINGER, 1)
    			#Msg = "setsockopt..SO_LINGER."
			#PCA_GenLib.WriteLog(Msg,9) 
			
			
	    			
	    		if self.host == "any":
    				SocketDescriptor.bind(("", self.port))      
    			else:
    				SocketDescriptor.bind((self.host, self.port))     
    			
    			
    			
	    		SocketDescriptor.listen(5)                         # listen, allow 5 pending connects
	    		
	    		Msg = "setsockopt..Listen.SocketFD=<%s>" % (SocketDescriptor)
			PCA_GenLib.WriteLog(Msg,9)
 
    			self.SocketConnectionPool.append(SocketDescriptor) # add to main list to identify
	    		
	    		self.ReadSet.append(SocketDescriptor)              # add to select inputs list 
	    		self.WriteSet.append(SocketDescriptor)             # add to select output list 
	    			
    			
    			
    			Msg = "Acceptor Initial Ok "
			PCA_GenLib.WriteLog(Msg,9)	
		except :
			Msg = "Acceptor Initial error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise

	########################################################		
	## Wating Client Connection by non-blocking I/O       ##
	##						      ##
	########################################################
	def dispatcher(self,TimeOut=0.2):
		try:
  			
  			Msg = "dispatcher server starting"
			PCA_GenLib.WriteLog(Msg,9)
			RecvDataCNT = 0
			
			while 1:
				
    				readables, writeables, exceptions = select(self.ReadSet, [], [],TimeOut) 
    				for self.SocketConnection in readables:
    					##################################
    				        #### for ready input sockets #####
    				        ##################################
        				if self.SocketConnection in self.SocketConnectionPool:  
        					####################################
	            				## port socket: accept new client ##
	            				## accept should not block	  ##
	            				####################################
	        	    			connection, address = self.SocketConnection.accept()
        	    				Msg = 'Dispatcher New Connection <%s> from :%s' % (id(connection),address)   # connection is a new socket        	    				
            					PCA_GenLib.WriteLog(Msg,1)   
            					         				
            					self.ReadSet.append(connection)   # add to select list, wait
            					self.WriteSet.append(connection)  # add to select list, wait
            					
            					self.ConnectionLoginState[id(connection)] = 'N'
                				Msg = "Set ConnectionLoginState <%s> to N " % id(connection)
                				PCA_GenLib.WriteLog(Msg,1)
            					
        				else:
            					try:
            						RecvDataCNT = RecvDataCNT + 1
            						ClientMessage = self.SocketConnection.recv(1)
            					
            						if not ClientMessage:
            							Msg = "Client Close Connection ..id=%s" % id(self.SocketConnection)
                						PCA_GenLib.WriteLog(Msg,1)
                						self.SocketConnection.close()                   # close here and remv from
                						self.ReadSet.remove(self.SocketConnection)      # del list else reselected 
                						self.WriteSet.remove(self.SocketConnection)     # del list else reselected 
                						
                						Msg = "Del ConnectionLoginState <%s>" % id(self.SocketConnection)
                						PCA_GenLib.WriteLog(Msg,1)
								del self.ConnectionLoginState[id(self.SocketConnection)]

                					else:
                						###################################
                						### Got Data Message From Client ##
                						###################################
                						#Message = self.readDataFromSocket(ClientMessage)
                						self.handle_event(self.SocketConnection,ClientMessage)
                						
                				except socket.error:
                					Msg = "dispatcher socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                					PCA_GenLib.WriteLog(Msg,0)	
                					
                					self.SocketConnection.close()                   # close here and remv from
                					self.ReadSet.remove(self.SocketConnection)      # del list else reselected 
                					self.WriteSet.remove(self.SocketConnection)     # del list else reselected 
                					del self.ConnectionLoginState[id(self.SocketConnection)]
                					
                					break
                		
                		if len(readables) == 0 or RecvDataCNT >= 10:
                			RecvDataCNT = 0
					self.handle_timeout()                					
		except :
			Msg = "dispatcher error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)			
			raise
	
	
	########################################################		
	## 						      ##
	##						      ##
	########################################################					
	def handle_event(self,SocketEventFD,ClientMessage):
		try:
			Msg = "handle_event Init"
			PCA_GenLib.WriteLog(Msg,9)
			
			
			
			Msg = "handle_event OK"
			PCA_GenLib.WriteLog(Msg,9)			
		except:
			Msg = "handle_event Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise	
	
	########################################################		
	## 						      ##
	##						      ##
	########################################################					
	def handle_timeout(self):
		try:
			Msg = "handle_timeout Init"
			PCA_GenLib.WriteLog(Msg,9)
			
			
			
			Msg = "handle_timeout OK"
			PCA_GenLib.WriteLog(Msg,9)			
		except:
			Msg = "handle_timeout Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise	
				
	########################################################		
	## Non-Block I/O Read Socket Data		      ##
	##						      ##
	########################################################
	def readDataFromSocket(self,SocketEventFD,Length=1024,TimeOut = 3.0,ReadAttempts = 1):
		try:
			Msg = "readDataFromSocket "
			PCA_GenLib.WriteLog(Msg,9)
			
			for i in range(ReadAttempts):    				  		
    				readables, writeables, exceptions = select(self.ReadSet, [], [],TimeOut)
    				for SocketFD in readables:
        				if (SocketFD == SocketEventFD):
						Message = SocketFD.recv(Length)  
						if len(Message) == 0:
							Msg = "Client Close Connection "
							PCA_GenLib.WriteLog(Msg,1)
							raise socket.error,Msg
            					
						Msg = "ReadDataFromSocket OK"
						PCA_GenLib.WriteLog(Msg,9)
						return Message
				
			
			Msg = "readDataFromSocket retry time out !"
			PCA_GenLib.WriteLog(Msg,6)
			return None
		except socket.error:
			raise socket.error
			
		except:
			Msg = "readDataFromSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
			
	########################################################		
	## Non-Block I/O Send Socket Data		      ##
	##						      ##
	########################################################
	def sendDataToSocket(self,SocketEventFD,Message,TimeOut=5.0,WriteAttempts=1):
		try:
			Msg = "sendDataToSocket "
			PCA_GenLib.WriteLog(Msg,9)	
	
			for i in range(WriteAttempts):    				  		
    				readables, writeables, exceptions = select([], self.WriteSet, [],TimeOut)
    				for SocketFD in writeables:
        				if (SocketFD == SocketEventFD):
        					SocketFD.send(Message)
            					Msg = "sendDataToSocket OK"
						PCA_GenLib.WriteLog(Msg,9)
            					return 1
        				
			Msg = "sendDataToSocket error ,Time out !"
			PCA_GenLib.WriteLog(Msg,1)
			return None
		except:
			Msg = "sendDataToSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
	########################################################		
	## Close Socket					      ##
	##						      ##
	########################################################					
	def close(self):
		try:
			Msg = "close Acceptor Socket Init"
			PCA_GenLib.WriteLog(Msg,9)
			
			##self.SocketConnection.shutdown(1)		# Send FIN , further sends are disallowed
			
			#self.SocketConnection.close()	
			
			for SocketFD in self.ReadSet:
				try:
					Msg = "close Socket id=<%s>" % id(SocketFD)
					PCA_GenLib.WriteLog(Msg,1)
        				SocketFD.close()
        			except:
        				Msg = "close Socket error id=<%s>" % id(SocketFD)
					PCA_GenLib.WriteLog(Msg,1)
        				
            			
			Msg = "close Acceptor Socket OK"
			PCA_GenLib.WriteLog(Msg,9)
			
		except socket.error:
			Msg = "close socket error"
			PCA_GenLib.WriteLog(Msg,0)
		except AttributeError:
			self.SocketConnectionPool[0].close()		
		except:
			Msg = "close Acceptor Socket Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise	
			
			
