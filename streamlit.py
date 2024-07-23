import streamlit as st
import os
import json
from acr_images import *
from dotenv import load_dotenv

def get_data_from_acr(acr_name: str):
	"""
	Image details from azure container registry
	:param acr_name:
	:return:
	"""
	image_details = list_image_tag_details(acr_name=acr_name)
	with st.container():
		st.write(f'Total number of images available in "{acr_name}" ACR - :hash:{len(image_details)}')
		st.write(f'The image details are as follows: :arrow_heading_down:')

		# Convert the dictionary to a JSON string
		json_string = json.dumps(image_details, indent=4)
		# print(json_string)
		st.json(json_string)


	st.write(f'Thanks for visiting :crossed_fingers:')
# Add footer at the end of the page
	st.markdown("""
	<style>
	.footer {
	    position: fixed;
	    bottom: 0;
	    left: 0;
	    width: 100%;
	    text-align: center;
	    background-color: #000000;  /* Set background color to black */
	    padding: 10px;
	    font-size: 14px;
	    color: white;  /* Set text color to white */
	}
	.footer a {
	    color: white; /* Link color */
	    text-decoration: none; /* Remove underline from link */
	    font-weight: bold; /* Make text bold */
	}
	</style>
	<div class="footer">
	    This is built & maintained by <a href="mailto:krishnadhasnk1997@gmail.com,krishnadhas@devwithkrishna.in"><strong>githubofkrishnadhas</strong></a>
	</div>
	""", unsafe_allow_html=True)


def main():
	"""
	run the code
	:return:
	"""
	load_dotenv()
	st.header("Azure Container Registry Image Details",divider='rainbow')

	acr_name = st.text_input("Enter Azure Container Registry Name:")

	if st.button("Submit"):
		st.session_state.acr_name = acr_name
		st.rerun()

	# Check if acr_name is stored in session state
	if 'acr_name' in st.session_state:
		print(f'Received input as {st.session_state.acr_name}')
		st.write(f"You have provided the input : {st.session_state.acr_name}")
		get_data_from_acr(acr_name=st.session_state.acr_name)



if __name__ == "__main__":
	main()
