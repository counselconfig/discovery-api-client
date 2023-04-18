import unittest
import requests
import re
import json
import tracemalloc
import sys
from main import Client



tracemalloc.start() # supresses warning

# all pass

"""
----------------------------------------------------------------------
Ran 10 tests in 1.731s

OK
"""

#create new instances for isolated log test
class client_log_error_tests(unittest.TestCase): 
# exception test
	def test_get_record(self): #auto generates a client log file in the root with a status 500 error 
		# provide base url without query parameter
		Client.get_record("http://discovery.nationalarchives.gov.uk/API/records/v1/details/")
		self.assertRaises(requests.exceptions.HTTPError)	
		
	def test_json_format(self): #auto generates a client log file with details of the incorrect json fomat
		jpath_dr = "./test_data/incorrect_format.json"
		Client.open_json(jpath_dr)
		self.assertRaises(Exception)	

class client_tests(unittest.TestCase):
# preprocessing description test
	def test_remove_tags(self): 
		
		test_cleaned = "British Honduras, later Belize, Acts "
		test_tags = "<scopecontent><p>British Honduras, later Belize, Acts </p></scopecontent>"  # id C345456
		cleaned = Client.remove_tags(test_tags)
		m = "cleaned and test_cleaned not equal" # if fail
		self.assertEqual(cleaned, test_cleaned, m)


# insufficient test
	def test_display_not_sufficient_info(self): 
		# load dummy data file 
		with open("./test_data/display_not_sufficient_info.json") as f: 
			json_object = json.load(f)
			f.close() 
		not_sufficient = Client.display_not_sufficient_info(json_object)
		m = "not_suffient is not None"
		self.assertIsNone(not_sufficient, m)

# reference test
	def test_display_reference(self): 
		# load dummy data file 
		with open("./test_data/display_reference.json") as f: 
			json_object = json.load(f)
			f.close()
		citableReference = Client.display_reference(json_object)
		test_citableReference = "AA 10/10/TEST 1/100"
		m = "citableReference and test_citableReference not equal"
		self.assertEqual(citableReference, test_citableReference, m)


# description test
	def test_scopeContent_description(self): 
		url = "http://discovery.nationalarchives.gov.uk/API/records/v1/details/C169097"
		response = requests.get(url)
		json_object = response.json()
		description = Client.display_description(json_object)
		test_description = "Booby traps"
		m = "description and test_description not equal"
		self.assertEqual(description, test_description, m)


# title test
	def test_title(self): 
		url = "https://discovery.nationalarchives.gov.uk/API/records/v1/details/2f88d18a-ce2c-4671-9fb3-eebb8cf06a04"
		response = requests.get(url)
		json_object = response.json()
		title = Client.display_title(json_object)
		test_title = "Hampton Court Estate"
		m = "title and test_title not equal"
		self.assertEqual(title, test_title, m)


# status code test
	def test_record_exists(self): 
		# pass dummy no record information asset id to return status code 204
		mock_url = "https://discovery.nationalarchives.gov.uk/API/records/v1/details/C17865452" 
		response = requests.get(mock_url)
		sc = Client.display_no_record_found(response) # return status code
		test_sc = 204
		m = "sc and test_sc have different codes"
		self.assertEqual(sc, test_sc, m)


# get record test
	def test_get_record(self):
		no_http_error = Client.get_record("https://discovery.nationalarchives.gov.uk/API/records/v1/details/N17865452") # should be true allowing GET request less than 500
		m = "no_http_error is true"
		self.assertTrue(no_http_error, m)
		
	
# validate id test
	def test_validate(self):
		true = Client.validate("a147aa58-38c5-45fb-a340-4a348efa01e6") #pass guid conformant id
		self.assertTrue(true)

# display test
	def test_display(self):
		test_url = "https://discovery.nationalarchives.gov.uk/API/records/v1/details/a147aa58-38c5-45fb-a340-4a348efa01e6"
		url = Client.display("2513a7ba-728a-4cc8-9c1a-0877be57710b")
		m = "url and test_url not equal"
		self.assertNotEqual(url, test_url)


if __name__ == '__main__':
    unittest.main()