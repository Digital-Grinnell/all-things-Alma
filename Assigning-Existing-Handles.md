# Assigning Existing Handles to Alma Records

The workflow suggested by agent Sabine in December 2025...

Workflow for new digital titles without handles:
1. Create a set with the digital titles that need to receive a handle.
2. Run the Handle integration profile on this set with the following option:
DC METADATA Upon Create = Add new Handles to Metadata


The earlier workflow suggested by support agent Anchi Hsu is...  

1. Create a title set that already includes a handle identifier. (record 991011592645304641 is the only member of set 7333418150004641)  
2. Admin > Run a job > search name: Copy dcterm to dcidentifier > wait for it to finish, and go to the next step (ran process ID 7333418330004641)  
3. Admin > Run a job > search name: DG Handle Migration > wait for it to finish, and go to the next step (ran process ID 7333418800004641)  
4. Configuration > General > Integration Profile > Persistent Handle Identifiers for Digital Resource > Actions > Run  

## Workflow with Screen Captures

That workflow in practice looks something like this:  

1) Build an itemized set of titles from a list of MMS IDs.  In my case the set named `Handles - First Batch from mms_ids.csv` was created with 6040 digital titles.  

2) Next, as suggested `Admin` > `Run a job` find the `Copy dcterm to dc:identifier` job and run it with the set defined above.  The suggested process would looked like this...

![Run the "Copy dcterm to dc:idenfifier" job](<./Documents/Screenshot 2025-05-08 at 9.39.16 AM.png>)

![Select New Set for the Job](<./Documents/Screenshot 2025-05-08 at 9.41.09 AM.png>)

### Some Records Skipped

If our `change-bib-by-request` process is not run ahead of step 2 all records may not have the necessary `dc.identifier`: `http://hdl.handle.net/11084...` value.  In this instance I had to run `change-bib-by-request.py` which produced the attached [change-bib-by-request.log](./Documents/change-bib-by-request.log) file for review.  It shows no errors.  

Once the script and subsequent job are complete and successful proceed to step 3.

3) From `Admin` > `Run a job` find the `DG Handle Migration` job, edit it to include the set defined in step 1, and run it like so...
 
![Setup the "DG Handle Migration" job](<./Documents/Screenshot 2025-05-08 at 9.46.20 AM.png>)

![Select Our Set](<./Documents/Screenshot 2025-05-08 at 1.18.30 PM.png>)

Submit the job and when it is complete and successful proceed to step 4

**Attention: There was indication of a problem here.  Many of the records did NOT process successfully because of the condition illustrated below.

The `dc:identifier` field should NOT have a `dcterms:URI` attribute!  Those attributes need to be removed before handle assignment will work!  

Once that error was corrected the results were...  

![Some Records Skipped](<./Documents/Screenshot 2025-05-08 at 1.22.38 PM.png>)  

Examining some of the 99 skipped records shows statements consistent with...  

```
Record 991011592644004641 was skipped. Reason: BIB record MMS ID 991011592644004641 already has a handle identifier 11084/34662	05/08/2025 13:21:24 CDT	Information	Repository	System  2 	
Record 991011592643604641 was skipped. Reason: BIB record MMS ID 991011592643604641 already has a handle identifier 11084/34664	05/08/2025 13:21:24 CDT	Information	Repository	System  3
```

...and those records do indeed already have working handles.  So, it's all good!  

4) The final step from `Configuration` > `General` > `Integration Profile` > `Persistent Handle Identifiers for Digital Resource` > `Edit` > `Actions` > `Run` appears to work **AFTER** editing the `Set name`, like so...  

![Be Sure to Edit the Set Name!](<./Documents/Screenshot 2025-05-08 at 1.27.56 PM.png>)

Once the run completed the event report showed this:  

![99 Complete?](<./Documents/Screenshot 2025-05-08 at 1.33.53 PM.png>)  

So, it looks like the workflow keeps processing ONLY the 99 records that were completed a couple of days ago?  


# Update

I started to run the entire 4-step workflow again, process ID 7337283030004641, this time using the full set of digital titles from set 7337283030004641... and after step 3, running the `DG Handle Migration Job`, I got this result:  

![All Skipped?](<Documents/Screenshot 2025-05-08 at 4.06.10 PM.png>)  

The report says that all 11,442 records were skipped because they already have handles.  Ok, so I started checking them again, spot checking about a dozen handles from various pages... AND THEY ALL WORK!   

I am thrilled with this outcome, but still wondering why this didn't work on the previous attempt?   For future reference I would dearly love to know if the 4-step sequence is correct, or is one of those steps out-of-order?  

# Resolved

I received this follow-up on the morning of May 12, 2025, and it confirms my suspicion that some operations were performed out-of-order.    

```
A new comment has been added to case  07949018.

Case Title: Alma Chat - handle identifier request
Last Comment:
Dear Mark,
My name is Sabine. I work in the Alma Tier 2 Support Team and took over responsibility for your case.
I reviewed this case several times with Anchi.
I read through all the comments and checked the attached PDF file.
When I looked at the job history for 08/05/2025, I found that 3 jobs have been performed on a set with 11442 records.
I assume this is the set "All Digital Titles in DCAP01 Format"
1. job = Job 7336725260004641 = Handle integration
Submitted at 05/08/2025 14:09:45 CDT
2. job = 7337053600004641 = Copy dcterm to dcidentifier - All Digital Titles in DCAP01 Format - 05/08/2025 15:50:53 CDT
Submitted at 05/08/2025 15:50:56 CDT
3. job = 7337283030004641 = DG Handle Migration - All Digital Titles in DCAP01 Format - 05/08/2025 15:56:22 CDT
Submitted at 05/08/2025 15:56:26 CDT

The correct order would have been:
1. Copy dcterm to dcidentifier
2. DG Handle Migration
3. Handle integration profile

However, it might explain what you mention in the final 'Update' section in the attached PDF: the handles worked after process ID 7337283030004641, as they had been aldready handled by the integration profile job 7336725260004641

The message '.. already has a handle identifier ...' in the job events for the Handle Migration job can be ignored. It will always display this message for the migration of handles.
The records need to be checked only if the message says '... does not have a handle identifier'. It this case, the bib record needs to be checked to find out why the handle could not be migrated.

For already existing handles that should be redirected to Primo, it is necessary to
1. Create a set with these records
2. Run the Handle Migration job, using the control number sequence with the prefix used in the existing handles. Even if the records already have handles, this job is needed, as it copies the existing handles from the metadata to the handle identifier in the background.
3. Run the Persistent Handle Identifiers for Digital Resource integration profile on the set, selecting 'Create and Update' as action, and 'Do not add metadata' for the DC METADATA.

If you perform step 3 before step 2, the handles will not resolve correctly.
However, they will even if you perform step 2 after step 3.
```








