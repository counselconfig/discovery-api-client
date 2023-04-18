import requests
import re
import logging
from datetime import datetime
from getch import pause, pause_exit
import json
import sys
import os.path

  
class Client:

	def remove_tags(tags):
		c = tags
		removetags = re.compile('<.*?>') 
		cleaned = re.sub(removetags, '', c)
		return cleaned
		
	def display_title(json_object):
		title = json_object["title"]
		if title is not None: 
			clean_title = Client.remove_tags(title)
			print("\nTitle:", clean_title)
		return title
		
	def display_description(json_object):
		title = json_object["title"]
		description = json_object["scopeContent"]["description"]
		reference = json_object["citableReference"]
		clean_description = ""
		if title is None and description is not None:
			#tag removal
			clean_description = Client.remove_tags(description)
			print("\nDescription:", clean_description)
		else:
			Client.display_title(json_object)
		return clean_description
		
	def display_reference(json_object):      
		title = json_object["title"]
		description = json_object["scopeContent"]["description"]
		reference = json_object["citableReference"]
		if title is None and description is None:
			if reference is not None:
				print("\nCitable Reference:", reference) 
		else:
			Client.display_description(json_object)
		return reference
			
	def display_not_sufficient_info(json_object):
		title = json_object["title"]
		description = json_object["scopeContent"]["description"]
		reference = json_object["citableReference"]
		kv = [title, description, reference]
		if all(v is None for v in kv):
			print("\nInfo: not sufficient information")
		else:
			Client.display_reference(json_object)
		return None 

	def open_json(o):
		try: 
			j = o
			with open(sys.path[0] + j) as f: # test data
				#breakpoint()
				json_object = json.load(f)
				f.close() 
		except Exception as err:
			logger.exception(err)
			pause("\nJSON error see log, press any key to continue")
		else:
			return Client.display_not_sufficient_info(json_object)

	def display_no_record_found(response):
		sc = response.status_code
		if sc == 200:
			json_object = response.json()
			Client.display_not_sufficient_info(json_object)
		elif sc == 204:
			print ("\nInfo: no record found")
		# in case neither 200 nor 204
		else:
			print ("Info: api status", sc)
		return sc

	def get_record(base_url_id):
		try:
			url_id = base_url_id
			headers = {"Accept":"application/json"} #return only json object
			s = requests.Session() #group requests 
			response = s.get(url_id, headers=headers) 
			response.raise_for_status() #needed for logging http errors
		except requests.exceptions.HTTPError as e: 
			logger.exception(e) # Send any connection error to log
			s.close()
			pause("\nConnection error see log, press any key to continue")
		else:
			#rsc = response.ok # True < 4xx client error
			if response.ok is True: 
				Client.display_no_record_found(response) # pass response object
				s.close()
			return response.ok 
			
	def get_url(Id):

		# outputs local mock data
		local_ids = ["40e863e1-a723-492b-bcb3-89634b55cd82", "D53006911"] # mock ids
		if Id == local_ids[0]:
			jpath_dnsi = "./test_data/display_not_sufficient_info.json"
			if os.path.exists (jpath_dnsi): # if true
				printthis = Client.open_json(jpath_dnsi)
			else:
				print("add test data")
		elif Id == local_ids[1]:
			jpath_dr = "./test_data/display_reference.json"
			if os.path.exists (jpath_dr):
				Client.open_json(jpath_dr)
			else:
				print("add test data")
		# returns live data
		else:
			record_id = Id # url query parameter
			base_url = "https://discovery.nationalarchives.gov.uk/API/records/v1/details"
			base_url_id = f"{base_url}/{record_id}"
			Client.get_record(base_url_id)
			return base_url_id

	def validate(Id):
		rgx_guid = "[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}"
		rgx_iaid = "^[CDN]{1}[1-9][0-9]+$"
		rgx = [rgx_guid, rgx_iaid]
		line_id = Id
		
		m = False 
		for i in rgx:
			s = re.search(i, line_id)
			if s:
				m = True
				break
		if m:
			return True
		elif line_id == "":
			print ("\nInfo: no id entered")
		else:
			print ("\nInfo: wrong id format")
			
	def display(Id):
		if Client.validate(Id): # returns True
			return Client.get_url(Id)
	
	@staticmethod
	def enter_id():
		while True: 
			Client.display(Id = input("\n\nEnter a discovery record id: "))
			continue

#log settings
logger = logging.getLogger("discovery-api-client")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(datetime.now().strftime("./logs/clientlogfile_%H_%M_%d_%m_%Y.log"), delay=True)  
fh.setLevel(logging.INFO) 
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

		
if __name__ == '__main__':
	c = Client()
	c.enter_id()