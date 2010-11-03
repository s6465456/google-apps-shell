#!/usr/bin/env python
#
# Google Apps Manager
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

"""Google Apps Manager (GAM) is a command line tool which allows Administrators to control their Google Apps domain and accounts.

With GAM you can programatically create users, turn on/off services for users like POP and Forwarding and much more.

For more information, see http://code.google.com/p/google-apps/manager/
"""

__author__ = 'jlee@pbu.edu (Jay Lee)'
__version__ = '1.6.1F1' # F for Forked
__license__ = 'Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)'

import sys, os, time, datetime, random, cgi, socket, urllib, csv, getpass
from sys import exit
import gdata.apps.service
import gdata.apps.emailsettings.service
import gdata.apps.adminsettings.service
import gdata.apps.groups.service
import gdata.apps.audit.service
import gdata.apps.multidomain.service
import gdata.apps.orgs.service
import gdata.apps.res_cal.service
from hashlib import sha1


def showUsage():
  global __version__
  print '''
Usage: gam [OPTIONS]...

Google Apps Manager version '''+__version__+'''.
Retrieve or set Google Apps domain, user, group and nickname settings.
Exhaustive list of commands can be found at: 
http://code.google.com/p/google-apps-manager/wiki/GAMExamples

Examples:
gam info domain
gam create user jsmith firstname John lastname Smith password secretpass
gam update user jsmith suspended on
gam.exe update group announcements add member jsmith
...

'''

def getTokenPath():
  path = os.path.dirname(os.path.abspath(sys.argv[0]))
  if os.path.abspath('/') != -1:
    divider = '/'
  else:
    divider = '\\'
  return path+divider+'token.txt'

def getAuthPath():
  path = os.path.dirname(os.path.abspath(sys.argv[0]))
  if os.path.abspath('/') != -1:
    divider = '/'
  else:
    divider = '\\'
  return path+divider+'auth.txt'

def getAppsObject(skipRawInput=False, newUsername='', newDomain='', newPasswd=''):
  global domain
  #First see if a auth token is stored in token.txt
  path = os.path.dirname(os.path.abspath(sys.argv[0]))
  if os.path.abspath('/') != -1:
    divider = '/'
  else:
    divider = '\\'
  tokenPath = getTokenPath()
  authPath = getAuthPath()
  isValid = False
  if os.path.isfile(tokenPath):
    #See if our token is still valid
    tokenfile = open(tokenPath, 'r')
    domain = tokenfile.readline()[0:-1]
    token = tokenfile.readline()
    tokenfile.close()
    apps = gdata.apps.service.AppsService(domain=domain)
    apps.SetClientLoginToken(token)
    try:
      edition = apps.Get('/a/feeds/domain/2.0/%s/accountInformation/edition' % apps.domain)
      isValid = True
    except gdata.service.RequestError, e:
      if e.message['reason'] == 'Domain cannot use API':
        print 'The Provisioning API is not on for your domain, please see:'
        print '  http://code.google.com/p/google-apps-manager/wiki/GettingStarted'
        raise StandardError('The Provisioning API is not on for your domain. See: http://code.google.com/p/google-apps-manager/wiki/GettingStarted')
    except socket.error, e:
      print "\nERROR: Failed to connect to Google's servers.  Please make sure GAM is not being blocked by Firewall or Antivirus software"
      raise StandardError("\nERROR: Failed to connect to Google's servers.  Please make sure GAM is not being blocked by Firewall or Antivirus software")
  if not isValid:
    if os.path.isfile(authPath):
      authfile = open(authPath, 'r')
      domain = authfile.readline()[0:-1]
      username = authfile.readline()[0:-1]
      passwd = authfile.readline()
    else:
      if skipRawInput:
        domain = newDomain
        username = newUsername
        passwd = newPasswd
      else:
        # will ask the user to input this info
        domain = raw_input('Google Apps Domain: ')
        username = raw_input('Google Apps Admin Username: ')
        passwd = getpass.getpass('Google Apps Admin Password: ')
    email = username+'@'+domain
    apps = gdata.apps.service.AppsService(email=email, domain=domain, password=passwd)
    try:
      apps.ProgrammaticLogin()
      testapps = apps.RetrieveUser(username)
    except gdata.service.BadAuthentication, e:
      print "\nERROR: Invalid username or password.  Please try again."
      raise StandardError("\nERROR: Invalid username or password.  Please try again.")
    except gdata.apps.service.AppsForYourDomainException, e:
      print "\nERROR: Either the user you entered is not a Google Apps Administrator or the Provisioning API is not enabled for your domain. Please see: http://www.google.com/support/a/bin/answer.py?hl=en&answer=60757"
      raise StandardError("\nERROR: Either the user you entered is not a Google Apps Administrator or the Provisioning API is not enabled for your domain. Please see: http://www.google.com/support/a/bin/answer.py?hl=en&answer=60757")
    except socket.error, e:
      print "\nERROR: Failed to connect to Google's servers.  Please make sure GAM is not being blocked by Firewall or Antivirus software"
      raise StandardError("\nERROR: Failed to connect to Google's servers.  Please make sure GAM is not being blocked by Firewall or Antivirus software")
    tokenfile = open(tokenPath, 'w')
    tokenfile.write(domain+"\n")
    tokenfile.write(apps.current_token.get_token_string())
    tokenfile.close()
  return apps

def getEmailSettingsObject():
  global domain
  apps = getAppsObject()
  emailsettings = gdata.apps.emailsettings.service.EmailSettingsService(domain=domain)
  emailsettings.SetClientLoginToken(apps.current_token.get_token_string())
  return emailsettings

def getAdminSettingsObject():
  global domain
  apps = getAppsObject()
  adminsettings = gdata.apps.adminsettings.service.AdminSettingsService(domain=domain)
  adminsettings.SetClientLoginToken(apps.current_token.get_token_string())
  return adminsettings

def getGroupsObject():
  global domain
  apps = getAppsObject()
  groupsObj = gdata.apps.groups.service.GroupsService(domain=domain)
  groupsObj.SetClientLoginToken(apps.current_token.get_token_string())
  return groupsObj

def getAuditObject():
  global domain
  apps = getAppsObject()
  auditObj = gdata.apps.audit.service.AuditService(domain=domain)
  auditObj.SetClientLoginToken(apps.current_token.get_token_string())
  return auditObj

def getMultiDomainObject():
  global domain
  apps = getAppsObject()
  multidomainObj = gdata.apps.multidomain.service.MultiDomainService(domain=domain)
  multidomainObj.SetClientLoginToken(apps.current_token.get_token_string())
  return multidomainObj

def getOrgObject():
  global domain
  apps = getAppsObject()
  orgObj = gdata.apps.orgs.service.OrganizationService(domain=domain)
  orgObj.SetClientLoginToken(apps.current_token.get_token_string())
  return orgObj

def getResCalObject():
  global domain
  apps = getAppsObject()
  resCalObj = gdata.apps.res_cal.service.ResCalService(domain=domain)
  resCalObj.SetClientLoginToken(apps.current_token.get_token_string())
  return resCalObj

def _reporthook(numblocks, blocksize, filesize, url=None):
    #print "reporthook(%s, %s, %s)" % (numblocks, blocksize, filesize)
    base = os.path.basename(url)
    #XXX Should handle possible filesize=-1.
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
    except:
        percent = 100
    if numblocks != 0:
        sys.stdout.write("\b"*70)
    sys.stdout.write(str(percent)+'% ')
    #print str(percent)+"%\b\b"

def geturl(url, dst):
    if sys.stdout.isatty():
        urllib.urlretrieve(url, dst,
                           lambda nb, bs, fs, url=url: _reporthook(nb,bs,fs,url))
        sys.stdout.write('\n')
    else:
        urllib.urlretrieve(url, dst)

def doImap(users):
  global domain
  checkTOS = True
  if sys.argv[4].lower() == 'on':
    enable = True
  elif sys.argv[4].lower() == 'off':
    enable = False
  if len(sys.argv) > 5 and sys.argv[5] == 'noconfirm':
    checkTOS = False
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Setting IMAP Access to %s for %s (%s of %s)" % (str(enable), user, i, count)
    if checkTOS:
      if not hasAgreed2TOS(user):
        print ' Warning: IMAP has been enabled but '+user+' has not logged into GMail to agree to the terms of service (captcha).  IMAP will not work until they do.'
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdateImap(username=user, enable=enable)
    i = i + 1

def doPop(users):
  checkTOS = True
  if sys.argv[4].lower() == 'on':
    enable = True
  elif sys.argv[4].lower() == 'off':
    enable = False
  i = 5
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'for':
      if sys.argv[i+1].lower() == 'allmail':
        enable_for = 'ALL_MAIL'
        i = i + 2
      elif sys.argv[i+1].lower() == 'newmail':
        enable_for = 'MAIL_FROM_NOW_ON'
        i = i + 2
    elif sys.argv[i].lower() == 'action':
      if sys.argv[i+1].lower() == 'keep':
        action = 'KEEP'
        i = i + 2
      elif sys.argv[i+1].lower() == 'archive':
        action = 'ARCHIVE'
        i = i + 2
      elif sys.argv[i+1].lower() == 'delete':
        action = 'DELETE'
        i = i + 2
    elif sys.argv[i].lower() == 'noconfirm':
      checkTOS = False
      i = i + 1
    else:
      showUsage()
      raise StandardError("Incorrect usage.")
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Setting POP Access to %s for %s (%s of %s)" % (str(enable), user, i, count)
    if checkTOS:
      if not hasAgreed2TOS(user):
        print ' Warning: POP has been enabled but '+user+' has not logged into GMail to agree to the terms of service (captcha).  POP will not work until they do.'
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdatePop(username=user, enable=enable, enable_for=enable_for, action=action)
    i = i + 1

def doSendAs(users):
  sendas = sys.argv[4]
  sendasName = sys.argv[5]
  make_default = reply_to = None
  i = 6
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'default':
      make_default = True
      i = i + 1
    elif sys.argv[i].lower() == 'replyto':
      reply_to = sys.argv[i+1]
      i = i + 2
    else:
      showUsage()
      raise StandardError("Incorrect usage.")
  emailsettings = getEmailSettingsObject()
  if sendas.find('@') < 0:
    sendas = sendas+'@'+domain
  count = len(users)
  i = 1
  for user in users:
    print "Allowing %s to send as %s (%s of %s)" % (user, sendas, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.CreateSendAsAlias(username=user, name=sendasName, address=sendas, make_default=make_default, reply_to=reply_to)
    i = i + 1

def doLanguage(users):
  language = sys.argv[4].lower()
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Setting the language for %s to %s (%s of %s)" % (user, language, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdateLanguage(username=user, language=language)
    i = i + 1

def doUTF(users):
  if sys.argv[4].lower() == 'on':
    SetUTF = True
  elif sys.argv[4].lower() == 'off':
    SetUTF = False
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Setting UTF-8 to %s for %s (%s of %s)" % (str(SetUTF), user, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdateGeneral(username=user, unicode=SetUTF)
    i = i + 1

def doPageSize(users):
  if sys.argv[4] == '25':
    PageSize = '25'
  elif sys.argv[4] == '50':
    PageSize = '50'
  elif sys.argv[4] == '100':
    PageSize = '100'
  else:
    showUsage()
    raise StandardError("Incorrect usage.")
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Setting Page Size to %s for %s (%s of %s)" % (PageSize, user, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdateGeneral(username=user, page_size=PageSize)
    i = i + 1

def doShortCuts(users):
  if sys.argv[4].lower() == 'on':
    SetShortCuts = True
  elif sys.argv[4].lower() == 'off':
    SetShortCuts = False
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Setting Keyboard Short Cuts to %s for %s (%s of %s)" % (str(SetShortCuts), user, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdateGeneral(username=user, shortcuts=SetShortCuts)
    i = i + 1

def doArrows(users):
  if sys.argv[4].lower() == 'on':
    SetArrows = True
  elif sys.argv[4].lower() == 'off':
    SetArrows = False
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Setting Personal Indicator Arrows to %s for %s (%s of %s)" % (str(SetArrows), user, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdateGeneral(username=user, arrows=SetArrows)
    i = i + 1

def doSnippets(users):
  if sys.argv[4].lower() == 'on':
    SetSnippets = True
  elif sys.argv[4].lower() == 'off':
    SetSnippets = False
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Setting Preview Snippets to %s for %s (%s of %s)" % (str(SetSnippets), user, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdateGeneral(username=user, snippets=SetSnippets)
    i = i + 1

def doLabel(users):
  label = sys.argv[4]
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Creating label %s for %s (%s of %s)" % (label, user, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.CreateLabel(username=user, label=label)
    i = i + 1

def doFilter(users):
  i = 4 # filter arguments start here
  from_ = to = subject = has_the_word = does_not_have_the_word = has_attachment = label = should_mark_as_read = should_archive = None
  haveCondition = False
  while sys.argv[i].lower() == 'from' or sys.argv[i].lower() == 'to' or sys.argv[i].lower() == 'subject' or sys.argv[i].lower() == 'haswords' or sys.argv[i].lower() == 'nowords' or sys.argv[i].lower() == 'musthaveattachment':
    if sys.argv[i].lower() == 'from':
      from_ = sys.argv[i+1]
      i = i + 2
      haveCondition = True
    elif sys.argv[i].lower() == 'to':
      to = sys.argv[i+1]
      i = i + 2
      haveCondition = True
    elif sys.argv[i].lower() == 'subject':
      subject = sys.argv[i+1]
      i = i + 2
      haveCondition = True
    elif sys.argv[i].lower() == 'haswords':
      has_the_word = sys.argv[i+1]
      i = i + 2
      haveCondition = True
    elif sys.argv[i].lower() == 'nowords':
      does_not_have_the_word = sys.argv[i+1]
      i = i + 2
      haveCondition = True
    elif sys.argv[i].lower() == 'musthaveattachment':
      has_attachment = True
      i = i + 1
      haveCondition = True
  if not haveCondition:
    showUsage()
    raise StandardError("Incorrect usage.")
  haveAction = False
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'label':
      label = sys.argv[i+1]
      i = i + 2
      haveAction = True
    elif sys.argv[i].lower() == 'markread':
      should_mark_as_read = True
      i = i + 1
      haveAction = True
    elif sys.argv[i].lower() == 'archive':
      should_archive = True
      i = i + 1
      haveAction = True
    else:
      showUsage()
      raise StandardError("Incorrect usage.")
  if not haveAction:
    showUsage()
    raise StandardError("Incorrect usage.")
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Creating filter for %s (%s of %s)" % (user, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.CreateFilter(username=user, from_=from_, to=to, subject=subject, has_the_word=has_the_word, does_not_have_the_word=does_not_have_the_word, has_attachment=has_attachment, label=label, should_mark_as_read=should_mark_as_read, should_archive=should_archive)
    i = i + 1

def doForward(users):
  checkTOS = True
  action = forward_to = None
  gotAction = gotForward = False
  if sys.argv[4] == 'on':
    enable = True
  elif sys.argv[4] == 'off':
    enable = False
  else:
    showUsage()
    raise StandardError("Incorrect usage.")
  i = 5
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'keep' or sys.argv[i].lower() == 'archive' or sys.argv[i].lower() == 'delete':
      action = sys.argv[i].upper()
      i = i + 1
      gotAction = True
    elif sys.argv[i].lower() == 'noconfirm':
      checkTOS = False
      i = i + 1
    elif sys.argv[i].find('@') != -1:
      forward_to = sys.argv[i]
      gotForward = True
      i = i + 1
    else:
      showUsage()
      raise StandardError("Incorrect usage.")
  if enable and (not gotAction or not gotForward):
    showUsage()
    raise StandardError("Incorrect usage.")
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Turning forward %s for %s, emails will be %s (%s of %s)" % (sys.argv[4], user, action, i, count)
    if checkTOS:
      if not hasAgreed2TOS(user):
        print ' Warning: Forwarding has been enabled but '+user+' has not logged into GMail to agree to the terms of service (captcha).  Forwarding will not work until they do.'
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdateForwarding(username=user, enable=enable, action=action, forward_to=forward_to)
    i = i + 1

def doSignature(users):
  signature = cgi.escape(sys.argv[4]).replace('\\n', '&#xA;')
  xmlsig = '''<?xml version="1.0" encoding="utf-8"?>
<atom:entry xmlns:atom="http://www.w3.org/2005/Atom" xmlns:apps="http://schemas.google.com/apps/2006">
    <apps:property name="signature" value="'''+signature+'''" />
</atom:entry>'''
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Setting Signature for %s (%s of %s)" % (user, i, count)
    #emailsettings.UpdateSignature(username=user, signature=signature)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    uri = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/'+emailsettings.domain+'/'+user+'/signature'
    emailsettings.Put(xmlsig, uri)
    i = i + 1

def doWebClips(users):
  if sys.argv[4].lower() == 'on':
    enable = True
  elif sys.argv[4].lower() == 'off':
    enable = False
  else:
    showUsage()
    raise StandardError("Incorrect usage.")
  emailsettings = getEmailSettingsObject()
  count = len(users)
  i = 1
  for user in users:
    print "Turning Web Clips %s for %s (%s of %s)" % (sys.argv[4], user, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    emailsettings.UpdateWebClipSettings(username=user, enable=enable)
    i = i + 1

def doVacation(users):
  subject = message = ''
  contacts_only = 'false'
  if sys.argv[4] == 'on':
    enable = 'true'
  elif sys.argv[4] == 'off':
    enable = 'false'
  else:
    showUsage()
    raise StandardError("Incorrect usage.")
  i = 5
  while i < len(sys.argv):
    if sys.argv[i] == 'subject':
      subject = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i] == 'message':
      message = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i] == 'contactsonly':
      contacts_only = 'true'
      i = i + 1
    else:
      showUsage()
      raise StandardError("Incorrect usage.")
  i = 1
  count = len(users)
  emailsettings = getEmailSettingsObject()
  message = cgi.escape(message).replace('\\n', '&#xA;')
  vacxml = '''<?xml version="1.0" encoding="utf-8"?>
<atom:entry xmlns:atom="http://www.w3.org/2005/Atom" xmlns:apps="http://schemas.google.com/apps/2006">
    <apps:property name="enable" value="'''+enable+'''" />
    <apps:property name="subject" value="'''+subject+'''" />
    <apps:property name="message" value="'''+message+'''" />
    <apps:property name="contactsOnly" value="'''+contacts_only+'''" />
</atom:entry>'''
  for user in users:
    print "Setting Vacation for %s (%s of %s)" % (user, i, count)
    if user.find('@') > 0:
      emailsettings.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    else:
      emailsettings.domain = domain #make sure it's back at default domain
    uri = 'https://apps-apis.google.com/a/feeds/emailsettings/2.0/'+emailsettings.domain+'/'+user+'/vacation'
    emailsettings.Put(vacxml, uri)
    #emailsettings.UpdateVacation(username=user, enable=enable, subject=subject, message=message, contacts_only=contacts_only)
    i = i + 1

def doCreateUser():
  gotFirstName = gotLastName = gotPassword = False
  suspended = 'false'
  password_hash_function = quota_limit = change_password = None
  user_name = sys.argv[3].lower()
  i = 4
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'firstname':
      given_name = sys.argv[i+1]
      gotFirstName = True
      i = i + 2
    elif sys.argv[i].lower() == 'lastname':
      family_name = sys.argv[i+1]
      gotLastName = True
      i = i + 2
    elif sys.argv[i].lower() == 'password':
      password = sys.argv[i+1]
      gotPassword = True
      i = i + 2
    elif sys.argv[i].lower() == 'suspended':
      suspended='true'
      i = i + 1
    elif sys.argv[i].lower() == 'sha' or sys.argv[i].lower() == 'sha1' or sys.argv[i].lower() == 'sha-1':
      password_hash_function = 'SHA-1'
      i = i + 1
    elif sys.argv[i].lower() == 'md5':
      password_hash_function = 'MD5'
      i = i + 1
    elif sys.argv[i].lower() == 'quota':
	  quota_limit = sys.argv[i+1]
	  i = i + 2
    elif sys.argv[i].lower() == 'changepassword':
      change_password = 'true'
      i = i + 1
    else:
      showUsage()
      raise StandardError("Incorrect usage.")
  if not (gotFirstName and gotLastName and gotPassword):
    showUsage()
    raise StandardError("Incorrect usage.")
  if password_hash_function == None:
    newhash = sha1()
    newhash.update(password)
    password = newhash.hexdigest()
    password_hash_function = 'SHA-1'
  print "Creating account for %s" % user_name
  apps = getAppsObject()
  if user_name.find('@') > 0:
    apps.domain = user_name[user_name.find('@')+1:]
    user_name = user_name[:user_name.find('@')]
  apps.CreateUser(user_name=user_name, family_name=family_name, given_name=given_name, password=password, suspended=suspended, quota_limit=quota_limit, password_hash_function=password_hash_function, change_password=change_password)

def doCreateGroup():
  group = sys.argv[3]
  got_name = got_description = got_permission = False
  i = 4
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'name':
      group_name = sys.argv[i+1]
      got_name = True
      i = i + 2
    elif sys.argv[i].lower() == 'description':
      group_description = sys.argv[i+1]
      got_description = True
      i = i + 2
    elif sys.argv[i].lower() == 'permission':
      group_permission = sys.argv[i+1]
      if group_permission.lower() == 'owner':
        group_permission = 'Owner'
      elif group_permission.lower() == 'member':
        group_permission = 'Member'
      elif group_permission.lower() == 'domain':
        group_permission = 'Domain'
      elif group_permission.lower() == 'anyone':
        group_permission = 'Anyone'
      else:
        showUsage()
        raise StandardError("Incorrect usage.")
      got_permission = True
      i = i + 2
  if not got_name or not got_description or not got_permission:
    showUsage()
    raise StandardError("Incorrect usage.")
  groupObj = getGroupsObject()
  result = groupObj.CreateGroup(group, group_name, group_description, group_permission)

def doCreateNickName():
  nickname = sys.argv[3]
  if sys.argv[4].lower() != 'user':
    showUsage()
    raise StandardError("Incorrect usage.")
  username = sys.argv[5]
  apps = getAppsObject()
  apps.CreateNickname(username, nickname)

def doCreateOrg():
  name = sys.argv[3]
  description = ''
  parent_org_unit_path = '/'
  block_inheritance = False
  i = 4
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'description':
      description = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'parent':
      parent_org_unit_path = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'noinherit':
      block_inheritance = True
      i = i + 1
  org = getOrgObject()
  org.CreateOrganizationUnit(name=name, description=description, parent_org_unit_path=parent_org_unit_path, block_inheritance=block_inheritance)

def doCreateResource():
  id = sys.argv[3]
  common_name = sys.argv[4]
  description = None
  type = None
  i = 5
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'description':
      description = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'type':
      type = sys.argv[i+1]
      i = i + 2
  rescal = getResCalObject()
  rescal.CreateResourceCalendar(id=id, common_name=common_name, description=description, type=type)

def doUpdateUser():
  gotPassword = isMD5 = isSHA1 = False
  user_name = sys.argv[3]
  i = 4
  apps = getAppsObject()
  if user_name.find('@') > 0:
    apps.domain = user_name[user_name.find('@')+1:]
    user_name = user_name[:user_name.find('@')]
  try:
    user = apps.RetrieveUser(user_name)
  except gdata.apps.service.AppsForYourDomainException, e:
    if e.reason == 'EntityDoesNotExist':
      print "ERROR: "+user_name+" is not an existing user."
      raise StandardError("ERROR: "+user_name+" is not an existing user.")
    else:
      print 'ERROR: '+e.reason+' Status Code: '+e.status
      raise StandardError('ERROR: '+e.reason+' Status Code: '+e.status)
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'firstname':
      user.name.given_name = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'lastname':
      user.name.family_name = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'username':
      user.login.user_name = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'password':
      user.login.password = sys.argv[i+1]
      i = i + 2
      gotPassword = True
    elif sys.argv[i].lower() == 'admin':
      if sys.argv[i+1].lower() == 'on':
        user.login.admin = 'true'
      elif sys.argv[i+1].lower() == 'off':
        user.login.admin = 'false'
      i = i + 2
    elif sys.argv[i].lower() == 'suspended':
      if sys.argv[i+1].lower() == 'on':
        user.login.suspended = 'true'
      elif sys.argv[i+1].lower() == 'off':
        user.login.suspended = 'false'
      i = i + 2
    elif sys.argv[i].lower() == 'ipwhitelisted':
      if sys.argv[i+1].lower() == 'on':
        user.login.ip_whitelisted = 'true'
      elif sys.argv[i+1].lower() == 'off':
        user.login.ip_whitelisted = 'false'
      i = i + 2
    elif sys.argv[i].lower() == 'sha1' or sys.argv[i].lower() == 'sha1' or sys.argv[i].lower() == 'sha-1':
      user.login.hash_function_name = 'SHA-1'
      i = i + 1
      isSHA1 = True
    elif sys.argv[i].lower() == 'md5':
      user.login.hash_function_name = 'MD5'
      i = i + 1
      isMD5 = True
    elif sys.argv[i].lower() == 'changepassword':
      if sys.argv[i+1].lower() == 'on':
        user.login.change_password = 'true'
      elif sys.argv[i+1].lower() == 'off':
        user.login.change_password = 'false'
      i = i + 2
  if gotPassword and not (isSHA1 or isMD5):
    newhash = sha1()
    newhash.update(user.login.password)
    user.login.password = newhash.hexdigest()
    user.login.hash_function_name = 'SHA-1'
  try:
    apps.UpdateUser(user_name, user)
  except gdata.apps.service.AppsForYourDomainException, e:
    print e
    if e.reason == 'EntityExists':
      print "ERROR: "+user.login.user_name+" is an existing user, group or nickname. Please delete the existing entity with this name before renaming "+user_name
    elif e.reason == 'UserDeletedRecently':
      print "ERROR: "+user.login.user_name+" was a user account recently deleted. You'll need to wait 5 days before you can reuse this name."
    else:
      print "ERROR: "+e.reason
    raise StandardError("ERROR: "+e.reason)

def doUpdateGroup():
  groupObj = getGroupsObject()
  group = sys.argv[3]
  if sys.argv[4].lower() == 'add':
    if sys.argv[5].lower() == 'owner':
      userType = 'Owner'
    elif sys.argv[5].lower() == 'member':
      userType = 'Member'
    user = sys.argv[6]
    if user.find('@') == -1:
      email = user+'@'+domain
    else:
      email = user
    if userType == 'Member':
      result = groupObj.AddMemberToGroup(email, group)
      result2 = groupObj.RemoveOwnerFromGroup(email, group)
    elif userType == 'Owner':
      result = groupObj.AddMemberToGroup(email, group)
      result2 = groupObj.AddOwnerToGroup(email, group)
  elif sys.argv[4].lower() == 'remove':
    user = sys.argv[5]
    if user.find('@') == -1:
      email = user+'@'+domain
    else:
      email = user
    result = groupObj.RemoveMemberFromGroup(email, group)
  else:
    groupInfo = groupObj.RetrieveGroup(group)
    i = 4
    while i < len(sys.argv):
      if sys.argv[i].lower() == 'name':
        groupInfo['groupName'] = sys.argv[i+1]
        i = i + 2        
      elif sys.argv[i].lower() == 'description':
        groupInfo['description'] = sys.argv[i+1]
        i = i + 2
      elif sys.argv[i].lower() == 'permission':
        if sys.argv[i+1].lower() == 'owner':
          groupInfo['emailPermission'] = 'Owner'
        elif sys.argv[i+1].lower() == 'member':
          groupInfo['emailPermission'] = 'Member'
        elif sys.argv[i+1].lower() == 'domain':
          groupInfo['emailPermission'] = 'Domain'
        elif sys.argv[i+1].lower() == 'anyone':
          groupInfo['emailPermission'] = 'Anyone'
        i = i + 2
    result = groupObj.UpdateGroup(group, groupInfo['groupName'], groupInfo['description'], groupInfo['emailPermission'])

def doUpdateNickName():
  nickname = sys.argv[3]
  if sys.argv[4].lower() != 'user':
    showUsage()
    raise StandardError("Incorrect usage.")
  username = sys.argv[5]
  apps = getAppsObject()
  apps.DeleteNickname(nickname)
  apps.CreateNickname(username, nickname)

def doUpdateResourceCalendar():
  id = sys.argv[3]
  common_name = None
  description = None
  type = None
  i = 4
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'name':
      common_name = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'description':
      description = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'type':
      type = sys.argv[i+1]
      i = i + 2
  rescal = getResCalObject()
  rescal.UpdateResourceCalendar(id=id, common_name=common_name, description=description, type=type)

def doUpdateOrg():
  name = sys.argv[3]
  new_name = None
  description = None
  parent_org_unit_path = None
  block_inheritance = None
  users_to_move = []
  org = getOrgObject()
  users = []
  apps = getAppsObject()
  i = 4
  if sys.argv[4].lower() == 'add':
    users = sys.argv[5].split(' ')
    i = 6
  elif sys.argv[4].lower() == 'fileadd' or sys.argv[4].lower() == 'addfile':
    users = []
    filename = sys.argv[5]
    usernames = csv.reader(open(filename, 'r'))
    for row in usernames:
      users.append(row.pop())
    i = 6
  elif sys.argv[4].lower() == 'groupadd'or sys.argv[4].lower() == 'addgroup':
    groupsObj = getGroupsObject()
    group = sys.argv[5]
    members = groupsObj.RetrieveAllMembers(group)
    for member in members:
      users.append(member['memberId'])
    i = 6
  elif sys.argv[4].lower() == 'addnotingroup':
    print 'Retrieving all users in Google Apps Organization (may take some time)'
    allorgusersresults = org.RetrieveAllOrganizationUsers()
    print 'Retrieved %s users' % len(allorgusersresults)
    for auser in allorgusersresults:
      users.append(auser['orgUserEmail'])
    group = sys.argv[5]
    print 'Retrieving all members of %s group (may take some time)' % group
    groupsObj = getGroupsObject()
    members = groupsObj.RetrieveAllMembers(group)
    for member in members:
      try:
        users.remove(member['memberId'])
      except ValueError:
        continue
    i = 6
  totalusers = len(users)
  if totalusers > 50:
    print "got %s users to be added" % totalusers
    alreadyInOU = org.RetrieveAllOrganizationUnitUsers(name)
    alreadyCount = 0
    for user in alreadyInOU:
      try:
        users.remove(user['orgUserEmail'])
        alreadyCount = alreadyCount + 1
      except ValueError:
        continue
    if alreadyCount > 0:
      print "%s users were already in org %s and won't be re-added" % (alreadyCount, name)
      totalusers = len(users)
  currentrange = 1
  while len(users) > 20:
    reason = invalidInput = None
    while len(users_to_move) <= 20:
      users_to_move.append(users.pop())
    print "Adding users %s to %s out of %s total to org %s" % (currentrange, currentrange+19, totalusers, name)
    try:
      org.UpdateOrganizationUnit(old_name=name, users_to_move=users_to_move)
      currentrange = currentrange + 20
      users_to_move = []
      continue
    except gdata.apps.service.AppsForYourDomainException, e:
      reason = e.reason
      invalidInput = e.invalidInput
      if reason == 'EntityDoesNotExist' and invalidInput == 'orgUnitUsersToMove':
        #find out which user is not in the domain
        remove_users = []
        for user in users_to_move:
          try:
            if user.find('@') != -1:
              apps.domain = user[user.find('@')+1:]
              username = user[0:user.find('@')]
            else:
              apps.domain = domain
              username = user
            apps.RetrieveUser(username)
          except gdata.apps.service.AppsForYourDomainException, e:
            if e.message['reason'][:59] == 'You are not authorized to perform operations on the domain ' or e.message['reason'] == 'Invalid domain.':
              remove_users.append(user)
              print 'not adding external user '+user
            elif e.reason == 'EntityDoesNotExist':
              remove_users.append(user)
              print 'not adding non-existant user '+user
        for user in remove_users:
          users_to_move.remove(user)
        if len(users_to_move) > 0:
          org.UpdateOrganizationUnit(old_name=name, users_to_move=users_to_move)
        currentrange = currentrange + 20
        users_to_move = []
  while len(users) > 0:
    users_to_move.append(users.pop())
  if len(users_to_move) < 1:
    users_to_move = None
  else:
    print 'Adding users %s to %s and making other updates to org %s' % (currentrange, totalusers, name)
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'name':
      new_name = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'description':
      description = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'parent':
      parent_org_unit_path = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'noinherit':
      block_inheritance = True
      i = i + 1
    elif sys.argv[i].lower() == 'inherit':
      block_inheritance = False
      i = i + 1
  try:
    reason = invalidInput = None
    org.UpdateOrganizationUnit(old_name=name, new_name=new_name, description=description, parent_org_unit_path=parent_org_unit_path, block_inheritance=block_inheritance, users_to_move=users_to_move)
    exit(0)
  except gdata.apps.service.AppsForYourDomainException, e:
    reason = e.reason
    invalidInput = e.invalidInput
  if reason == 'EntityDoesNotExist' and invalidInput == 'orgUnitUsersToMove':
    #find out which users aren't local or are invalid
    remove_users = []
    for user in users_to_move:
      if user.find('@') != -1:
        apps.domain = user[user.find('@')+1:]
        username = user[0:user.find('@')]
      else:
        apps.domain = domain
        username = user
      try:
        apps.RetrieveUser(username)
      except gdata.apps.service.AppsForYourDomainException, e:
        if e.message['reason'][:59] == 'You are not authorized to perform operations on the domain ' or e.message['reason'] == 'Invalid domain.':
          remove_users.append(user)
          print 'not adding external user '+user
        elif e.reason == 'EntityDoesNotExist':
          remove_users.append(user)
          print 'not adding non-existant user '+user
    for user in remove_users:
      users_to_move.remove(user)
    if len(users_to_move) < 1:
      users_to_move = None
    org.UpdateOrganizationUnit(old_name=name, new_name=new_name, description=description, parent_org_unit_path=parent_org_unit_path, block_inheritance=block_inheritance, users_to_move=users_to_move)
      

def doGetUserInfo():
  user_name = sys.argv[3]
  apps = getAppsObject()
  if user_name.find('@') > 0:
    apps.domain = user_name[user_name.find('@')+1:]
    user_name = user_name[:user_name.find('@')]
  user = apps.RetrieveUser(user_name)
  print 'User: %s' % user.login.user_name
  print 'First Name: %s' % user.name.given_name
  print 'Last Name: %s' % user.name.family_name
  print 'Is an admin: %s' % user.login.admin
  print 'Has agreed to terms: %s' % user.login.agreed_to_terms
  print 'IP Whitelisted: %s' % user.login.ip_whitelisted
  print 'Account Suspended: %s' % user.login.suspended
  print 'Must Change Password: %s' % user.login.change_password
  nicknames = apps.RetrieveNicknames(user_name)
  print 'Nicknames:'
  for nick in nicknames.entry:
    print '  ' + nick.nickname.name
  groupObj = getGroupsObject()
  groupObj.domain = apps.domain
  groups = groupObj.RetrieveGroups(user_name)
  print 'Groups:'
  for group in groups:
    if group['directMember'] == 'true':
      directIndirect = 'direct'
    else:
      directIndirect = 'indirect'
    print '  ' + group['groupName'] + ' <' + group['groupId'] + '> (' + directIndirect + ' member)'

def doGetGroupInfo():
  group_name = sys.argv[3]
  groupObj = getGroupsObject()
  group = groupObj.RetrieveGroup(group_name)
  print 'Group Name: ',group['groupName']
  print 'Email Permission: ',group['emailPermission']
  print 'Group ID: ',group['groupId']
  print 'Description: ',group['description']
  members = groupObj.RetrieveAllMembers(group_name)
  users = []
  for member in members:
    users.append(member['memberId'])
  for user in users:
    if groupObj.IsOwner(user, group_name):
      print 'Owner:',user
    else:
      print 'Member:',user

def doGetNickNameInfo():
  nickname = sys.argv[3]
  apps = getAppsObject()
  result = apps.RetrieveNickname(nickname)
  print 'Nickname: '+nickname
  print 'User: '+result.login.user_name

def doGetResourceCalendarInfo():
  id = sys.argv[3]
  rescal = getResCalObject()
  result = rescal.RetrieveResourceCalendar(id)
  print ' Resource ID: '+result['resourceId']
  print ' Common Name: '+result['resourceCommonName']
  print ' Email: '+result['resourceEmail']
  try:
    print ' Type: '+result['resourceType']
  except KeyError:
    print ' Type: '

def doGetOrgInfo():
  name = sys.argv[3]
  org = getOrgObject()
  result = org.RetrieveOrganizationUnit(name)
  print 'Organization Unit: '+result['name']
  if result['description'] != None:
    print 'Description: '+result['description']
  else:
    print 'Description: '
  if result['parentOrgUnitPath'] != None:
    print 'Parent Org: '+result['parentOrgUnitPath']
  else:
    print 'Parent Org: /'
  print 'Block Inheritance: '+result['blockInheritance']
  result2 = org.RetrieveAllOrganizationUnitUsers(name)
  print 'Users: '
  for user in result2:
    print ' '+user['orgUserEmail']

def doGetDomainInfo():
  adminObj = getAdminSettingsObject()
  #pause 1 sec inbetween calls to prevent quota warning
  print 'Google Apps Domain: ', adminObj.domain
  time.sleep(0.6)
  print 'Default Language: ', adminObj.GetDefaultLanguage()
  time.sleep(0.6)
  print 'Organization Name: ', adminObj.GetOrganizationName()
  time.sleep(0.6)
  print 'Maximum Users: ', adminObj.GetMaximumNumberOfUsers()
  time.sleep(0.6)
  print 'Current Users: ', adminObj.GetCurrentNumberOfUsers()
  time.sleep(0.6)
  print 'Domain is Verified: ',adminObj.IsDomainVerified()
  time.sleep(0.6)
  print 'Support PIN: ',adminObj.GetSupportPIN()
  time.sleep(0.6)
  print 'Domain Edition: ', adminObj.GetEdition()
  time.sleep(0.6)
  print 'Customer PIN: ', adminObj.GetCustomerPIN()
  time.sleep(0.6)
  print 'Domain Creation Time: ', adminObj.GetCreationTime()
  time.sleep(0.6)
  print 'Domain Country Code: ', adminObj.GetCountryCode()
  time.sleep(0.6)
  print 'Admin Secondary Email: ', adminObj.GetAdminSecondaryEmail()
  time.sleep(0.6)
  cnameverificationstatus = adminObj.GetCNAMEVerificationStatus()
  print 'CNAME Verification Record Name: ', cnameverificationstatus['recordName']
  print 'CNAME Verification Verified: ', cnameverificationstatus['verified']
  print 'CNAME Verification Method: ', cnameverificationstatus['verificationMethod']
  time.sleep(0.6)
  mxverificationstatus = adminObj.GetMXVerificationStatus()
  print 'MX Verification Verified: ', mxverificationstatus['verified']
  print 'MX Verification Method: ', mxverificationstatus['verificationMethod']
  time.sleep(0.6)
  ssosettings = adminObj.GetSSOSettings()
  print 'SSO Enabled: ', ssosettings['enableSSO']
  print 'SSO Signon Page: ', ssosettings['samlSignonUri']
  print 'SSO Logout Page: ', ssosettings['samlLogoutUri']
  print 'SSO Password Page: ', ssosettings['changePasswordUri']
  print 'SSO Whitelist IPs: ', ssosettings['ssoWhitelist']
  print 'SSO Use Domain Specific Issuer: ', ssosettings['useDomainSpecificIssuer']
  time.sleep(0.6)
  if ssosettings['enableSSO'].lower() == 'true':
    ssokey = adminObj.GetSSOKey()
    try:
      algorithm = str(ssokey['algorithm'])
      print 'SSO Key Algorithm: ' + algorithm
    except KeyError:
      pass
    try:
      format = str(ssokey['format'])
      print 'SSO Key Format: ' + format
    except KeyError:
      pass
    try:
      modulus = str(ssokey['modulus'])
      print 'SSO Key Modulus: ' + modulus
    except KeyError:
      pass
    try:
      exponent = str(ssokey['exponent'])
      print 'SSO Key Exponent: ' + exponent
    except KeyError:
      pass
    try:
      yValue = str(ssokey['yValue'])
      print 'SSO Key yValue: ' + yValue
    except KeyError:
      pass
    try:
      signingKey = str(ssokey['signingKey'])
      print 'Full SSO Key: ' + signingKey
    except KeyError:
      pass

def doDeleteUser():
  user_name = sys.argv[3]
  apps = getAppsObject()
  if user_name.find('@') > 0:
    apps.domain = user_name[user_name.find('@')+1:]
    user_name = user_name[:user_name.find('@')]
  print "Deleting account for %s" % user_name
  #Rename the user to a random string, this allows the user to be recreated
  #immediately instead of waiting the usual 5 days
  timestamp = time.strftime("%Y%m%d%H%M%S")
  renameduser = user_name+'-'+timestamp+'-'
  randomstring = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 25))
  renameduser = renameduser+randomstring
  user = apps.RetrieveUser(user_name)
  user.login.user_name = renameduser
  apps.UpdateUser(user_name, user)
  apps.DeleteUser(renameduser)

def doDeleteGroup():
  group = sys.argv[3]
  groupObj = getGroupsObject()
  print "Deleting group %s" % group
  groupObj.DeleteGroup(group)

def doDeleteNickName():
  nickname = sys.argv[3]
  apps = getAppsObject()
  print "Deleting nickname %s" % nickname
  apps.DeleteNickname(nickname)

def doDeleteResourceCalendar():
  name = sys.argv[3]
  rescal = getResCalObject()
  rescal.DeleteResourceCalendar(name)

def doDeleteOrg():
  name = sys.argv[3]
  org = getOrgObject()
  try:
    org.DeleteOrganizationUnit(name)
  except gdata.apps.service.AppsForYourDomainException, e:
    if e.reason == 'EntityHasMembersCannotDelete':
      print 'Not Deleted. You must remove all users from an organization unit before deleting it.'
    elif e.reason == 'EntityDoesNotExist':
      print 'That Organization Unit does not exist.'
    else:
      print e.reason

def doPrintUsers():
  org = getOrgObject()
  sys.stderr.write("Getting all users in the organization (may take some time on a large Google Apps account)...\r\n")
  i = 3
  getUserFeed = getNickFeed = getGroupFeed = False
  firstname = lastname = username = ou = suspended = changepassword = agreed2terms = admin = nicknames = groups = False
  user_attributes = []
  user_attributes.append({'Email': 'Email'})
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'firstname':
      getUserFeed = True
      firstname = True
      user_attributes[0].update(Firstname='Firstname')
      i = i + 1
    elif sys.argv[i].lower() == 'lastname':
      getUserFeed = True
      lastname = True
      user_attributes[0].update(Lastname='Lastname')
      i = i + 1
    elif sys.argv[i].lower() == 'username':
      username = True
      user_attributes[0].update(Username='Username')
      i = i + 1
    elif sys.argv[i].lower() == 'ou':
      ou = True
      user_attributes[0].update(OU='OU')
      i = i + 1
    elif sys.argv[i].lower() == 'suspended':
      getUserFeed = True
      suspended = True
      user_attributes[0].update(Suspended='Suspended')
      i = i + 1
    elif sys.argv[i].lower() == 'changepassword':
      getUserFeed = True
      changepassword = True
      user_attributes[0].update(ChangePassword='ChangePassword')
      i = i + 1
    elif sys.argv[i].lower() == 'agreed2terms':
      getUserFeed = True
      agreed2terms = True
      user_attributes[0].update(AgreedToTerms='AgreedToTerms')
      i = i + 1
    elif sys.argv[i].lower() == 'admin':
      getUserFeed = True
      admin = True
      user_attributes[0].update(Admin='Admin')
      i = i + 1
    elif sys.argv[i].lower() == 'nicknames':
      getNickFeed = True
      nicknames = True
      user_attributes[0].update(Nicknames='Nicknames')
      i = i + 1
    elif sys.argv[i].lower() == 'groups':
      getGroupFeed = True
      groups = True
      user_attributes[0].update(Groups='Groups')
      i = i + 1
    else:
      showUsage()
      exit(5)
  while True:
    try:
      all_users = org.RetrieveAllOrganizationUsers()
      break
    except gdata.apps.service.AppsForYourDomainException:
      continue
  domains = []
  for user in all_users:
    email = user['orgUserEmail']
    domain = email[email.find('@')+1:]
    user_attributes.append({'Email': email.lower()})
    if username:
      location = 0
      try:
        location = user_attributes.index({'Email': email})
        user_attributes[location].update(Username=email[:email.find('@')])
      except ValueError:
        pass
    if ou:
      try:
        location = user_attributes.index({'Email': email})
        user_ou = user['orgUnitPath']
        if user_ou == None:
          user_ou = ''
        user_attributes[location].update(OU=user_ou)
      except ValueError:
        pass
    try:
      domains.index(domain)
    except ValueError:
      domains.append(domain)
    del(email, domain)
  apps = getAppsObject()
  if getUserFeed:
    for domain in domains:
      sys.stderr.write("Getting detailed info for users in %s domain (may take some time on a large domain)...\r\n" % domain)
      apps.domain = domain
      for page in apps.GetGeneratorForAllUsers():
        for user in page.entry:
          email = user.login.user_name.lower() + '@' + domain.lower()
          try:
            location = -1
            gotLocation = False
            while not gotLocation and location < len(user_attributes):
              location = location + 1
              if user_attributes[location]['Email'] == email:
                gotLocation = True
            if firstname:
              userfirstname = user.name.given_name
              if userfirstname == None:
                userfirstname = ''
              user_attributes[location].update(Firstname=userfirstname)
            if lastname:
              userlastname = user.name.family_name
              if userlastname == None:
                userlastname = ''
              user_attributes[location].update(Lastname=userlastname)
            if suspended:
              user_attributes[location].update(Suspended=user.login.suspended)
            if agreed2terms:
              user_attributes[location].update(AgreedToTerms=user.login.agreed_to_terms)
            if admin:
              user_attributes[location].update(Admin=user.login.admin)
          except ValueError:
            pass
          del (email)
  total_users = len(user_attributes)
  if getNickFeed:
    multi = getMultiDomainObject()
    user_count = 1
    for user in user_attributes:
      if user['Email'] == 'Email':
        continue
      nicknames = []
      while True:
        try:
          sys.stderr.write("Getting Aliases for %s (%s/%s)\r\n" % (user['Email'], user_count, total_users))
          nicknames = multi.GetUserAliases(user['Email'])
          break
        except gdata.apps.service.AppsForYourDomainException, e:
          if e.reason == 'EntityDoesNotExist':
            break
          continue
      nicklist = ''
      for nickname in nicknames:
        nicklist += nickname['aliasEmail']+' '
      user.update(Nicknames=nicklist)
      user_count = user_count + 1
      del (nicknames, nicklist)
  if getGroupFeed:
    groupsObj = getGroupsObject()
    user_count = 1
    for user in user_attributes:
      if user['Email'] == 'Email':
        continue
      sys.stderr.write("Getting Group Membership for %s (%s/%s)\r\n" % (user['Email'], user_count, total_users))
      groupsObj.domain = user['Email'][user['Email'].find('@')+1:]
      username = user['Email'][:user['Email'].find('@')]
      groups = []
      while True:
        try:
          groups = groupsObj.RetrieveGroups(username)
          break
        except gdata.apps.service.AppsForYourDomainException, e:
          if e.reason == 'EntityDoesNotExist':
            break
          continue
      grouplist = ''
      for groupname in groups:
        grouplist += groupname['groupId']+' '
      user.update(Groups=grouplist)
      user_count = user_count + 1
      del (username, groups, grouplist)
  for row in user_attributes:
    for cell in row.values():
      print cell+',',
    print ''      
      
def doPrintGroups():
  i = 3
  printname = printdesc = printperm = usedomain = False
  group_attributes = []
  group_attributes.append({'GroupID': 'GroupID'})
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'name':
      printname = True
      group_attributes[0].update(Name='Name')
      i = i + 1
    elif sys.argv[i].lower() == 'description':
      group_attributes[0].update(Description='Description')
      printdesc = True
      i = i + 1
    elif sys.argv[i].lower() == 'permission':
      group_attributes[0].update(Permission='Permission')
      printperm = True
      i = i + 1
    elif sys.argv[i].lower() == 'domain':
      usedomain = sys.argv[i+1]
      i = i + 2
    else:
      showUsage()
      exit(7)
  groupsObj = getGroupsObject()
  if usedomain:
    groupsObj.domain = usedomain
  sys.stderr.write("Retrieving All Groups for domain %s (may take some time on large domain)..." % groupsObj.domain)
  all_groups = groupsObj.RetrieveAllGroups()
  for group_vals in all_groups:
    group = {}
    group.update({'GroupID': group_vals['groupId']})
    if printname:
      name = group_vals['groupName']
      if name == None:
        name = ''
      group.update({'Name': name})
    if printdesc:
      description = group_vals['description']
      if description == None:
        description = ''
      group.update({'Description': description})
    if printperm:
      group.update({'Permission': group_vals['emailPermission']})
    group_attributes.append(group)
  for row in group_attributes:
    for cell in row.values():
      print str(cell)+',',
    print ''


def doPrintNicknames():
  i = 3
  usedomain = False
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'domain':
      usedomain = sys.argv[i+1]
      i = i + 2
  multi = getMultiDomainObject()
  if usedomain:
    multi.domain = usedomain
  sys.stderr.write("Retrieving All Nicknames for domain %s (may take some time on large domain)..." % multi.domain)
  print "Nickname, User"
  nicknames = multi.RetrieveAllAliases()
  for nickname in nicknames:
    print "%s, %s" % (nickname['aliasEmail'], nickname['userEmail'])

def doPrintOrgs():
  i = 3
  printname = printdesc = printparent = printinherit = False
  org_attributes = []
  org_attributes.append({'Path': 'Path'})
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'name':
      printname = True
      org_attributes[0].update(Name='Name')
      i = i + 1
    elif sys.argv[i].lower() == 'description':
      printdesc = True
      org_attributes[0].update(Description='Description')
      i = i + 1
    elif sys.argv[i].lower() == 'parent':
      printparent = True
      org_attributes[0].update(Parent='Parent')
      i = i + 1
    elif sys.argv[i].lower() == 'inherit':
      printinherit = True
      org_attributes[0].update(InheritanceBlocked='InheritanceBlocked')
      i = i + 1
    else:
      showUsage()
      exit(8)
  org = getOrgObject()
  sys.stderr.write("Retrieving All Organizational Units for your account (may take some time on large domain)...")
  orgs = org.RetrieveAllOrganizationUnits()
  for org_vals in orgs:
    orgUnit = {}
    orgUnit.update({'Path': org_vals['orgUnitPath']})
    if printname:
      name = org_vals['name']
      if name == None:
        name = ''
      orgUnit.update({'Name': name})
    if printdesc:
      desc = org_vals['description']
      if desc == None:
        desc = ''
      orgUnit.update({'Description': desc})
    if printparent:
      parent = org_vals['parentOrgUnitPath']
      if parent == None:
        parent = ''
      orgUnit.update({'Parent': parent})
    if printinherit:
      orgUnit.update({'InheritanceBlocked': org_vals['blockInheritance']})
    org_attributes.append(orgUnit)
  for row in org_attributes:
    for cell in row.values():
      print str(cell)+',',
    print ''    

def doPrintResources():
  i = 3
  res_attributes = []
  res_attributes.append({'Name': 'Name'})
  printid = printdesc = printemail = False
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'id':
      printid = True
      res_attributes[0].update(ID='ID')
      i = i + 1
    if sys.argv[i].lower() == 'description':
      printdesc = True
      res_attributes[0].update(Description='Description')
      i = i + 1
    if sys.argv[i].lower() == 'email':
      printemail = True
      res_attributes[0].update(Email='Email')
      i = i + 1
  resObj = getResCalObject()
  sys.stderr.write("Retrieving All Resource Calendars for your account (may take some time on a large domain)")
  resources = resObj.RetrieveAllResourceCalendars()
  for resource in resources:
    resUnit = {}
    resUnit.update({'Name': resource['resourceCommonName']})
    if printid:
      resUnit.update({'ID': resource['resourceId']})
    if printdesc:
      try:
        desc = resource['resourceDescription']
      except KeyError:
        desc = ''
      resUnit.update({'Description': desc})
    if printemail:
      resUnit.update({'Email': resource['resourceEmail']})
    res_attributes.append(resUnit)
  for row in res_attributes:
    for cell in row.values():
      print str(cell)+',',
    print ''

def hasAgreed2TOS(user_name):
  apps = getAppsObject()
  if user_name.find('@') > 0:
    apps.domain = user_name[user_name.find('@')+1:]
    user_name = user_name[:user_name.find('@')]
  userInfo = apps.RetrieveUser(user_name)
  if userInfo.login.agreed_to_terms == 'true':
    return True
  elif userInfo.login.agreed_to_terms == 'false':
    return False

def doCreateMonitor():
  source_user = sys.argv[4].lower()
  destination_user = sys.argv[5].lower()
  #end_date defaults to 30 days in the future...
  end_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
  begin_date = None
  incoming_headers_only = outgoing_headers_only = drafts_headers_only = chats_headers_only = False
  drafts = chats = True
  i = 6
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'end':
      end_date = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'begin':
      begin_date = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'incoming_headers':
      incoming_headers_only = True
      i = i + 1
    elif sys.argv[i].lower() == 'outgoing_headers':
      outgoing_headers_only = True
      i = i + 1
    elif sys.argv[i].lower() == 'nochats':
      chats = False
      i = i + 1
    elif sys.argv[i].lower() == 'nodrafts':
      drafts = False
      i = i + 1
    elif sys.argv[i].lower() == 'chat_headers':
      chats_headers_only = True
      i = i + 1
    elif sys.argv[i].lower() == 'draft_headers':
      drafts_headers_only = True
      i = i + 1
    else:
      showUsage()
      raise StandardError("Incorrect usage.")
  audit = getAuditObject()
  if source_user.find('@') > 0:
    audit.domain = source_user[source_user.find('@')+1:]
    source_user = source_user[:source_user.find('@')]
  
  results = audit.createEmailMonitor(source_user=source_user, destination_user=destination_user, end_date=end_date, begin_date=begin_date,
                           incoming_headers_only=incoming_headers_only, outgoing_headers_only=outgoing_headers_only,
                           drafts=drafts, drafts_headers_only=drafts_headers_only, chats=chats, chats_headers_only=chats_headers_only)

def doShowMonitors():
   user = sys.argv[4].lower()
   audit = getAuditObject()
   if user.find('@') > 0:
     audit.domain = user[user.find('@')+1:]
     user = user[:user.find('@')]
   results = audit.getEmailMonitors(user)
   print sys.argv[4].lower()+' has the following monitors:'
   print ''
   for monitor in results:
     print ' Destination: '+monitor['destUserName']
     try:
       print '  Begin: '+monitor['beginDate']
     except KeyError:
       print '  Begin: immediately'
     print '  End: '+monitor['endDate']
     print '  Monitor Incoming: '+monitor['outgoingEmailMonitorLevel']
     print '  Monitor Outgoing: '+monitor['incomingEmailMonitorLevel']
     print '  Monitor Chats: '+monitor['chatMonitorLevel']
     print '  Monitor Drafts: '+monitor['draftMonitorLevel']
     print ''

def doDeleteMonitor():
  source_user = sys.argv[4].lower()
  destination_user = sys.argv[5].lower()
  audit = getAuditObject()
  if source_user.find('@') > 0:
    audit.domain = source_user[source_user.find('@')+1:]
    source_user = source_user[:source_user.find('@')]
  results = audit.deleteEmailMonitor(source_user=source_user, destination_user=destination_user)

def doRequestActivity():
  user = sys.argv[4].lower()
  audit = getAuditObject()
  if user.find('@') > 0:
    audit.domain = user[user.find('@')+1:]
    user = user[:user.find('@')]
  results = audit.createAccountInformationRequest(user)
  print 'Request successfully submitted:'
  print ' Request ID: '+results['requestId']
  print ' User: '+results['userEmailAddress']
  print ' Status: '+results['status']
  print ' Request Date: '+results['requestDate']
  print ' Requested By: '+results['adminEmailAddress']

def doStatusActivityRequests():
  audit = getAuditObject()
  try:
    user = sys.argv[4].lower()
    if user.find('@') > 0:
      audit.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    request_id = sys.argv[5].lower()
    results = audit.getAccountInformationRequestStatus(user, request_id)
    print ''
    print '  Request ID: '+results['requestId']
    print '  User: '+results['userEmailAddress']
    print '  Status: '+results['status']
    print '  Request Date: '+results['requestDate']
    print '  Requested By: '+results['adminEmailAddress']
    print ''
  except IndexError:
    results = audit.getAllAccountInformationRequestsStatus()
    print 'Current Activity Requests:'
    print ''
    for request in results:
      print ' Request ID: '+request['requestId']
      print '  User: '+request['userEmailAddress']
      print '  Status: '+request['status']
      print '  Request Date: '+request['requestDate']
      print '  Requested By: '+request['adminEmailAddress']
      print ''

def doDownloadActivityRequest():
  user = sys.argv[4].lower()
  request_id = sys.argv[5].lower()
  audit = getAuditObject()
  if user.find('@') > 0:
    audit.domain = user[user.find('@')+1:]
    user = user[:user.find('@')]
  results = audit.getAccountInformationRequestStatus(user, request_id)
  if results['status'] != 'COMPLETED':
    print 'Request needs to be completed before downloading, current status is: '+results['status']
    raise StandardError('Request needs to be completed before downloading, current status is: '+results['status'])
  try:
    if int(results['numberOfFiles']) < 1:
      print 'ERROR: Request completed but no results were returned, try requesting again'
      raise StandardError('ERROR: Request completed but no results were returned, try requesting again')
  except KeyError:
    print 'ERROR: Request completed but no files were returned, try requesting again'
    raise StandardError('ERROR: Request completed but no files were returned, try requesting again')
  for i in range(0, int(results['numberOfFiles'])):
    url = results['fileUrl'+str(i)]
    filename = 'activity-'+user+'-'+request_id+'-'+str(i)+'.txt.gpg'
    print 'Downloading '+filename+' ('+str(i+1)+' of '+results['numberOfFiles']+')'
    geturl(url, filename)

def doRequestExport():
  begin_date = end_date = search_query = None
  headers_only = include_deleted = False
  user = sys.argv[4].lower()
  i = 5
  while i < len(sys.argv):
    if sys.argv[i].lower() == 'begin':
      begin_date = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'end':
      end_date = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'search':
      search_query = sys.argv[i+1]
      i = i + 2
    elif sys.argv[i].lower() == 'headersonly':
      headers_only = True
      i = i + 1
    elif sys.argv[i].lower() == 'includedeleted':
      include_deleted = True
      i = i + 1
    else:
      showUsage()
      raise StandardError("Incorrect usage.")
  audit = getAuditObject()
  if user.find('@') > 0:
    audit.domain = user[user.find('@')+1:]
    user = user[:user.find('@')]
  results = audit.createMailboxExportRequest(user=user, begin_date=begin_date, end_date=begin_date, include_deleted=include_deleted,
                                             search_query=search_query, headers_only=headers_only)
  print 'Export request successfully submitted:'
  print ' Request ID: '+results['requestId']
  print ' User: '+results['userEmailAddress']
  print ' Status: '+results['status']
  print ' Request Date: '+results['requestDate']
  print ' Requested By: '+results['adminEmailAddress']
  print ' Include Deleted: '+results['includeDeleted']
  print ' Requested Parts: '+results['packageContent']
  try:
    print ' Begin: '+results['beginDate']
  except KeyError:
    print ' Begin: account creation date'
  try:
    print ' End: '+results['endDate']
  except KeyError:
    print ' End: export request date'

def doDeleteExport():
  audit = getAuditObject()
  user = sys.argv[4].lower()
  if user.find('@') > 0:
    audit.domain = user[user.find('@')+1:]
    user = user[:user.find('@')]
  request_id = sys.argv[5].lower()
  results = audit.deleteMailboxExportRequest(user=user, request_id=request_id)

def doDeleteActivityRequest():
  audit = getAuditObject()
  user = sys.argv[4].lower()
  if user.find('@') > 0:
    audit.domain = user[user.find('@')+1:]
    user = user[:user.find('@')]
  request_id = sys.argv[5].lower()
  results = audit.deleteMailboxExportRequest(user=user, request_id=request_id)

def doStatusExportRequests():
  audit = getAuditObject()
  try:
    user = sys.argv[4].lower()
    if user.find('@') > 0:
      audit.domain = user[user.find('@')+1:]
      user = user[:user.find('@')]
    request_id = sys.argv[5].lower()
    results = audit.getMailboxExportRequestStatus(user, request_id)
    print ''
    print '  Request ID: '+results['requestId']
    print '  User: '+results['userEmailAddress']
    print '  Status: '+results['status']
    print '  Request Date: '+results['requestDate']
    print '  Requested By: '+results['adminEmailAddress']
    print '  Requested Parts: '+results['packageContent']
    try:
      print '  Request Filter: '+results['searchQuery']
    except KeyError:
      print '  Request Filter: None'
    print '  Include Deleted: '+results['includeDeleted']
    try:
      print '  Number Of Files: '+results['numberOfFiles']
    except KeyError:
      pass
  except IndexError:
    results = audit.getAllMailboxExportRequestsStatus()
    print 'Current Export Requests:'
    print ''
    for request in results:
      print ' Request ID: '+request['requestId']
      print '  User: '+request['userEmailAddress']
      print '  Status: '+request['status']
      print '  Request Date: '+request['requestDate']
      print '  Requested By: '+request['adminEmailAddress']
      print '  Requested Parts: '+request['packageContent']
      try:
        print '  Request Filter: '+request['searchQuery']
      except KeyError:
        print '  Request Filter: None'
      print '  Include Deleted: '+request['includeDeleted']
      try:
        print '  Number Of Files: '+request['numberOfFiles']
      except KeyError:
        pass
      print ''

def doDownloadExportRequest():
  user = sys.argv[4].lower()
  request_id = sys.argv[5].lower()
  audit = getAuditObject()
  if user.find('@') > 0:
    audit.domain = user[user.find('@')+1:]
    user = user[:user.find('@')]
  results = audit.getMailboxExportRequestStatus(user, request_id)
  if results['status'] != 'COMPLETED':
    print 'Request needs to be completed before downloading, current status is: '+results['status']
    raise StandardError('Request needs to be completed before downloading, current status is: '+results['status'])
  try:
    if int(results['numberOfFiles']) < 1:
      print 'ERROR: Request completed but no results were returned, try requesting again'
      raise StandardError('ERROR: Request completed but no results were returned, try requesting again')
  except KeyError:
    print 'ERROR: Request completed but no files were returned, try requesting again'
    raise StandardError('ERROR: Request completed but no files were returned, try requesting again')
  for i in range(0, int(results['numberOfFiles'])):
    url = results['fileUrl'+str(i)]
    filename = 'export-'+user+'-'+request_id+'-'+str(i)+'.mbox.gpg'
    print 'Downloading '+filename+' ('+str(i+1)+' of '+results['numberOfFiles']+')'
    geturl(url, filename)

def doUploadAuditKey():
  auditkey = sys.stdin.read()
  audit = getAuditObject()
  results = audit.updatePGPKey(auditkey)

def doMoveUser():
  old_email = sys.argv[3].lower()
  new_email = sys.argv[4].lower()
  multi = getMultiDomainObject()
  multi.RenameUser(old_email=old_email, new_email=new_email)

def doCreateAlias():
  alias_email = sys.argv[4].lower()
  user_email = sys.argv[5].lower()
  multi = getMultiDomainObject()
  multi.CreateAlias(user_email=user_email, alias_email=alias_email)

def doInfoAlias():
  alias_email = sys.argv[4].lower()
  multi = getMultiDomainObject()
  results = multi.RetrieveAlias(alias_email=alias_email)
  print ''
  print ' Alias: '+results['aliasEmail']
  print ' User: '+results['userEmail']

def doDeleteAlias():
  alias_email = sys.argv[4].lower()
  multi = getMultiDomainObject()
  results = multi.DeleteAlias(alias_email=alias_email)

def getUsersToModify():
  entity = sys.argv[1].lower()
  if entity == 'user':
    users = [sys.argv[2].lower(),]
  elif entity == 'group':
    groupsObj = getGroupsObject()
    group = sys.argv[2].lower()
    members = groupsObj.RetrieveAllMembers(group)
    users = []
    for member in members:
      if member['memberId'].find('@'+domain) == -1:
        continue
      users.append(member['memberId'][0:member['memberId'].find('@')])
  elif entity == 'all':
    apps = getAppsObject()
    users = []
    print "Getting all users in the domain (may take some time on a large domain)..."
    for page in apps.GetGeneratorForAllUsers():
      for user in page.entry:
        users.append(user.login.user_name)
  else:
    showUsage()
    raise StandardError("Incorrect usage.")
  return users


## MAIN PROCESSING ##

def execute():
  try:
    if sys.argv[1].lower() == 'create':
      if sys.argv[2].lower() == 'user':
        doCreateUser()
      elif sys.argv[2].lower() == 'group':
        doCreateGroup()
      elif sys.argv[2].lower() == 'nickname':
        doCreateNickName()
      elif sys.argv[2].lower() == 'org':
        doCreateOrg()
      elif sys.argv[2].lower() == 'resource':
        doCreateResource()
    elif sys.argv[1].lower() == 'update':
      if sys.argv[2].lower() == 'user':
        doUpdateUser()
      elif sys.argv[2].lower() == 'group':
        doUpdateGroup()
      elif sys.argv[2].lower() == 'nickname':
        doUpdateNickName()
      elif sys.argv[2].lower() == 'org':
        doUpdateOrg()
    elif sys.argv[1].lower() == 'info':
      if sys.argv[2].lower() == 'user':
        doGetUserInfo()
      elif sys.argv[2].lower() == 'group':
        doGetGroupInfo()
      elif sys.argv[2].lower() == 'nickname':
        doGetNickNameInfo()
      elif sys.argv[2].lower() == 'domain':
        doGetDomainInfo()
      elif sys.argv[2].lower() == 'org':
        doGetOrgInfo()
      elif sys.argv[2].lower() == 'resource':
        doGetResourceCalendarInfo()
    elif sys.argv[1].lower() == 'delete':
      if sys.argv[2].lower() == 'user':
        doDeleteUser()
      elif sys.argv[2].lower() == 'group':
        doDeleteGroup()
      elif sys.argv[2].lower() == 'nickname':
        doDeleteNickName()
      elif sys.argv[2].lower() == 'org':
        doDeleteOrg()
      elif sys.argv[2].lower() == 'resource':
        doDeleteResourceCalendar()
    elif sys.argv[1].lower() == 'audit':
      if sys.argv[2].lower() == 'monitor':
        if sys.argv[3].lower() == 'create':
          doCreateMonitor()
        elif sys.argv[3].lower() == 'list':
          doShowMonitors()
        elif sys.argv[3].lower() == 'delete':
          doDeleteMonitor()
      elif sys.argv[2].lower() == 'activity':
        if sys.argv[3].lower() == 'request':
          doRequestActivity()
        elif sys.argv[3].lower() == 'status':
          doStatusActivityRequests()
        elif sys.argv[3].lower() == 'download':
          doDownloadActivityRequest()
        elif sys.argv[3].lower() == 'delete':
          doDeleteActivityRequest()
      elif sys.argv[2].lower() == 'export':
        if sys.argv[3].lower() == 'status':
          doStatusExportRequests()
        elif sys.argv[3].lower() == 'download':
          doDownloadExportRequest()
        elif sys.argv[3].lower() == 'request':
          doRequestExport()
        elif sys.argv[3].lower() == 'delete':
          doDeleteExport()
      elif sys.argv[2].lower() == 'uploadkey':
        doUploadAuditKey()
    elif sys.argv[1].lower() == 'multi':
      if sys.argv[2].lower() == 'move':
        doMoveUser()
      elif sys.argv[2].lower() == 'alias':
        if sys.argv[3].lower() == 'create':
          doCreateAlias()
        elif sys.argv[3].lower() == 'info':
          doInfoAlias()
        elif sys.argv[3].lower() == 'delete':
          doDeleteAlias()
    elif sys.argv[1].lower() == 'print':
      if sys.argv[2].lower() == 'users':
        doPrintUsers()
      elif sys.argv[2].lower() == 'nicknames':
        doPrintNicknames()
      elif sys.argv[2].lower() == 'groups':
        doPrintGroups()
      elif sys.argv[2].lower() == 'orgs':
        doPrintOrgs()
      elif sys.argv[2].lower() == 'resources':
        doPrintResources()
    else:
      users = getUsersToModify()
      command = sys.argv[3].lower()
      if command == 'print':
        for user in users:
          print user
      elif command == 'imap':
        doImap(users)
      elif command == 'pop' or command == 'pop3':
        doPop(users)
      elif command == 'sendas':
        doSendAs(users)
      elif command == 'language':
        doLanguage(users)
      elif command == 'utf' or command == 'utf8' or command == 'utf-8' or command == 'unicode':
        doUTF(users)
      elif command == 'pagesize':
        doPageSize(users)
      elif command == 'shortcuts':
        doShortCuts(users)
      elif command == 'arrows':
        doArrows(users)
      elif command == 'snippets':
        doSnippets(users)
      elif command == 'label':
        doLabel(users)
      elif command == 'filter':
        doFilter(users)
      elif command == 'forward':
        doForward(users)
      elif command == 'sig' or command == 'signature':
        doSignature(users)
      elif command == 'vacation':
        doVacation(users)
      elif command == 'webclips':
        doWebClips(users)
      else:
        showUsage()
        raise StandardError("Incorrect usage.")
  except IndexError:
    showUsage()
    raise StandardError("Incorrect usage.")


if __name__ == '__main__':
  execute()
