# Compound Object Handling Logic

## Overview
This document describes the logic for processing parent/children compound relationships in Alma metadata CSV files.

## Compound Relationship Detection

A **parent/children compound relationship** occurs when Alma metadata contains the following pattern in the `compoundrelationship` field:

1. A row with **"parent"** in the `compoundrelationship` column
2. Followed by **one or more adjacent rows** with **"child"** in the same column

The logic processes these relationships sequentially, identifying each parent and collecting all immediately following children before moving to the next potential parent.

## Processing Logic

### Step 1: Parent Detection
- Scan through CSV rows sequentially
- Identify rows where `compoundrelationship` value starts with "parent"
- Each detected parent initiates compound object processing

### Step 2: Child Collection
For each identified parent:
- Scan forward through subsequent CSV rows
- Collect all consecutive rows where `compoundrelationship` starts with "child"
- Stop collection when encountering:
  - A row that is not a child
  - The end of the CSV file

### Step 3: Validation
Before applying changes, validate the compound group:
- **Minimum Requirement**: At least 2 children per parent
- **If validation fails**:
  - Log error message
  - Mark parent's `mms_id` field with: `*ERROR* Too few children!`
  - Skip processing for this group

### Step 4: CSV Modifications

#### For the Parent Record:
1. **Set group_id**: 
   - `group_id` = parent's `originating_system_id`
   - This creates the linking identifier for the entire family

2. **Build Table of Contents (TOC)**:
   - For each child, create an entry containing:
     - Child's `dc:title`
     - Child's `dc:type` (if available)
   - Format each entry as: `"Title (Type) | "` or `"Title | "`
   - Concatenate all entries with pipe (`|`) separators
   - Store complete string in parent's `dcterms:tableOfContents` field

3. **Update object type**:
   - Set `dc:type` = "compound"
   - Clear `dcterms:type.dcterms:DCMIType` = "" (empty string)

#### For Each Child Record:
1. **Link to parent**:
   - Set `group_id` = parent's `originating_system_id`
   - This creates the relationship to the parent

2. **Set representation fields**:
   - `rep_label` = child's `dc:title`
   - `rep_public_note` = child's `dc:type`
   - These fields describe the digital representation in Alma

## Example

### Before Processing:
```csv
compoundrelationship,originating_system_id,dc:title,dc:type,group_id
parent:album,dg_1234567890,Summer Album,Collection,
child:page1,dg_1234567891,Page 1,StillImage,
child:page2,dg_1234567892,Page 2,StillImage,
child:page3,dg_1234567893,Page 3,StillImage,
```

### After Processing:
```csv
compoundrelationship,originating_system_id,dc:title,dc:type,group_id,dcterms:tableOfContents,rep_label,rep_public_note
parent:album,dg_1234567890,Summer Album,compound,dg_1234567890,"Page 1 (StillImage) | Page 2 (StillImage) | Page 3 (StillImage)",,
child:page1,dg_1234567891,Page 1,StillImage,dg_1234567890,,Page 1,StillImage
child:page2,dg_1234567892,Page 2,StillImage,dg_1234567890,,Page 2,StillImage
child:page3,dg_1234567893,Page 3,StillImage,dg_1234567890,,Page 3,StillImage
```

### Changes Applied:
- ✅ Parent's `group_id` = its own `originating_system_id` (dg_1234567890)
- ✅ All children's `group_id` = parent's `originating_system_id` (dg_1234567890)
- ✅ Parent's `dc:type` changed from "Collection" to "compound"
- ✅ Parent's `dcterms:tableOfContents` populated with formatted child entries
- ✅ Parent's `dcterms:type.dcterms:DCMIType` cleared
- ✅ Each child's `rep_label` set to its title
- ✅ Each child's `rep_public_note` set to its type

## Key Logic Points

### Sequential Processing
- The CSV is processed from top to bottom
- Each parent-children group is handled as a unit
- Multiple parent-children groups in one CSV are processed independently

### Group Identification
- The `group_id` field serves as the primary linking mechanism
- Parent's `originating_system_id` becomes the `group_id` for all members
- This allows Alma to recognize and assemble the compound object

### Table of Contents Format
- Entries are concatenated with pipe (`|`) separators
- Each entry includes both title and type when available
- Format: `Title1 (Type1) | Title2 (Type2) | Title3 (Type3)`
- Trailing pipe may be present after the last entry

### Error Handling
- Validates minimum child count (2) before processing
- Marks invalid parents with error message in `mms_id` field
- Continues processing remaining valid compound groups
- Safely handles missing columns or empty values

## Edge Cases

### Case 1: Single Child
```
Parent with 1 child → ERROR: Too few children!
```
Result: Error logged, no changes applied to that group

### Case 2: Non-Adjacent Children
```
parent:album
child:page1
<regular-row>     ← Breaks the group
child:page2       ← Not included with parent above
```
Result: Only page1 is associated with parent

### Case 3: Missing Optional Fields
- Missing `dc:title` → Entry added to TOC without title
- Missing `dc:type` → Entry added to TOC without type in parentheses
- Missing `dcterms:tableOfContents` column → Column not updated (safe)

### Case 4: Multiple Parent Groups
```
parent:album1
child:page1
child:page2
<regular-row>
parent:album2
child:page3
child:page4
```
Result: Two independent groups processed successfully

## Implementation Reference

This logic is implemented in Python using Pandas DataFrames with the following characteristics:

- **Framework**: Pandas (uses `.at[]` accessor for cell updates)
- **Mode**: Alma Digital workflows only
- **Timing**: Runs automatically during "Apply All Updates" operation
- **Logging**: Comprehensive INFO and ERROR logging for all operations
- **Safety**: Only processes when `compoundrelationship` column exists

For detailed implementation, see the comprehensive documentation in `ALMA-COMPOUND-HANDLING.md`.
