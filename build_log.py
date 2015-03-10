#!/usr/bin/python
# Purpose: Turn nightly build summary text files into table rows and output the table as an html page
# Usage: argument 1 .. n = complete path to individual build summary files
#        ( ex. /export/home/autobuild/autobuild_x86_64/nightly0.txt )

import sys
import string
import platform
import re
import codecs

arch = platform.processor()
problem = 0
problem_count = 0
thisrow = ""
str_list = []
html_start = []
html_table1 = ""
html_table2 = ""
html_problems = []
html_rows = []
jump_behind_int = 0
done_first_section_flag = 0

page_color = "#4477aa"
table_color = "#f0f0dd"
border_color = "#6699cc"

html_start.append("<html><head><style type=\"text/css\">")
html_start.append("     .normal-text {")
html_start.append("         font-family: Verdana;")
html_start.append("         font-weight: normal;")
html_start.append("         font-size: 12px;")
html_start.append("         color: black;")
html_start.append("         background-color: " + table_color + "; }")
html_start.append("     .green-text {")
html_start.append("         font-family: Verdana;")
html_start.append("         font-weight: normal;")
html_start.append("         font-size: 12px;")
html_start.append("         color: black;")
html_start.append("         background-color: lightgreen; }")
html_start.append("     .build-text {")
html_start.append("         font-family: Verdana;")
html_start.append("         font-weight: normal;")
html_start.append("         font-size: 12px;")
html_start.append("         color: white;")
html_start.append("         background-color: " + border_color + "; }")
html_start.append("     .gtk_warning-text {")
html_start.append("         font-family: Verdana;")
html_start.append("         font-weight: normal;")
html_start.append("         font-size: 12px;")
html_start.append("         color: black;")
html_start.append("         background-color: #fcc000; }")
html_start.append("     .warning-text {")
html_start.append("         font-family: Verdana;")
html_start.append("         font-weight: normal;")
html_start.append("         font-size: 14px;")
html_start.append("         color: black;")
html_start.append("         background-color: yellow; }")
html_start.append("     .error-text {")
html_start.append("         font-family: Verdana;")
html_start.append("         font-weight: bold;")
html_start.append("         font-size: 14px;")
html_start.append("         color: white;")
html_start.append("         background-color: red; }")
html_start.append("     .segfault-text {")
html_start.append("         font-family: Verdana;")
html_start.append("         font-weight: bold;")
html_start.append("         font-size: 14px;")
html_start.append("         color: black;")
html_start.append("         background-color: ff00ff; }")
html_start.append("     .executing_unit_tests-text {")
html_start.append("         font-family: Verdana;")
html_start.append("         font-weight: normal;")
html_start.append("         font-size: 14px;")
html_start.append("         color: white;")
html_start.append("         background-color: #ff9000; }")
html_start.append("</style></head><body bgcolor=" + page_color + ">")

sectionwatch = []
lastsection = ''
count = 0
for line in codecs.open(sys.argv[1],'r','utf-8'):
    count += 1
    problem = 0
    sectionwatch.append(line)
    problem_count += 1
    str_count = ''.join(`problem_count`)
    if re.search("segmentation",line,re.IGNORECASE):
        line_color = "segfault-text"
        problem = 1
    elif re.search("Gtk-WARNING",line,re.IGNORECASE):
        if re.search("cannot add non scrollable widget use gtk_scrolled_window_add_with_viewport",line,re.IGNORECASE):
            problem = 0
        else:
            line_color = "gtk_warning-text"
            problem = 1
    elif re.search("warning[: ]",line):
        if re.search("autoheader: WARNING:",line):
            problem = 0
        else:
            line_color = "warning-text"
            problem = 1
    elif re.search(" error: 0",line):
        line_color = "normal-text"
        problem = 0
    elif re.search(" Errors: 0",line,re.IGNORECASE) and re.search(" Failures: 0",line,re.IGNORECASE):
        line_color = "normal-text"
        problem = 0
    elif re.search(" Errors: ",line) or re.search(" Failures: ",line):
        line_color = "error-text"
        problem = 1
    elif re.search(" error[: ]",line) or re.search(" Error ",line):
        line_color = "error-text"
        problem = 1
    else:
        line_color = "normal-text"
        problem = 0

    if problem == 1:
        behindcount_int = int(str_count) - jump_behind_int
        behindcount = str(behindcount_int)
        thisrow = "<tr><td class=\"" + line_color + "\"><a href=\"#" + behindcount + "\">" + str_count + "</a></td><td class=\"" + line_color + "\"><a href=\"#" + behindcount + "\">" + line + "</td></a></tr>"
        
        # BACKTRACK TO GET SECTION
        sectionwatch.reverse()
        insectioncount = 0
        for x in sectionwatch:
            count += 1
            if re.match("Building.*:", x):
                section = x
                break
            if re.match("Executing Unit Tests.*:", x):
                section = x
                break
            else:
                section = "No regex match with \"Building.*:\" or \"Executing Unit Tests.*:\" -- This should never happen!"
        sectionwatch.reverse()
        htmlsection = "<tr><td colspan=2>" + section + "</td></tr>"
        if section != lastsection:
            lastsection = section
            if done_first_section_flag > 0:
                htmlbreakup = "</table><p></p><table border=\"1\" cellpadding=\"0\" cellspacing=\"0\" width=\"95%\" style=\"background-color:" + table_color + ";border:5px solid " + border_color + ";\">"
                thisrow = htmlbreakup + htmlsection + thisrow
            else:
                done_first_section_flag += 1
                thisrow = htmlsection + thisrow
        else:
            # section is the same as lastsection
            pass
        
        # END BACKTRACK TO GET SECTION
        html_problems.append(thisrow)
    else:
        # No problems
        pass

'''going through the list backwards now, looking for sections'''
count = 0
for line in codecs.open(sys.argv[1], mode='r', encoding='utf-8'):
    count += 1
    str_count = ''.join(`count`)

    if re.search("segmentation",line,re.IGNORECASE):
        line_color = "segfault-text"
    elif re.match("Building ",line):
        line_color = "build-text"
    elif re.match("Executing Unit Tests.*:",line):
        line_color = "executing_unit_tests-text"
    elif re.match("OK \(",line):
        line_color = "green-text"
    elif re.search("Gtk-WARNING",line,re.IGNORECASE):
        line_color = "gtk_warning-text"
    elif re.search("warning[: ]",line):
        if re.search("autoheader: WARNING:",line):
            line_color = "normal-text"
        else:
            line_color = "warning-text"
    elif re.search(" error: 0",line):
        line_color = "normal-text"
    elif re.search(" Errors: 0",line) and re.search(" Failures: 0",line):
        line_color = "normal-text"
    elif re.search(" Errors: ",line) or re.search(" Failures: ",line):
        line_color = "error-text"
    elif re.search(" error[: ]",line) or re.search(" Error ",line):
        line_color = "error-text"
    else:
        line_color = "normal-text"

    thisrow = "<tr><td class=\"" + line_color + "\"><a name=\"" + str_count + "\">" + str_count + "</a></td><td class=\"" + line_color + "\">" + line + "</td></a></tr>"
    html_rows.append(thisrow)

str_list.append("<center><H1>Build Problems</H1>")
str_list.append("<H3>(The problems below are clickable)</H3><table border=\"1\" cellpadding=\"0\" cellspacing=\"0\" width=\"95%\" ")
str_list.append("style=\"background-color:" + table_color + ";border:5px solid " + border_color + ";\">\n<tr>")
html_table1 = html_table1 + ''.join(str_list)
str_list = []

str_list.append("<center><H1>Complete Build Log</H1>")
str_list.append("<H4>" + sys.argv[1] + "</H4><table border=\"1\" cellpadding=\"0\" cellspacing=\"0\" width=\"95%\" ")
str_list.append("style=\"background-color:" + table_color + ";border:5px solid " + border_color + ";\">\n<tr>")
html_table2 = html_table2 + ''.join(str_list)
str_list = []

html_table_close = "</table></center>"
html_finish = "</body></html>"


outfile = codecs.open(sys.argv[2],"w","utf-16")

for row in html_start:
    outfile.write( row )
outfile.write( html_table1 )
for row in html_problems:
    outfile.write( row )
outfile.write( html_table_close )
outfile.write( html_table2 )
for row in html_rows:
    outfile.write( row )
outfile.write( html_table_close )
outfile.write( html_finish )

outfile.close()
sys.exit()
