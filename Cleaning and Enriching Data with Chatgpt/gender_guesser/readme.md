# Gender guesser mini app

## A primitive gender guesser

Data is from: https://www.openml.org/search?type=data&status=active&id=42996

Data includes both count and probability for each gender in each name

I first picked the higher count of each name 

    For example:
    _Charlie --> Count: Male: 100, Female: 50
    (Male is picked here because it has the higher count)
    _Charlie --> Male: 100

Then, a basic statistical analysis was done and I selected the 25 percentile and above of the Probability column --> If in the lower 25% then the name will be assigned Androgenous

This dataset is a good starting point, I will write a program that returns the gender from this list given a name, if name is not found in the existing data set, gender-api.com is called to guess the first name's gender and update the existing database

Might even add chatgpt is second line of defense in case I run out of api calls from gender api