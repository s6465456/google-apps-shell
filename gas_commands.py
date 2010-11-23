# gas_commands.py
#
# Documentation for the GAS commands.
commands = {

  'createUser': {
    'title': 'Creating a User',
    'category': 'Users',
    'usage': 'gas createUser user_name=<name> first_name=<First Name> last_name=<Last Name> password=<Password> [password_hash_function=SHA-1|MD5] [suspended=true|false] [quota_limit=<quota size>] [change_password=true|false]',
    'description': """
Creates a user account named user_name, with name first_name and last_name, and password password. These fields should be quoted if they contain spaces.
Optional parameter password_hash_function tells GAS that the password is being already given in an encrypted format, either SHA-1 or MD5.
Optional parameter suspended creates the account but marks it as suspended.
Optional parameter quota allows you to set the user's email quota.
Optional parameter change_password will force the user to change their password after their first successful login.
""",
    'examples': [
      ('gas createUser user_name=monkey first_name=David last_name=Monkey password=ILikeBananas',
      'This example creates a user account.'),
      ('gas createUser user_name=elephant@secondarydomain.com first_name=Big last_name=Ears password=ILikePeanuts',
      'This example creates a user in a secondary domain. This is useful when a Google Apps account has multiple domains.')
      ]
  },
  
  'updateUser': {
    'title': 'Update (and Rename) a User',
    'category': 'Users',
    'usage': 'gas updateUser user_name=<name> [new_user_name=<New Name>] [first_name=<First Name>] [last_name=<Last Name>] [password=<Password>] [password_hash_function=SHA-1|MD5] [suspended=true|false] [quota_limit=<quota size>] [change_password=true|false] [admin=true|false] [suspended=true|false] [ip_whitelisted=true|false]',
    'description': """
Updates the user account for user_name. All parameters except user_name are optional. If you wish to rename the username for this user, set new_user_name.

Google makes the following recommendations when renaming a user account:

    * Before renaming a user, it is recommended that you logout the user from all browser sessions and services. For instance, you can get the user on your support desk telephone line during the rename process to ensure they have logged out. The process of renaming can take up to 10 minutes to propagate across all services.
    * Google Talk will lose all remembered chat invitations after renaming. The user must request permission to chat with friends again.
    * When a user is renamed, the old username is retained as a nickname to ensure continuous mail delivery in the case of email forwarding settings and will not be available as a new username. If you prefer not to have the nickname in place after the rename, you'll need to Delete the Nickname 
""",
    'examples': [
      ('gam updateUser user_name=jack first_name=Jack last_name=Johnson password=MovingOut admin=true suspended=false',
      'This example updates a user account, setting the first_name, last_name and password and making them an administrator.'),
      ('gam updateUser user_name=jeffrey new_user_name=jeff',
      'This example renames the user jeffrey to jeff.')
      ]
  },
  
  'readUser': {
    'title': 'Get User Info',
    'category': 'Users',
    'usage': 'gas readUser user_name=<name>',
    'description': """
Retrieve details about the given user.
""",
    'examples': [
      ('gas readUser user_name=daniel',
      'This example will show information on the user daniel.')
      ]
  },
  
  'deleteUser': {
    'title': 'Delete a User',
    'category': 'Users',
    'usage': 'gas deleteUser user_name=<name> [no_rename=true]',
    'description': """
Delete the given user's account. GAS will first rename the user with the current timestamp and then delete the account. This allows the user to be recreated immediately rather than waiting the 5 days that Google normally requires. 
""",
    'examples': [
      ('gas deleteUser user_name=igotfired no_rename=true',
      'This example will delete the account for user igotfired without first renaming the account.')
      ]
  },
  
  'suspendUser': {
    'title': 'Suspend a User',
    'category': 'Users',
    'usage': 'gas suspendUser user_name=<name>',
    'description': """
Suspends the given user's account.
""",
    'examples': [
      ('gas deleteUser user_name=igotfired no_rename=true',
      'This example suspend the account for user igotfired. Suspended accounts can be restored at a later date.')
      ]
  },

  'restoreUser': {
    'title': 'Restore a User',
    'category': 'Users',
    'usage': 'gas restoreUser user_name=<name>',
    'description': """
Restores a user (from a suspended user state). 
""",
    'examples': [
      ('gas restoreUser user_name=ihavereturned',
      'This example restores the user ihavereturned, in the case that ihavereturned was suspended earlier.')
      ]
  },

  '_TEMPLATE': {
    'title': '',
    'usage': '',
    'description': """

""",
    'examples': [
      ('',
      '')
      ]
  },
}
