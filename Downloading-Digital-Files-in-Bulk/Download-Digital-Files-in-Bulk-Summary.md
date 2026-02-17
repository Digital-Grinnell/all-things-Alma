# From a Slack Post

```
Julia Bauder
 
alma-d
Jul 8th at 4:02 PM

Seen today on the Alma-D mailing list: "You can use a combination of Analytics and scripting using the Amazon S3 APIs to bulk download content from your Alma digital storage.
"Analytics will have the file path where the objects are stored; "File Details"."File Internal Path"
"You’d then need to use that path to download the file(s) from your Alma’s Amazon S3 storage.
 *  https://urldefense.proofpoint.com/v2/url?u=https-3A__developers.exlibrisgroup.com_alma_integrations_digital_almadigital_&d=DwIGaQ&c=HUrdOLg_tCr0UMeDjWLBOM9lLDRpsndbROGxEKQRFzk&r=635534ScZfXSRDpdzWobNE_dcO1rW4hQ5FtRlzG9QFY&m=F_CyvZXVhqMjG5PPyielLwL_CHVvf1dPuLBvTzwWZJ4hegDljdxCtzeRt7jnliPF&s=-6skRLr8tmYku8syXfl8cwJSX7-Krq5uP3auybF7z90&e=
"We’ve done this exact thing using PowerShell scripts (using Copy-S3Object) previously, and it works without fault.
 *  https://docs.aws.amazon.com/powershell/v5/userguide/powershell_s3_code_examples.html
"Reach out if you’d like specific examples and/or guidance.
Cheers,
Ben
Ben Dalwood
Manager, Library Applications | University Library
The University of Adelaide"
```

# My Experience

I tried in January 2026 to do something like this using CABB. but that failed on several fronts involving lack of permission.  _Perhaps the solution to that dilema lies above?_  

A chat with Ex Libris support suggested I create a set (already did that) and the `Download Files` job.  OK, tried that, but it returned nothing.  Some analysis seemed to indicate that it was strictly for digital reps tied to MARC bibs or digital holdings, and we have none.  Along the way there I discovered the `Download Digital Titles Inventory` job, so I took that for a spin.  

## I've just run a "Download Digital Titles Inventory" in Alma. So, where will I find these files?

You retrieve those files from the job’s report in Alma, under Monitor Jobs.[^1_1][^1_2]

### Where to click

- Go to **Admin → Manage Jobs and Sets → Monitor Jobs**.[^1_3][^1_1]
- Switch to the **History** tab and locate the **Download Digital Titles Inventory** job you just ran.[^1_2][^1_1]
- Click the job’s **Report** link to open the job details.[^1_1][^1_3]
- In the report, use the **Actions (…) → Download** option next to the output file; your browser will save it according to your usual download settings.[^1_1]
<span style="display:none">[^1_10][^1_11][^1_12][^1_13][^1_14][^1_15][^1_4][^1_5][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://www.carli.illinois.edu/products-services/i-share/physical-res-man/export-records

[^1_2]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/050Administration/070Managing_Jobs/020Manual_Jobs_on_Defined_Sets

[^1_3]: https://flvc.libguides.com/c.php?g=1156894\&p=9618183

[^1_4]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/080Analytics/Alma_Analytics_Subject_Areas/Digital_Inventory

[^1_5]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/Digital_Resource_Management/010_Working_with_Digital_Resources/010_Working_with_Digital_Resources_-_Overview

[^1_6]: https://www.carli.illinois.edu/products-services/i-share/external-system/BatchInventory

[^1_7]: https://pul-confluence.atlassian.net/wiki/spaces/ALMA/pages/1770094/Cataloging+and+Inventory+Management+FAQ

[^1_8]: https://www.youtube.com/watch?v=IRDYH6rqRlY

[^1_9]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/040Resource_Management/050Inventory/050Managing_Collections

[^1_10]: https://ucldata.atlassian.net/wiki/display/LibraryServices/Alma+Cataloguing

[^1_11]: https://knowledge.exlibrisgroup.com/Alma/Product_Materials/050Alma_FAQs/Analytics/Digital

[^1_12]: https://clo.libguides.com/clsp-almaprimoguide/new-features

[^1_13]: https://support.thirdiron.com/support/solutions/articles/72000642993-alma-configuring-the-automated-job-export

[^1_14]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/040Resource_Management/075Publishing_Profiles/030Export_and_Publishing

[^1_15]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/080Analytics/Alma_Analytics_Subject_Areas/Titles

# Feburary Update

On February 16 I was able to **successfully** run the `Download Digital Titles Inventory` job against 100 of our solitary TIFF bib records.  Since the job finished without error I was then able to download the 100 pieces of digital content!  

Later, I tried the same process with 500 objects, but it FAILED.  I tried again with 250 but that also FAILED.  

So, for now our practical digital titles download limit is 100 bibs and corresponding files.  
