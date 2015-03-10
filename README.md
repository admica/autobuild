#Autobuild

Purpose: Autobuild calls the build script then calls python scripts to parse logs,
         build colorful html pages, and send email notifications of build errors.
Platforms: i386, x86_64, ppc, ppc64
Usage: Run autobuild as root in a shell or cron job.
       ( ex. /etc/cron.daily/autobuild )

Version history:
1.5 - 03/10/2015
  * Stripped organization specifics for submission to github.

1.4 - 04/14/2009
  * Added * Added segmentation fault detection.
  * Added new CSS selector, ".segfault-text".
  * For all selectors, changed font size prop:value pairs to either 12px or 14px.

1.3 - 04/09/2009
  * Fixed error detection to properly exclude subversion checkout

1.2 - 01/12/2008
  * implemented reporting for unit test execution
  * added css style tags for tables and javascript events
  * new scripts for manually recreating summary and log html from existing builds

1.1 - 12/16/2008
  * Errors/warnings in the problem section of all build pages are now grouped
  * by makefile
  * Bug fix: ~/.Xauthority ownership was changing to root; now it changes back

1.0 - 12/10/2008
  This initial release performs a number of functions:
  * Maintains a history of a user definable number of builds.
  * Checks out the trunk from subversion and builds the code.
  * Dynamically creates html pages providing:
    - A summary page of current and previous builds with error and warning status.
    - html of each build.log with color highlighting and line numbering.
  * Provides email notification when build errors occur.
  * html pages are created in ${HOME}/${SUBDIR} which is derived from ${ARCH}

