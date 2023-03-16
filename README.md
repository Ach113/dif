# dif 
implementation of `diff` in Python. 
Works more like `git diff`, as `dif` displays not just the differences between lines, 
but also the line numbers where the changes occurred, much like `git diff`.

## How to run:
`python dif.py <file1> <file2>`

## Output:
<font color="red"><pre>1 - #include "stdio.h"</font> \
<font color="green">1 + #include &lt;iostream></font> \
<font color="green">2 + using namespace std;</font> \
<font color="lightgray">3   </font> \
<font color="lightgray">4   int main() {</font> \
<font color="red">5 -     printf("Hello world!\n");</font>  \
<font color="green">5 +     cout << "Hello world!" << endl;</font> \
<font color="lightgray">6       return 0;</font> \
<font color="lightgray">7   }</pre></font> 