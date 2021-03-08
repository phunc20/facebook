When reading `ageron`'s `Julia for Pythonista.ipynb` on the section about strings and characters
in Julia, I had this need to print unicode characters. At that time, I did not devise
immediately a way to use sth like a for loop to print many unicode characters; I just write
things like `'\u0064'` many many times.

After discussing with people in the facebook group, I've got these as solutions:


### `Char` in Julia isn't much different from in C
One can do arithmetics on `Char` in Julia just like in C.<br>
And expressions like `Char(0)` and `'\u0000'` are really the same thing expressed in two
differently ways only.<br>
Thanks to
- `Peter Cheng`
- `Shao-Ching Huang`

for providing stimulating ideas.


```
julia> typeof(Char(0))
Char

julia> typeof('\u0000')
Char

julia> Char(0) == '\u0000'
true

julia> Char(65)
'A': ASCII/Unicode U+0041 (category Lu: Letter, uppercase)

julia> Char(65) + 1
'B': ASCII/Unicode U+0042 (category Lu: Letter, uppercase)

julia> Char(65) + 25
'Z': ASCII/Unicode U+005A (category Lu: Letter, uppercase)

julia> '\u0041'
'A': ASCII/Unicode U+0041 (category Lu: Letter, uppercase)

julia> '\u0041' + 1
'B': ASCII/Unicode U+0042 (category Lu: Letter, uppercase)

julia> String(['\u0000' + i for i in 0:127])
"\0\x01\x02\x03\x04\x05\x06\a\b\t\n\v\f\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\e
\x1c\x1d\x1e\x1f !\"#\$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijk
lmnopqrstuvwxyz{|}~\x7f"

julia> for i in 0:127
         print(String(['\u0000' + i]))
       end



123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
julia> String([Char(i) for i in 0:127])
"\0\x01\x02\x03\x04\x05\x06\a\b\t\n\v\f\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\e
\x1c\x1d\x1e\x1f !\"#\$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijk
lmnopqrstuvwxyz{|}~\x7f"

julia> Char(0):Char(127)
'\0':1:'\x7f'

julia> collect(Char(0):Char(127))
128-element Array{Char,1}:
 '\0': ASCII/Unicode U+0000 (category Cc: Other, control)
 '\x01': ASCII/Unicode U+0001 (category Cc: Other, control)
 '\x02': ASCII/Unicode U+0002 (category Cc: Other, control)
 '\x03': ASCII/Unicode U+0003 (category Cc: Other, control)
 '\x04': ASCII/Unicode U+0004 (category Cc: Other, control)
 '\x05': ASCII/Unicode U+0005 (category Cc: Other, control)
 '\x06': ASCII/Unicode U+0006 (category Cc: Other, control)
 '\a': ASCII/Unicode U+0007 (category Cc: Other, control)
 '\b': ASCII/Unicode U+0008 (category Cc: Other, control)
 '\t': ASCII/Unicode U+0009 (category Cc: Other, control)
 '\n': ASCII/Unicode U+000A (category Cc: Other, control)
 '\v': ASCII/Unicode U+000B (category Cc: Other, control)
 '\f': ASCII/Unicode U+000C (category Cc: Other, control)
 ⋮
 't': ASCII/Unicode U+0074 (category Ll: Letter, lowercase)
 'u': ASCII/Unicode U+0075 (category Ll: Letter, lowercase)
 'v': ASCII/Unicode U+0076 (category Ll: Letter, lowercase)
 'w': ASCII/Unicode U+0077 (category Ll: Letter, lowercase)
 'x': ASCII/Unicode U+0078 (category Ll: Letter, lowercase)
 'y': ASCII/Unicode U+0079 (category Ll: Letter, lowercase)
 'z': ASCII/Unicode U+007A (category Ll: Letter, lowercase)
 '{': ASCII/Unicode U+007B (category Ps: Punctuation, open)
 '|': ASCII/Unicode U+007C (category Sm: Symbol, math)
 '}': ASCII/Unicode U+007D (category Pe: Punctuation, close)
 '~': ASCII/Unicode U+007E (category Sm: Symbol, math)
 '\x7f': ASCII/Unicode U+007F (category Cc: Other, control)

julia> [(i, UInt16(i), Char(i)) for i in 0:1000]
1001-element Array{Tuple{Int64,UInt16,Char},1}:
 (0, 0x0000, '\0')
 (1, 0x0001, '\x01')
 (2, 0x0002, '\x02')
 (3, 0x0003, '\x03')
 (4, 0x0004, '\x04')
 (5, 0x0005, '\x05')
 (6, 0x0006, '\x06')
 (7, 0x0007, '\a')
 (8, 0x0008, '\b')
 (9, 0x0009, '\t')
 (10, 0x000a, '\n')
 (11, 0x000b, '\v')
 (12, 0x000c, '\f')
 ⋮
 (989, 0x03dd, 'ϝ')
 (990, 0x03de, 'Ϟ')
 (991, 0x03df, 'ϟ')
 (992, 0x03e0, 'Ϡ')
 (993, 0x03e1, 'ϡ')
 (994, 0x03e2, 'Ϣ')
 (995, 0x03e3, 'ϣ')
 (996, 0x03e4, 'Ϥ')
 (997, 0x03e5, 'ϥ')
 (998, 0x03e6, 'Ϧ')
 (999, 0x03e7, 'ϧ')
 (1000, 0x03e8, 'Ϩ')

julia>

```




