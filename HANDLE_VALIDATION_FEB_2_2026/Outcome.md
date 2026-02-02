# Handle Validation - Feb. 2, 2026

Output from CABB reports...  

```
Handle validation complete: 12102 handles tested, 4 records without handles, 0 failed. Status codes: 12081 OK (200), 19 Not Found (404), 2 Other. File: handle_validation_20260202_092523.csv
```

The 19 'Not Found' (404) errors were all from new oral history objects temporarily housed in the `Pending Review` collection. These 19 were expected and properly detected.  

## Errors

The other errant records indicated above include...  

```
MMS ID,Handle URL,dc:title,HTTP Status Code,Status Message,Final Redirect URL,Returned Correct MMS ID,Titles Match!
991011546652304641,http://hdl.handle.net/11084/14702,"Greetings from Iowa, The Corn State, scene showing boating on beautiful Lake Okoboji",200,OK,Error fetching page,N/A,N/A
991011593355504641,http://hdl.handle.net/11084/35486,Wayman Hancock in Ottawa,200,OK,Error fetching page,N/A,N/A
991011591572804641,http://hdl.handle.net/11084/11789,"New Field House and Men's Gymnasium, Grinnell, Iowa -- 22",200,OK,https://grinnell.primo.exlibrisgroup.com/discovery/fulldisplay/alma991011591572104641/01GCL_INST:GCL,FALSE,N/A
991011600793704641,http://hdl.handle.net/11084/1742929397,"Student Protest, Undated",200,OK,https://grinnell.primo.exlibrisgroup.com/discovery/fulldisplay/alma991011600793904641/01GCL_INST:GCL,FALSE,N/A
991011687622804641,http://hdl.handle.net/11084/1750186419,"Correspondence to Isabella, 1908, Letter Two",200,OK,https://grinnell.primo.exlibrisgroup.com/discovery/fulldisplay/alma991011687623404641/01GCL_INST:GCL,FALSE,N/A
991011688287704641,http://hdl.handle.net/11084/1749071023,"Correspondence to Isabella, Undated, Letter 4",200,OK,https://grinnell.primo.exlibrisgroup.com/discovery/fulldisplay/alma991011688287604641/01GCL_INST:GCL,FALSE,N/A
991011546573204641,http://hdl.handle.net/11084/14259,"Amana Meat Shop, Amana, Iowa",200,OK,https://grinnell.primo.exlibrisgroup.com/discovery/fulldisplay/alma991011546573204641/01GCL_INST:GCL,TRUE,N/A
991011546573604641,http://hdl.handle.net/11084/14255,"South Amana Sandwich Shop, Amana, Iowa",200,OK,https://grinnell.primo.exlibrisgroup.com/discovery/fulldisplay/alma991011546573604641/01GCL_INST:GCL,TRUE,N/A
991011593354304641,http://hdl.handle.net/11084/35492,Henry and his Automobile,200,OK,https://grinnell.primo.exlibrisgroup.com/discovery/fulldisplay/alma991011593354304641/01GCL_INST:GCL,TRUE,N/A
991011692198804641,http://hdl.handle.net/11084/1742659990,No title found,200,OK,https://grinnell.primo.exlibrisgroup.com/discovery/fulldisplay/alma991011692198804641/01GCL_INST:GCL,TRUE,N/A
991011588277504641,http://hdl.handle.net/11084/19974,"Biking, 1988",0,Timeout,,N/A,N/A
991011588537904641,http://hdl.handle.net/11084/19919,"New Student Days, 1978 [019]",0,Timeout,,N/A,N/A
```

## Individual Outcomes

When tested manually (clicking the Handle below) one record at a time I got the follwoing tabulated results.   

  | MMS ID and Handle | Outcome |
  | --- | --- |
  | 991011546652304641, http://hdl.handle.net/11084/14702 | Opens correctly in Firefox.  This object is NOT a problem. |
  | 991011593355504641, http://hdl.handle.net/11084/35486 | Opens correctly in Firefox.  This object is NOT a problem.  Note: The Handle URL in CABB was NOT properly terminated. |
  | 991011591572804641, http://hdl.handle.net/11084/11789 | This is a LEGITIMATE error.  Please investigate. |
  | 991011600793704641, http://hdl.handle.net/11084/1742929397 | This is a LEGITIMATE error.  Please investigate. |
  | 991011687622804641, http://hdl.handle.net/11084/1750186419 | This Handle points to letter ONE, not letter TWO! |
  | 991011688287704641, http://hdl.handle.net/11084/1749071023 | This Handle points to undated letter FIVE, not letter FOUR! |
  | 991011546573204641, http://hdl.handle.net/11084/14259 | Opens correctly in Firefox.  This object is NOT a problem. |
  | 991011546573604641, http://hdl.handle.net/11084/14255 | Opens correctly in Firefox.  This object is NOT a problem. |
  | 991011593354304641, http://hdl.handle.net/11084/35492 | Opens correctly in Firefox.  This object is NOT a problem.  Note: The Handle URL in CABB was NOT properly terminated. |
  | 991011692198804641, http://hdl.handle.net/11084/1742659990 | This Handle appears to open correctly, but this record's title is clearly an error. |
  | 991011588277504641, http://hdl.handle.net/11084/19974 | Opens correctly in Firefox.  This object is NOT a problem. |
  | 991011588537904641, http://hdl.handle.net/11084/19919 | Opens correctly in Firefox.  This object is NOT a problem. |


That leaves us with `FIVE` legitiamte problems left to resolve.  
