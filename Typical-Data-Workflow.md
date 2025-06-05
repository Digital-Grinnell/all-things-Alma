# Typical Data Workflow

This documents a typical workflow engaging `Alma Analytics` to produce a `.csv` file, importing that CSV into a Google Sheet, the using `XLOOKUP` or similar method of merging the data into a larger set with additional fields.  

## Alma Analytics

The workflow typically begins by opening _Alma_ and then `Access Analytics` like so:  

![](https://dgdocumentation.blob.core.windows.net/eluna-atlanta/2025-06-05-13-59-43.png)

![](https://dgdocumentation.blob.core.windows.net/eluna-atlanta/2025-06-05-14-01-51.png)

Inside `Analytics` I have defined two "MASTER" reports...  

    1) `Migrant-Digital-Titles-MASTER` - Holds key information about digital titles (items/objects), with `grinnell:xxxxx` identifiers, that migrated from Islandora.  
    
    2) `NEW-Digital-Titles-MASTER` - Holds key information about digital titles, with `dg_xxxxxxxxxx` identifiers, that were NOT previously in Islandora. 

These reports can easily be copied, and the new copies modified to add more detail if needed.  

![](https://dgdocumentation.blob.core.windows.net/eluna-atlanta/2025-06-05-14-09-01.png)

In the dashboard screen shown above you'll see the two reports listed in the pull-down under `Open` on the right-hand side of the window.  

### Numeric ID

A key component of each "MASTER" report is the `Numeric ID` column which contains `regex` logic to extract an object's Handle suffix from the `Network Number` column.  As illustrated below, `Numeric ID` is the column farthest to the right.  

![](https://dgdocumentation.blob.core.windows.net/eluna-atlanta/2025-06-05-14-12-34.png)

### Export Results to CSV

Typically I will export the _Analytics_ results to a tab-delimited CSV file (really a TSV) as shown in the illustration below.  

![](https://dgdocumentation.blob.core.windows.net/eluna-atlanta/2025-06-05-14-17-27.png)

Exporting in this manner will create a new `.csv` file in my `~/Downloads` directory with a name matching the name of the report, so `~/Downloads/NEW-Digital-Titles-MASTER.csv` in the example above.  

### Importing to a Google Sheet

In Google Sheets I generally use menu selections `File`, `Import` and `Upload` to select my exported `.csv` (tab-delimited export from Analytics) and bring it into a sheet as a "new" worksheet as illustrated below.  I always choose the `Detect Automatically` option so that the tab-delimited (IMO tabs work better in most cases than comma-delimited) data is properly parsed.  

![](https://dgdocumentation.blob.core.windows.net/eluna-atlanta/2025-06-05-14-30-31.png)

The newly imported worksheet will have a name matching the _Analytics_ report name, and should look something like you see illustrated below.  

![](https://dgdocumentation.blob.core.windows.net/eluna-atlanta/2025-06-05-14-35-29.png)

### A Typical Merge Example

My aim is typically to bring a portion of our exported TSV data into an existing Google Sheet where I can easily manipulate or merge it with other data.  For example, as I am writing this I have a `Complete Object Data` "review" worksheet at https://docs.google.com/spreadsheets/d/1CcU7y_TMoq6BZO3lQvWmTsHmSAAL8Z9mQSbFQcUR0n0/edit?gid=652937759#gid=652937759.  This will be our "target" worksheet for this example.  That sheet includes an all-important `MMS ID` column -- we typically use `MMS ID` as our "key" data for lookup -- but an empty `HANDLE` column that needs to be populated.  

Our `HANDLE` data will be built from the `Numeric ID` column of another worksheet that was imported from different _Analytics_ export, specifically https://docs.google.com/spreadsheets/d/1up8_aZNtBeSUuMcaDiqnRBZS0_Thw6KMGi9iA9QixYM/edit?pli=1&gid=53763122#gid=53763122.  I'll refer to this worksheet as "to-be-merged" in our example.  

#### XLOOKUP to Merge Data

In this example, I'm going to pull values from the `Numeric ID` column (Column C of the to-be-merged data) back into corresponding cells of the `Handle Suffix` column (B) of the target worksheet.  I do so using an `XLOOKUP` formula in the `Handle Suffix` cells of our target.  In the case of row 2 (cell `C2`) the formula is:   

```
=XLOOKUP(A2,'NEW-Digital-Titles-MASTER'!A:A,'NEW-Digital-Titles-MASTER'!C:C)
```






