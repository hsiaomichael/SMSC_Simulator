#!/usr/bin/python
########################################################################################
#
# Filename:    PCA_M3UAClientSocket.py
#  
# Description
# ===========
# M3UA Client
#
#
# Author : Michael Hsiao , 
# Date   : 2004/07/23
# Desc   : Implement M3UA 

########################################################################################

import sys, string,time,struct,socket
import PCA_GenLib
import PCA_XMLParser
import select
import PCA_SCTPClientSocket
import PCA_M3UAMessage
import PCA_M3UAParser



###########################################################



class Connector(PCA_SCTPClientSocket.Connector):

  M3UA_ASUP_UP = chr(0x00)
  M3UAMessage = None
  ########################################################		
  ## Init Socket Environment and set socket option     
  ########################################################
  def __init__(self,XMLCFG):		
    try:	
      Msg = "Connector init ..."
      PCA_GenLib.WriteLog(Msg,9)
      PCA_SCTPClientSocket.Connector.__init__(self,XMLCFG)
			
      self.M3UAMessage = PCA_M3UAMessage.Writer(XMLCFG)
      #self.M3UAMessage.getASUP_UP()
      #self.M3UA_ASUP_UP = M3UAMessage.getASUP_UP()
      #self.M3UA_ASP_Active = M3UAMessage.getASP_Active()
	  
      self.parser = PCA_M3UAParser.Parser()
      self.handler = PCA_M3UAParser.Handler()
      self.parser.setContentHandler(self.handler)


      Msg = "Connector OK."
      PCA_GenLib.WriteLog(Msg,9)	    						
    except :
      Msg = "Connector Initial error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
      PCA_GenLib.WriteLog(Msg,0)			
      raise
	  
  ########################################################		
  ## Connect To Server	
  ########################################################
  def connect(self):
    try:
      Msg = "connect Init"
      PCA_GenLib.WriteLog(Msg,9)

      PCA_SCTPClientSocket.Connector.connect(self)

      time.sleep(1)

      Msg = "send M3UA ASUP_UP"
      PCA_GenLib.WriteLog(Msg,2)

      Message = self.M3UAMessage.getASUP_UP()
      self.parser.parse(Message)
      response_message = self.handler.getHandlerResponse()
      ServerID = self.handler.getTID()
      DebugStr = self.handler.getDebugStr()
      Msg = "send : %s*" % DebugStr
      PCA_GenLib.WriteLog(Msg,1)

      self.sendDataToSocket(Message)

      #Msg = "send = *\n%s\n*" % PCA_GenLib.HexDump(self.M3UA_ASUP_UP)
      #PCA_GenLib.WriteLog(Msg,2)

      Message = self.readDataFromSocket()

      if Message != None:
        #Msg = "receive = *\n%s\n*" % PCA_GenLib.HexDump(Message)
        #PCA_GenLib.WriteLog(Msg,2)

        self.parser.parse(Message)

        response_message = self.handler.getHandlerResponse()
        ServerID = self.handler.getTID()
        DebugStr = self.handler.getDebugStr()
        Msg = "recv : %s*" % DebugStr
        PCA_GenLib.WriteLog(Msg,1)

        message_type = ord(Message[3])
        Msg = "message type = %s" % message_type
        PCA_GenLib.WriteLog(Msg,2)
        if message_type == 4:
          Msg = "ASUP up ack"
          PCA_GenLib.WriteLog(Msg,2)
		  
          Message = self.M3UAMessage.getASP_Active()
          self.parser.parse(Message)
          response_message = self.handler.getHandlerResponse()
          ServerID = self.handler.getTID()
          DebugStr = self.handler.getDebugStr()
          Msg = "send : %s*" % DebugStr
          PCA_GenLib.WriteLog(Msg,1)
          self.sendDataToSocket(Message)
          #Msg = "send = *\n%s\n*" % PCA_GenLib.HexDump(self.M3UA_ASP_Active)

          Message = self.readDataFromSocket()
          if Message != None:
            #Msg = "receive = *\n%s\n*" % PCA_GenLib.HexDump(Message)
            #PCA_GenLib.WriteLog(Msg,1)
            self.parser.parse(Message)
            response_message = self.handler.getHandlerResponse()
            ServerID = self.handler.getTID()
            DebugStr = self.handler.getDebugStr()
            Msg = "recv : %s*" % DebugStr
            PCA_GenLib.WriteLog(Msg,1)
		
      Msg = "connect OK"
      PCA_GenLib.WriteLog(Msg,9)

    except :
      Msg = "connect error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
      PCA_GenLib.WriteLog(Msg,0)	
      raise
	
  
	  
#######################################################	   
# Main Program 
#######################################################   
if __name__ == '__main__':

  def MainTest(XMLCFG):
    try:
      print 'Start Program ...'
      try:
        PCA_GenLib.DBXMLCFGInit(XMLCFG)	
        Server = Connector(XMLCFG)
        try:
          Server.connect()
          #for i in range(1):
          #  Message = chr(0x01)+ chr(0x00)+ chr(0x03)+  chr(0x01)+  chr(0x00)+  chr(0x00)+  chr(0x00)+  chr(0x08)  
          #  Server.sendDataToSocket(Message)
          parser = PCA_M3UAParser.Parser()
          handler = PCA_M3UAParser.Handler()
          parser.setContentHandler(handler)
          while (1):
            Message = Server.readDataFromSocket()
            if Message != None:
              Msg = "receive = *\n%s\n*" % PCA_GenLib.HexDump(Message)
              PCA_GenLib.WriteLog(Msg,2)
              parser.parse(Message)
              response_message = handler.getHandlerResponse()
              ServerID = handler.getTID()
              DebugStr = handler.getDebugStr()


              Msg = "recv : %s*" % DebugStr
              PCA_GenLib.WriteLog(Msg,1)

              for m3ua_key in response_message:
                 if m3ua_key == "M3UA sccp_msg_dict":
                   sccp_msg_dict = response_message[m3ua_key]
                   for sccp_key in sccp_msg_dict:
                     if sccp_key == "SCCP tcap_msg_dict":
                       tcap_msg_dict = sccp_msg_dict[sccp_key]
                       for tcap_key in tcap_msg_dict:
                         Msg = "key=<%s> : value=<%s>*" % (tcap_key,tcap_msg_dict[tcap_key])
                         PCA_GenLib.WriteLog(Msg,1)
                     else:
                       Msg = "key=<%s> : value=<%s>*" % (sccp_key,sccp_msg_dict[sccp_key])
                       PCA_GenLib.WriteLog(Msg,1)
                 else:
                   Msg = "key=<%s> : value=<%s>*" % (m3ua_key,response_message[m3ua_key])
                   PCA_GenLib.WriteLog(Msg,1)


          time.sleep(20)
        finally:
          Server.Close()
      finally:
        PCA_GenLib.CloseLog()
      return 0
    except:
      print '\n\n uncaught ! < ',sys.exc_type,sys.exc_value,' >'
      import traceback
      traceback.print_exc()  
      raise

#################################################################
  try:	
  	print "Open cfg file"
	XMLCFG =  open("M3UAClient.cfg","r").read()
	MainTest(XMLCFG)
  except:
  	print "Error or .cfg configuration file not found"
 	print "Msg = : <%s>,<%s>" % (sys.exc_type,sys.exc_value)
 	import traceback
	traceback.print_exc()  	
  	sys.exit()
	
