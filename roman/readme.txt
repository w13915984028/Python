
[usage]:

#  python3 roman.py roman_numeral_test.txt  -f
#  param 1: 
#   file name like: a.txt: used as input file
#   if not given, use roman_numeral_test.txt as default
#  param 2:
#   -f: with it, output is composed of input and output
#       without, output is only numbers/error message

# python3 romanExtended.py roman_numeral_test.txt  -f
#  When use the extended version, it has additional 3 rules as below
#   "IIII",   4
#   "XXXX",  40
#   "CCCC", 400

# The script itself doesn't wirte output to file, if want, please use cmd like
# python3 romanExtended.py roman_numeral_test.txt -f  > out.txt


[Various test]
 [test of: non-existing input file]
$ python3 roman.py not_existing_file.txt
input file: not_existing_file.txt is not existing/open error, CHECK

 [test of: empty input file]
$ python3 roman.py empty_input.txt
input file: empty_input.txt is empty, CHECK

 [test of: a file full of error input]
$ python3 roman.py error_input.txt
IM             : is not a valid roman numeral, at index:2
VIVI           : is not a valid roman numeral, at index:3
XYZ            : is not a valid roman numeral
VIAI           : is not a valid roman numeral

 [test of: the given input file]
$ python3 roman.py roman_numeral_test.txt  -f
I              :         1
II             :         2
III            :         3
IIII           : is not a valid roman numeral, error at index:4
IV             :         4
V              :         5
VI             :         6
VII            :         7
VIII           :         8
IX             :         9
X              :        10
XIIII          : is not a valid roman numeral, error at index:5
XI             :        11
XII            :        12
XIII           :        13
XIV            :        14
XV             :        15
XVI            :        16
...

MMMCMLXXXXIX   : is not a valid roman numeral, at index:10
MMMCMXC        :      3990
MMMCMXCI       :      3991
MMMCMXCII      :      3992
MMMCMXCIII     :      3993
MMMCMXCIV      :      3994
MMMCMXCV       :      3995
MMMCMXCVI      :      3996
MMMCMXCVII     :      3997
MMMCMXCVIII    :      3998
MMMCMXCIX      :      3999
MMMM           : is not a valid roman numeral, at index:4
CVIIIIIX       : is not a valid roman numeral, at index:6

$ python3 roman.py roman_numeral_test.txt
1
2
3
IIII           : is not a valid roman numeral, error at index:4
4
5
6
7
8
9
10
XIIII          : is not a valid roman numeral, error at index:5
11
12
13
14
15
16

$ python3 romanExtended.py roman_numeral_test.txt -f
I              :         1
II             :         2
III            :         3
IIII           :         4
IV             :         4
V              :         5
VI             :         6
VII            :         7
VIII           :         8
IX             :         9
X              :        10
XIIII          :        14
XI             :        11
XII            :        12
XIII           :        13
XIV            :        14
XV             :        15
XVI            :        16

$ python3 romanExtended.py roman_numeral_test.txt
1
2
3
4
4
5
6
7
8
9
10
14
11
12
13
14
15

