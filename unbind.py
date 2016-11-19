
import sys,struct,time
import PCA_GenLib
import PCA_Parser
import PCA_SMPP_Parameter_Tag
import PCA_DLL

#reload(PCA_GEIP_Parameter_Tag)

##############################################################################
###    Message Handler   	
##############################################################################
class Handler(PCA_Parser.ContentHandler):	
	
	
	
 	def __init__(self):
		PCA_Parser.ContentHandler.__init__(self)
	 	
	      
	def startElement(self, name, attrs):
		self.TID = ''
		self.SOURCD_ID = "HeartBeat"			
			  	

	def endDocument(self,debugstr,TID,SOURCD_ID ):
        	self.DebugStr = debugstr
        	self.TID = TID
        	self.SOURCD_ID = SOURCD_ID
	
	def getSOURCD_ID(self):	
		return self.SOURCD_ID	

#########################################################################
# 
#
#########################################################################
class Parser(PCA_Parser.Parser):
	
	
	
	bind_receiver = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01)
	bind_receiver_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x01)
	bind_transmitter = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x02)
	bind_transmitter_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x02)
	outbind = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x0b) 
	unbind = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x06) 
	unbind_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x06) 
	submit_sm = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x04) 
	submit_sm_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x04) 
	deliver_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x05) 
	deliver_sm_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x05) 	
	query_sm = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x03) 
	query_sm_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x03) 
	cancel_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x08) 
	cancel_sm_resp =chr(0x80)+chr(0x0)+chr(0x00)+chr(0x08) 
	replace_sm =  chr(0x00)+chr(0x0)+chr(0x00)+chr(0x07) 
	replace_sm_resp=  chr(0x80)+chr(0x0)+chr(0x00)+chr(0x07) 
	enquire_link =  chr(0x00)+chr(0x0)+chr(0x00)+chr(0x0a) 
	enquire_link_resp =  chr(0x80)+chr(0x0)+chr(0x00)+chr(0x0a) 
 	generic_nack =  chr(0x80)+chr(0x00)+chr(0x00)+chr(0x00) 
	
	command_id_dict = {}
 	command_id_dict[bind_receiver] = 'bind_receiver'
 	command_id_dict[bind_receiver_resp] = 'bind_receiver_resp'
 	command_id_dict[bind_transmitter] = 'bind_transmitter'
 	command_id_dict[bind_transmitter_resp] = 'bind_transmitter_resp'
 	command_id_dict[submit_sm] = 'submit_sm'
 	command_id_dict[submit_sm_resp] = 'submit_sm_resp'
 	command_id_dict[deliver_sm] = 'deliver_sm' 	
 	command_id_dict[deliver_sm_resp] = 'deliver_sm_resp'
 	command_id_dict[enquire_link] = 'enquire_link'
 	command_id_dict[enquire_link_resp] = 'enquire_link_resp'
 	
 	command_id_dict[unbind] = 'unbind'
 	command_id_dict[unbind_resp] = 'unbind_resp'
		
	
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
	        		
	        		
