#!/usr/bin/python
#
# Google Apps Shell
#
# Google Apps Shell is a script allowing Google Apps administrators to issue simple commands to their Apps domain.
# For more information, see http://code.google.com/p/google-apps-shell/
# It was inspired by the Google Apps Manager (see http://code.google.com/p/google-apps/manager/)
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

"""Google Apps Shell is a script allowing Google Apps administrators to issue simple commands to their Apps domain."""

__author__ = 'jeffpickhardt@google.com (Jeff Pickhardt)'
__version__ = '1.0.0'
__license__ = 'Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)'

import sys, os, time, datetime, random, cgi, socket, urllib, csv
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
import getpass


## CREDENTIALS / AUTHENTICATION RELATED STUFF ##
class Credentials:
    def __init__(self, email='', password=''):
        """Comments"""
        
        if len(email):
            split = email.split('@')
            self.username = split[0]
            self.domain = split[1]
            self.password = password
        else:
            self.username = ''
            self.domain = ''
            self.password = ''
            # self.logIn will attempt to use last authentication token used
          
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        if os.path.abspath('/') != -1:
            divider = '/'
        else:
            divider = '\\'
        self.tokenPath = path+divider+'gas_credential_log.txt'
        self.logIn()
    
    def getEmail(self):
        """Returns the email address made up from the username and domain name."""
        return self.username+'@'+self.domain
    
    def getUsername(self):
        """Returns the currently logged in username."""
        return self.username
    
    def getDomain(self):
        """Returns the currently logged in domain name."""
        return self.domain
    
    def credentialLineToList(self, line):
        splitLine = line.split(',')
        splitLine = [newLine.strip() for newLine in splitLine]
        
        if len(splitLine)==5:
            return splitLine # in format date, activity, username, domain, token
        else:
            return ['','','','','']
        
    def lastCredentials(self):
        # First checks to see whether the username/password combination has a token from Google.
        try:
            if os.path.isfile(self.tokenPath):
                tokenFile = open(self.tokenPath, 'r')
                tokenFileLines = tokenFile.readlines()
                tokenFile.close()
            
                lastLine = tokenFileLines[-1] # the last line in the file should be the most up-to-date authorization token
                return self.credentialLineToList(lastLine)
            else:
                return ['','','','','']
        except:
            return ['','','','','']

    def logIn(self):
        """Authorizes the username, domain, and password with Google.  Stores a token in the text file tokens.txt"""
        isAuthorized = False
        
        # First checks to see whether the username/password combination has a token from Google.
        (lineDate, lineActivity, lineUsername, lineDomain, lineToken) = self.lastCredentials()
        if (lineUsername==self.username and lineDomain==self.domain) or self.username=='':
            # Either the token matches, or no username was given, in which case we'll try the last token.
            try:
                service = gdata.apps.service.AppsService(domain=lineDomain)
                service.SetClientLoginToken(lineToken)
                service.RetrieveUser(lineUsername) # test that we're successfully authorized
                
                isAuthorized = True
                self.domain = lineDomain
                self.username = lineUsername
                self.token=lineToken
            except gdata.apps.service.AppsForYourDomainException, e:
                pass
            except socket.error, e:
                raise Exception("Failed to connect to Google's servers.")
        
        if not isAuthorized:
            service = gdata.apps.service.AppsService(email=self.getEmail(), domain=self.domain, password=self.password)
            try:
                service.ProgrammaticLogin()
                service.RetrieveUser(self.username) # test that we're successfully authorized
                isAuthorized = True
            except gdata.service.BadAuthentication, e:
                raise Exception("Invalid username and password combination. Please try again.")
            except gdata.apps.service.AppsForYourDomainException, e:
                raise Exception ("Either the user you entered is not a Google Apps Administrator or the Provisioning API is not enabled for your domain. Please see: http://www.google.com/support/a/bin/answer.py?hl=en&answer=60757")
            except socket.error, e:
                raise Exception("Failed to connect to Google's servers.")
            
            self.token = service.current_token.get_token_string()
            
            tokenFile = open(self.tokenPath, 'a')
            tokenFile.write("\n"+time.asctime() + ',log_in,' + self.username + ',' + self.domain + ',' + self.token)
            tokenFile.close()
            
        self.service = service
        return service
    
    def logOut(self):
        """Removes the authentication token from the token file, and adds a log out activity."""
        
        tokenFile = open(self.tokenPath, 'r')
        tokenLines = tokenFile.readlines()
        tokenFile.close()
        
        tokenFile = open(self.tokenPath, 'w')
        for line in tokenLines:
            (lineDate, lineActivity, lineUsername, lineDomain, lineToken) = self.credentialLineToList(line)
            if lineActivity=='log_in' and lineToken==self.token:
                tokenFile.write(lineDate + ',log_in,' + lineUsername + ',' + lineDomain + ',' + 'removed')
            else:
                tokenFile.write(line)
        tokenFile.write("\n"+time.asctime() + ',log_out,' + self.username + ',' + self.domain + ',no_token')
        tokenFile.close()
        
        self.username = ''
        self.domain = ''
        self.token = ''
        self.service = False

def logIn(email='', password=''):
    """Logs in with the credentials provided by the email and password arguments."""
    credential = Credentials(email=args[1], password=args[2])
    return credential

def logOut(credential):
    """Logs out of the current credentials."""
    credential.logOut()
    
def printAuthentication(credential):
    """Prints output explaining the current authentication status."""
    log('Currently authenticated as %s to %s' % (credential.getEmail(), credential.getDomain()))


## USER FUNCTIONS ##
def createUser(credential, user_name, first_name, last_name, password, password_hash_function=None, suspended='false', quota_limit=None, change_password=None):
    """Creates a user."""
        
    if not password_hash_function:
        new_hash = sha1()
        new_hash.update(password)
        password = new_hash.hexdigest()
        password_hash_function = 'SHA-1'
    
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
        
    log("Creating account for %s" % user_name)
    try:
        credential.service.CreateUser(user_name=user_name, family_name=last_name, given_name=first_name, password=password, suspended=suspended, quota_limit=quota_limit, password_hash_function=password_hash_function, change_password=change_password)
    except gdata.apps.service.AppsForYourDomainException, e:
        if e.reason == 'EntityExists':
            raise Exception('EntityExists error. '+user_name+" is an existing user, group or nickname. Please delete the existing entity with this name before creating "+user_name)
        elif e.reason == 'UserDeletedRecently':
            raise Exception('UserDeletedRecently error. '+user_name+" was recently deleted within five days. You'll need to wait five days before a user can be created or renamed to this name.")
        else:
            raise StandardError('An error occurred: '+e.reason)        
    
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def updateUser(credential, user_name, new_user_name=None, first_name=None, last_name=None, password=None, password_hash_function=None, admin=None, suspended=None, ip_whitelisted=None, change_password=None):
    """Updates the user."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    user = credential.service.RetrieveUser(user_name)
    
    if new_user_name!=None:
        user.login.user_name = new_user_name

    if first_name!=None:
        user.name.given_name = first_name
    
    if last_name!=None:
        user.name.family_name = last_name
    
    if password!=None:
        if not password_hash_function:
            new_hash = sha1()
            new_hash.update(password)
            password = new_hash.hexdigest()
            password_hash_function = 'SHA-1'
        user.login.password = password
        user.login.hash_function_name = password_hash_function
    
    if admin!=None:
        if not admin:
            user.login.admin = 'false'
        else:
            user.login.admin = 'true'
    
    if suspended!=None:
        if not suspended:
            user.login.suspended = 'false'
        else:
            user.login.suspended = 'true'
    
    if ip_whitelisted!=None:
        if not ip_whitelisted:
            user.login.ip_whitelisted = 'false'
        else:
            user.login.ip_whitelisted = 'true'
    
    if change_password!=None:
        if not ip_whitelisted:
            user.login.change_password = 'false'
        else:
            user.login.change_password = 'true'
    
    log('Updating %s' % user_name)
    try:
        credential.service.UpdateUser(user_name, user)
    except gdata.apps.service.AppsForYourDomainException, e:
        if e.reason == 'EntityExists':
            raise Exception('EntityExists error. '+user.login.user_name+" is an existing user, group or nickname. Please delete the existing entity with this name before renaming "+user_name)
        elif e.reason == 'UserDeletedRecently':
            raise Exception('UserDeletedRecently error. '+user.login.user_name+" was recently deleted within five days. You'll need to wait five days before a user can be created or renamed to this name.")
        else:
            raise StandardError('An error occurred: '+e.reason)        
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain


def readUser(credential, user_name, first_name=True, last_name=True, admin=True, suspended=True, ip_whitelisted=True, change_password=True, agreed_to_terms=True):
    """Reads the user with username user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    try:
        user = credential.service.RetrieveUser(user_name)
    except gdata.apps.service.AppsForYourDomainException, e:
        if e.reason == 'EntityDoesNotExist':
            raise Exception('EntityDoesNotExist error. '+user_name+" does not exist.")
        else:
            raise StandardError('An error occurred: '+e.reason)        
    
    print 'User: %s' % user.login.user_name
    
    if first_name:
        print 'First Name: %s' % user.name.given_name
    
    if last_name:
        print 'Last Name: %s' % user.name.family_name
    
    if admin:
        print 'Is Admin: %s' % user.login.admin
    
    if suspended:
        print 'Is Suspended: %s' % user.login.suspended
    
    if ip_whitelisted:
        print 'IP Whitelisted: %s' % user.login.ip_whitelisted
    
    if change_password:
        print 'Must Change Password: %s' % user.login.change_password
    
    if agreed_to_terms:
        print 'Has Agreed to Terms: %s' % user.login.agreed_to_terms    
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def suspendUser(credential, user_name):
    """Suspends the user with username user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    log('Suspending %s' % user_name)
    credential.service.SuspendUser(user_name)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def restoreUser(credential, user_name):
    """Suspends the user with username user_name."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    log('Restoring %s' % user_name)
    credential.service.RestoreUser(user_name)

    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain

def deleteUser(credential, user_name, no_rename=False):
    """Deletes the user with username user_name. The username is first renamed to include the current timestamp; this is so that a new user with the same username can be recreated immediately. If no_rename is set, this part is skipped."""
    old_domain=''
    if user_name.find('@') > 0:
        old_domain = credential.service.domain
        credential.service.domain = user_name[user_name.find('@')+1:]
        user_name = user_name[:user_name.find('@')]
    
    if no_rename.lower()=='true':
        log('Deleting %s' % user_name)
        credential.service.DeleteUser(user_name)
    else:
        time_stamp = time.strftime("%Y%m%d%H%M%S")
        renamed_user_name = user_name+'-'+time_stamp
        user = credential.service.RetrieveUser(user_name)
        user.login.user_name = renamed_user_name
        log('Renaming %s to %s' % (user_name, renamed_user_name))
        credential.service.UpdateUser(user_name, user)
        log('Deleting %s' % renamed_user_name)
        credential.service.DeleteUser(renamed_user_name)
    
    if old_domain:
        # reset domain to the old domain
        credential.service.domain = old_domain


## USER EMAIL SETTING FUNCTIONS ##



## NICKNAME FUNCTIONS ##



## GROUP FUNCTIONS ##



## SHARED CONTACT FUNCTIONS ##



## MULTI DOMAIN FUNCTIONS ##



## RESOURCE CALENDAR FUNCTIONS ##



## AUDIT FUNCTIONS ##



## ORGANIZATIONAL UNIT FUNCTIONS ##



## DOCS FUNCTIONS ##



## PROCESSING FUNCTIONS ##

def log(message):
    """Logs the message."""
    print message

def buildArgDict(args, caseSensitive=False):
    """Takes an array of arguments and builds a dictionary out of it."""
    dictionary = {}
    for arg in args:
        splits = arg.split('=')
        if len(splits)<2:
            splits.append(True)
        if not caseSensitive:
            # dictionary keys are not case sensitive
            splits[0]=splits[0].lower()
        dictionary[splits[0]]=splits[1]
    return dictionary

whitelist_functions = {
    'createUser': createUser,
    'readUser': readUser,
    'updateUser': updateUser,
    'deleteUser': deleteUser,
    'suspendUser': suspendUser,
    'restoreUser': restoreUser,
    'printAuthentication': printAuthentication,
    }

def execute(args):
    call_function = args[0]
    dictionary = buildArgDict(args[1:])
    
    # logIn and logOut are treated specially since they use the credential
    if call_function=='logIn':
        credential = Credentials(**dictionary)
    elif call_function=='logOut':
        try:
            credential = Credentials(**dictionary)
        except:
            raise Exception('Cannot log out because you are not logged in.')
        logOut(credential, **dictionary)
    else:
        credential = Credentials('', '')
        if call_function in whitelist_functions:
            whitelist_functions[call_function](credential, **dictionary)
        else:
            raise Exception('Unknown function '+call_function)

## MAIN ##
def __main__():
    args = sys.argv
    if len(args)<=1:
        raise Exception('Must provide at least one argument.')
    execute(args[1:])

if __name__ == '__main__':
    __main__()
