README_WINDOWS.txt

GASI is a graphical user interface for GAS.  It allows
administrators to programmatically execute commands from GAS
without having to write a bash script. Some use cases include...
  * Changing every user's signature to a custom signature including their email address.
  * Moving every user from one domain to another, then removing the old user alias.
  * ...and many other interesting combination of Google Apps API commands.

GASI comes with an executable for certain computers. Depending on whether your
computer has the same specs as the computer where the executable was created, it
may work for you. In the future, an installer to build an executable for your
computer is planned.

The Windows executable is found in the windows_app directory. To use it,
double click on the gasi.exe file in the windows_app directory.

If your computer cannot run your GASI executable, you can still use GASI,
by calling it from the command line.  Here's how.

To run GAS or GASI from any computer with Python installed, you can run the
gasi.py file with Python.  This can be done by navigating to this directory
from a terminal, then execute a command to open gasi.py with Python.
This command is typically "python gasi.py" (provided your environment path or
bash aliases are set up to use the term "python").

For more information, see:
    https://code.google.com/p/google-apps-shell
