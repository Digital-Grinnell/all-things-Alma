# Alma Analytics Formula Building

## Some Examples from the Documentation

CASE
WHEN ""Bibliographic Details"."Network Number" Physical Item Details"."Statistics Note 2" IS NOT NULL
THEN CAST(SUBSTRING("Physical Item Details"."Statistics Note
2" FROM 12 FOR 3) as INT)
ELSE

SUBSTRING("Physical Item Details"."Statistics Note 2" FROM
LOCATE('LastDateReturn: ',"Physical Item Details"."Statistics Note
2")+20 FOR 2)||'/'||
SUBSTRING("Physical Item Details"."Statistics Note 2" FROM
LOCATE('LastDateReturn: ',"Physical Item Details"."Statistics Note
2")+22 FOR 2)||'/'||
SUBSTRING("Physical Item Details"."Statistics Note 2" FROM
LOCATE('LastDateReturn: ',"Physical Item Details"."Statistics Note
2")+16 FOR 4)


In Alma Analytics, you can use regular expressions (regex) within formulas to manipulate and extract specific information from various data fields
. Alma Analytics uses Oracle's regular expression functions. 
Key Regex Functions in Alma Analytics Formulas:

    EVALUATE(): This function allows you to use non-Analytics Oracle SQL functions within your Alma Analytics formulas. You'll often use EVALUATE() to call regular expression functions like regexp_substr and regexp_replace.
    regexp_substr(): This function returns a portion of a string that matches a specified regular expression pattern.
    regexp_replace(): This function returns a string where occurrences of a pattern matching a regular expression have been replaced with a specified string.
    regexp_instr(): This function returns the starting position of the first occurrence of a pattern within a string, or 0 if no match is found.
    regexp_count(): This function counts the number of times a pattern appears within a string. 

Example Formulas:
Here are some examples of how regex can be used in Alma Analytics formulas:

    Extracting data from a field using regexp_substr():
        Evaluate('regexp_substr(%1,''[A-z]+'')',"Holding Details"."Permanent. Call Number") extracts alphabetic characters from a call number field.
        Evaluate('regexp_substr(%1,%2,%3,%4,%5,%6)',"Bibliographic Details"."Network Number", '(\\(?[ oO0][cC]\\w+\\)?\\ W?\\d+)\', 1,1, NULL, 0) retrieves the first OCLC Number from the Network Number field.
    Filtering data based on regex patterns:
        evaluate('REGEXP_INSTR(%1, ''^[0-9]+$'')', "User Details"." Primary Identifier") checks if a Primary Identifier contains only numeric characters. It returns "1" if it does and "0" if it contains at least one alphabetic character.
    Replacing characters using regexp_replace():
        Evaluate('regexp_replace(%1,''; [0-9Xx]{8}'', '''')',"Bibliographic Details"."ISSN") removes duplicates from the ISSN field.
    Parsing and extracting data based on patterns:

        CASE
          WHEN Evaluate('regexp_instr(%1, %2)', "Physical Item Details"." Internal Note 3", 'HISTORICAL_CHARGES: (\\d+)') != 0
          THEN CAST( Evaluate( 'regexp_substr(%1, %2, %3, %4, %5, %6)', "Physical Item Details"." Internal Note 3", 'HISTORICAL_CHARGES: (\\d+)', 1, 1, 'c', 1 ) as INT)
          ELSE CAST('0' as INT)
        END

        This formula uses regexp_instr to check for a pattern and then regexp_substr to extract numerical data related to historical charges from a string in the "Internal Note 3" field. 

Important Notes:

    Be mindful of quotation marks when copying and pasting formulas, as they must transfer correctly.
    The EVALUATE() function uses positional arguments (e.g., %1, %2) to pass data and patterns to the Oracle regex functions.
    You can adapt these formulas to work with different fields and data types by changing the field names and regex patterns.
    Consult the Oracle documentation for more information on specific regex functions and syntax. 



    Using REGEXP_SUBSTR in Alma Analytics Formulas: Example
In Alma Analytics, the REGEXP_SUBSTR function is a powerful tool used to extract specific parts of a string based on a regular expression pattern. 
General Syntax (within Evaluate() function):
sql

Evaluate('regexp_substr(%1,%2,%3,%4,%5,%6)', field_to_search, regex_pattern, start_position, nth_occurrence, match_param, subexpression_group)

Example: Extracting a specific OCLC Number from the "Network Number" field 
Let's say you have a field in Alma Analytics named "Network Number" that contains multiple identifiers separated by semicolons, and you want to extract the first OCLC number that starts with "(Nz)" or "(nz)". You can use REGEXP_SUBSTR with a specific regular expression pattern to achieve this. 
Formula:
sql

Evaluate('regexp_substr(%1,%2,%3,%4,%5,%6)',"Bibliographic Details"."Network Number", \'(\\(?[ oO0][cC]\\w+\\)?\\ W?\\d+)\', 1,1, NULL, 0)

Explanation:

    Evaluate('regexp_substr(%1,%2,%3,%4,%5,%6)', ...): This uses the Alma Analytics Evaluate function to call the underlying Oracle regexp_substr function.
    "Bibliographic Details"."Network Number": This specifies the field you want to search within.
    \'(\\(?[ oO0][cC]\\w+\\)?\\ W?\\d+)\' : This is the regular expression pattern used to identify the desired string.
        \\(: Matches a literal opening parenthesis.
        \\)?: Matches an optional closing parenthesis.
        [ oO0][cC]: Matches " o", " O", "0c", "OC", etc.
        \\w+: Matches one or more word characters (letters, numbers, and underscore).
        \\ W?: Matches an optional space followed by a W.
        \\d+: Matches one or more digits.
    1: Start position (begin search from the first character).
    1: Nth occurrence to return (return the first match).
    NULL: Match parameter (default behavior).
    0: Subexpression group to return (return the entire match, not a specific group within the parentheses). 

This formula will extract the first occurrence of an OCLC Number that starts with "(Nz)" or "(nz)" from the "Network Number" field and display it in your report. 
Important Notes:

    You may need to adjust the regular expression pattern to match the specific format of the OCLC numbers in your data.
    This is just one example. You can adapt the REGEXP_SUBSTR function with different regular expressions to extract various parts of strings in your Alma Analytics reports.
    Be sure to escape any special characters within your regular expression pattern, such as parentheses, brackets, and semicolons, with a backslash (\).
    If you need to extract the content of a specific subfield within a MARC field (like the 852 field), you may need to use a pattern that includes the subfield delimiter and identifier. 

## Ugly But Works

This works but it's ugly...
    CAST(REPLACE(REPLACE(SUBSTRING("Bibliographic Details"."Network Number" FROM LOCATE('grinnell:',"Bibliographic Details"."Network Number")+9 FOR 5),' ',''),'p;','') as INT)

## Works for Me!

This column formula from the `Numeric ID` field of `Migrant-Digital-Titles-MASTER` works, just note that the regex parameters like `\d+` are NOT double escaped as they are in some documentation!

```
CAST(Evaluate('regexp_substr(%1,%2,%3,%4,%5,%6)',"Bibliographic Details"."Network Number", 'grinnell:(\d+)', 1,1, NULL, 1) as INT)
```

A similar formula from `NEW-Digital-Titles-MASTER` reads like this:  

```
CAST(Evaluate('regexp_substr(%1,%2,%3,%4,%5,%6)',"Bibliographic Details"."Network Number", 'dg_(\d+)', 1,1, NULL, 1) as INT)
```

## Helpful Resource

https://digitalcommons.wku.edu/cgi/viewcontent.cgi?article=1020&context=ebug_newsletter - Covers a lot of stuff but not `Evaluate` and Oracle `regex`. 
