# Write-up 3

**Name:** Leslie Chan  
**Student ID:** lchan8  
**Date:** 11/23/2025  

---
## Data.md
**Database**

Couldn't figure out how to run Slurm jobs in container, so ended up running the script with the sbatch file in container terminal.

- 3 tables will be created in the bacteria_db database.
    - GFF table
    - Protein cluster table
    - Metadata table
- 5 parallel tasks are executing simultaneously as set up in the array job. SQLite uses file-level locking, where when one process is writing to the database, it locks the entire file, preventing other processes from writing simultaneously. Thus, here the "try" and "except" is used to create the following logic
    - Try to write to the SQL database.
    - If it succeeds, break out of the loop.
    - If it fails with a "database is locked" error, wait 1 second and retry.
    - If it fails with any other error, re-raise that error and don't retry.
    - If it fails max-retries times, don't retry (give up).

**Screenshot**
![Screenshot showing create_bacteria_db.sh script finished running in container](./create_bacteria_db_in_container_screenshot.png)

## Overview

This section introduces the purpose of the write-up.  
For example:  
> This document is a practice exercise in writing and formatting Markdown files clearly and professionally.

---

## Content

This is the main part of your write-up.  
You can include explanations, examples, and notes 

You can use some text formating, lists, and tables to imporve the write-up readability
#### **Text Formatting**

You can make text **bold**, *italic*, or even ***bold and italic*** for emphasis.

#### **Lists**

**Unordered list:**
- Apple  
- Banana  
- Cherry  

**Ordered list:**
1. First step  
2. Second step  
3. Third step  

#### **Table Example**

| Tool | Description         | Example Command        |
|------|---------------------|------------------------|
| `ls` | Lists files         | `ls -la`               |
| `grep` | Searches text     | `grep "pattern" file.txt` |
| `wc` | Counts words/lines  | `wc -l filename.txt`   |

Code snippets and images are highly recommended to document your work.

#### **Code Examples**

**Inline code example:** Use the `print()` function to display text.  

**Code block example:**

```bash
# Example command line code
echo "Hello, Markdown!"
```

```python
# Example Python code
for i in range(3):
    print("Iteration:", i)
```

For longer script, you can say something like, `script1.py` contains functions for reading fasta file. Ideally, all codes you run should be saved in corresponding files. 


#### **Image Example**

![Example placeholder image](./snyderlab.png)

#### **Link Example**

Learn more about Markdown syntax here:  
[Markdown Guide](https://www.markdownguide.org/basic-syntax/)

---


## Acknowledgement
Collaborator: Brady Hislop
