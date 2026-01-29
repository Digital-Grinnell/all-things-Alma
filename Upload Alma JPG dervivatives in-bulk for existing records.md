<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# I've asked other AI providers for help with this before, and they all failed, but I'll ask here anyway. In my Alma Digital environment, is there any way that I can successfully automate uploading new JPG derivatives, in bulk, to digital title records that currently have only a TIFF representation? Can this be done via the API or an Alma Job, anything?

Yes, you can automate bulk uploads of JPG derivatives to existing Alma Digital titles that already have TIFF representations, primarily using the Digital Uploader tool with a properly configured Digital import profile.[^1_1][^1_2]

This approach matches metadata (e.g., MARC XML exported from your existing bib set using the title's MMS ID or 001 field) to attach new representations without creating duplicates, specifying "Derivative" as the usage type for JPGs.[^1_3]

## Primary Method: Digital Uploader

Alma's Digital Uploader (Resources > Advanced Tools > Digital Uploader) handles bulk file uploads tied to an import profile.[^1_2]

- Export MARC XML from a set of your existing digital titles (use MMS ID matching).
- Create/configure a Digital import profile (Resources > Import > Manage Import Profiles) set to match on existing bibs (e.g., 001), action "Upon match: Import/Update", and "Upon no match: Do not import". Specify collection, library, usage type (Derivative), and access rights.[^1_3]
- Prepare JPG files (name matching metadata expectations, e.g., via deposit ID or filename rules; max 1 GB/file, 1000 files/ingest).
- In Digital Uploader: Create ingest, drag/drop files + metadata XML, select profile, upload to S3 if needed, then run "Run MD Import" job.[^1_2]

This adds JPGs as new representations to the TIFF bibs.[^1_1]

## Alternative: Manual per Title (Not Bulk)

Use Resources > Create Inventory > Add Digital Representation > Existing Title to add one JPG rep at a time by searching the bib.[^1_1]

## API Considerations

Alma's REST APIs support digital inventory (via Developers Network), but bulk file uploads for representations typically route through S3 presigned URLs rather than direct POST for large JPG batches—check /digitalInventory/representations endpoints for scripting new reps on existing titles.  No dedicated "bulk derivatives job" exists beyond import profiles.[^1_4]

Test on a small set first, as matching rules are critical for existing titles.
<span style="display:none">[^1_10][^1_11][^1_12][^1_13][^1_14][^1_15][^1_16][^1_17][^1_18][^1_19][^1_20][^1_21][^1_5][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/Digital_Resource_Management/040Creating_Digital_Inventory/020Adding_Representations

[^1_2]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/Digital_Resource_Management/040Creating_Digital_Inventory/040Creating_Digital_Content_in_Bulk

[^1_3]: https://knowledge.exlibrisgroup.com/Alma/Knowledge_Articles/How_to_Load_Representations_to_an_existing_Alma_Digital_record

[^1_4]: https://knowledge.exlibrisgroup.com/Alma/Product_Materials/050Alma_FAQs/General/APIs

[^1_5]: https://www.youtube.com/watch?v=ip8FEYOQob0

[^1_6]: https://www.rightindustries.in/vacuum-cola/vaccume-cola_main-2/

[^1_7]: https://speak-e.com/product/appointment-booking-product-for-professor-keating-for-service-182/

[^1_8]: https://www.econtabiliza.com.br/blog/abrir-de-empresa/

[^1_9]: https://www.angelfire.com/poetry/pravinchandra/Astonishing_Stories.html

[^1_10]: https://harvardwiki.atlassian.net/wiki/spaces/LibraryStaffDoc/pages/43394499/Alma+Digital+Uploader+XML+spec+and+manual+process+via+Alma+UI

[^1_11]: https://www.youtube.com/watch?v=eD8QWoL4Ps8

[^1_12]: https://publicdata.canterbury.ac.nz/Research/NZILBB/jonathandunn/Frontiers_in_AI/2.Code_c2xg/c2xg/data/dictionaries/Text/v.02/English.ukWac.DIM=500.SG=1.HS=1.ITER=25.txt

[^1_13]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/Digital_Resource_Management/010_Working_with_Digital_Resources/010_Working_with_Digital_Resources_-_Overview

[^1_14]: https://www.carli.illinois.edu/products-services/i-share/physical-res-man/import-workflows

[^1_15]: https://www.almabetter.com/bytes/articles/guide-to-create-restful-api

[^1_16]: http://sisyphus.way-nifty.com/sisyphus/2008/10/ssd-fe86.html

[^1_17]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/Digital_Resource_Management/040Creating_Digital_Inventory/Editing_Representation_Metadata_and_Content

[^1_18]: https://flvc.libguides.com/c.php?g=1156885\&p=8448851

[^1_19]: https://www.youtube.com/watch?v=IRDYH6rqRlY

[^1_20]: https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/080Analytics/Alma_Analytics_Subject_Areas/Digital_Inventory

[^1_21]: https://sunyolis.libguides.com/c.php?g=986218\&p=7692866

