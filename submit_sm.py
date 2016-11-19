
import sys,struct,time,string
import PCA_GenLib
import PCA_Parser
import random

##############################################################################
###    Message Handler   	
##############################################################################
class Handler(PCA_Parser.ContentHandler):	
	
	
        source_address = 'na'	
        dest_address = 'na'	
        sms_text = 'na'	
 	def __init__(self):
		PCA_Parser.ContentHandler.__init__(self)
	 	
	      
	def startElement(self, name, attrs):
		self.TID = ''
		self.SOURCD_ID = "HeartBeat"
		
		if name == "dest_address":
			self.dest_address = attrs
		if name == "source_address":
			self.source_address = attrs
		if name == "sms_text":
			self.sms_text = attrs

	def endDocument(self,debugstr,TID,SOURCD_ID ):
        	self.DebugStr = debugstr
        	self.TID = TID
        	self.SOURCD_ID = SOURCD_ID
	
	def getSOURCD_ID(self):	
		return self.SOURCD_ID	

	def getHandlerResponse(self):
		
		CurrentSeconds = time.time()
		date_tuple =  time.localtime(CurrentSeconds)		
		message_id = "%04d%02d%02d%02d%02d%02d" % (date_tuple[0:6])
		
		self.Message = message_id + chr(0x00)
    		return self.Message	
	
	def getDEST_ADDR(self):	
		return self.dest_address	
	def get_msg_for_mt(self):	
		return (self.source_address,self.dest_address,self.sms_text)
	
#########################################################################
# 
#
#########################################################################
class Parser(PCA_Parser.Parser):
	
	
	DebugStr = 'na'
	SMS_TYPE='na'
	
	TID = 'na'
	
	Service_Type = 'na'
	SOURCD_ID = 'HeartBeat'
	
	#Debug_Str_Dict = {}
	

	def __init__(self):
		try:
			Msg = "parser __init__"
			PCA_GenLib.WriteLog(Msg,9)
		
			PCA_Parser.Parser.__init__(self)
  			
  			Msg = "parser __init__ ok"
			PCA_GenLib.WriteLog(Msg,9)
		except:
 			Msg = "parser __init__  :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
	
	def set_handler(self,name,attrs,content):
			
		self._cont_handler.startElement(name, attrs)        		
		self._cont_handler.characters(content)
        	self._cont_handler.endElement(name)
        	
	
	

	def parse(self, source):
		try:
			Msg = "parser init"
			PCA_GenLib.WriteLog(Msg,9)	
			self.SOURCD_ID = 'HeartBeat'
			self.DebugStr = ' '
			orig_data = source
			name = 'none'	
			self.StartParsing = 1			
			
			
			start_pos = string.find(source,chr(0x00))			
			service_type = source[0:start_pos]			
			self.DebugStr = "system_id = <%s>" % service_type	
			
			source = source[start_pos+1:]
			source_addr_ton = struct.unpack("!b",source[0])[0]			
			self.DebugStr = "%s , source_addr_ton = <%s>" % (self.DebugStr,source_addr_ton)	
			
			source = source[1:]
			source_addr_npi = struct.unpack("!b",source[0])[0]			
			self.DebugStr = "%s , source_addr_npi = <%s>" % (self.DebugStr,source_addr_npi)	
			
			
			source = source[1:]
			start_pos = string.find(source,chr(0x00))
			source_addr = source[0:start_pos]
			self.DebugStr = "%s , source_addr = <%s>" % (self.DebugStr,source_addr)	
			
			name = "source_address"
			attrs = source_addr
			content = attrs
			self.set_handler(name,attrs,content)
			
			source = source[start_pos+1:]
			dest_addr_ton = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , dest_addr_ton = <%s>" % (self.DebugStr,dest_addr_ton)	
			
			source = source[1:]
			dest_addr_npi = struct.unpack("!b",source[0])[0]			
			self.DebugStr = "%s , dest_addr_npi = <%s>" % (self.DebugStr,dest_addr_npi)	
			
			source = source[1:]
			start_pos = string.find(source,chr(0x00))
			dest_addr = source[0:start_pos]
			self.DebugStr = "%s , dest_addr = <%s>" % (self.DebugStr,dest_addr)

			name = "dest_address"
			attrs = dest_addr
			content = attrs
			self.set_handler(name,attrs,content)
			
						
			source = source[start_pos+1:]
			esm_class = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , esm_class = <%s>" % (self.DebugStr,esm_class)
			
			source = source[1:]
			protocol_id = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , protocol_id = <%s>" % (self.DebugStr,protocol_id)
				
			source = source[1:]
			priority_flag = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , priority_flag = <%s>" % (self.DebugStr,priority_flag)
			
			source = source[1:]
			start_pos = string.find(source,chr(0x00))
			schedule_delivery_time = source[0:start_pos]
			self.DebugStr = "%s , schedule_delivery_time = <%s>" % (self.DebugStr,schedule_delivery_time)
			
			source = source[start_pos+1:]
			start_pos = string.find(source,chr(0x00))
			validity_period = source[0:start_pos]
			self.DebugStr = "%s , validity_period = <%s>" % (self.DebugStr,validity_period)
				
			source = source[start_pos+1:]
			registered_delivery = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , registered_delivery = <%s>" % (self.DebugStr,registered_delivery)
			
			source = source[1:]
			replace_if_present_flag = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , replace_if_present_flag = <%s>" % (self.DebugStr,replace_if_present_flag)
			
			source = source[1:]
			data_coding = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , data_coding = <%s>" % (self.DebugStr,data_coding)
				
			
			source = source[1:]
			sm_default_msg_id = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , sm_default_msg_id = <%s>" % (self.DebugStr,sm_default_msg_id)
			
			source = source[1:]
			sm_length = struct.unpack("!b",source[0])[0]
			self.DebugStr = "%s , sm_length = <%s>" % (self.DebugStr,sm_length)
			
			
			source = source[1:]
			short_message = source[:sm_length]
			self.DebugStr = "%s , short_message = <%s>" % (self.DebugStr,short_message)
			name = "sms_text"
			attrs = short_message
			content = attrs
			self.set_handler(name,attrs,content)
			
				
			if self.StartParsing == 1:
        			self._cont_handler.endDocument(self.DebugStr,self.TID,self.SOURCD_ID)
        		
        		
			Msg = "parser OK"
			PCA_GenLib.WriteLog(Msg,9)
		except:
 			Msg = "parser  :<%s>,<%s>,name=<%s>" % (sys.exc_type,sys.exc_value,name)
			PCA_GenLib.WriteLog(Msg,0)
			
			Msg = "orig data =\n%s" % PCA_GenLib.HexDump(orig_data)
			PCA_GenLib.WriteLog(Msg,0)
			
			Msg = "rest data =\n%s" % PCA_GenLib.HexDump(source)
			PCA_GenLib.WriteLog(Msg,0)
			if self.StartParsing == 1:
        			self._cont_handler.endDocument(self.DebugStr,self.TID,self.SOURCD_ID)
        		return
	        		
	        		
	
