#!/usr/bin/python
# Purpose: Turn nightly build summary text files into table rows and output the table as an html page
# Usage: argument 1 .. n = full path to individual build summary files (ex. /export/home/autobuild/nightly0.txt)

import sys
import string
import platform
import re
import time

todaysdate = str(time.localtime()[1]) + "/" + str(time.localtime()[2]) + "/" + str(time.localtime()[0])
count = 0
str_list = []
html_start = ""
html_table = ""
html_rows = []

page_color = "#4477aa"
table_color = "#f0f0dd"
border_color = "#6699cc"

g1_bg = "#4aaa4a"
g1_text = "black"
g2_bg = "black"
g2_text = "#30ff30"

w1_bg = "yellow"
w1_text = "black"
w2_bg = "black"
w2_text = "yellow"

e1_bg = "red"
e1_text = "black"
e2_bg = "black"
e2_text = "#ff3030"

for x in sys.argv:
    if x == sys.argv[1]:
        # get the architecture from the first argument
        arch = x
    elif x == sys.argv[0]:
        # argv[0] is the program's filename itself -- use this iteration to write out the opening html and css
        html_start = '''<html><head><style>
.good_color {background-color:''' + g1_bg + '''; color:''' + g1_text + '''; text-align:left; }
.good_color2 {background-color:''' + g2_bg + '''; color:''' + g2_text + '''; text-align:left; }
.warn_color {background-color:''' + w1_bg + '''; color:''' + w1_text + '''; text-align:left; }
.warn_color2 {background-color:''' + w2_bg + '''; color:''' + w2_text + '''; text-align:left; }
.error_color {background-color:''' + e1_bg + '''; color:''' + e1_text + '''; text-align:left; }
.error_color2 {background-color:''' + e2_bg + '''; color:''' + e2_text + '''; text-align:left; }
</style></head><body bgcolor=''' + page_color + ">"

        # write the table header
        str_list.append("<center><H1>Autobuild Summary for " + todaysdate + "</H1><table border=\"1\" cellpadding=\"9\" cellspacing=\"9\" width=\"90%\" ")
        str_list.append("style=\"background-color:" + table_color + ";border:5px solid " + border_color + ";\">\n<tr>")
        str_list.append("<th style=\"text-align:left\"># of Days old</th>")
        str_list.append("<th style=\"text-align:left\">Click on a Summary to view the corresponding build log.</th></tr>")
        html_table = html_table + ''.join(str_list)
    else:
        # 2nd argument and higher are the real args, dump the contents into the next table row
        infile = file(x,'r')
        content = infile.read()
        str_count = ''.join(`count`)
        str_content = ''.join(content)
#        str_content = "<a href=\"" + arch + "_build.log_" + str_count + ".html\">" + ''.join(content) + "</a>"
        # check for warnings and errors and pick the corresponding icon to display
        if re.search("Errors: 0, Warnings: 0, Missing Rules: 0",str_content):
            result = "good_color"
            resultmouse = "good_color2"
        elif re.search("Errors: 0, Warnings",str_content):
            result = "warn_color"
            resultmouse = "warn_color2"
        else:
            result = "error_color"
            resultmouse = "error_color2"

        thisrow = "<tr class='" + result + "'><td align=center>" + str_count + "</td><td OnMouseOver=\"this.className='" + resultmouse + "'\" OnMouseOut=\"this.className='" + result + "'\" OnClick=\"window.location.href='" + arch + "_build.log_" + str_count + ".html'\">" + str_content + "</td></tr>"
        html_rows.append(thisrow)
        count += 1

html_finish = "</table></center></body></html>"

print html_start
print html_table
for row in html_rows:
    print row
print html_finish

sys.exit()
