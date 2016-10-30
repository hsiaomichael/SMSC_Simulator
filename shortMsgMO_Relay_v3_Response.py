########################################################################################
#
# Filename:    shortMsgMO_Relay_v3_Response.py
#  
# Description
# ===========
# 
#
# Author        : Michael Hsiao 
#
# Create Date   : 2016/09/24
# Desc          : Initial

########################################################################################

import sys,string,struct
import PCA_GenLib
import PCA_Parser
import PCA_XMLParser
import PCA_MAPParameters


##############################################################################
###    Message Handler   	
##############################################################################

##############################################################################
###    Message Handler   	
##############################################################################
class Handler(PCA_Parser.ContentHandler):	
	
  attrs = None	
  Message = {}
  def __init__(self):
	PCA_Parser.ContentHandler.__init__(self)
	self.Message = {}
		
  def startDocument(self):
       self.ExtraSocketData = ''
       self.IsApplicationMessage = 0
       self.Operation = chr(0x00)
       self.TID='na'
       self.Message = {}
	
  def startElement(self, name, attrs):
    try:
      Msg = "startElement init"
      PCA_GenLib.WriteLog(Msg,9)

      #Msg = "name=<%s>,attrs=<%s>" % (name,PCA_GenLib.HexDump(attrs))
      #PCA_GenLib.WriteLog(Msg,0)
      name = "MAP %s" % name
      self.MessageName = name
      self.attrs = attrs
      if name == "version":			
        self.version =  attrs
			
			
      Msg = "startElement OK"
      PCA_GenLib.WriteLog(Msg,9)        	
    except:
      Msg = "startElement Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
      PCA_GenLib.WriteLog(Msg,0)
      raise

 	
  def characters(self,content):
    try:
       		
      Msg = "characters Init "
      PCA_GenLib.WriteLog(Msg,9)
			
      Msg = "%-20s=<%-25s>,Hex=%s" % (self.MessageName ,content,PCA_GenLib.HexDump(self.attrs))
      PCA_GenLib.WriteLog(Msg,3)
      self.Message[self.MessageName] = content
			
      Msg = "characters OK"
      PCA_GenLib.WriteLog(Msg,9)
        	
    except:
      Msg = "characters Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
      PCA_GenLib.WriteLog(Msg,0)
      raise


  def endDocument(self,data,debugstr):
    try:
     
      self.DebugStr = debugstr
        	
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
							
			
					
							
						

#########################################################################
# 
#
#########################################################################
class Parser(PCA_Parser.Parser):
  DebugStr = ""
  ResponseCode = "NA"
  

  def set_handler(self,name,attrs,content):
    self._cont_handler.startElement(name, attrs)        		
    self._cont_handler.characters(content)
    self._cont_handler.endElement(name)



  def parseTLV(self,data):
    try:
      Msg = "parseTLV Init "
      PCA_GenLib.WriteLog(Msg,9)

      source = data
      tlv_desc = 'na'
      tlv_type = 'na'
      name = 'na'
      number_of_tlv = 0
      
      Msg = "MAP parseTLV data =\n%s" % PCA_GenLib.HexDump(source)
      PCA_GenLib.WriteLog(Msg,3)
      tag_index = 0
      while len(source) > 0:

        if number_of_tlv > 100:
          Msg = "number of TLV > 100 "
          PCA_GenLib.WriteLog(Msg,0)
          break
        
        tag_index = tag_index + 1
	name = "Tag"
        name = "%s %s" % (name,tag_index)
        attrs = source[0]
        content = PCA_GenLib.getHexString(attrs)
        self.set_handler(name,chr(0x00),content)
	
        tag_class = ord(attrs) & 0xc0
        tag_class = tag_class >> 6


        Tag_Type = 'Primitive'
        if (ord(attrs) & 0x20):
          name = "C_%s-" % name
          name = "%s %s" % (name,tag_index)
          attrs = source[0:2]
          content = PCA_GenLib.getHexString(attrs)
          Tag_Type = 'Constructor'
        else:
          name = "P_%s-" % name
          name = "%s %s" % (name,tag_index)
	  content = ord(attrs)
          Tag_Type = 'Primitive'
        
        name = "%s-%s" % (name,PCA_MAPParameters.tag_class[tag_class])
        if Tag_Type == 'Primitive':
          attrs = struct.pack("!b",ord(attrs) & 0x1f)
        name = "%s %s" % (name,tag_index)
	self.set_handler(name,attrs,content)
        self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,name,content)

    
        if Tag_Type == 'Primitive':
          source = source[1:]
        else:
          source = source[2:]
         
        name = "length"
        name = "%s %s" % (name,tag_index)
	attrs = source[0]
	content = ord(attrs)
        tag_length = content
        tag_length_form = "short"
        if tag_length > 128:
           tag_length_form = "long"
           attrs = source[1]
	   content = ord(attrs)
           tag_length = content
        else:
           tag_length_form = "short"
	self.set_handler(name,attrs,content)
        self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,name,content)
        
        if tag_length_form == "short":
          source = source[1:]
        else:
          source = source[2:]

        name = "value"
        name = "%s %s" % (name,tag_index)
	attrs = source[0:tag_length]
        if Tag_Type == 'Constructor':
	  content = PCA_GenLib.getHexBCDString(attrs[1:])
        else:
          content = PCA_GenLib.getHexString(attrs)
	self.set_handler(name,attrs,content)
        self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,name,content)
        
        if Tag_Type == 'Constructor':
          self.parseTLV(attrs)
        
        try:
          source = source[tag_length:]
        except IndexError:
          Msg = "parseTLV index error : <%s>,<%s>,name=<%s> " % (sys.exc_type,sys.exc_value,name)
          PCA_GenLib.WriteLog(Msg,0)
          break


      Msg = "parseTLV Ok "
      PCA_GenLib.WriteLog(Msg,9)
    except:
      Msg = "parseTLV error : <%s>,<%s>,name=<%s> " % (sys.exc_type,sys.exc_value,name)
      PCA_GenLib.WriteLog(Msg,0)
      #Msg = "dump source data =<\n%s\n>" % PCA_GenLib.HexDump(source)
      #PCA_GenLib.WriteLog(Msg,0)
	
  def parse(self, source):
    try:
      Msg = "parser init"
      PCA_GenLib.WriteLog(Msg,9)	
      orig_data = source
      name = 'none'	
      self.StartParsing = 0
      TID = "na"
      content = "na"

      Msg = "MAP shortMORelay Response data =<\n%s\n>" % PCA_GenLib.HexDump(source)
      PCA_GenLib.WriteLog(Msg,5)

      

			
      if (source != None)  : 
        self._cont_handler.startDocument()
	self.StartParsing = 1
        
      
        self.DebugStr = ""  
      
        self.parseTLV(source)
        

					
      if self.StartParsing == 1:
        self._cont_handler.endDocument(orig_data,self.DebugStr)
        		
	Msg = "parser OK"
	PCA_GenLib.WriteLog(Msg,9)
    except:
      Msg = "parser  :<%s>,<%s>,name=<%s>" % (sys.exc_type,sys.exc_value,name)
      PCA_GenLib.WriteLog(Msg,0)
      Msg = "orig data =\n%s" % PCA_GenLib.HexDump(orig_data)
      PCA_GenLib.WriteLog(Msg,0)
      raise
	        		
	
  def parse_old(self, source):
    try:
      Msg = "parser init"
      PCA_GenLib.WriteLog(Msg,9)	
      orig_data = source
      name = 'none'	
      self.StartParsing = 0
      TID = "na"
      content = "na"

      Msg = "MAP shortMORelay Response data =<\n%s\n>" % PCA_GenLib.HexDump(source)
      PCA_GenLib.WriteLog(Msg,5)

      

			
      if (source != None)  : 
        self._cont_handler.startDocument()
	self.StartParsing = 1
        
      
        self.DebugStr = ""  
        name = "MAP Tag"
	attrs = source[0]
        Tag_Type = 'Primitive'
        if (ord(attrs) & 0x40):
          name = "%s-Constructor" % name
          attrs = source[0:2]
          content = PCA_GenLib.getHexString(attrs)
        else:
          name = "%s-Primitive" % name
	  content = ord(attrs)
	self.set_handler(name,attrs,content)
        
        if Tag_Type == 'Primitive':
          source = source[1:]
        else:
          source = source[2:]

        self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,name,content)
        name = "length"
	attrs = source[0]
	content = ord(attrs)
        tag_length = content
	self.set_handler(name,attrs,content)
        self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,name,content)

        source = source[1:]
        name = "value"
	attrs = source[0:tag_length]
	content = PCA_GenLib.getHexString(attrs)
	self.set_handler(name,attrs,content)
        #self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,name,content)
        
        
        #self.parseTLV(attrs)
        source = attrs
        name = "invoke"
        tag_name = name
	attrs = source[0]
        content = ord(attrs)
	#self.set_handler(name,attrs,content)

        source = source[1:]
        name = "length"
	attrs = source[0]
	content = ord(attrs)
        tag_length = content
	self.set_handler(name,attrs,content)
        #self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,name,content)

        source = source[1:]
        name = "invoke value"
	attrs = source[0]
	content = ord(attrs)
        tag_value = content
	self.set_handler(name,attrs,content)
        self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,tag_name,tag_value)


        source = source[1:]
        name = "resultretres"
        tag_name = name
	attrs = source[0]
        content = ord(attrs)

        source = source[1:]
        name = "length"
	attrs = source[0]
	content = ord(attrs)
        tag_length = content

        source = source[1:]
        name = "resultretres value"
	attrs = source[0:tag_length]
	#content = ord(attrs)



        source = attrs
        name = "opCode"
        tag_name = name
	attrs = source[0]
        content = ord(attrs)

        source = source[1:]
        name = "length"
	attrs = source[0]
	content = ord(attrs)
        tag_length = content

        source = source[1:]
        name = "opCode value"
	attrs = source[0]
	content = ord(attrs)
        try:
          tag_value = PCA_MAPParameters.op_code[content]
        except:
          Msg = "unknow opCode Value = %s" % content
          PCA_GenLib.WriteLog(Msg,0)
        self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,tag_name,tag_value)
        self.set_handler(name,attrs,tag_value)



        source = source[1:]
        name = "sm-rp-UI"
        tag_name = name
	attrs = source[0]
        content = ord(attrs)
        self.set_handler(name,attrs,content)

        source = source[1:]
        name = "length"
	attrs = source[0]
	content = ord(attrs)
        tag_length = content
        self.set_handler(name,attrs,content)

        source = source[1:]
        name = "sm-rp-UI value"
	attrs = source[0:tag_length]	
        tag_value = PCA_GenLib.getHexString(attrs)
        self.DebugStr = "%s,<%s>=<%s>" % (self.DebugStr,tag_name,tag_value)
        self.set_handler(name,attrs,tag_value)


					
      if self.StartParsing == 1:
        self._cont_handler.endDocument(orig_data,self.DebugStr)
        		
	Msg = "parser OK"
	PCA_GenLib.WriteLog(Msg,9)
    except:
      Msg = "parser  :<%s>,<%s>,name=<%s>" % (sys.exc_type,sys.exc_value,name)
      PCA_GenLib.WriteLog(Msg,0)
      Msg = "orig data =\n%s" % PCA_GenLib.HexDump(orig_data)
      PCA_GenLib.WriteLog(Msg,0)
      raise
	        		
				
	  

