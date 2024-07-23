import os
import sys
import argparse
import logging
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, EnvironmentCredential
from azure.containerregistry import ContainerRegistryClient
from date_time import date_time
from azure_resource_graph_query import validate_input_acr_name
from azure.core.exceptions import HttpResponseError, ClientAuthenticationError


def return_acr_endpoint(acr_name:str):
	"""
	Function returns acr url from its name
	:param acr_name:
	:return:
	"""
	acr_endpoint = f'https://{acr_name.lower()}.azurecr.io'
	return acr_endpoint


def list_image_tag_details(acr_name: str):
	"""
	list the images and total tag counts per images
	:param acr_name:
	:return:
	"""
	credential = EnvironmentCredential()

	repositories = get_image_names_from_acr(acr_name=acr_name)
	acr_url = return_acr_endpoint(acr_name=acr_name)
	print(f'Image details will be fetched from : {acr_url}')
	# validate acr input
	valid = validate_input_acr_name(acr_name=acr_name)

	# Image - tag count
	image_tag_count = {}
	client = ContainerRegistryClient(endpoint=acr_url, credential=credential)
	for repository in repositories:
		tags_list = []
		# print(f'image name is: {acr_url}/{repository}')
		# print(f'available tags are:')
		for tag in client.list_tag_properties(repository = repository):
			tag_details = {}
			# print(f'Image name : {repository}')
			# print(f'Tag name : {tag.name}')
			tag_details['tag_name'] = tag.name
			created_on = tag.created_on
			fmt_date = date_time(created_on)
			tag_details['tag_created_on'] = fmt_date
			# print(f'Tag created on {fmt_date}')
			tag_sha = tag.digest
			tag_details['tag_sha'] = tag_sha
			tags_list.append(tag_details)
			# print(f'{"*" * 50}')
		image_tag_count[repository] = tags_list

	return image_tag_count # dictionary with key as image name and value as available tag and details


def get_image_names_from_acr(acr_name: str):
	"""
	this will be used to pull image details from acr
	:param acr_name:
	:return:
	"""
	try:
		acr_url = return_acr_endpoint(acr_name=acr_name)

		# define credentials
		credential= EnvironmentCredential()
		client = ContainerRegistryClient(endpoint= acr_url, credential= credential)

		repository_list = []
		# List all images in acr
		repository_names = client.list_repository_names()
		# print(repository_names)
		for repository in repository_names:
			# print(repository)
			repository_list.append(repository)

		return repository_list

	except ClientAuthenticationError:
		logging.error("Authentication failed. Please check your credentials.")
		return {"error": "Authentication failed. Please check your credentials."}

	except HttpResponseError as e:
		logging.error(f"HTTP error occurred: {e.response.status_code} {e.response.reason}")
		return {"error": f"HTTP error occurred: {e.response.status_code} {e.response.reason}"}

	except Exception as e:
		logging.error(f"An unexpected error occurred: {str(e)}")
		return {"error": f"An unexpected error occurred: {str(e)}"}


def main():
	"""
	to run main function
	:return:
	"""
	parser = argparse.ArgumentParser("To fetch image details from Azure container registry")
	parser.add_argument("--acr_name", help="Azure container registry name", type=str, required=True)

	args = parser.parse_args()

	acr_name = args.acr_name
	load_dotenv()
	# return_acr_endpoint(acr_name=acr_name)
	# get_image_names_from_acr(acr_name=acr_name)
	image_tag_count = list_image_tag_details(acr_name=acr_name)
	# print(image_tag_count)

if __name__ == "__main__":
	main()