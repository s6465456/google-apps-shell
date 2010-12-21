README.txt

For the Google Apps Shell (GAS) and the Google Apps Shell Interface (GASI).

GAS (gas.py) is a script that allows Google Apps administrators to issue 
commands to their domain from a command line, without having to do any 
heavy API programming.  It is modelled after the open source project 
Google Apps Manager (GAM).

GASI (gasi.py) is a graphical user interface for GAS and GAM.  It allows
administrators to programmatically execute commands from GAM and GAS
without having to write a bash script. Some use cases include...
  * Changing every user's signature to a custom signature including their email address.
  * Moving every user from one domain to another, then removing the old user alias.
  * Creating resource calendars from a CSV file containing calendar resource information.
  * ...and any other interesting combination of Google Apps API commands.

To run GASI on Mac OS X, double click on the gasi.app file in the mac folder.

To run GASI on Windows, double click on the gasi.exe file in the windows directory.

To run GAS or GASI from any computer with Python installed, you can run the
gasi.py file with Python.  This can be done by navigating to this directory
from a terminal, then execute a command to open gasi.py with Python.
This command is typically "python gasi.py" (provided your environment path or
bash aliases are set up to use the term "python").

For more information, see:
    https://code.google.com/p/google-apps-shell
