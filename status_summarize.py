#!/usr/bin/python
from __future__ import print_function
from alchemyapi import AlchemyAPI
import json
from get_twitter_graph import getStatus
import sys

alchemyapi = AlchemyAPI()

def get_Status_Concepts(status):
	response = alchemyapi.concepts('text', status)

	if response['status'] == 'OK':
		print('')
		print('## Concepts ##')
		for concept in response['concepts']:
			print('text: ', concept['text'] + ' ' + concept['relevance'])
		return response['concepts']
	else:
		print('Error in concept tagging call: ', response['statusInfo'])
		return None

def get_Status_Categories(status):
	response = alchemyapi.category('text',status)

	if response['status'] == 'OK':
		print('')
		print('## Category ##')
		print('text: ', response['category'] + ' ' + response['score'])
		return response
	else:
		print('Error in text categorization call: ', response['statusInfo'])
		return None

if __name__ == "__main__":
	if len(sys.argv)>1:
		twitterid = int(sys.argv[1])
	else:
		twitterid = 66690578

	statuses = getStatus(twitterid)
	concepts = get_Status_Concepts(statuses)
	categories = get_Status_Categories(statuses)



