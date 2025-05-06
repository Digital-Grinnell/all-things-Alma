# Lifted from https://developers.exlibrisgroup.com/forums/topic/anyone-having-issues-putting-a-bib-record/

import requests
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os
from pprint import pprint

# This script is designed to get a bib record from Alma, modify it, and then put it back.
# It uses the Alma API to perform these operations.
# It requires the requests library and the xml.etree.ElementTree module for XML parsing.
# It also uses the dotenv library to load environment variables from a .env file.

# get_and_put(api_key, mmsid)
#
# The get_and_put function takes an API key and a MMS ID as arguments.
# ----------------------------------------------------------------------------
def get_and_put(api_key, mmsid):
    # Get the bib record
    headers = {'Accept': 'application/xml'}
    response = requests.get(f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{mmsid}?view=full&expand=None&apikey={api_key}", headers=headers)
    
    # Parse the XML response into an ElementTree
    root = ET.fromstring(response.text)

    # Fetch all the dcterms:identifier elements in the xml_string
    # The namespace is defined in the XML string, so we need to register it for validation
    namespaces = {'dcterms': 'http://purl.org/dc/terms/', 'dc': 'http://purl.org/dc/elements/1.1/'}
    # Register the namespaces
    for prefix, uri in namespaces.items( ):
        ET.register_namespace(prefix, uri)

    # Make changes here...
    root = make_changes(root, namespaces)
    
    # Convert the ElementTree back to bytes
    xml_bytes = ET.tostring(root)
    
    # And put it back
    headers = {'Accept': 'application/xml', 'Content-Type': 'application/xml; charset=utf-8'}
    response = requests.put(f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{mmsid}?validate=false&override_warning=true&override_lock=true&stale_version_check=false&check_match=false&apikey={api_key}", headers=headers, data=xml_bytes)
    
    # If the response is NOT successful, print the status code the response text
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
    else:  # If the response is successful, print the status code and a success message
        print(f"Bib record {mmsid} updated successfully with status code {response.status_code}.")
        
    

# Check if the root element is a <bib> element
#
# check_for_bib_tag(root)
# ----------------------------------------------------------------------------
def check_for_bib_tag(root):
    # Check if the root element is a <bib> element
    if root.tag != 'bib':
        # If not, create a new <bib> element and append the original root element to it
        new_root = ET.Element('bib')
        new_root.append(root)
        return new_root
    else:
        # If it is already a <bib> element, return the original root element
        return root

  
# This function is a placeholder for making changes to the XML tree.
# You can modify this function to make specific changes to the XML structure.
# For example, you can add or remove elements, change text values, etc.
#
# make_changes(root)
# ----------------------------------------------------------------------------
def make_changes(root, namespaces):
    has_handle = False
    
    # Check if the root element is a <bib> element
    root = check_for_bib_tag(root)

    # Print some information about the XML string
    print(f"\nThe XML string has been parsed into an ElementTree object.")
    print(f"The XML string has {len(root)} elements.")
    print(f"The XML string has {len(root.findall('.//dcterms:identifier', namespaces))} dcterms:identifier elements.")
    print(f"The XML string has {len(root.findall('.//dc:identifier', namespaces))} dc:identifier elements.")
    
    print(f"\nThe {len(root.findall('.//dcterms:identifier', namespaces))} dcterms:identifier elements are:")
    
    # Fetch all the dcterms:identifier elements in the xml_string   
    dcterms_identifiers = root.findall('.//dcterms:identifier', namespaces) 
    # Print the dcterms:identifier elements
    for identifier in dcterms_identifiers:
        print(identifier.tag, identifier.text, sep=':', end='\n', flush=False)
    
    print(f"\nThe {len(root.findall('.//dc:identifier', namespaces))} dc:identifier elements are:")

    # Fetch all the dc:identifier elements in the xml_string
    dc_identifiers = root.findall('.//dc:identifier', namespaces)
    # Print the dc:identifier elements
    for identifier in dc_identifiers:
        print(identifier.tag, identifier.text, sep=':', end='\n', flush=False)
        
    # If we have a dcterms:identiier handle, set has_handle to True, save the dcterms:identifier as a new dc:identifier, and we are done!
    for identifier in dcterms_identifiers:
        if identifier.text.startswith("http://hdl.handle.net/"):
            # If we have a handle, set has_handle to True, save the dcterms:identifier as a new dc:identifier, and break out of the loop
            has_handle = True
            # Create a new field with the same value as the dcterms:identifier
            new_field = ET.Element('dc:identifier', namespaces=namespaces)
            new_field.text = identifier.text
            # Append the new field to the bib record and return the new root
            root.append(new_field)
            return root
    
    # If we don't have a handle now, loop on all the dc:identifier fields in the bib record
    if not has_handle:   
        # Loop on all the dc:identifier fields in the bib record
        for identifier in dc_identifiers:
            # If we have a handle, break out of the loop... no use creating duplicates
            if has_handle:
                break
            
            if identifier.text.startswith("alma:"):
                continue
            # If it starts with "grinnell", save the numeric part and discard the rest
            elif identifier.text.startswith("grinnell:"):
                # Extract the numeric part of the identifier
                numeric_part = identifier.text.split(':')[1]
                # Update the field to carry our Handle
                identifier.text = f"http://hdl.handle.net/11084/{numeric_part}"
                # # Print the updated field
                # print(identifier.tag, identifier.text, sep=':', end='\n', flush=False)
                # Now, put the new field back into the bib record
                root.append(identifier)  
                # Set has handle to True to avoid duplicates
                has_handle = True     
                
            # If it starts with "dg_", save the numeric part and discard the rest
            elif identifier.text.startswith("dg_"):
                # Extract the numeric part of the identifier
                numeric_part = identifier.text.split('_')[1]
                # Update the field to carry our Handle
                identifier.text = f"http://hdl.handle.net/11084/{numeric_part}"
                # # Print the updated field
                # print(identifier.tag, identifier.text, sep=':', end='\n', flush=False)
                # Now, put the new field back into the bib record
                root.append(identifier)  
                # Set has handle to True to avoid duplicates
                has_handle = True
                
    # Pretty print the updated XML string
    # xml_string = ET.tostring(root, encoding='unicode', default_namespace='http://alma.exlibrisgroup.com/dc/01GCL_INST')   
    xml_string = ET.tostring(root, encoding='unicode')   
    print(f"\nThe updated XML string is:\n")
    pprint(xml_string, indent=4)

    return root
    

# This is the main function that runs the script.
if __name__ == "__main__":

    log_filename = 'change-bib-by-request.log'
    with open(log_filename, 'w') as bib_log_file:

        # Initialize some stuff
        # -----------------------------------------------------------------------
        load_dotenv( )
        DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
        ALMA_API_KEY = os.getenv('ALMA_API_KEY')
        if not ALMA_API_KEY:
            exit('ALMA_API_KEY is not set in the environment variables.')
        ALMA_API_REGION = os.getenv('ALMA_API_REGION')
        if not ALMA_API_REGION:
            exit('ALMA_API_REGION is not set in the environment variables.')

        # Read all the MMS IDs from the file    
        # -----------------------------------------------------------------------
        mms_ids = []
        with open('mms_ids.csv', 'r') as file:      
            for line in file:
                # Strip whitespace and newline characters from each line
                mms_ids.append(line.strip())
                
        
        # Where the rubber meets the road...
        # -----------------------------------------------------------------------
        for mms_id in mms_ids:  
            # Print the MMS ID to the log file
            msg = f"\nProcessing MMS ID: {mms_id}"
            print(msg)
            bib_log_file.write(msg)
            
            # Call the get_and_put function with the API key and MMS ID
            get_and_put(ALMA_API_KEY, mms_id)
        
        msg = f"\nThat's a wrap!"
        print(msg)
        bib_log_file.write(msg)
