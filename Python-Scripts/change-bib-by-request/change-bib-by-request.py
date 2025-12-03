# Lifted from https://developers.exlibrisgroup.com/forums/topic/anyone-having-issues-putting-a-bib-record/

import requests
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os
from pprint import pprint
import datetime

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

    # Make changes here... return FALSE if no changes are made
    root = make_changes(root, namespaces)
    if root is False:
        msg = f"\n  No changes needed in bib record {mmsid}.\n"
        print(msg)
        bib_log_file.write(msg)
        return
    
    # Convert the ElementTree back to bytes
    xml_bytes = ET.tostring(root)
    
    # Before putting the XML back, we need to register the default namespace.  This is necessary to ensure that the XML is well-formed and valid
    # We need to set the default namespace to the one used in the XML string
    # ET.register_namespace('', 'http://alma.exlibrisgroup.com/dc/01GCL_INST')
    # ET.register_namespace('grin', 'http://alma.exlibrisgroup.com/dc/01GCL_INST')
            
    # And put it back
    headers = {'Accept': 'application/xml', 'Content-Type': 'application/xml; charset=utf-8'}
    response = requests.put(f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/{mmsid}?validate=true&override_warning=true&override_lock=true&stale_version_check=false&check_match=false&apikey={api_key}", headers=headers, data=xml_bytes)    
    
    # If the response is NOT successful, print the status code the response text
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        bib_log_file.write(f"\n\nBib record {mmsid} NOT updated. Status code: {response.status_code}\n")
        bib_log_file.write(f"\n\nResponse text:\n")
        bib_log_file.write(response.text)
    else:  # If the response is successful, print the status code and a success message
        print(f"\n\nBib record {mmsid} updated successfully with status code {response.status_code}.\n")
        bib_log_file.write(f"\n\nBib record {mmsid} updated successfully with status code {response.status_code}.\n")
        
        
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
    
    # Print the dcterms:identifier elements with their attributes
    for identifier in dcterms_identifiers:
        print(identifier.tag, identifier.text, sep=':', end='\n', flush=False)
        for key, value in identifier.attrib.items( ):
            print(f"  attribute={key}: {value}", end='\n', flush=False)
    
    print(f"\nThe {len(root.findall('.//dc:identifier', namespaces))} dc:identifier elements are:")

    # Fetch all the dc:identifier elements in the xml_string
    dc_identifiers = root.findall('.//dc:identifier', namespaces)
    
    # Print the dc:identifier elements
    for identifier in dc_identifiers:
        print(identifier.tag, identifier.text, sep=':', end='\n', flush=False)
        for key, value in identifier.attrib.items( ):
            print(f"  attribute={key}: {value}", end='\n', flush=False)
    
    # If we have a dc:identiier handle with a dcterms:URI attribute, REMOVE the dcterms:URI attribute and we are done!
    # Note that the dcterms:URI attribute is not needed in the dc:identifier element and was left from an earlier version of the code
    attrib_target = '{http://www.w3.org/2001/XMLSchema-instance}type'
    for identifier in dc_identifiers:
        if identifier.text.startswith("http://hdl.handle.net/") and identifier.attrib.get(attrib_target) == 'dcterms:URI':
            # If it has a dcterms:URI attribute, remove it      
            identifier.attrib.pop(attrib_target, None)
            # Change the dcterms:identifier tag to dc:identifier
            has_handle = True
            # Log the change
            msg = f"\n  Removed dcterms:URI attribute from {identifier.text}"
            bib_log_file.write(msg)
            print(msg)
            return root

    # If any of the remaining dc:identifer elements start with "http://hdl.handle.net/", set has_handle to True and return False, no changes needed
    for identifier in dc_identifiers:
        if identifier.text.startswith("http://hdl.handle.net/"):
            # If we have a handle, set has_handle to True and return False, no changes needed
            has_handle = True
            return False
      
    # If we have a dcterms:identiier handle, set has_handle to True, change the dcterms:identifier tag to dc:identifier, REMOVE the dcterms:URI attribute, and we are done!
    for identifier in dcterms_identifiers:
        if identifier.text.startswith("http://hdl.handle.net/"):
            # Remove the dcterms:URI attribute
            identifier.attrib.pop(attrib_target, None)
            # Change the dcterms:identifier tag to dc:identifier
            identifier.tag = 'dc:identifier'
            has_handle = True
            # Log the change
            msg = f"\n  Changed dcterms:identifier to dc:identifier for {identifier.text}"
            bib_log_file.write(msg)
            print(msg)
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
                # Set has handle to True to avoid duplicates
                has_handle = True     
                return root

            # If it starts with "dg_", save the numeric part and discard the rest
            elif identifier.text.startswith("dg_"):
                # Extract the numeric part of the identifier
                numeric_part = identifier.text.split('_')[1]
                # Update the field to carry our Handle
                identifier.text = f"http://hdl.handle.net/11084/{numeric_part}"
                has_handle = True
                return root
                
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
        with open('/Users/mcfatem/GitHub/all-things-Alma/Python-Scripts/mms_ids.csv', 'r') as file:  
            for line in file:
                # If value is numeric, add it to the list
                if line.strip( ).isdigit( ):
                    # Append the MMS ID to the list
                    mms_ids.append(line.strip( ))
                
        
        # Where the rubber meets the road...
        # -----------------------------------------------------------------------
        for mms_id in mms_ids:  
            # Print the MMS ID to the log file with a timestamp
            timestamp = datetime.datetime.now( ).strftime("%Y-%m-%d %H:%M:%S")
            # Write the timestamp and MMS ID to the log file
            msg = f"\n{timestamp} - Processing MMS ID: {mms_id}"
            print(msg)
            bib_log_file.write(msg)
            
            # Call the get_and_put function with the API key and MMS ID
            get_and_put(ALMA_API_KEY, mms_id)
        
        msg = f"\nThat's a wrap!"
        print(msg)
        bib_log_file.write(msg)
