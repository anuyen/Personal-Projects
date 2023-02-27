# Script for cleaning data

## Step 1: Clean all duplicates

Most of the time, the file will have some duplicate data.

So clean duplicates based on 2 filters:

    Linkedin_id
    Job_title

## Step 2: Domain cleaning

Clean domain by removing what’s after the .com
keep only the .com, .fr, .net, etc… and clean what is after.

Examples:

    www.google.com/images -> www.google.com
    https://facebook.fr/fuiewfwefuib -> facebook.com

## Step 3: Remove "null" values in "overview" and "website" column

Delete these values so there is no information inside the cell.

## Step 4: Guess country based on location

- First check if a country is already available
- If country not available, then check if country name is included in location data

    (list of countries is provided)

- If country name is not available, use chat gpt to find the corresponding country

- Update dictionary with {"location_name":"country"}

        For this step, we can probably use something like this:
        1. Check country column
        2. Check if country name is in set['country_names'] from location column
        3. Use chat gpt ext to search up the location, extract country name and update column

## Step 5: Clean first and last name

- Remove all information after a comma
- When there is a first name with 2 names and “” at the end of the second first name, remove that second first name
- Take out all the first and last names between ( ), [ ], “ ”
- If first name ends with a comma, switch first name with last name
- If first name with 2 names and ends with a comma
- If 2 names in first name, or 2 names in last name, keep only the 1st name
- Remove all lines with other alphabets
- Clean the names with Uppercase for first letter, and lower case for the rest of the letters
- Take out all the English honorifics such as "Dr.", "Sr.", "Mr."
- First name: remove solo characters or characters followed by punctuation sign(s)
- If the first name has “Letter.” and another name, remove the “letter.”, but keep when only “letter.” with no other information
- Extract all lines in a separate tab which contain in first name or last name:

        one character 
        one character + punctuation
        Blank

## Step 6: Guess gender based on first name

## Step 7: Clean up company names
