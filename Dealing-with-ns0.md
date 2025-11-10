# Dealing with ns0: Namespace

> The following is a Slack post from October 20205...  

Kayla Reed. 
  9:05 AM. 
From Exlibris: But we created an XSL normalization rule that removes the "ns0:" prefix in any DC field where it exists.  
The rule is named "DC_ns0:_prefix_delete"; you can check it in the MDE.  
We also created a DC normalization process in the "DigitalGrinnell Qualified DC" profile, named "delete DC ns0: prefix".  
This process can be found when you open Admin > Run a job. This normalization job needs to be run on the records of the "DG_Collection" set.  
This will correct the prefixes in all the affected fields.  
But please note that the "DG_Collection" has a couple of MARC21 records:  
- 991011505711304641
- 991011505711204641
- 991011505711104641
- 991011504611004641
- 991011504610904641

During the normalization job run, one bulk (100 records) will fail when these records are present, which will result in 100 records with exceptions in the job report. This is because the normalization rule is written to handle DC records and cannot process MARC21 records.
When this happens, the failed records should be exported, and those MMS IDs should be removed from the list. Then, a new itemized set should be created with the remaining 95 records, and the normalization job should be initiated on them to correct the ns0: namespace in the remaining DC records.  
After the normalization jobs finish, the "DG OAI harvest - advanced" publishing profile will need to be republished with the rebuild entire index option.  
Once it is finished, the OAI set in this link should have no issue displaying all the dc:, dc:terms and the local DC fields:  
https://libweb.grinnell.edu/oai/?verb=ListRecords&metadataPrefix=oai_qdc&set=DG2. 

Please confirm this once you have completed all the steps, or let us know if you'd like us to do it.  
Best regards,  
Adam

> Action was taken on November 7 to run the job as specified above.  Process ID 7640734270004641 has the results which included exactly 100 errors out of 11849 records processed.  