#!/bin/sh 
#
#  build.sh - The Scheduled Build script for the software.
#
# The build script accepts the following input parameters
#    <svn_repository> : svn trunk or branch to check out code from
# 
#    <target_name> : The target directory name for the build.  Defaults
#                       to the current date (YYYYMMDD) + "_" + a 2-digit 
#                       sequence number.
#
#    <Doxygen document generation flag> : 0 or 1. If set to 1, documentation would be created for the modules 
#                                                 specified by INPUT tag in Documentation/Doxygen/doxygenConfigFile.txt
#                                                 If set to 0, documentation would not be generated
#  
# The build script will create a subdirectory of the specified target_name
#  under an architecture-specific subdirectory of the Build Home location.
#  So if the Build Home location is /export/builds/, and the script is run
#  on a Motorola PPC system with the target_name specified as "test_build", 
#  the build will be placed in /export/builds/ppc/test_build/.
#

BUILD_HOME=/export/builds/autobuild
ARCH_TYPE=`uname -m`
BUILD_NOTIFICATIONS="admin@domain.com,other@domain.com"
BUILD_START_TIME=`date`

#############################################################################
# Function to calculate the Target Build Directory
#
function calculateTargetDir()
{
    if [ ! -d ${BUILD_HOME}/${ARCH_TYPE} ]
    then
        echo "Creating directory ${BUILD_HOME}/${ARCH_TYPE} ..."
        mkdir -p ${BUILD_HOME}/${ARCH_TYPE}
    fi

    CURDATE=`date +%Y%m%d`
    found_it=0

    for ((num=1; num<=99 && found_it==0;num++)); do
        SEQNUM=`printf "%02d" ${num}`
        TARGET_DIR=${BUILD_HOME}/${ARCH_TYPE}/${CURDATE}_${SEQNUM}
	if [ ! -d ${TARGET_DIR} ]; then
	    found_it=1
	fi
    done

    if [ -d ${TARGET_DIR} ]; then
        echo "Error: target directories ${CURDATE}_01-99 already exist in ${BUILD_HOME}/${ARCH_TYPE}/."
	exit 1
    fi
}

#########################   Main   #############################
# Need to do some additional setup to be able to run svn from a cron 
#  job on the Motorola PPC linux distribution...
source /etc/profile
PATH=${PATH}:/usr/local/bin

# The command must be invoked with 0 or 3 arguments, otherwise display usage information
if [ $# -eq 1 -o $# -eq 2 -o $# -ge 4 ]
then
   # We need both svn repository and target directory name
   echo "********************************************************************************************************************"
   echo "Usage - 1) $0 <svn repository> <target directory> <documentation generation flag( 0 or 1)>"
   echo "        2) $0"
   echo ""
   echo "NOTE: If all the flags are omitted (as in option 2), svn repository would be the trunk"
   echo "and target directory would be <BUILD_HOME>/<ARCH_TYPE>/<YYYYMMDD_SEQUENCE NUMBER>"
   echo "and documentation generation flag would be 0 or false"
   echo "********************************************************************************************************************"
   exit 1
fi

if [ -n "${1}" ] 
then
    # Set the target directory to what was specified on the command line
    SVN_REPOSITORY=${1}
else
    # No svn repository specified... Default to the trunk i.e. "svn://host/target"
    SVN_REPOSITORY="svn://host/target/trunk"
fi

if [ -n "${2}" ] 
then
    # Set the target directory to what was specified on the command line
    TARGET_DIR=${BUILD_HOME}/${ARCH_TYPE}/${2}
else
    # No target directory was specified... calculate it...
    calculateTargetDir
fi

if [ -n "${3}" ]
then
    # Set the target directory to what was specified on the command line
    DOCUMENTATION_GENERATION=${3}
else
    # No documentation generation flag specified... Set it to 0 or false
    DOCUMENTATION_GENERATION=0
fi


if [ -d ${TARGET_DIR} ]; then
    echo "Error: target directory ${TARGET_DIR} already exists."
    exit 1
fi

# First create the target directory (so we can put our build.log file there)
mkdir -p ${TARGET_DIR}

# Now do the checkout and build, logging the output to a build.log file
cd ${HOME}
./checkout_and_build.sh ${SVN_REPOSITORY} ${TARGET_DIR} &>${TARGET_DIR}/build.log 

# Perform any post-build processing here... (e.g. e-mail notification?)

#NUM_ERRORS=`grep -v "A " ${TARGET_DIR}/build.log | egrep -i " error[: ]" | wc -l`
NUM_ERRORS=`grep -v "A " ${TARGET_DIR}/build.log \
  | grep -i -e " error[: ]" -e "Failures: " -e "Errors: " \
  | grep  -v "error[s: 0|: 0]" | grep -v "Failures: 0  Errors: 0" | wc -l`

NUM_WARNINGS=`egrep -i "warning[: ]" ${TARGET_DIR}/build.log \
  | grep -v "autoheader: WARNING:" \
  | grep -v "cannot add non scrollable widget use gtk_scrolled_window_add_with_viewport() instead" \
  | wc -l`

NUM_MISSING_RULES=`egrep -i " No rule to make target " ${TARGET_DIR}/build.log | wc -l`

BUILD_END_TIME=`date`

echo "Build started ${BUILD_START_TIME}, completed ${BUILD_END_TIME}... "
echo "  Errors: ${NUM_ERRORS}, Warnings: ${NUM_WARNINGS}, Missing Rules: ${NUM_MISSING_RULES}, Build Location: ${TARGET_DIR}/." 

# Check to see if documentation generation flag is set. If the flag is set to 0, no documentation would be generated
# Otherwise documentation would be generated.
if [ $DOCUMENTATION_GENERATION -gt 0 ]
then
   echo "Documentation Generation flag is set to a positive number. Generating Doxygen Documentation..."
   # Check to see if doxygenConfigFile.txt exists underneath Documentation/Doxygen directory
   if [ -f "$TARGET_DIR/Documentation/Doxygen/doxygenConfigFile.txt" ]
   then
     # Generate Doxygen documentation
     # The output directory is specified by OUTPUT_DIRECTORY option in Documentation/Doxygen/doxygenConfigFile.txt file

     # First cd to the TARGET_DIR as the directories specified in INPUT option are relative to the TARGET_DIR
     cd $TARGET_DIR
     # Now invoke doxygen
     /usr/bin/doxygen `echo $TARGET_DIR`/Documentation/Doxygen/doxygenConfigFile.txt
   else
      echo "$TARGET_DIR/Documentation/Doxygen/doxygenConfigFile.txt file is missing. Doxygen documentation would not be generated"
   fi
else
   echo "Documentation Generation flag is set to 0. Doxygen documentation would not be generated."
fi

