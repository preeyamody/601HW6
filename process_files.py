# 36601 HW6, Oct. 2018
# Your name: Preeya Mody

# This is a repeat of HW2, but in Python.
# This file should be called "process_files.py".
# See the function requirements in the comments.
# See the assignment requirements in "601HW6.pdf".

import sys  # for command line arguments
import os  # for variou path and file processing functions
import re


def process_files(folder=".", maxTimes=10):
    """
    Process all .txt files in one directory for Energy Monitor, Inc.

    INPUT:
       folder: 'str' with a relative or absolute folder
       maxTimes: 'int' with maximum observation times

    OUTPUT:
    Combined results are printed to "stdout".  The output
    is in a form suitable for redirection to a .csv file.

    The output has a header of the form:
    "filename", "location", "year", "month", "day", "v1", ...,
    "vM", "t1", ..., "tM"
    where "M" is 'maxTimes'.

    The output continues with one line per data line from
    each file, with quoted strings for base file name and location,
    and unquoted numbers for the remaining values, with "N/A" for
    each value where the supplied number of values and times is
    less than 'maxTimes'.

    DETAILS:
    Valid files start with this header line:
    # integerCode yyyy-mm-dd
    Nothing is printed if the header is invalid.

    The remainder of the file is any mixture of single data lines
    or a multiplier line followed by a data line.

    Data lines have this form:
    location; v1, ..., vN; t1, .. tN

    where v# and t1 (values and times) are numeric, and
    N <= maxTimes.

    Multiplier lines have this form:
    mult realNumber

    The presence of a multiplier line indicates that the values
    (not the times) for the next line should be multiplied by
    the realNumber.

    We can assume that, if the header is valid, if follows the
    above form exactly (though the location may have embedded
    spaces), and that each data line contains the same number
    of times as it has values.

    If a file is not readable, the function will end with
    the corresponding Python-raised error.
    """

    # Check input and obtain folder
    if not os.path.isdir(folder):
        raise TypeError(folder + " is not a valid directory")

    # Obtain a list of .txt files
    files = []
    for f in os.listdir(folder):
        f_full = os.path.join(folder, f)
        if not os.path.isfile(f_full):
            continue
        if not f[-4:] == ".txt":
            continue
        files.append(f)

    # Output the header line
    header = '"filename", "location", "year", "month", "day"'
    vals = ', '.join(['"v' + str(ii + 1) + '"' for ii in range(maxTimes)])
    times = ', '.join(['"t' + str(ii + 1) + '"' for ii in range(maxTimes)])
    print(header, ", ", vals, ", ", times, sep="")

    # Process and print file each file in turn
    for f in [os.path.join(folder, f) for f in files]:
        dtf = file_name_to_dtfs(f, maxTimes)
        for s in dtf:
            print(s)


def file_name_to_dtfs(fname, maxTimes):
    """ Return a "data.frame" for one (fully specified) file name.

    INPUT: a full-path file name

    OUTPUT: a list of 'str's, where each string is a data row
            as defined below.

    We define data.frame as a list of str's of the form:
    "filename, year, month, day, location, v1, ..., vN, t1, ..., tN"
    where v is a value, t is a time and N is 'maxTimes'.  The file
    name has the path stripped off.

    If the input file does not start with a valid header, return an
    empty list.

    Assume that if the date has two dashes then everything else in the
    date is appropriate.

    Stop with an error if the number of values is more than 'maxTimes'.
    """
    # Setup regular expression to match a full valid header line
    headerRE = re.compile("<<code>>")

    # Open the file
    fp = open(fname, "r")

    # Setup output and variable that keep track of status
    dtf = []
    on_header = True
    mult = 1.0  # multiplier for all values on a line

    # Process each line in the file
    for line in fp:
        line = line.strip(" \n")
        if on_header:
            # Process header (extract year, month, day into list 'ymd')
            on_header = False
            # Return empty list if header is invalid
            if headerRE.search(line) is None:
                return []
            ymd = line[<<code>>].split("-")
        elif line.startswith("mult ") and line.count(";") == 0:
            # Extract the multiplier (as a number)
            mult = <<code>>
        else:
            # Process a data line
            location, _, RHS = line.partition(";")
            values, _, times = RHS.partition(";")

            # Compute number of values and quit if more than 'maxTimes'
            n = values.count(",") + 1
            if n > maxTimes:
                raise IndexError("number of values in " + fname +
                                 " is greater than 'maxTimes'")

            # Multiply values by converting to numeric (and the back to 'str')
            if mult != 1.0:
                values = [mult * float(x) for x in values.split(",")]
                values = <<code: convert to comma-separated string>>
                mult = 1.0  # setup for next line read

            # Add N/A padding out to 'maxTimes'
            if (n < maxTimes):
                nas = <<code: what needs to be appended to values and times>>
                values = values + nas
                times = times + nas

            # Construct initial portion of 'data.frame' row string
            prefix = '"' + os.path.basename(fname) + '", "' +\
                     location + '", ' + \
                     ', '.join(ymd)

            # Complete 'data.frame' row string
            row_data = prefix + ", " + values + ", " + times

            # Add data.frame row to data.frame
            <<code>>
    return dtf


#    One way to use process_files() is to work at the Python prompt and
# run "import process_files".  Then a directory can be processed by
# using "process_files(directory_name).
#    Alternatively, a python file can import process_files and run
# processFiles().
#    Finally a user may process a folder by entering "python process files"
# or, e.g., "python process_files spamDir eggs" where "spamDir" is a
# directory and "eggs" is the maximum observation times.
#
#    A terminal section of code that checks if '__name__' is equal
# to "__main__" will only run in the third case above, i.e., if
# the code is run at the operating system prompt.
#
#     Here we use sys.argv[] to check the user's syntax and run the
# process_files() code.  Note that sys.argv[0] is equal to the
# name of the python file, sys.argv[1] is the first argument,
# etc.
#
if __name__ == "__main__":
    # Check for valid syntax
    if len(sys.argv) > 3:
        raise Exception('call syntax: processFiles [folder="." [maxTimes=10]]')
    maxTimes = 10

    # Extract folder and 'maxTimes' or default appropriately
    if len(sys.argv) == 1:
        folder = os.getcwd()
    else:
        folder = sys.argv[1]
        if not os.path.isdir(folder):
            raise Exception(folder + " is not a valid directory")
        if len(sys.argv) == 3:
            maxTimes = int(sys.argv[2])

    # Process the files in the folder by calling the function
    process_files(folder, maxTimes)
