

import sys,string,struct,time
import PCA_GenLib
import PCA_Parser
import PCA_XMLParser
import PCA_SMPPParser
import PCA_SMPP_Parameter_Tag

reload(PCA_SMPPParser)                    

##############################################################################
###    Message Handler   	
##############################################################################
class Handler(PCA_Parser.ContentHandler):	
	
	bind_transmitter_resp_pdu = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x02)
	
	DebugStr = "na"
	
	TID = 'na'
	Message = None
	
 	def __init__(self):
		PCA_Parser.ContentHandler.__init__(self)
		self.Message = None
		
	def startDocument(self):
		self.sequence_number = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x00)
		self.IsApplicationMessage = 0
		self.Operation = chr(0x00)
		self.ServiceType = None
	       
		self.command_status = struct.pack('!i',0)
		self.command_length = struct.pack('!i',16)
		self.command_id = self.bind_transmitter_resp_pdu
		self.address_range = 'undef'
		self.request_command_id = 'undef'
		self.dest_address = 'undef'
		self.source_address = 'undef'
		self.sms_text = 'undef'
		
	
	def startElement(self, name, attrs):
		try:
			Msg = "startElement init"
			PCA_GenLib.WriteLog(Msg,9)
			
			self.MessageName = name						
		
			if name == "sequence_number":
				self.sequence_number = attrs
			
			if name == "command_id":
				self.command_id = chr(0x80) + attrs[1:4]
			
			Msg = "startElement OK"
			PCA_GenLib.WriteLog(Msg,9)        	
		except:
 			Msg = "startElement Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
	
	def characters(self, content):
	
		if self.MessageName == "command_id":
			self.request_command_id = content
		if self.MessageName == "address_range":
			self.address_range = content
		if self.MessageName == "dest_address":
			self.dest_address = content
		if self.MessageName == "source_address":
			self.source_address = content
		if self.MessageName == "sms_text":
			self.sms_text = content
        	
	def endDocument(self,DebugStr,TID,SOURCD_ID,response_message):
        	try:
        		self.TID = TID
        		self.DebugStr = DebugStr
                	
                	if response_message == None:
                	
                		self.Message = self.command_length + self.command_id + self.command_status + self.sequence_number
			
                	else:
                		message = self.command_id + self.command_status + self.sequence_number + response_message
                		
                		self.command_length = struct.pack("!i",len(message)+4)
                		
                		self.Message = self.command_length + message
				
        		
        	except:
        		Msg = "startElement Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
	

	def getHandlerResponse(self):	
		try:
			Msg = "getHandlerResponse Init "
			PCA_GenLib.WriteLog(Msg,9)
			
			Msg = "getHandlerResponse OK"
			PCA_GenLib.WriteLog(Msg,9)
			
			return self.Message
			
		except:
			Msg = "getHandlerResponse  error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise								
	def getTID(self):	
		try:
			Msg = "getTID Init "
			PCA_GenLib.WriteLog(Msg,9)
			
			Msg = "getTID OK"
			PCA_GenLib.WriteLog(Msg,9)
			
			return self.TID
			
		except:
			Msg = "getTID  error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise								
							
	def getDebugStr(self):	
		try:
			Msg = "getDebugStr Init "
			PCA_GenLib.WriteLog(Msg,9)
			
			
			
			Msg = "getDebugStr OK"
			PCA_GenLib.WriteLog(Msg,9)
			
			return self.DebugStr
			
		except:
			Msg = "getDebugStr  error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise								
			
	
	def getCOMMAND_ID(self):	
		return self.request_command_id	

	def getADDRESS_RANGE(self):	
		return self.address_range	
	
	def getDEST_ADDR(self):	
		return self.dest_address	
		

	def get_msg_for_mt(self):	
		return (self.source_address,self.dest_address,self.sms_text)
	

						
#########################################################################
# 
#
#########################################################################
class Parser(PCA_SMPPParser.Parser):
	
	
	def __init__(self):
		try:
			Msg = "parser __init__"
			PCA_GenLib.WriteLog(Msg,9)
		
			PCA_SMPPParser.Parser.__init__(self)
  			
  			Msg = "parser __init__ ok"
			PCA_GenLib.WriteLog(Msg,9)
		except:
 			Msg = "parser __init__  :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
	
	

    
		
