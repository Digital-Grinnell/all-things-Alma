# Assigning Existing Handles to Alma Records

The workflow suggested by support agent Anchi Hsu is...  

1. Create a title set that already includes a handle identifier. (record 991011592645304641 is the only member of set 7333418150004641)  
2. Admin > Run a job > search name: Copy dcterm to dcidentifier > wait for it to finish, and go to the next step (ran process ID 7333418330004641)  
3. Admin > Run a job > search name: DG Handle Migration > wait for it to finish, and go to the next step (ran process ID 7333418800004641)  
4. Configuration > General > Integration Profile > Persistent Handle Identifiers for Digital Resource > Actions > Run  

## Workflow with Screen Captures

That workflow in practice looks something like this:  

1) Build an itemized set of titles from a list of MMS IDs.  In my case something like...

![Create an Itemized Set](<./Documents/Screenshot 2025-05-08 at 9.35.17 AM.png>)

2) From `Admin` > `Run a job` find the `Copy dcterm to dc:identifier` job and run it with the set defined above, like so...

![Run the "Copy dcterm to dc:idenfifier" job](<./Documents/Screenshot 2025-05-08 at 9.39.16 AM.png>)

![Select New Set for the Job](<./Documents/Screenshot 2025-05-08 at 9.41.09 AM.png>)

Once the job is complete and successful proceed to step 3.

3) From `Admin` > `Run a job` find the `DG Handle Migration` job, edit it to include the set defined in step 1, and run it like so...
 
![Setup the "DG Handle Migration" job](<./Documents/Screenshot 2025-05-08 at 9.46.20 AM.png>)

![Select Our Set](<./Documents/Screenshot 2025-05-08 at 9.48.04 AM.png>)

Submit the job and when it is complete and successful proceed to step 4

**Attention: There is indication of a problem here.  Many of the records did NOT process successfully because of the condition illustrated below.

The `dc:identifier` field should NOT have a `dcterms:URI` attribute!  Those attributes need to be removed before handle assignment will work!  

4) 