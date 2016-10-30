
SMSC Simulator
========================
Native SS7 stack
Sigtran Support :  encode/decode (M3UA|SCCP|TCAP|MAP|GSM 0340) protocol
Receive MO , send SRI and MT to STP 

TODO : Support SMPP protocol (bind_transmitter|submit_sm)


Pre-Request
========================
pre-request : Python SCTP -> https://github.com/philpraxis/pysctp
              Python SMSPDU -> https://pypi.python.org/pypi/smspdu

Test Procedure 
=================

   * Get STP IP,Port,Point Code
   * chmod +x run.sh
   * vi SMSC_Simulator.cfg update sctp server ip port , M3UA Point Code and MAP SC_Address
   * ./run.sh
  
   * This simulator accept MO-Forward-SMS request
   * once Simulator receiver MO-FSM , will send MO-FSM-act back to STP 
   * message will store internally and initial SRI-SM request to STP 
   * if SRI-SM received from STP with imsi and NNN  , will initial MT-Forward-SMS to STP 
   * after received MT-FSM-ack , message will remove from Queue
   * This simulator only for test purpose -> support 1 MDA only
 


