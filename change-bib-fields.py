# change-bib-fields.py
# 
# This script uses https://github.com/Digital-Grinnell/almapipy to fetch a bib record and apply specific field
# changes using Python.
#
## See https://docs.python-guide.org/scenarios/xml/
#
## For Alma API handling see... https://github.com/Digital-Grinnell/almapipy

# import community packages
from almapipy import AlmaCnxn as AlmaAPIConn
import json
import xml.dom.minidom
from xml.etree import ElementTree as ET

# import csv, os, argparse, gspread, json
# import polars as pl
# import urllib.parse
# from datetime import datetime
# from almapipy import AlmaCnxn as AlmaAPIConn
# from pathlib import Path

# import my packages
import constant

# initialize some stuff
alma_api = None
api_log_file = None

#----------------------------------------------------------------------
# pretty_print_xml is a function that takes an XML string as input and returns a pretty-printed version of the XML.
#
def pretty_print_xml(xml_string):
    dom = xml.dom.minidom.parseString(xml_string)
    return dom.toprettyxml( )

#----------------------------------------------------------------------
# bibs_catalog_get(mms_id)
#
# # This function uses the Alma API to get a bib record by its mms_id.
# The bib record is returned as a Python dictionary.
#
# The bib record is a dictionary with the following keys:
#   'mms_id': The mms_id of the bib record.
#   'title': The title of the bib record.
#
def bibs_catalog_get(mms_id):
    try:
        bib_record = alma_api.bibs.catalog.get(mms_id)
        if constant.DEBUG:
          print(json.dumps(bib_record, indent=4))
        # Find the 'anies' key in the bib record
        if 'anies' in bib_record:
            # Pretty print the 'anies' list XML record  
            print("Found 'anies' key in the bib record:")
            pretty_xml = pretty_print_xml(bib_record['anies'][0])
            print(pretty_xml)
        else:
            print("No 'anies' key found in the bib record.")    
            
    except Exception as e:
        exit(f'Alma bib.catalog.get exception: {e}')
    
    return bib_record

#----------------------------------------------------------------------
# bibs_catalog_post(mms_id, bib_record)
#
def bibs_catalog_post(mms_id, bib_record):
    try:
        alma_api.bibs.catalog.post(mms_id, bib_record)
        if constant.DEBUG:
            print(bib_record, sep=' ', end='\n', flush=False)
    except Exception as e:
        exit(f'Alma bib.catalog.post exception: {e}')
    return bib_record

## === MAIN ======================================================================================

log_filename = 'change-bib-fields.log'
with open(log_filename, 'w') as bib_log_file:

    # Open the Alma API
    try: 
        alma_api = AlmaAPIConn(constant.ALMA_API_KEY, data_format='json')
        msg = "\nAlma API connection is now open for bibs"
        print(msg)
    except:
        exit('Alma API connection failed!')
    
    # Open and examine one bib record
    mms_id = "991011592841304641"
    bib_record = bibs_catalog_get(mms_id)
    xml_string = bib_record['anies'][0]
  
    has_handle = False  

    # Parse the XML string into an ElementTree object
    root = ET.fromstring(xml_string)

    # Fetch all the dcterms:identifier elements in the xml_string
    # The namespace is defined in the XML string, so we need to register it
    namespaces = {'dcterms': 'http://purl.org/dc/terms/', 'dc': 'http://purl.org/dc/elements/1.1/'}
    # Register the namespaces
    for prefix, uri in namespaces.items( ):
        ET.register_namespace(prefix, uri)
    
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
        
    # If we have a handle, set has_handle to True, save the dcterms:identifier as a new dc:identifier, and we are done for now
    for identifier in dcterms_identifiers:
        if identifier.text.startswith("http://hdl.handle.net/"):
            # If we have a handle, set has_handle to True, save the dcterms:identifier as a new dc:identifier, and break out of the loop
            has_handle = True
            # Create a new field with the same value as the dcterms:identifier
            new_field = ET.Element('dc:identifier', namespaces=namespaces)
            new_field.text = identifier.text
            # Append the new field to the bib record
            root.append(new_field)
            break       
    
    # If we don't have a handle, loop on all the dc:identifier fields in the bib record
    if not has_handle:   
        # Loop on all the dc:identifier fields in the bib record
        for identifier in dc_identifiers:
            if identifier.text.startswith("alma:"):
                continue
            # If it starts with "grinnell", save the numeric part and discard the rest
            elif identifier.text.startswith("grinnell:"):
                # Extract the numeric part of the identifier
                numeric_part = identifier.text.split(':')[1]
                # Update the field to carry our Handle
                identifier.text = f"http://hdl.handle.net/11084/{numeric_part}"
                # Print the updated field
                print(identifier.tag, identifier.text, sep=':', end='\n', flush=False)
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
                # Print the updated field
                print(identifier.tag, identifier.text, sep=':', end='\n', flush=False)
                # Now, put the new field back into the bib record
                root.append(identifier)  
                # Set has handle to True to avoid duplicates
                has_handle = True
                
    # Pretty print the updated XML string
    xml_string = ET.tostring(root, encoding='unicode', default_namespace='http://alma.exlibrisgroup.com/dc/01GCL_INST')
    pretty_xml = pretty_print_xml(xml_string)
    print(f"\nThe updated XML string is:\n{pretty_xml}")
                
        
    # Now, if the bib has a handle, update the bib record in Alma
    if has_handle:
        bib_record['anies'][0] = xml_string
        # Post the updated bib record to Alma
        result = bibs_catalog_post(mms_id, bib_record)
        # Print the updated bib record
        print(result, sep=' ', end='\n', flush=False)
        # Print a message indicating the bib record was updated
        msg = f"Bib record {mms_id} was updated with a new Handle dc:identifier."
        print(msg, sep=' ', end='\n', flush=False)
    else:
        # Print a message indicating the bib record was not updated
        msg = f"Bib record {mms_id} was not updated because it does not have a handle."
        print(msg, sep=' ', end='\n', flush=False)


    msg = f"\nThat's a wrap!"
    print(msg)
    bib_log_file.write(msg)
            
    # Close the Alma API
    try:
        alma_api.close( )
        msg = "\nAlma API connection is now closed."
        print(msg)
    except:
        exit('Alma API connection close failed!')
    
    # Close the log file
    bib_log_file.close( )
    msg = f"\nThe log file {log_filename} is now closed."
    print(msg)
    
    # Print a message indicating the script has finished
    msg = f"\nThe script has finished."
    print(msg)
    
