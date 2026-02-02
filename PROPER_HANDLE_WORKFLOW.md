# Proper HANDLE Workflow

The following was saved from an Ex Libris support ticket (08197740) final note on Feb-2-2026...  

```
From now on, this should be your workflow:
1. Run the job 'DG Handle Migration'
2. Run the handle integration profile on the same set, using
Action = Create and Update
DC metadata = 'Do not add metadata'
```

The entire ticket post reads...  

```
Hello Mark,

A new comment has been added to case  08197740.

Case Title: Alma Chat - Assigning Handles to existing digital titles
Last Comment:
Dear Mark,
Today, we corrected the remaining handles in your file.
First, we deleted the incorrectly registered handles from our database.
Then we performed the handle migration workflow for the records:
1. Run the job 'DG Handle Migration'
2. Run the handle integration profile on the same set, using
Action = Create and Update
DC metadata = 'Do not add metadata'

I verified that the handle_ids in the database are now the same as in your file.
I apologise again for not registering these handles correctly in December.

We enabled the search index for the Handle Identifier in your environment.
Now you can verify the correct handles using and andvanced search.
E.g.
Digital Titles
(1 - 1 of 1)
Search Query:
MMS ID Equals "991011691989504641" and Handle Identifier Contains Keywords "11084/1762286371"

From now on, this should be your workflow:
1. Run the job 'DG Handle Migration'
2. Run the handle integration profile on the same set, using
Action = Create and Update
DC metadata = 'Do not add metadata'

Please let me know if there are any remaining problems or questions.

Best regards,
Sabine

Status: In Progress - Tier 2
Priority: Medium
Description:
250929_175836; NA03; 01GCL_INST; McFate, Mark - Alma Chat
```