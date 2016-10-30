#!/usr/bin/python
########################################################################################
#
# Filename:    PCA_SCTPClientSocket.py
#  
# Description
# ===========
# SCTP Client
#
#
# Author : Michael Hsiao , 
# Date   : 2004/07/23
# Desc   : Socket Client PCA Standard Class

# Update By : Michael Hsiao , 
# Date      : 2016/07/23
# Desc      : implement sctp 
########################################################################################

import sys, string,time,struct,socket
import PCA_GenLib
import PCA_XMLParser
import _sctp
import sctp
import select

###########################################################

class Connector:	
  ########################################################		
  ## Init Socket Environment and set socket option     
  ########################################################
  def __init__(self,XMLCFG):		
    try:	
      Msg = "Connector init ..."
      PCA_GenLib.WriteLog(Msg,9)
      self.XMLCFG = XMLCFG	
      Tag = "REMOTE_HOST"
      host = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
      Tag = "CONNECT_PORT"
      connect_port = PCA_XMLParser.GetXMLTagValue(XMLCFG,Tag)
			
      self.host = host
      self.connect_port = string.atoi(connect_port)			
      		
      if _sctp.getconstant("IPPROTO_SCTP") != 132:
        Msg = "Connector init getconstant failed"
        PCA_GenLib.WriteLog(Msg,0)

      Msg = "Call SCTP Socket..."
      PCA_GenLib.WriteLog(Msg,7)
      # make a TCP/IP spocket object
      self.SocketDescriptor = sctp.sctpsocket_tcp(sctp.socket.AF_INET)
    			
      self.saddr = (self.host, self.connect_port)
      Msg = "Host=<%s>,Port=<%s>" % (self.host,self.connect_port)
      PCA_GenLib.WriteLog(Msg,7)
      self.SocketDescriptor.initparams.max_instreams = 3
      self.SocketDescriptor.initparams.num_ostreams = 3

      self.SocketDescriptor.events.clear()
      self.SocketDescriptor.events.data_io = 1

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
      Msg = "Connect to Host=<%s>,Port=<%s>" % (self.host,self.connect_port)
      PCA_GenLib.WriteLog(Msg,1)
      self.SocketDescriptor.connect(self.saddr)
      Msg = "connect OK"
      PCA_GenLib.WriteLog(Msg,9)
    except sctp.socket.error:
      Msg = "connect socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
      PCA_GenLib.WriteLog(Msg,0)	
      raise
    except :
      Msg = "connect error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
      PCA_GenLib.WriteLog(Msg,0)	
      raise
			
  ########################################################		
  ## SCTP Def Non-Block I/O Send Socket Data		 
  ########################################################
  def sendDataToSocket(self,Message):
    try:
      Msg = "sendDataToSocket "
      PCA_GenLib.WriteLog(Msg,9)	
       
      to=("",0)
      ppid=50331648
      self.SocketDescriptor.sctp_send(Message,to,ppid) 
      Msg = "send : data=<%s>" % Message
      PCA_GenLib.WriteLog(Msg,3)
      Msg = "sendDataToSocket OK"
      PCA_GenLib.WriteLog(Msg,9)
      return 1     
    except:
      Msg = "sendDataToSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
      PCA_GenLib.WriteLog(Msg,0)
      raise
	  
  ########################################################		
  ## SCTP Def Read Socket Data use blocking read		
  ########################################################
  def readDataFromSocket(self,Length=1024,TimeOut = 1.0,ReadAttempts = 1):
    try:
      Msg = "readDataFromSocket "
      PCA_GenLib.WriteLog(Msg,9)
      self.ReadSet = []			
      self.ReadSet.append(self.SocketDescriptor)              # add to select inputs list 
      Msg = "Length to read = <%s>  " % Length
      PCA_GenLib.WriteLog(Msg,8)
      Msg = "TimeOut = <%s> Seconds " % TimeOut
      PCA_GenLib.WriteLog(Msg,8)			
			   				  		
      readables, writeables, exceptions = select.select(self.ReadSet, [], [],TimeOut)
      for SocketFD in readables:
        if (SocketFD == self.SocketDescriptor):
          Message = self.SocketDescriptor.recv(Length)  
          if not Message:
            Msg = "server close connection"
            PCA_GenLib.WriteLog(Msg,0)
            raise socket.error,"server close connection"

        Msg = "ReadDataFromSocket OK"
        PCA_GenLib.WriteLog(Msg,9)
        return Message
				
			
      Msg = "ReadDataFromSocket retry time out !"
      PCA_GenLib.WriteLog(Msg,3)
      return None
			
    except socket.error:
      Msg = "ReadDataFromSocket socket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
      PCA_GenLib.WriteLog(Msg,0)
      raise
	
    except:
      Msg = "ReadDataFromSocket error : <%s>,<%s> " % (sys.exc_type,sys.exc_value)
      PCA_GenLib.WriteLog(Msg,0)
      raise	

	  
  ########################################################		
  ## Close Socket					     
  ########################################################					
  def Close(self):
    try:
      Msg = "Close Socket Init"
      PCA_GenLib.WriteLog(Msg,9)
    
      Msg = "Close connection from Host=<%s>,Port=<%s>" % (self.host,self.connect_port)
      PCA_GenLib.WriteLog(Msg,1)
				
      self.SocketDescriptor.close()	
			
      Msg = "Close Socket OK"
      PCA_GenLib.WriteLog(Msg,9)			
    except sctp.socket.error:
      Msg = "Connection close"
      PCA_GenLib.WriteLog(Msg,0)			
    except:
      Msg = "Close Socket Error :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
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
          for i in range(1000000):
            Message = "Data From Client 2 %s" % time.time()
            Server.sendDataToSocket(Message)
            Message = Server.readDataFromSocket()
            time.sleep(1)
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
	XMLCFG =  open("SCTPClient.cfg","r").read()
	MainTest(XMLCFG)
  except:
  	print "Error or .cfg configuration file not found"
 	print "Msg = : <%s>,<%s>" % (sys.exc_type,sys.exc_value)
 	import traceback
	traceback.print_exc()  	
  	sys.exit()
	
