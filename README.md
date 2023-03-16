# dif 
implementation of `diff` in Python. 
Works more like `git diff`, as `dif` displays not just the differences between lines, 
but also the line numbers where the changes occurred, much like `git diff`. \

Utilizes [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) to calculate
minimum number of operations (and type of operations) required to transform `<file1>` to `<file2>`.

## How to run:
`python dif.py <file1> <file2>`

## Output:
![sample_output](https://i.imgur.com/iEIqiG4.png)
