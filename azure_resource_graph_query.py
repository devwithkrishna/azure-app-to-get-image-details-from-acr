from azure.identity import DefaultAzureCredential, EnvironmentCredential
import azure.mgmt.resourcegraph as arg
import logging
import os
import sys
from dotenv import load_dotenv
import streamlit as st

def run_azure_rg_query():
    """
    Run a resource graph query to get the acr details
    :return: subscription_id str
    """
    credential = EnvironmentCredential()
    # Create Azure Resource Graph client and set options
    arg_client = arg.ResourceGraphClient(credential)

    query = f"""
             resources 
            | where type == "microsoft.containerregistry/registries"
            | project name
            """

    print(f"query is {query}")

    # Create query
    arg_query = arg.models.QueryRequest(query=query)

    # Run query
    arg_result = arg_client.resources(arg_query)

    # Show Python object
    acr_details_from_query = arg_result.data
    return acr_details_from_query

def validate_input_acr_name(acr_name: str):
    """
    validate the input acr name
    :param acr_name:
    :return:
    """
    acr_details_from_query= run_azure_rg_query()
    # Convert all elements to lowercase
    acr_details_from_query_list = [item['name'].lower() for item in acr_details_from_query]

    acr = acr_name.lower()

    if acr in acr_details_from_query_list:
        print(f"{acr} is valid.")
    else:
        print(f"ACR {acr} can not be found in azure")
        # displaying error in streamlit ui
        st.text(f"Azure container resistry with name '{acr}' can not be found in azure 🚫")
        st.text(f"Please verify & provide right ACR name")
        sys.exit(f"Error: ACR {acr} can not be found in azure")
        return False


def main():
    """
    To test the script
    :return:
    """
    load_dotenv()
    logging.info("ARG query being prepared......")
    acr = run_azure_rg_query()
    logging.info("ARG query Completed......")


if __name__ == "__main__":
    main()