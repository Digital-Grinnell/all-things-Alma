
 Just hit another BIG (?) bump in the road here...   Trying to assign handles to a couple of collections using the workflow that EXL support provided earlier.   It starts with creating an itemized list to feed into subsequent steps.   Only problem is I can't create a "digital titles" set from a list of collections, it apparently has to be a "collection set".  So I tried that, but apparently you cannot create such a set from a CSV list of the collection MMS_IDs.  Collection sets appear to be quite different than other sets?  So, I'm stuck again and probably looking at another chat support call that will escalate to tier 2... and maybe we will have a solution in a few weeks?  


Julia Bauder
  9:25 AM
I ran into this before and figured out a way around it. Let me see if I can reconstruct what I did....


Mark M.
  9:26 AM
Follow up... When I try to create a "collection" itemized list I keep getting this error:
Header line in input file is missing an ID column. Supported IDs are: PID
So I change the header in my CSV file to "PID" and then I get an error saying more columns are missing from my data, but I get a "successful" job run and a set with NO members.   :big_dumpster_fire:


Julia Bauder
  9:29 AM
Collection ID (All Sub-Levels) Contains Keywords "81302943070004641" and Collection ID (One Level) Not Equals "81324790870004641" . That's the query I'm using to generate the set for OAI harvesting. It gets all items in overarching digital collection EXCEPT those in the equipment collection.

9:29 And it's a digital titles logical set.
9:30 Look at the DG_Collection set in Manage Sets.
9:30 You can convert any logical set into an itemized set.
9:31 By opening up the set in Manage Sets and clicking the Itemize button at the top.

Mark M.
  9:45 AM
OK, will look at this as soon as I return.  However, I need a set of collections, not titles in the collections. Is that what this would give me?

Julia Bauder
  10:27 AM
Oh, no, sorry, that's titles in the collections.

10:30 Okay, I just created a new logical set of all collections, called, appropriately enough, All Collections.
10:30 And that one is collections.

Mark M.
  11:08 AM
So, if I understand correctly, you (@Julia Bauder) built a logical set with all the collections and I should be able to turn that into an itemized set, which is what the workflow needs.  I never thought to take the "logical" route first.  Thanks! 

Mark M.
  12:30 PM
@Julia Bauder
 Hmmm, I'm not finding a set named "All Collections", or anything similar?


Mark M.
  12:43 PM
Well, I think this entire process is doomed.  :big_dumpster_fire:  I have to create an itemized set, which I have finally done, then run the job named DG Handle Migration and feed my set into it.  But I can't seem to do that.  The set exists, as does the logical set I created it from as you can see below.  But when I go to pick that set from the job, it's is consistently NOT found?
I give up... need to work on the ELUNA presentation ASAP.

Kayla Reed
  12:48 PM
Can you make the all collections set public so I can see it?


Mark M.
  1:00 PM
I just toggled Private OFF on both the logical and itemized.  Note that they don't actually contain ALL collections, just the one that I want a handle for, for now.

1:02
FWIW I still can't select either set for the DG Handle Migration job.   Unfortunately, that job was created for us by EXL so I have no idea what it's made of. (edited) 

Kayla Reed
  1:06 PM
Weird. I still can't see it
1:07
Ah! Never mind! Found it


Julia Bauder
  1:11 PM
You can only run the Handle migration job on bib records:

1:11
Collection records are not bib records, hence why they aren't in the list.
1:11
^They = the sets of collection records.

Kayla Reed
  1:19 PM
Can we redo the set for the bibs of collections?

Julia Bauder
  1:20 PM
Collections don't have bibs. They have records, but they aren't bib records.

Kayla Reed
  1:20 PM
Exlibris says they have bib records https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(Englis[…]esource_Management/050Inventory/050Managing_Collections
Ex Libris Knowledge CenterEx Libris Knowledge Center
Managing Collections
Overview and instructions for managing collections.
Dec 3rd, 2015


Mark M.
  1:23 PM
Ok, I was worried that might be the case but thanks for confirming.
So, IMO Alma has a fundamental flaw here, but certainly I'm biased from Islandora experience and my time before that at HP.
In Islandora, and manu other systems I've worked with, ALL data has certain structure, characteristics and behaviors in common.  In the case of Islandora EVERY digital object was built from a single class, so items, compounds, collections, everything... had a PID, a title, description, and a type.   The 'type' determined how the thing behaved, but operations like ingest, editing, filtering, searching, and set building were all based on those common, fundamental characteristics.


Julia Bauder
  1:30 PM
Oh, this is interesting. The DG-related collections all have DCAP01 records, which Alma does not treat as bib records. But you can have collections with MARC records -- the Sierra Media Management collection has a MARC record.
1:30
So I think if you converted our DCAP01 collection records to MARC records, you might be able to work with them as bib records????


Mark M.
  1:31 PM
My frustration is largely due to what I know about Handles.   All you need to apply a Handle is a properly formed one-line statement (per object) that says THIS is an ALIAS for THAT.    The trick is getting that simple statement into the Handle server to teach it how to behave.  It's extremely simple, the only real complexity from the Handle folks is in authentication so the Handle server knows you are a "qualified teacher" and are permitted to teach it.   The owner of the server then has to craft a process (also not too difficult) in which the teaching and learning can happen.
When we owned our own Handle server it was a piece of cake.    EXL seems to have created their Handle server by taking something so simple, and providing a complex wrapper for it, one that is only capable of accommodating a very limited set of data.


Kayla Reed
  1:31 PM
I was able to open the collection in the metadata editor

Julia Bauder
  1:32 PM
Yes, and look at what kind of record the metadata editor thinks it is.


Kayla Reed
  1:32 PM
Yea could we create a copy and convert it?


Mark M.
  1:32 PM
Yes, the MDE works, that's how I got the dc:identifier into the new Baumann Essay Prize Winner collection, the one that I need a Handle for.
1:33
Even if you convert it to MARC, I think the DG Handle Migration process expects to find a dc:identifier field in the record.
1:35
I'm tempted to just create a Handle .bat file (where the THIS is an ALIAS for THAT statements go) and tell (ask?) EXL to just make it happen.   Whoever built their Handle server should be savy enough to understand what the file is for and how to "handle" it.


Kayla Reed
  1:38 PM
I have time I can poke chat for a bit and see if there is any other solution?


Mark M.
  1:40 PM
That sounds good to me @Kayla Reed

Or, maybe we just need to create and run our own Handle server again, then we are in complete control?  And, if Alma ever goes away or is replaced, completely or partially, we remain in control.
I'm not fond of creating another server, especially on-prem, but it's not that difficult either.   I would almost bet that Azure has a push-button Handle server config for $5/month or less.


Julia Bauder
  1:42 PM
OH! I GOT IT!


Mark M.
  1:42 PM
:drum_with_drumsticks:
:smile:

Julia Bauder
  1:42 PM
As long as the Set content type is set to All Titles rather than Collections, it shows up as an option under the Handle migration job.


Julia Bauder
  1:42 PM
I haven't tried running it to see if it works, but I can at least get it to show up as an option:


Kayla Reed
  1:43 PM
That's usually a good sign



Mark M.
  1:43 PM
Ok, I'll take it from here.  Thanks @Julia Bauder and @Kayla Reed!   I thought I had tried that already... but maybe not.


Julia Bauder
  1:44 PM
It's going to be a pain, but I think now if you search collection title by collection title from an all titles search and add them to that itemized collection, it should work.


Mark M.
  1:44 PM
Did you happen to build such an itemized set of collections yet?


Julia Bauder
  1:45 PM
I did not. I just added a single collection to see if I could get it to show up as an option for that job.


Kayla Reed
  1:46 PM
I can do it. All DG collections included?


Mark M.
  1:47 PM
Sure @Kayla Reed.  I'd like to add at least the Baumann collection (MMS = 991011621841904641) to it, but all DG collections should be fine, they just don't all have dc:identifier values yet.   But that's OK, the job should return 2 successes and 39 failures IF it works the way I expect it to.


Kayla Reed
  1:57 PM
Ok set made. Collections - new. shows up as an option for the job too
1:57
Only thing not in there is Scriptorium


Mark M.
  1:58 PM
I did a quick search for any cloud service providers with HDL (Handle) server one-click provisioning.  No for Azure, or any other established provider for that matter.  So building one would probably involve creating and provisioning a simple Linux node (perhaps no database or PHP required).
When I have a little more time I might ping the Handle folks out in Virginia and see what they suggest.  I'll bet they even have a provisioned server that one can subscribe to, but still maintain control.
1:58

1:59
...drumroll please...  :drum_with_drumsticks:
2:00
Only got 18 collections in the set... by my count there are 41 if you include all levels.


Kayla Reed
  2:01 PM
And it skipped all but 2...wow


Mark M.
  2:02 PM
That's what I expected...  Record 991011578629104641 was skipped. Reason: BIB record MMS ID 991011578629104641 does not have a handle identifier
2:03
There are only 2 collections that DO have a Handle dc:identifier because I had to add those manually, one-at-a-time.  True to form, Alma reports the errors but not the successes.  Process of elimination required to know what worked... I hate it.
:big_dumpster_fire:


2:07
Ok, Baumann was one of the 18 so... Assuming that was one of the two the did work, that completes step 3 of the 4-part Handle workflow.  Trying step 4 now...  :drum_with_drumsticks:
:crossed_fingers:


2:11
Nope.  Step 4 requires the set... again, and it only allows selection of 'Digital title' sets?  :big_dumpster_fire::big_dumpster_fire::big_dumpster_fire::big_dumpster_fire::big_dumpster_fire::big_dumpster_fire:
2:12
I think we need an emoji of a bug having painted itself into a corner... name it ALMA.


Julia Bauder
  2:34 PM
:lower_left_paintbrush::beetle::lower_left_paintbrush:
2:35
Let me see if I can coerce it into being a digital title set....

2:38
No, I cannot. Alma is really, really adamant that the Baumann Essay Prize collection is not a digital title.


Mark M.
  2:57 PM
There is still hope... maybe the "fix" they promised to release in July will return Handles to the simple things they should be.  :crossed_fingers::skin-tone-3::crossed_fingers::skin-tone-3::crossed_fingers::skin-tone-3:


