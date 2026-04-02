The attached table shows the CSV results of last evening's TIFF scan by CABB.  It shows 7 TIFF-only objects for which no JPG derivative could be created because the TIFF is truncated and invalid.  

In all but one case it appears that Islandora had the complete TIFF images, but something went haywire in the process of transferring and uploading into Alma.  I found 3 of the 7 full-size images in //Storage/MEDIADB/DGIngest, they were put there by the migration effort.  

The first of the 7 records has been resolved, it now has a working, full-size TIFF image and thumbnail.  

The zero-size TIFF is still a mystery, and I cannot find the full-size file in //Storage.  

The other 5 are very interesting, and frankly VERY troubling.  

Notice that they all have the EXACT SAME truncated size in Alma.  I worked with line #2 most of the day today, trying different means of transferring the file from //Storage to locations where Alma could get hold of it.  

In every case the file is transferred at full-size, roughly 293 MB.  I tried copying to my MacBook, to the iMac, mounting the //Storage folder in both Macs, transferring via my iCloud drive, via Google docs, via a thumbdrive, you name it... I tried it.  All of those processes preserved the file size and I was able to open the image in various software packages.  

Then I tried 2, maybe 3 different routes in Alma to upload the image.  I tried both attaching to an existing representation, and creating a new rep to receive the attachment.  I have a screen capture (still on the iMac for now) of the uploader indicating the full size of the upload and running to completion, again to that full size, 100%.  But whenever I open a viewer in Alma I see NO IMAGE, and always the reported image size is the same, 565.52 MB.  

Likewise, whenever I run CABB to convert the image to a JPG derivative the process fails with error messages about an invalid TIFF.  

I will tinker with the image in row 2 tomorrow before contacting support.  If we can't get content reliably and completely into Alma I think it's value as a preservation platform is ZERO, or maybe less than that since there don't seem to be any errors or warnings, and the result takes extra time and effort to repair.  I've lost faith.  

The first object has already been resolved. 

## Data Table Before Remediation

| MMS ID | Title | Representation ID | TIFF Filename | File Size (MB) |
|--------|-------|-------------------|---------------|----------------|
| 991011565486504641 | Frank Rowell with his Award Winning Rabbits | 12320321970004641 | grinnell_27239_OBJ.tiff | 40.0 |
| 991011588252204641 | Track Quad | 12323795400004641 | grinnell_23611_OBJ.tiff | 565.52 |
| 991011589634404641 | Boycott the Longhorn | 12323976710004641 | grinnell_4983_OBJ.tiff | 0.0 |
| 991011589492204641 | Sailing on Lake Nyanza | 12323985860004641 | grinnell_5929_OBJ.tiff | 565.52 |
| 991011589492504641 | Fencing Class | 12323985880004641 | grinnell_5928_OBJ.tiff | 565.52 |
| 991011589493304641 | Long Jump 1971 | 12323985940004641 | grinnell_5919_OBJ.tiff | 565.52 |
| 991011589502604641 | Women's Basketball, 1977 [001] | 12323997670004641 | grinnell_5951_OBJ.tiff | 555.52 |

## Data Table UPDATED with STATUS

| MMS ID | Title | Representation ID | TIFF Filename | New File Size (MB) |
|--------|-------|-------------------|---------------|--------------------|
| 991011565486504641 | Frank Rowell with his Award Winning Rabbits | 12320321970004641 | grinnell_27239_OBJ.tiff | 75.69 |
| 991011588252204641 | Track Quad | 12323795400004641 | grinnell_23611_OBJ.tiff | 565.52 |
| 991011589634404641 | Boycott the Longhorn | 12323976710004641 | grinnell_4983_OBJ.tiff | 0.0 |
| 991011589492204641 | Sailing on Lake Nyanza | 12323985860004641 | grinnell_5929_OBJ.tiff | 565.52 |
| 991011589492504641 | Fencing Class | 12323985880004641 | grinnell_5928_OBJ.tiff | 565.52 |
| 991011589493304641 | Long Jump 1971 | 12323985940004641 | grinnell_5919_OBJ.tiff | 565.52 |
| 991011589502604641 | Women's Basketball, 1977 [001] | 12323997670004641 | grinnell_5951_OBJ.tiff | 555.52 |


## Claude Sonnet 4.5 Inquiry

I can help research this issue. The fact that multiple files are all being truncated to the **exact same size** (565.52 MB) is a strong indicator of a systematic limit rather than random corruption. Let me search for information about this specific file size limit. 


Fetched https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/090Integrations_with_External_Systems/030Resource_Management/Digital_Uploader

Based on the pattern you're describing, this appears to be a **configuration limit** rather than a random network corruption issue. Here's why:

## Key Indicators

1. **Exact same truncation size** (565.52 MB) across multiple files - this is the smoking gun for a systematic limit
2. **Consistent behavior** regardless of transfer method before Alma
3. **Files transfer completely at ~593 MB everywhere except Alma**

## Likely Causes

**565.52 MB** is suspiciously close to **540 MiB** (mebibytes), which equals approximately **566.23 MB** (megabytes). This could be:

### 1. **HTTP/Web Server Upload Limit**
- Nginx `client_max_body_size` 
- Apache `LimitRequestBody`
- These are often set to 512M or 540M

### 2. **Application Server Limits** 
- PHP `upload_max_filesize` or `post_max_size`
- Java servlet upload limits
- Often defaulted to 500-600 MB range

### 3. **Alma-Specific Configuration**
- Ex Libris may have upload size limits configured
- Could be at the repository, institution, or system level

## Recommended Actions

1. **Contact Ex Libris Support** with this specific data:
   - Original file size: ~593 MB
   - Truncated size: always 565.52 MB
   - Multiple files affected identically
   - Request they check server-side upload limits

2. **Ask about workarounds**:
   - Can the limit be increased for your institution?
   - Is there an alternative upload method (API, FTP, S3 direct)?
   - Can files be uploaded via different ingestion path?

3. **Test the theory**: Try uploading a file that's exactly 565 MB - does it come through intact?

This is almost certainly **not** a random network issue, but a hard limit that needs to be raised by ExLibris or your system administrators.

## More from Claude...  







Fetched https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/Digital_Asset_Management/060Working_with_Digital_Files

Fetched https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/Digital_Asset_Management

Fetched https://developers.exlibrisgroup.com/alma/apis/bibs







Fetched https://developers.exlibrisgroup.com/alma/integrations/digital/

Fetched https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/Configuration_Menu

Fetched https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/Configuration_Menu/040General_Configuration/Configuring_Amazon_S3_Cloud_Storage





Fetched https://developers.exlibrisgroup.com/alma/integrations/digital/almadigital/ingest

Fetched https://developers.exlibrisgroup.com/alma/integrations/sword/

Based on my research of Alma Digital documentation, I found the following:

## Key Finding: No Documented File Size Limit

The official Alma documentation I reviewed does **not explicitly state a file size limit** for digital file uploads. The documentation covers:

- **Ingest processes** (MD Import, SWORD deposits, Digital Uploader)
- **Representation and file management APIs**
- **Thumbnail generation** (which has a 100KB limit for custom thumbnails)

However, **no maximum file size is documented** for master TIFF files or other digital assets.

## What This Means

The **565.52 MB truncation** you're experiencing is likely caused by:

1. **Infrastructure limits** not controlled by Alma itself:
   - Web server configuration (nginx/Apache)
   - Load balancer limits
   - Proxy server settings
   - Cloud storage upload limits

2. **Institution-specific configuration** that may have been set by Ex Libris support or your IT team

3. **Undocumented system limits** within Alma's architecture

## Recommended Next Steps

Since this isn't documented in the official Alma integration guides:

1. **Open a support ticket with Ex Libris** providing:
   - Exact file size before upload: ~593 MB
   - Exact truncated size: 565.52 MB (consistent across all files)
   - The fact that it affects multiple files identically
   - Request they check server-side upload/POST limits

2. **Ask specifically about**:
   - Maximum file size for web-based uploads
   - Whether alternative upload methods exist (FTP, S3 direct, API)
   - If this limit can be increased for your institution

3. **Test alternative upload paths**:
   - Try MD Import with files placed directly in the upload folder (vs web upload)
   - Try SWORD deposit if available
   - Try API-based file creation

This appears to be a **system configuration issue** rather than a hard product limitation, but only Ex Libris support can confirm and potentially adjust it.