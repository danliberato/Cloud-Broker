from __future__ import print_function # Python 2/3 compatibility
import boto3
import os

class ProviderTable():
	
	def createTable(client):
		table = client.create_table(
			TableName='Provider',
			KeySchema=[
				{
					'AttributeName': 'id',
					'KeyType': 'HASH'  #Sort key
				}
			],
			AttributeDefinitions=[
				{
					'AttributeName': 'id',
					'AttributeType': 'N'
				}
			],
			ProvisionedThroughput={
				'ReadCapacityUnits': 5,
				'WriteCapacityUnits': 5
			}
		)
		return table
