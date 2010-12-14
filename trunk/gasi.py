#!/usr/bin/env python
#
# Google Apps Shell Interface
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Apps Shell Interface is a graphical user interface designed to simplify use of the Google Apps related APIs."""

__author__ = 'jeffpickhardt@google.com (Jeff Pickhardt)'
__version__ = '1.0.0'
__license__ = 'Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)'

import sys
import os
from Tkinter import * # TODO(pickhardt) refactor this to simply "import Tkinter"

SKIP_USERNAME_PROMPT_IN_GAM = True
import gam
SKIP_USERNAME_PROMPT_IN_GAM = False
import gam_commands

import gas
import gas_commands

import shlex
import time
import tkFont
import webbrowser

def PathFromCurrent(relative_path):
  """Returns the operating system absolute path to a given relative path, from the current directory.
  
  Args:
    relative_path: the relative path to append to the current directory.
    
  Returns:
    This function returns the operating system absolute path to a given relative path, from the current directory.
  """
  path = os.path.dirname(os.path.abspath(sys.argv[0]))
  if os.path.abspath('/') != -1:
    divider = '/'
  else:
    divider = '\\'
  return path+divider+relative_path

class MyApp:
  """MyApp is the container class for the entire user interface and application."""
  def __init__(self, parent):
    """Creates the entire user interface for GASI, as well as initially logging the user in."""
    self.error_log = ''
    self.last_error = ''
    
    self.parent = parent
    self.parent.title("Google Apps Shell Interface")
    
    # build header frame
    self.header_frame = Frame(parent)
    self.header_frame.pack()
    self.MakeHeaderFrame(self.header_frame)
    
    # build help frame
    self.help_frame = Frame(parent)
    self.help_frame.pack()
    self.MakeHelpFrame(self.help_frame)
    
    # build credential frame
    self.credential_frame = Frame(parent, pady=40)
    self.credential_frame.pack()
    self.MakeCredentialFrame(self.credential_frame)
    
    # build command line frame
    self.command_frame = Frame(parent)
    self.command_frame.pack()
    self.MakeCommandFrame(self.command_frame)
    
    # build error frame
    self.error_frame = Frame(parent)
    self.error_frame.pack()
    self.MakeErrorFrame(self.error_frame)
    
    # build input/outputs
    self.extra_frame = Frame(parent)
    self.extra_frame.pack()
    self.MakeExtraFrame(self.extra_frame)
    
    # try to auto log in
    try:
      self.AutoLogIn()
    except:
      self.log_in_frame.pack()
  
  def MakeHelpFrame(self, parent_frame):
    """Creates a help frame containing buttons for more information (to documentation and the project website).
    
    Args:
      self: The object.
      parent_frame: This frame is where the helper buttons are placed.
      
    Returns:
      Nothing.
    """
    self.current_help_command = ''
    
    self.help_button = Button(parent_frame, text="Open Documentation")
    self.help_button.pack(side=LEFT)
    self.help_button.bind("<Button-1>", self.PopHelp)
    self.help_button.bind("<Return>", self.PopHelp)
    
    self.website_button = Button(parent_frame, text="Open Website")
    self.website_button.pack(side=LEFT)
    self.website_button.bind("<Button-1>", self.OpenProjectWebsite)
    self.website_button.bind("<Return>", self.OpenProjectWebsite)
    
    self.help_button = Button(parent_frame, text="View Last Error")
    self.help_button.pack(side=LEFT)
    self.help_button.bind("<Button-1>", self.PopErrorLog)
    self.help_button.bind("<Return>", self.PopErrorLog)
    
  
  def OpenProjectWebsite(self, event, url='http://code.google.com/p/google-apps-shell/'):
    """Opens the project website.
    
    Args:
      self: The object.
      event: The event calling this method.
      url: The url of the project website.
    
    Returns:
      Nothing.
    """
    webbrowser.open(url)
    
  def PopHelp(self, event, total_width=600):
    """Pops up a help dialog, allowing the user to get extra help.
    
    Args:
      self: The object.
      event: The event calling this method.
    
    Returns:
      Nothing.
    """
    helper_frame = Toplevel(width=total_width)
    helper_frame.title("Help")
    
    medium_font = tkFont.Font(family="Arial", size=18)    
    label = Label(helper_frame, font=medium_font, text="Help")
    label.pack()
    
    help_menu_list = []
    for gam_entry in gam_commands.commands:
      if gam_entry!='_TEMPLATE':
        if 'category' in gam_commands.commands[gam_entry]:
          command_entry = 'GAM > ' + gam_commands.commands[gam_entry]['category'] + ' > ' + gam_commands.commands[gam_entry]['title']
        else:
          command_entry = 'GAM > ' + gam_commands[gam_entry]['title']
        help_menu_list.append((command_entry,gam_entry))
    
    for gas_entry in gas_commands.commands:
      if gas_entry!='_TEMPLATE':
        if 'category' in gas_commands.commands[gas_entry]:
          command_entry = 'GAS > ' + gas_commands.commands[gas_entry]['category'] + ' > ' + gas_commands.commands[gas_entry]['title']
        else:
          command_entry = 'GAS > ' + gas_commands[gas_entry]['title']
        help_menu_list.append((command_entry,gas_entry))
    
    help_menu_list = sorted(help_menu_list, key=lambda entry: entry[0])
    help_menu = Menubutton(helper_frame,text='Select category...')
    help_menu.menu = Menu(help_menu)
    for entry in help_menu_list:
      help_menu.menu.add_command(label=entry[0], command=self.HelpFunction(entry[1]))
      
    help_menu.pack()
    help_menu['menu'] = help_menu.menu
    
    self.help_description = Label(helper_frame, wraplength=(total_width-50), justify=CENTER, padx=25)
    #self.help_description = Text(helper_frame, relief=FLAT)
    self.help_description.pack()
    
    button = Button(helper_frame, text="Copy to Execute Field", command=self.CopyHelpCommandToExecuteField)
    button.pack()

    button = Button(helper_frame, text="Close Help", command=helper_frame.destroy)
    button.pack()

  def PopErrorLog(self, event, total_width=600):
    """Pops up an error dialog, allowing the user to view the last error encountered.
  
    Args:
      self: The object.
      event: The event calling this method.
  
    Returns:
      Nothing.
    """
    error_frame = Toplevel(width=total_width)
    error_frame.title("Error Log")
    
    medium_font = tkFont.Font(family="Arial", size=18)
    label1 = Label(error_frame, font=medium_font, text="Last Error Details")
    label1.pack()
    
    label2 = Label(error_frame, text="Last error shown below. To view the full error log, open gas_details_log.txt")
    label2.pack()
  
    self.error_log_text_area = Label(error_frame, wraplength=(total_width-50), padx=25)
    self.error_log_text_area.configure(text=self.last_error)
    self.error_log_text_area.pack()
      
    button = Button(error_frame, text="Close Error Log", command=error_frame.destroy)
    button.pack()
  
  
  def CopyHelpCommandToExecuteField(self):
    """Copies the currently showing command from the help window to the execute field in the main window.
    
    Args:
      self: The object.
    
    Returns:
      Nothing.
    """
    currentCommand = str(self.command_field.get())
    textToAdd = self.current_help_command
    if currentCommand:
      textToAdd = '; '+textToAdd
    self.command_field.insert(END, textToAdd)
    self.command_field.focus_force()
  
  def HelpFunction(self, help_with):
    """Pops up a help dialog, allowing the user to get extra help.
    
    Args:
      self: The object.
      help_with: The specific command to print help details about.
    
    Returns:
      A function to get called associated with the specific command in GAM.
    """
    
    try:
      help_object = gam_commands.commands[help_with]
    except:
      try:
        help_object = gas_commands.commands[help_with]
      except:
        raise StandardError('HelpFunction could not find the help entry for the command %s' % help_with)
    
    def HelpForGivenEntry():
      """(This is a function inside a function)
        Sets the help window display elements to the associated documentation for help_with.

      Args:
        None.

      Returns:
        Nothing.
      """
      example_strings = ["  %s\n%s\n\n" % (example[0], example[1]) for example in help_object['examples']]
      full_example_string = "\n".join(example_strings)
      helpful_description_text = """
Usage:
%s

Description:%s

Examples:
%s
""" % (help_object['usage'],help_object['description'],full_example_string)
      self.help_description.configure(text=helpful_description_text)
      self.current_help_command = help_object['usage']
      return True # end the function within a function
    return HelpForGivenEntry
  
  def MakeExtraFrame(self, parent_frame):
    """Makes the frame containing the master template container and the output container."""
    self.left_container = Frame(parent_frame, bd=30)
    self.left_container.pack(side=LEFT)
        
    self.right_container = Frame(parent_frame, bd=30)
    self.right_container.pack(side=LEFT)
    
    ## Master template container ##
    label = Label(self.left_container, text='Master Template: (optional)')
    label.pack()
    
    temp_container = Frame(self.left_container)
    temp_container.pack()
    
    self.input_from = Entry(temp_container, width=30)
    self.input_from.configure(text="~/Desktop/master.txt")
    self.input_from.pack(side=LEFT)
    self.input_from.bind("<Return>", self.LoadInput)
    
    self.reload_button = Button(temp_container, text="Load")
    self.reload_button.pack(side=RIGHT)
    self.reload_button.bind("<Button-1>", self.LoadInput)
    self.reload_button.bind("<Return>", self.LoadInput)
    
    self.input_text = self.MakeTextFrame(self.left_container)
    
    ## Output container ##
    label = Label(self.right_container, text='Output File: (optional)')
    label.pack()
    
    temp_container2 = Frame(self.right_container)
    temp_container2.pack()
    
    self.output_to = Entry(temp_container2, width=30)
    self.output_to.configure(text="~/Desktop/output.txt")
    self.output_to.pack(side=LEFT)
    self.output_to.bind("<Return>", self.ClearOutput)
    
    self.clear_button = Button(temp_container2, text="Clear")
    self.clear_button.pack(side=RIGHT)
    self.clear_button.bind("<Button-1>", self.ClearOutput)
    self.clear_button.bind("<Return>", self.ClearOutput)
    
    self.output_text = self.MakeTextFrame(self.right_container)
      
  def MakeHeaderFrame(self, parent_frame):
    """Makes the frame containing the header."""
    big_font = tkFont.Font(family="Arial", size=24)
    label = Label(parent_frame, font=big_font, text='Google Apps Shell Interface')
    label.pack()
      
  def MakeErrorFrame(self, parent_frame):
    """Makes the frame containing the error label. The error label gets updated when any execution status changes."""
    self.standard_error_label = Label(parent_frame, text='')
    self.standard_error_label.pack()
    
  def MakeTextFrame(self, frame, withScroll=True):
    """Define a new frame and put a text area in it."""
    text_frame=Frame(frame, relief=RIDGE, borderwidth=2)
    
    text=Text(text_frame,height=10,width=50,background='white')
    text.pack(side=LEFT)
    
    # put a scroll bar in the frame
    scroll=Scrollbar(text_frame)
    text.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT,fill=Y)
    scroll.configure(command=text.yview)
    
    #pack everything
    text_frame.pack()
    return text
  
  def MakeCredentialFrame(self, parent_frame):
    """Builds the credential frame, which includes logged in/out info."""
    Label(parent_frame, text='Credentials').pack()
    
    self.log_in_frame = Frame(parent_frame)
    self.log_out_frame = Frame(parent_frame)
    
    username_label = Label(self.log_in_frame, text='Full username: (e.g. admin@domain.com)')
    username_label.pack()
    self.log_in_username = Entry(self.log_in_frame, width=30)
    self.log_in_username.pack()
    self.log_in_username.bind("<Return>", self.LogIn)
    
    password_label = Label(self.log_in_frame, text='Password:')
    password_label.pack()
    self.log_in_password = Entry(self.log_in_frame, width=30, show='*')
    self.log_in_password.pack()
    self.log_in_password.bind("<Return>", self.LogIn)
    
    self.log_in_button = Button(self.log_in_frame, text="Sign In")
    self.log_in_button.bind("<Button-1>", self.LogIn)
    self.log_in_button.bind("<Return>", self.LogIn)
    self.log_in_button.pack()
    
    self.log_out_label = Label(self.log_out_frame, text='Currently signed in to _____.')
    self.log_out_label.pack()
    
    self.log_out_button = Button(self.log_out_frame, text="Sign Out")
    self.log_out_button.bind("<Button-1>", self.LogOut)
    self.log_out_button.bind("<Return>", self.LogOut)
    self.log_out_button.pack()
  
  def MakeCommandFrame(self, parent_frame):
    """Builds the command frame, which contains the execute command field and button."""
    self.command_field = Entry(parent_frame, width=90, justify=CENTER)
    self.command_field.pack(side=LEFT)
    self.command_field.bind("<Return>", self.RunExecute)

    self.execute_button = Button(parent_frame, text="Execute")
    self.execute_button.pack(side=RIGHT)
    self.execute_button.bind("<Button-1>", self.RunExecute)
    self.execute_button.bind("<Return>", self.RunExecute)
  
  def RunExecute(self, event):
    """Executes the command."""
    master_template_lines = self.input_text.get(1.0,END)
    master_template_lines = master_template_lines.split("\n")
    master_template = []
    for line in master_template_lines:
      if line:
        # only take the lines that contain text
        master_template.append(str(line))
    raw_command = self.command_field.get()
    commands = raw_command.split(';')
    self.RunCommands(commands, master_template)
  
  def RunCommands(self, commands, master_template=[]):
    """Executes the command in the command field, or the commands using the master template."""
    if not master_template:
      master_template = ['']
    for template in master_template:
      mapping = template.split(',')
      for temp_command in commands:
        command = temp_command.strip()
        if not command:
          continue
        for index in range(len(mapping)):
          command = command.replace('{%d}' % (index+1), mapping[index].strip()) # Replace {i} with the value from the template.
        # Command now contains the right variables.
        # Execute it.
        command_list = [entry for entry in shlex.split(command)]
        sys.stderr.write('[gasi] Executing: '+command)
        self.last_error = '';
        engine = command_list[0].lower() # either 'gam' or 'gas'
        if engine=='gam':
          sys.argv = [sys.argv[0]]
          sys.argv.extend(command_list[1:])
          try:
            gam.execute() # requires arguments passed as sys.argv
          except StandardError, e:
            sys.stderr.write(e)
        else:
          # assume they are using GAS
          gas.execute(command_list[1:])
        sys.stderr.write('[gasi] Finished executing: '+command)
        
  def LoadInput(self, event):
    """Loads an input to the input text from a file."""
    self.input_text.delete('1.0', END)
    try:
      input_file = open(PathFromCurrent(self.input_from.get()))
      self.input_text.insert('1.0', input_file.read())
      input_file.close()
    except:
      self.input_text.insert('1.0', 'Error reading file.')
  
  def ClearOutput(self, event):
    """Clears the output text."""
    # Commented out: deleting the output file. 
    #output_path = getOutputPath()
    #if os.path.exists(output_path):
    #  os.remove(output_path)
    self.output_text.delete('1.0', END)
  
  def LogOut(self, event):
    """Logs out and deletes the token file, if it exists."""
    # Log out of GAM:
    
    # GAM specific code
    # delete token file
    token_file_path = gam.getTokenPath()
    if os.path.exists(token_file_path):
      os.remove(token_file_path)
    
    # delete auth file
    auth_file_path = gam.getAuthPath()
    if os.path.exists(auth_file_path):
      os.remove(auth_file_path)
    
    gam.domain = ''
    
    # Log out of GAS:
    gas.execute(['logOut'])
    
    # Reset the authentication frames
    self.log_in_frame.pack()
    self.log_out_frame.pack_forget()
  
  def AutoLogIn(self):
    """Logs in to Google Apps based on the credentials given in the apps object, which is assumed to work successfully."""
    gam_apps = gam.getAppsObject()
    # if we get here, then we've successfully logged in to gam
    
    gas.execute(['logIn'])
    # if we get here, then we've successfully logged in to gas
    
    self.log_out_label.configure(text='Currently signed in to '+gam_apps.domain)
    self.log_in_frame.pack_forget()
    self.log_out_frame.pack()
  
  def LogIn(self, event):
    """Logs in with the username and password supplied in the fields."""
    fullUsername = self.log_in_username.get()
    password = self.log_in_password.get()
    try:
      username = fullUsername.split('@')[0]
      domain = fullUsername.split('@')[1]
    except:
      sys.stderr.write('Username must be of form: name@domain.com')
    
    # log in to gam
    gam_apps = gam.getAppsObject(True, username, domain, password)
    # if we get here, then we've successfully logged in to gam
    
    # log in to gas    
    gas.execute(['logIn', 'email=%s' % fullUsername, 'password=%s' % password])
    # if we get here, then we've successfully logged in to gas
    
    self.log_out_label.configure(text='Currently signed in to '+gam_apps.domain)
    self.log_in_password.configure(text='')
    self.log_in_frame.pack_forget()
    self.log_out_frame.pack()
    sys.stderr.write('') # clears the status frame, in case there is anything there
  
  def WriteOutput(self, text):
    """Writes output."""
    try:
      output_file = open(PathFromCurrent(self.output_to.get()), 'a')
      output_file.write(text)
      output_file.close()
    except:
      pass
    self.output_text.insert(END, text)
  
  def WriteError(self, text):
    """Writes error output.""" # TODO
    self.standard_error_label.configure(text=text)

  
root = Tk()
my_app = MyApp(root)

class StdOut:
  """A class holding the write function for writing the output of commands."""
  def __init__(self, app):
    self.app = app
  
  def write(self, text):
    """Writes output."""
    self.app.WriteOutput(text)
    self.app.extra_frame.update_idletasks()

std_out = StdOut(my_app)
sys.stdout = std_out
    
class StdErr:
  """A class holding the write function for writing errors (or really, writing anything, not necessarily errors, that shouldn't be pushed to the output file)."""
  def __init__(self, app):
    self.app = app
    self.app.error_log = ''
    self.app.last_error = ''
  
  def write(self, text):
    """Writes error output."""
    self.app.error_log = self.app.error_log + str(text)
    self.app.last_error = self.app.last_error + str(text)
    
    # add to View Last Error viewer
    try:
        self.app.error_log_text_area.configure(text=self.app.last_error)
    except:
        pass # the error log does not exist
        
    # add to the gas_details_log.txt file
    if text[:6]!='[gasi]':
      # we will not log "Executing:" commands
      try:
        error_file = open(PathFromCurrent('gas_details_log.txt'), 'a')
        error_file.write(text)
        error_file.close()
      except:
        pass
    
    # add to the current error display
    self.app.WriteError(text)
    self.app.error_frame.update_idletasks()

std_err = StdErr(my_app)
sys.stderr = std_err

if __name__ == '__main__':
  root.mainloop()
