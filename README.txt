README.txt

For the Google Apps Shell (GAS) and the Google Apps Shell Interface (GASI).

GAS (gas.py) is a script that allows Google Apps administrators to issue 
commands to their domain from a command line, without having to do any 
heavy API programming.

GASI (gasi.py) is a graphical user interface for GAS.  It allows
administrators to programmatically execute commands from GAS
without having to write a bash script. Some use cases include...
  * Changing every user's signature to a custom signature including their email address.
  * Moving every user from one domain to another, then removing the old user alias.
  * ...and many other interesting combination of Google Apps API commands.

To run GASI on Mac OS X, double click on the gasi.app file in the mac_app folder.

To run GASI on Windows, double click on the gasi.exe file in the windows_app directory.

To run GAS or GASI from any computer with Python installed, you can run the
gasi.py file with Python.  This can be done by navigating to this directory
from a terminal, then execute a command to open gasi.py with Python.
This command is typically "python gasi.py" (provided your environment path or
bash aliases are set up to use the term "python").

For more information, see:
    https://code.google.com/p/google-apps-shell
