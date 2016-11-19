
import sys, time,string,struct,re
import select
import socket
import PCA_GenLib
import PCA_Parser
import PCA_XMLParser
import PCA_DLL
import PCA_ServerSocket

	
###############################################################################
## 
###############################################################################
class Acceptor(PCA_ServerSocket.Acceptor):        
	
	ConnectionLoginState = {}   
	bind_recever_socket_fd = {}   
        MSG_ID = 0
        MSG_Queue = None
	def __init__(self,XMLCFG):		
		try:	
			Msg = "ResponseHandler Init ..."
			PCA_GenLib.WriteLog(Msg,9)
			
			
			PCA_ServerSocket.Acceptor.__init__(self,XMLCFG)			
			
			
			
			Tag = "Handler"
			dll_file_name = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
			Msg = "dll_file_name=<%s> " % dll_file_name
                	PCA_GenLib.WriteLog(Msg,0)
			
			Script_File = PCA_DLL.DLL(dll_file_name)	
					
			factory_function="Parser"
			factory_component = Script_File.symbol(factory_function)
			self.parser = factory_component()
			
			
			factory_function="Handler"
			factory_component = Script_File.symbol(factory_function)
			self.handler  = factory_component()			
			self.parser.setContentHandler(self.handler )
				
				
				
			Msg = "ResponseHandler Ok ..."
			PCA_GenLib.WriteLog(Msg,9)
		except:
			Msg = "ResponseHandler error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                	PCA_GenLib.WriteLog(Msg,0)
                	raise
        ########################################################		
	## Wating Client Connection by non-blocking I/O       ##
	##						      ##
	########################################################
	def dispatcher(self,TimeOut,MSG_Queue):
		try:
  			Msg = "dispatcher server starting"
			PCA_GenLib.WriteLog(Msg,1)
                        self.MSG_Queue = MSG_Queue
			
			while 1:
				Msg = "listener dispatcher server loop"
				PCA_GenLib.WriteLog(Msg,9)

				readables, writeables, exceptions = select.select(self.ReadSet, [], [],TimeOut)    				
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

								for  address in self.bind_recever_socket_fd.keys():
                					
 									if id(self.bind_recever_socket_fd[address]) == id(self.SocketConnection):
 										del self.bind_recever_socket_fd[address] 									
 										Msg = "delete from self.bind_recever_socket_fd address=<%s>,socket_fd=<%s>" % (address,id(self.bind_recever_socket_fd[address]))
 										PCA_GenLib.WriteLog(Msg,1)
 					
                					else:
                						###################################
                						### Got Data Message From Client ##
                						###################################
                						
                						self.handle_event(self.SocketConnection,ClientMessage)
                						
                				except socket.error:
                					Msg = "dispatcher socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
                					PCA_GenLib.WriteLog(Msg,0)	
                					
                					self.SocketConnection.close()                   # close here and remv from
                					self.ReadSet.remove(self.SocketConnection)      # del list else reselected 
                					self.WriteSet.remove(self.SocketConnection)     # del list else reselected 
                					del self.ConnectionLoginState[id(self.SocketConnection)]
                			
                			
                					for  address in self.bind_recever_socket_fd.keys():
                					
 								if id(self.bind_recever_socket_fd[address]) == id(self.SocketConnection):
 									del self.bind_recever_socket_fd[address] 									
 									Msg = "delete from self.bind_recever_socket_fd address=<%s>,socket_fd=<%s>" % (address,id(self.bind_recever_socket_fd[address]))
 									PCA_GenLib.WriteLog(Msg,1)
 									
                					break	
            					
            		Msg = "Normal end of dispatcher"
			PCA_GenLib.WriteLog(Msg,0)	
            		
           	except :
			Msg = "dispatcher error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)	
			
			Msg = "Error end of dispatcher"
			PCA_GenLib.WriteLog(Msg,0)
            		time.sleep(2)		
			raise
   
   

	########################################################		
	## 						      ##
	##						      ##
	########################################################					
	def handle_event(self,SocketEventFD,ClientMessage):
		try:
			Msg = "handle_event Init"
			PCA_GenLib.WriteLog(Msg,9)
			
			
			#######################################################
			##	 Read Request from Client 		    ###
			##						    ###
			#######################################################
				
			Message = self.readDataFromSocket(SocketEventFD,Length=3,TimeOut = 10.0,ReadAttempts = 1)
			if Message == None:
				Msg = "read SMPP length error "
				PCA_GenLib.WriteLog(Msg,1)
			    
			
				raise socket.error
			
			Msg = "DEBUG recv from Client =\n%s" % PCA_GenLib.HexDump(Message)
			PCA_GenLib.WriteLog(Msg,2)
			
			MessageLength = ClientMessage+Message
			MessageLength_Int = struct.unpack("!i",MessageLength)[0]
			
			
			if (MessageLength_Int != 0) and (MessageLength_Int < 4096):	
			
				Message = self.readDataFromSocket(SocketEventFD,Length=MessageLength_Int-4,TimeOut = 5.0,ReadAttempts = 1)
				if Message == None:
					Msg = "read SMPP PDU error "
					PCA_GenLib.WriteLog(Msg,1)
					raise socket.error				
				
			else:
				Msg = "read SMPP PDU error incorrect length = <%s> " % MessageLength_Int
				PCA_GenLib.WriteLog(Msg,1)
				raise socket.error	
				
				
			
			SocketMessage = MessageLength + Message
			
			Msg = "recv from Client =\n%s" % PCA_GenLib.HexDump(SocketMessage)
			PCA_GenLib.WriteLog(Msg,2)
				
				
			self.parser.parse(SocketMessage)
			response_message = self.handler.getHandlerResponse()	
			ServerID = self.handler.getTID()
			DebugStr = self.handler.getDebugStr()
			
			
			if response_message != None:
			
				command_id = self.handler.getCOMMAND_ID()
 					
 				Msg = "command_id=<%s>" % command_id
 				PCA_GenLib.WriteLog(Msg,2)  
 				
 				if command_id[-4:] == "resp":
 					Msg = "SMPP response message no need to ack command_id=<%s>" % command_id
 					PCA_GenLib.WriteLog(Msg,1)  
 				
 				
 				else:
 				
					Msg = "send back to Client =\n%s" % PCA_GenLib.HexDump(response_message)
					PCA_GenLib.WriteLog(Msg,2)
				
					result = self.sendDataToSocket(SocketEventFD,response_message,TimeOut=2,WriteAttempts=3)
				
					if result != None:
						Msg = "send back to client ok : data recv from client : ServerID=<%s>,%s" % (ServerID,DebugStr)
 						PCA_GenLib.WriteLog(Msg,1)  
 										
 					
 						if command_id == "bind_receiver":
 							Msg = "save socket fd and address range"
 							PCA_GenLib.WriteLog(Msg,2)  
 						
 							address_range = self.handler.getADDRESS_RANGE()
 					
 							Msg = "save to bind_recever_socket_fd address_range=<%s>,SocketEventFD=<%s>" % (address_range,id(SocketEventFD))
 							PCA_GenLib.WriteLog(Msg,1)  
 						
 							self.bind_recever_socket_fd[address_range] = SocketEventFD
 					
 						elif command_id == "submit_sm":
 							
 							Msg = "send submit_sm back to client , insert msg to MSG_Queue"
 							PCA_GenLib.WriteLog(Msg,1)  
                                                        self.MSG_ID = self.MSG_ID + 1
                                                        submit_time = int(time.time())
			                                (originator,recipient,sms_text) = self.handler.get_msg_for_mt()
                                                        sms_text_ascii = sms_text
                                                        import smspdu 
                                                        #(dsc,gsm_sms_text) = smspdu.pdu.smpp_to_sms_data_coding(0,sms_text)
                                                        gsm_sms_text = smspdu.pdu.pack7bit(sms_text)[1]
 							Msg = "sms_text=<%s> , GSM format = <%s>" % (PCA_GenLib.HexDump(sms_text),PCA_GenLib.HexDump(gsm_sms_text))
 							PCA_GenLib.WriteLog(Msg,1)  

                                                        msg_to_queue = {}
                                                        msg_to_queue['id'] = self.MSG_ID
                                                        msg_to_queue['originator'] = originator
                                                        msg_to_queue['recipient'] = recipient
                                                        msg_to_queue['submit_time'] = submit_time
                                                        msg_to_queue['next_retry_time'] = submit_time
                                                        msg_to_queue['sms_text'] = gsm_sms_text
                                                        msg_to_queue['sms_text_ascii'] = sms_text_ascii
                                                        msg_to_queue['originator_imsi'] = None
                                                        msg_to_queue['recipient_imsi'] = None
                                                        msg_to_queue['NNN'] = None

                                                        Msg = "QUEUE : msg to queue =<%s>, <%s>,<%s>,<%s>" % (self.MSG_ID,originator,recipient,sms_text_ascii)
                                                        PCA_GenLib.WriteLog(Msg,1)
                                                        self.MSG_Queue.put(msg_to_queue)


 							Msg = "check destination address"
 							PCA_GenLib.WriteLog(Msg,2)  
 							
 							dest_address = self.handler.getDEST_ADDR()
 							#Msg = "dest_address = <%s>" % dest_address
 							#PCA_GenLib.WriteLog(Msg,1)  
 							
 							#Msg = "check if need to send delivery sm to exists bind_recever connection"
 							#PCA_GenLib.WriteLog(Msg,1)
 							found_receiver = 0
 							for  address in self.bind_recever_socket_fd.keys():
 				
 								if re.compile(address).search(dest_address) != None:
				
 									Msg = "found a receiver to delivery dest_addr = <%s>,receiver bind address=<%s>,socket_fd=<%s>" % (dest_address,address,id(self.bind_recever_socket_fd[address]))
 									PCA_GenLib.WriteLog(Msg,1)
 									found_receiver = 1
 									break
 						
 							if found_receiver == 1:
 								
 								Msg = "delivery sm to receiver socket_fd = <%s>" % id(self.bind_recever_socket_fd[address])
 								PCA_GenLib.WriteLog(Msg,1)
 								# convert submit_sm to delivery_sm
 								delivery_sm = SocketMessage[0:7]+chr(0x05)+SocketMessage[8:]
								
								try:
									Msg = "send delivery sm to receiver =\n%s" % PCA_GenLib.HexDump(delivery_sm)
									PCA_GenLib.WriteLog(Msg,1)
			
									result = self.sendDataToSocket(self.bind_recever_socket_fd[address],delivery_sm,TimeOut=2,WriteAttempts=3)
								
									if result != None:
								
										Msg = "send delivery sm to receiver ok : socket_fd = <%s>" % id(self.bind_recever_socket_fd[address])
 										PCA_GenLib.WriteLog(Msg,1)  
 								
									else:
										Msg = "send delivery sm to receiver failure : socket_fd = <%s>" % id(self.bind_recever_socket_fd[address])
 										PCA_GenLib.WriteLog(Msg,1)  
								except socket.error:
									Msg = "send delivery sm to receiver socket failure ignore : socket_fd = <%s>" % id(self.bind_recever_socket_fd[address])
 									PCA_GenLib.WriteLog(Msg,1)  
								
 							
			
 					else:
 						Msg = "send back to client failure timeout : data recv from client : ServerID=<%s>,%s " % (ServerID,DebugStr)
 						PCA_GenLib.WriteLog(Msg,1)  
 						
			
			else:
				Msg = "Error unknow response"
				PCA_GenLib.WriteLog(Msg,1)	
			
			
			Msg = "handle_event OK"
			PCA_GenLib.WriteLog(Msg,9)			
		except:
			Msg = "handle_event Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise	    
