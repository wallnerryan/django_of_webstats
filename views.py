#*********************************************
#Django Application for OpenFlow @ Marist.edu
#Author: Ryan Wallner 
#Rights Reserved By: Marist College, New York
#
#*********************************************

from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime
import urllib2
import simplejson
import json
from django.core import serializers
from django.http import HttpResponse

#Welcome
def welcome(request):
        time = datetime.datetime.now()
        return render_to_response('welcome.html', {'current_date' : time})
        
#Forums
def forums(request):
		return render_to_response('forums.html',{})

#Documents
def docs(request):
		#create model to hold docs? or serve as static/media/{files}.
		return render_to_response('docs.html',{})
		
#2012 ECC Pres
def ecc2012(request):
		return render_to_response('ecc2012.html',{})
		
#LiveView
def liveview(request):
	return render_to_response('liveview.html', {})

#Get Parameters 
def getOpenFlowParams(request):
			#***************************
		 	switchdata_tables = urllib2.urlopen('http://10.10.2.101:8080/wm/core/switch/all/table/json')
			switchdata_desc = urllib2.urlopen('http://10.10.2.101:8080/wm/core/switch/all/desc/json')
			switchdata_links = urllib2.urlopen('http://10.10.2.101:8080/wm/topology/links/json')
			switchdata_switches = urllib2.urlopen('http://10.10.2.101:8080/wm/core/controller/switches/json')
			switchdata_devices = urllib2.urlopen('http://10.10.2.101:8080/wm/devicemanager/device/all/json')
			switchdata_counters = urllib2.urlopen('http://10.10.2.101:8080/wm/core/counter/all/json')
			#_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+
			#switchdata_pktinhist = urllib2.urlopen('http://10.10.2.101:8080/wm/pktinhistory/history/json')
			#switchdata_pktouthist = urllib2.urlopen('http://10.10.2.101:8080/wm/pktinhistory/history/json')
			#ALSO PACKETOUT HIST	
			#_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+

			
			#GET JSON of Switches in Network
			data_switches = json.loads(switchdata_switches.read())
			jsondata_switches = simplejson.dumps(data_switches)
			sw_data_switches = simplejson.loads(jsondata_switches) 
			#Get number of switches on the network and pass number to "sw_num"
			switchlist = []
		 	#Initialize django dicts
			switchnum_dict = {}
			switchids_dict = {}
			
			sw_num = 0
			while sw_num < len(sw_data_switches):
				switchid = sw_data_switches[sw_num]['dpid']
				switchlist.append(switchid)
				#Update dictionary with the switch-# : dpid tuple
				switchids_dict.update({"sw_id-"+str(sw_num) : switchid})
				sw_num = sw_num + 1
			#update dict after while loop finishes for final number of switches
			switchnum_dict.update({'switches': sw_num})
			
			
			#GET JSON of Description Data of Switches
			data_desc = json.loads(switchdata_desc.read())
			jsondata_desc = simplejson.dumps(data_desc)
			sw_data_desc = simplejson.loads(jsondata_desc)
			#Initialize dictionaries for description data
			switchdesc_dict = {}			
			#Get the manufacturerDescription & hardwareDescription & softwareDescription
			#by the dpid of the switch
			for switch_dpid in switchlist:
				sw_manu = sw_data_desc[switch_dpid][0]['manufacturerDescription']
				sw_softw = sw_data_desc[switch_dpid][0]['softwareDescription']
				sw_hardw = sw_data_desc[switch_dpid][0]['hardwareDescription']
				
				switchdesc_dict.update({"sw_manu_for_"+str(switch_dpid) : sw_manu, 
												"sw_softw_for_"+str(switch_dpid) : sw_softw,
												"sw_hardw_for_"+str(switch_dpid) : sw_hardw}) 
			
			
			#GET JSON of Links
			data_links = json.loads(switchdata_links.read())
			jsondata_links = simplejson.dumps(data_links)
			sw_data_links = simplejson.loads(jsondata_links)
			#initiate dicts
			topology_links_dict = {}
			link_count = 0
			while link_count < len(sw_data_links):
				src_sw =  sw_data_links[link_count]['src-switch']
				src_prt =  sw_data_links[link_count]['src-port']
				dst_sw =  sw_data_links[link_count]['dst-switch']
				dst_prt =  sw_data_links[link_count]['dst-port']
				
				topology_links_dict.update({"lnk-"+str(link_count)+"_srcsw":src_sw,
										   								  "lnk-"+str(link_count)+"_srcprt":src_prt,
										   								  "lnk-"+str(link_count)+"_dstsw":dst_sw,
										   								  "lnk-"+str(link_count)+"_dstprt":dst_prt})
				link_count = link_count + 1
			
			#GET JSON of Connected Devices
			data_devices = json.loads(switchdata_devices.read())
			jsondata_devices = simplejson.dumps(data_devices)
			sw_data_devices = simplejson.loads(jsondata_devices)
			device_dict = {}
			device_count = 0
			for device in sw_data_devices:
				device_count = device_count + 1
			device_dict.update({"devices_on_network":device_count})
			
			#GET JSON of the Counters in the network
			#will be used for Packet_In and Packet_Out counters per switch per port (or an aggregate)
			data_counters = json.loads(switchdata_counters.read())
			jsondata_counters = simplejson.dumps(data_counters)
			sw_data_counters = simplejson.loads(jsondata_counters)
			counter_dict = {}
			for switch in switchlist:
				packetIn = 	sw_data_counters[switch+"__OFPacketIn"]
				offlowmod = sw_data_counters[switch+"__OFFlowMod"]
				packetout = sw_data_counters[switch+"__OFPacketOut"]
				
				counter_dict.update({'pktins_'+str(switch): packetIn,
																'flowmods_'+str(switch): offlowmod,
																'pktouts_'+str(switch): packetout})
			#GET JSON of Tables
			data_tables = json.loads(switchdata_tables.read())
			jsondata_tables = simplejson.dumps(data_tables)
			sw_data_tables = simplejson.loads(jsondata_tables)
				
			#_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+
			#GET JSON of Packet In History
			#data_pktinhist = json.loads(switchdata_pktinhist.read())
			#jsondata_pktinhist = simplejson.dumps(data_pktinhist)
			#sw_data_pktinhist = simplejson.loads(jsondata_pktinhist)
			#Initialize params			
			#pktin_list = []
			#pktin_dict = {}
			#Get the number of PACKET_IN message sent to the controller(for stat display) from the switch
			#and tuple the switches with the PACKET_IN Messages
			#pkt_in-<dpid> -> "type" (this will be used to show per switch how many PACKET_IN's
			
			#GET JSON of Packet Out History
			#data_pktouthist = json.loads(switchdata_pktouthist.read())
			#jsondata_pktouthist = simplejson.dumps(data_pktouthist)
			#sw_data_pktouthist = simplejson.loads(jsondata_pktouthist)
			#Initialize params			
			#pktout_list = []
			#pktout_dict = {}
			#Get the number of PACKET_OUT message sent to the controller(for stat display) from the switch
			#and tuple the switches with the PACKET_OUT Messages
			#pkt_out-<dpid> -> "type" (this will be used to show per switch how many PACKET_OUT's
			#_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+

			
			#Combine all dictionaries of info together for use
			combined_responsevars_dict = dict(switchnum_dict.items() +
																						   switchids_dict.items() + 
																						   switchdesc_dict.items() +
																						   device_dict.items() +
																						   counter_dict.items() +
																						   topology_links_dict.items())

			
			return HttpResponse(simplejson.dumps(combined_responsevars_dict), mimetype='application/javascript')
			#Keeping Below as Example
			#return render_to_response('liveview.html', {'vars' : simplejson.dumps(combined_responsevars_dict)})
				
