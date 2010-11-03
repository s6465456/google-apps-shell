# gam-command-tree.yaml
#
#
commands = {

  'create user': {
    'title': 'Creating a User',
    'category': 'Users',
    'usage': 'gam create user <username> firstname <First Name> lastname <Last Name> password <Password> [suspended] [quota <quota size>] [changepassword] [sha] [md5]',
    'description': """
Create an user account named username.
First Name, Last Name and Password arguments are required and should be quoted if they contain spaces.
Optional parameter suspended creates the account but marks it as suspended.
Optional parameter quota allows you to set the user's email quota
(Note: Unless You have specifically requested this ability from Google, setting quotas will not work, don't use this).
The optional parameter changepassword will force the user to change their password after their first successful login.
The optional parameters sha and md5 indicate that Password is a hash of the given type.
""",
    'examples': [
      ('gam create user droth firstname "David Lee" lastname Roth password MightAsWellJump',
      'This example creates a user account.'),
      ('gam create user superdave@secondary-domain.com firstname Super lastname Dave password ICanJumpThat',
      'When using multiple domains, this example creates a user in a secondary domain.')
      ]
  },
  
  'update user': {
    'title': 'Update (and Rename) a User',
    'category': 'Users',
    'usage': 'gam update user <username> [firstname <First Name>] [lastname <Last Name>] [password <Password>] [username <Username>] [admin on|off] [suspended on|off] [ipwhitelisted on|off] [sha] [md5] [changepassword on|off]',
    'description': """
Update an user account named username. First Name, Last Name and Password arguments are optional and should be quoted if they contain spaces. Username is optional and will rename the user's account name (and thus their email address) to Username. admin, suspended and ipwhitelisted arguments are optional and can be turned on or off. sha and md5 arguments are optional and indicate that the Password specified is a hash of the given type. changepassword is optional and indicates that the user should be forced to change their password on their next login.

Google makes the following recommendations when renaming a user account:

    * Before renaming a user, it is recommended that you logout the user from all browser sessions and services. For instance, you can get the user on your support desk telephone line during the rename process to ensure they have logged out. The process of renaming can take up to 10 minutes to propagate across all services.
    * Google Talk will lose all remembered chat invitations after renaming. The user must request permission to chat with friends again.
    * When a user is renamed, the old username is retained as a nickname to ensure continuous mail delivery in the case of email forwarding settings and will not be available as a new username. If you prefer not to have the nickname in place after the rename, you'll need to Delete the Nickname 
""",
    'examples': [
      ('gam update user pmcartney firstname Paul lastname McCartney password LetItBe admin on suspended off',
      'This example updates a user account, setting the firstname, lastname and password and giving them admin access to the domain.'),
      ('gam update user ljones username lsmith lastname Smith',
      'This example renames ljones to lsmith, also setting her last name to Smith (in the case of marriage).'),
      ('gam update gotfired username newguy firstname Nate lastname Ewguy password HopeILastHere',
      'In this example, George Otfired is no longer at the company and Nate Ewguy has taken his position, we\'ll change the username, first and last name and password all in one stroke thus retaining George\'s old Google Apps mail, documents, etc ')
      ]
  },
  
  'info user': {
    'title': 'Get User Info',
    'category': 'Users',
    'usage': 'gam info user <username>',
    'description': """
Retrieve details about the given username. GAM will print out a summary of the user.  Sample output:

gam info user rstarr

User: rstarr
First Name: Ringo
Last Name: Star
Is an admin: false
Has agreed to terms: true
IP Whitelisted: false
Account Suspended: false
Must Change Password: false
Nicknames:
  drummer
  havingthemostfun
Groups:
  The Beatles <beatles@beatles.com> (direct member)
""",
    'examples': [
      ('gam info user rstarr',
      'This example will show information on the user.')
      ]
  },
  
  'delete user': {
    'title': 'Delete a User',
    'category': 'Users',
    'usage': 'gam delete user <username>',
    'description': """
Delete the given user's account. GAM will first rename the user to a random string and then delete the account. This allows you to recreate the account immediately rather than needing to wait the 5 days that Google normally requires. 
""",
    'examples': [
      ('gam delete user pbest',
      'This example will first rename the user\'s account to a long string like pbest-20100705160016-lzfas390m7jwerh6xbk4ncud2 and then delete that account. If needed, a user account pbest can be recreated immediately.')
      ]
  },
  
  'create group': {
    'title': 'Create a Group',
    'category': 'Groups',
    'usage': 'gam create group <group> name <Group Name> description <Group Description> permission owner|member|domain|anyone',
    'description': """
Create a group. Group Name and Description are required and set the groups full name and description. Use quotes around them if they contain spaces. permission is required and can be set to owner, member, domain or anyone which determines who has rights to post to the group. If the User Groups service is enabled for the Google Apps domain, additional groups security settings are available but cannot be set by GAM, this is a Google limitation. For details on User Groups and how rights translate, see <a href="http://www.google.com/support/a/bin/answer.py?hl=en&answer=166148">here</a>.
""",
    'examples': [
      ('gam create group beatles name "The Beatles" description "Members of the Fab Four" permission member',
      'This example creates a group that all group members can send to.')
      ]
  },
  
  'update group settings': {
    'title': 'Update Group Settings',
    'category': 'Groups',
    'usage': 'gam update group <group> [name <Group Name>] [description <Group Description>] [permission owner|member|domain|anyone]',
    'description': """
Update a group's settings, modifying it's full name, description and/or permissions. 
""",
    'examples': [
      ('gam update group beatles name "The Beatles Rock Band" description "British Invasion Band" permission owner',
      'This example modifies the group, changing its full name, description and permissions.')
      ]
  },
  
  'update group <group> add': {
    'title': 'Add Members/Owners to a Group',
    'category': 'Groups',
    'usage': 'gam update group <group> add owner|member <email address>',
    'description': """
Add a member or owner to a group. Note that adding an existing owner to the group as a member will revoke their owner status. Adding an existing member to the group as an owner will give them owner privileges. 
""",
    'examples': [
      ('gam update group beatles add member rstarr@beatles.com',
      'This example adds a member to the group.')
      ]
  },
  
  'update group <group> remove': {
    'title': 'Remove members from a Group',
    'category': 'Groups',
    'usage': 'gam update group <group> remove <email address>',
    'description': """
Remove a member from the given group. Note that if the email address was an owner, they will retain owner rights to the group. To completely remove an owner from a group you should first remove their owner rights by re-adding them to the group as a member. 
""",
    'examples': [
      ('gam update group students remove grad@school.edu',
      'This example removes the user from the group.')
      ]
  },
  
  'info group': {
    'title': 'Get Group Info',
    'category': 'Groups',
    'usage': 'gam info group <group name>',
    'description': """
Retrieve information about a given group.

Sample output.

gam info group beatles

Group Name:  The Beatles
Email Permission:  Member
Group ID:  beatles@beatles.com
Description:  The Fab Four
Owner: jlennon@beatles.com
Owner: pmccartney@beatles.com
Member: gharrison@beatles.com
Member: rstarr@beatles.com
""",
    'examples': [
      ('gam info group beatles',
      'This example will provide information about the group.')
      ]
  },
  
  'delete group': {
    'title': 'Delete a Group',
    'category': 'Groups',
    'usage': 'gam delete group <group name>',
    'description': """
Delete a given group. 
""",
    'examples': [
      ('gam delete group beatles',
      'This example will delete the group ')
      ]
  },
  
  'create nickname': {
    'title': 'Creating a Nickname',
    'category': 'Nicknames',
    'usage': 'gam create nickname <nickname> user <user name>',
    'description': """
Create a nickname for the given user. 
""",
    'examples': [
      ('gam create nickname theking user epresley',
      'This example will create a nickname for the user .')
      ]
  },

  'update nickname': {
    'title': 'Updating a Nickname',
    'category': 'Nicknames',
    'usage': 'gam update nickname <nickname> user <user name>',
    'description': """
Update an existing nickname, changing the user it points to. 
""",
    'examples': [
      ('gam update nickname elvis user epresley',
      'This example will update an existing nickname, pointing it at another user ')
      ]
  },

  'info nickname': {
    'title': 'Retrieving Nickname Information',
    'category': 'Nicknames',
    'usage': 'gam info nickname <nickname>',
    'description': """
Retrieve information about the given nickname.
""",
    'examples': [
      ('gam info nickname president',
      'This example will retrieve information about the nickname.')
      ]
  },

  'delete nickname': {
    'title': 'Deleting a Nickname',
    'category': 'Nicknames',
    'usage': 'gam delete nickname <nickname>',
    'description': """
Removes a nickname. 
""",
    'examples': [
      ('gam delete nickname epresley',
      'This example will remove the nickname.')
      ]
  },

  'create resource': {
    'title': 'Creating a Resource Calendar',
    'category': 'Resource Calendars',
    'usage': 'gam create resource <id> <Common Name> [description <description>] [type <type>]',
    'description': """
Create a calendar resource. id is the short name of the calendar and is used to identify it. Common Name is a longer more detailed name, use quotes around the common name if it contains spaces. The optional argument description allows you enter further details about the calendar resource. The optional argument type allows you to classify the resource. For details on using the type argument to organize your resource calendars, see Google's guidance on organizing resource calendars. (http://code.google.com/googleapps/domain/calendar_resource/docs/1.0/calendar_resource_developers_guide_protocol.html#naming_strategy)
""",
    'examples': [
      ('gam create resource business-calendar "Acme Inc. Business Calendar"',
      'This example will create a calendar resource '),
      ('gam create resource ed101 "ED101 Conference Room" description "Conference Room containing conference phone, whiteboard and projector" type "Conference Room"',
      'This example will create a calendar with optional attributes.')
      ]
  },

  'update resource': {
    'title': 'Updating a Resource Calendar',
    'category': 'Resource Calendars',
    'usage': 'gam update resource <id> [name <Name>] [description <Description>] [type <Type>]',
    'description': """
update a calendar resource. Required argument id is the short name of the calendar and is used to identify it. Optional argument name is the resources Common Name and allows you to change the resource calendar name that users see. The optional argument description allows you enter further details about the calendar resource. The optional argument type allows you to classify the resource. For details on using the type argument to organize your resource calendars, see Google's guidance on organizing resource calendars. (http://code.google.com/googleapps/domain/calendar_resource/docs/1.0/calendar_resource_developers_guide_protocol.html#naming_strategy)
""",
    'examples': [
      ('gam update resource board-room name "Board Room 1" description "Board Room #1 with 25 seats and projector" type "Conference Room"',
      'This will update the calendar resource, changing the common name, description and type.')
      ]
  },

  'info resource': {
    'title': 'Retrieving Resource Calendar Information',
    'category': 'Resource Calendars',
    'usage': 'gam info resource <id>',
    'description': """
Retrieve information for a calendar resource. Required argument id is the short name of the calendar and is used to identify it.

Sample output:

gam info resource ed101

Resource ID: ed101
Common Name: ED101 Conference Room
Email: jay.powerposters.org_6564313031@resource.calendar.google.com
Type: Conference Room
""",
    'examples': [
      ('gam info resource ed101',
      'This example prints the information assocuated with the resource calendar ed101.')
      ]
  },

  'multi move': {
    'title': 'Moving Users between Domains',
    'category': 'Multiple Domains',
    'usage': 'gam multi move <old email address> <new email address>',
    'description': """
Moves the given user account between domains in a Google Apps Multi Domain setup. old email address and new email address are required and specify the full email address of the user account to be moved. Note that in addition to changing the domain, you can change the username portion of the email address during the move also.

When the user is moved, the old email address will automatically be added to the user as an Alias so that they do not lose mail to the old address.
""",
    'examples': [
      ('gam multi move jdean@primary.com jdean@secondary.com',
      'This example moves the user to a secondary domain '),
      ('gam multi move jdean@secondary.com jamesdean@primary.com',
      'This example moves the user back to the primary domain while also changing the username.')
      ]
  },

  'multi alias create': {
    'title': 'Creating an Alias',
    'category': 'Multiple Domains',
    'usage': 'gam multi alias create <alias email address> <user email address>',
    'description': """
Creates an alias email address for the given user email address. The user email address can be in the same domain as the alias or a different primary or secondary domain of the same Google Apps account. 
""",
    'examples': [
      ('gam multi alias create jdean@tertiary.com jdean@primary.com',
      'This example creates an alias for the given user.')
      ]
  },

  'multi alias info': {
    'title': 'Retrieving an Alias',
    'category': 'Multiple Domains',
    'usage': 'gam multi alias info <alias email address>',
    'description': """
Retrieve information about the given email alias. GAM will print the alias and the user that the alias is currently pointing to.

Sample output.

gam multi alias info jdean@tertiary.com

 Alias: jdean@tertiary.com
 User: jdean@primary.com
""",
    'examples': [
      ('gam multi alias info jdean@tertiary.com',
      'This example will print out the details of the alias ')
      ]
  },

  'multi alias delete': {
    'title': 'Deleting an Alias',
    'category': 'Multiple Domains',
    'usage': 'gam multi alias delete <alias email address>',
    'description': """
Delete the given email alias. 
""",
    'examples': [
      ('gam multi alias delete jdean@tertiary.com',
      'This example will delete the alias.')
      ]
  },

  'user language': {
    'title': 'Set User Language',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users language <language code>',
    'description': """
Set the display language used for the user. A full list of language codes can be found here (http://code.google.com/googleapps/domain/email_settings/developers_guide_protocol.html#GA_email_language_tags).  Note that language changes can take several hours to appear in the user's interface and may require the user to log out and log back in. 
""",
    'examples': [
      ('gam user jlennon language en-GB',
      'This example sets the user language to UK English')
      ]
  },

  'user pagesize': {
    'title': 'Set Messages Per Page',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users pagesize 25|50|100',
    'description': """
Determine how many messages a user will see on a web page when viewing their Inbox or other labels. 
""",
    'examples': [
      ('gam user jhendrix pagesize 50',
      'This example sets the page size to 50 for the user.')
      ]
  },

  'user shortcuts': {
    'title': 'Enable/Disable Keyboard Shortcuts',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users shortcuts on|off',
    'description': """
Enable/disable keyboard shortcuts for the given users. List of shortcuts can be found here (http://mail.google.com/support/bin/answer.py?hl=en&answer=6594) 
""",
    'examples': [
      ('gam all users keyboard shortcuts on',
      'This example turns keyboard shortcuts on for all users ')
      ]
  },

  'user arrows': {
    'title': 'Enable/Disable Personal Indicator Arrows',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users arrows on|off',
    'description': """
Enable/disable personal indicator arrows for the given users. Personal indicator arrows are described here. 
""",
    'examples': [
      ('gam user jamesdean arrows off',
      'This example turns personal indicator arrows off for the user ')
      ]
  },

  '_TEMPLATE': {
    'title': 'Enable/Disable Email Snippets',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users snippets on|off',
    'description': """
Enable/disable message snippets in inbox and other message lists. 
""",
    'examples': [
      ('gam group newbies snippets off',
      'This example turns snippets off for the group newbies.')
      ]
  },

  'utf8': {
    'title': 'UTF-8 (Unicode) for outgoing mail',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users utf on|off',
    'description': """
Turn on/off UTF-8 encoding of outgoing mail. 
""",
    'examples': [
      ('gam group faculty utf on',
      'This example sets UTF-8 outgoing mail encoding on for members of the faculty group ')
      ]
  },

  'user webclips': {
    'title': 'Enable/Disable Webclips',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users webclips on|off',
    'description': """
Enable or disable webclips for the given users. Webclips are described here (http://mail.google.com/support/bin/answer.py?hl=en&answer=18219)
""",
    'examples': [
      ('gam all users webclips off',
      'This example disables webclips for all users.')
      ]
  },

  'user signature': {
    'title': 'Setting a Signature',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users signature <signature text>',
    'description': """
Sets a email signature for the given users. Use quotes around the signature text if it contains spaces (which it almost certainly will. New lines can be specified with \n. An empty string like "" will disable the signature. 
""",
    'examples': [
      ('gam all users signature "Acme Inc\n1321 Main Ave\nhttp://www.acme.com"',
      'This example sets all user\'s signatures to "Acme Inc\n1321 Main Ave\nhttp://www.acme.com"')
      ]
  },

  'user vacation': {
    'title': 'Enabling/Disabling and Setting a Vacation (Away) Message',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users vacation on|off subject <subject text> message <message text> [contactsonly]',
    'description': """
Enable or disable a vacation/away message for the given users. Subject is the away message subject. Message is the message text. Use quotes around subject and message text if they contain spaces (which they probably will). In the message text, \n will be replaced with a new line. The optional argument contactsonly will only send away messages to persons in the user's Contacts. 
""",
    'examples': [
      ('gam user epresley vacation on subject "Elvis has left the building" message "I will be on Mars for the next 100 years. I\'ll get back to you when I return.\n\nElvis"',
      'This example sets the away message for the user.')
      ]
  },

  'user label': {
    'title': 'Create a Label',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users label <label name>',
    'description': """
Create a Gmail Label for the given users. Use quotes around the label name if it contains spaces. Labels are described here.

Warning: GAM cannot delete labels. This is because Google has not provided a method for label deletion in their APIs. Before creating labels for some or all users in your domain, please make sure you absolutely need/want them. The only way to get rid of them once created is to have each user manually delete them.
""",
    'examples': [
      ('gam all users label "New Label"',
      'This example creates a label called New Label for all users.')
      ]
  },

  'user filter': {
    'title': 'Create a Filter',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users filter from <email>|to <email>|subject <words>|haswords <words>|nowords <words>|musthaveattachment label <label name>|markread|archive',
    'description': """
Create a Filter for the given users. Filter must have one or more conditions (from, to, subject, haswords, nowords or musthaveattachment) and one or more actions (label, markread or archive). You do not need to create a label before creating a filter that labels messages, creating a filter that labels messages will automatically create the label. Filters are described here.  Note that while the user can set more conditions and actions than those listed above, GAM can only set the conditions and actions described above. This is a limitation of Google's API, not GAM.

Warning: GAM cannot delete filters or labels created by filters. This is because Google has not provided a method for filter or label deletion in their APIs. Before creating filters for some or all users in your domain, please make sure you absolutely need/want them. The only way to get rid of them once created is to have each user manually delete them.
""",
    'examples': [
      ('gam user john filter from dianne@gmail.com label Dianne archive',
      'This example creates a filter for the user john that labels message from dianne@gmail.com and archives them (thus they will only appear under the label) ')
      ]
  },

  'user sendas': {
    'title': 'User Send As',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users sendas <email address> <name> [default] [replyto <email address>]',
    'description': """
Allow the given users to send mail as another email address (also called Custom From). Name is the nice name users see with the email (Use quotes if name includes spaces). Optionally, default specifies that this should be the address used for outgoing mail by default (user can choose which address mail is sent from when they compose). Also optional, replyto specifies a Reply To address to be used when mail is sent out via this sendas.

Note: the email address must be under the direct control of your Google Apps account, the domain must be your Google Apps primary domain, a secondary domain or a domain alias.
""",
    'examples': [
      ('gam user fjones sendas fjones@yourcompany.com "Fred Jones" default',
      'This example will allow the user fjones to send mail as fredjones@yourcompany.com by default (it is assumed to fredjones@yourcompany.com is already setup as a user, group or nickname in your domain).')
      ]
  },

  'user imap': {
    'title': 'IMAP on/off',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users imap on|off',
    'description': """
Turn IMAP on or off for given users. 
""",
    'examples': [
      ('gam all users imap on',
      'This example will turn IMAP on for all current users in the domain.')
      ]
  },

  'user pop': {
    'title': 'POP on/off',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users pop on|off for allmail|newmail action keep|archive|delete',
    'description': """
turn POP3 on or off for given users, "for allmail" will expose all Inbox mail to the POP client while "for newmail" will expose only mail received after POP was enabled. POPped mail can be left alone (keep), archived (archive) or deleted (delete) 
""",
    'examples': [
      ('gam group students pop on for allmail action keep',
      'This example will turn POP on for any users in the group students. All mail in the Inbox will be exposed to the POP client and POPped emails will be kept in the Inbox.')
      ]
  },

  'user forward': {
    'title': 'Automatic Forwarding',
    'category': 'Email Settings',
    'usage': 'gam user <username>|group <groupname>|all users forward on|off [email address] [keep|archive|delete] [noconfirm]',
    'description': """
Enable/disable and set an automatic email forward for the given users. If turning forwarding on, an email address and action are both required. Actions (keep, archive and delete) specifies what to do with messages that have been forwarded. By default, GAM also checks to see if the user has agreed to Google's Terms of Service (ToS). this occurs the first time they log in to the web interface. If the user has not completed the Captcha and agreed to the ToS the forward will not work until they do. GAM will display a warning if it finds the user has not agreed to the ToS yet. The optional argument noconfirm disables the ToS check which can speed up GAM when setting a forward for many accounts.

Warning: Google has recently taken steps to limit what email addresses forwards can be set to via the API (and thus via GAM). See this blog post for details about what domains you can set forwards to. Generally you are limited to forwarding to your primary domain, alias and secondary domains and subdomains of those.
""",
    'examples': [
      ('gam user eclapton forward on eclapton@music.com delete',
      'This example sets a forward for the user, messages will be deleted after they are forwarded so they will not show up in the user\'s account.')
      ]
  },

  'audit monitor create': {
    'title': 'Create a Audit Monitor',
    'category': 'Audits',
    'usage': 'gam audit monitor create <source user> <destination user> [begin <begin date>] [end <end date>]  [incoming_headers] [outgoing_headers] [nochats] [nodrafts] [chat_headers] [draft_headers]',
    'description': """
Create an audit monitor for the source user. All Mail to and from the source user will be forwarded to the destination user. By default, the audit will begin immediately and last for 30 days. Optional parameters begin and end can set the start and end times. Both parameters must be in the future with end being later than begin, the format is "YYYY-MM-DD hh:mm". Optional parameters, incoming_headers and outgoing_headers configure the audit to not send the given message's full email body but just the message headers. By default, the audit will also forward the source user's Chats and saved message Drafts. The optional parameters nochats and nodrafts disable forwarding of these type of messages. The optional parameters chat_headers and draft_headers tell the audit to only send the headers of the given messages instead of the full message body.

Only one audit is possible per a source and destination user combo. Creating a new audit with the same source and destination of an existing audit will overwrite the settings of the current of the existing audit.
""",
    'examples': [
      ('gam audit monitor create jsmith fthomas',
      'This example configures an audit of the source user, forwarding full copies of all incoming, outgoing, chat and draft messages to the destination user. The audit will start immediately and terminate in 30 days time'),
      ('gam audit monitor create jsmith fthomas begin "2010-07-15 12:00" end "2011-07-15 12:00" incoming_headers outgoing_headers chat_headers draft_headers',
      'This example will start the audit on the given date and end it on the given date. Only message headers of each type will be sent to fthomas.'),
      ('gam audit monitor create jsmith fthomas nochats nodrafts',
      'This example will not capture drafts or chats.')
      ]
  },
  
  'audit monitor list': {
    'title': 'List Audit Monitors',
    'category': 'Audits',
    'usage': 'gam audit monitor list <source user>',
    'description': """
Shows the current audit monitors for the user source user.
""",
    'examples': [
      ('gam audit monitor list jsmith',
      'This example will list the current monitors for the user jsmith')
      ]
  },

  'audit monitor delete': {
    'title': 'Delete an Audit Monitor',
    'category': 'Audits',
    'usage': 'gam audit monitor delete <source user> <destination user>',
    'description': """
Delete the audit monitor for the given source user / destination user combo. 
""",
    'examples': [
      ('gam audit monitor delete jsmith fthomas',
      'This example deletes the monitor that is sending all jsmith\'s mail to fthomas ')
      ]
  },

  'audit activity request': {
    'title': 'Request an Account\'s Activity',
    'category': 'Audits',
    'usage': 'gam audit activity request <user>',
    'description': """
Request the account activity of the given user. Requests can take several hours/days to be completed by Google's servers. GAM will print out a request ID which can be used to monitor the progress of the request (see Retrieving Request Status below). Note that before requesting an account's activity, a GPG key should be uploaded to Google Servers. See Using GPG with Audits (http://code.google.com/p/google-apps-manager/wiki/ExamplesAccountAuditing#Using_GPG_with_Audits) for more details on GPG keys. Failure to upload a key will result in the activity request always getting a status of ERROR. 
""",
    'examples': [
      ('gam audit activity request jsmith',
      'This example creates a request for the user\'s activity.')
      ]
  },

  'audit activity status': {
    'title': 'Retrieving Current Status of Activity Request(s)',
    'category': 'Audits',
    'usage': 'gam audit activity status [user request_id]',
    'description': """
Get the current status of existing account activity requests. Optionally, a user and request_id can be specified to limit the retrieval to a single request. 
""",
    'examples': [
      ('gam audit activity status',
      'This example retrieves the status of all current activity requests.')
      ]
  },

  'audit activity download': {
    'title': 'Downloading the Results of a Completed Activity Request',
    'category': 'Audits',
    'usage': 'gam audit activity download <user> <request_id>',
    'description': """
Download the results of an activity request that has a status of COMPLETED. The required parameters user and request_id specify which request to download. The GPG encrypted activity file will be saved to a file named with the format activity-username-request_id-1.txt.gpg and should be decrypted with GPG. 
""",
    'examples': [
      ('gam audit activity download jsmith 234342',
      'This example downloads the encrypted activity log of the COMPLETED request ')
      ]
  },

  'audit activity delete': {
    'title': 'Deleting a Completed Activity Request',
    'category': 'Audits',
    'usage': 'gam audit activity delete <user> <request_id>',
    'description': """
Delete the completed activity request for the given user. User and Request ID are required parameters. 
""",
    'examples': [
      ('gam audit activity delete jsmith 234342',
      'This example deletes the completed activity request for the user ')
      ]
  },

  'audit export request': {
    'title': 'Request an Export of a User\'s Mailbox',
    'category': 'Audits',
    'usage': 'gam audit export request <user> [begin <Begin Date>] [end <End Date>] [search <Search Query>] [headersonly] [includedeleted]',
    'description': """
Request an export of all mail in a user's mailbox. Optional parameters begin and end date specify the range of messages that should be included in the export and should be of the format "YYYY-MM-DD hh:mm". By default, export begins at account creation and ends at the time of the export request. Optional parameter search, specifies a search query defining what messages should be included in the export. The query parameters are the same as those used in the Gmail interface and described here (http://mail.google.com/support/bin/answer.py?hl=en&answer=7190). Optional parameter headersonly specifies that only the message headers should be included in the export instead of the full message body. Optional parameter includedeleted specifies that deleted messages should also be included in the export.

Note that before requesting an export of an account, a GPG key should be uploaded to Google's Server. See Using GPG with Audits for more details on GPG keys. Failure to upload a key will result in the export request always getting a status of ERROR.
""",
    'examples': [
      ('gam audit export request jsmith includedeleted',
      'This example requests an export of all of a user\'s mail including deleted messages.'),
      ('gam audit export request jsmith begin "2010-06-01 00:00" end "2010-07-01 00:00" includedeleted',
      'This example requests an export of all of a user\'s mail for a 30 day range including deleted.'),
      ('gam audit export request jsmith search "subject:secret"',
      'This example requests an export of all of a user\'s mail that has the word secret in the message subject.')
      ]
  },

  'audit export status': {
    'title': 'Retrieving Current Status of Export(s)',
    'category': 'Audits',
    'usage': 'gam audit export status [user request_id]',
    'description': """
Retrieve the status of current export requests. If the optional parameters user and request_id are specified, only the status of the one request will be retrieved, otherwise all current requests' status will be retrieved. 
""",
    'examples': [
      ('gam audit export status',
      'This example shows the status of all current export requests.')
      ]
  },

  'audit export download': {
    'title': 'Downloading the Results of a Completed Export Request',
    'category': 'Audits',
    'usage': 'gam audit export download <user request_id>',
    'description': """
Download the encrypted results of a completed export request. The required parameters user and request_id specify which request's results should be downloaded. The encrypted files are saved with file names of export-username-request_id-file_number.mbox.gpg. After they have been downloaded, they can be decrypted with GPG and then viewed with a mail client like Thunderbird. 
""",
    'examples': [
      ('gam audit export download jsmith 344920',
      'This example downloads the completed export request for jsmith ')
      ]
  },

  'audit export delete': {
    'title': 'Deleting a Completed Export Request',
    'category': 'Audits',
    'usage': 'gam audit export delete <user request_id>',
    'description': """
Delete the completed export request. The required parameters user and request_id specify which request to delete. 
""",
    'examples': [
      ('gam audit export delete jsmith 344920',
      'This example deletes the export request for the given user.')
      ]
  },

  'create org': {
    'title': 'Creating an Organization Unit',
    'category': 'Organizations',
    'usage': 'gam create org <name> [description <Description>] [parent <Parent Org>] [noinherit]',
    'description': """
Create an organizational unit. The required argument name is the organization unit name, if it contains spaces, it should be quoted. The optional argument description offers more details on the organizational unit, if it contains spaces it should be quoted. The optional argument parent allows the organization unit to be created as a sub-org of an existing organization unit, if it contains spaces it should be quoted. If parent is not specified, the new organization is created at the top level. The optional argument noinherit blocks policy setting inheritance from organization units higher in the organization tree, inheritance is enabled by default if noinherit is not specified. 
""",
    'examples': [
      ('gam create org "Mail Enabled Faculty" description "Faculty with access to Gmail" parent Employees noinherit',
      'This example creates an Organization Unit with all optional arguments.')
      ]
  },

  'update org': {
    'title': 'Updating (and adding users to) an Organization Unit',
    'category': 'Organizations',
    'usage': 'gam update org <name> [name <New Name>] [description <Description>] [parent <Parent>] [inherit|noinherit] [add <Users> | addfile <File Name> | addgroup <Group Name> | addnotingroup <Group Name>]',
    'description': """
Update an organization unit. The required argument name is the organization unit name, if it contains spaces, it should be quoted. If the organization unit is a sub-organization, it should use the format "parent org/org" (use the / character between the parent and the sub-org). The optional argument "name ..." specifies a new name for the organization unit, if it contains spaces, it should be quoted. The optional argument description offers more details on the organizational unit, if it contains spaces it should be quoted. The optional argument parent allows the organization unit to be moved as a sub-org of an existing organization unit, if it contains spaces it should be quoted. The optional arguments inherit and noinherit enable/disable inheritance respectfully. The optional arguments add, addfile and addgroup specify a list, filename or group of users that should be moved into the organization unit. If using add, the list of users should be quoted and spaces should be used between each user. If using addfile, the given file should contain a list of users to be added, one per line. If using addgroup, specify the name of a Google Apps group that contains the users you would like moved into the organization unit. If using addnotingroup, specify the name of a Google Apps group, all Google Apps users not in the given group will be moved into the organization unit.

Important: Users can only exist in one organization unit at a time. When you add them to an organization unit with this command, they will be removed from their previous organization unit.
""",
    'examples': [
      ('gam update org Faculty description "Faculty Users" parent Employees inherit',
      'This example updates the organization unit\'s parameters without adding any users.'),
      ('gam update org Faculty name "Faculty and Staff"',
      'This example renames the organization unit '),
      ('gam update org Faculty add "socrates plato aristotle"',
      'This example adds the given list of users to the organization unit '),
      ('gam update org Faculty addfile faculty.txt',
      'This example assumes that the file faculty.txt exists and looks like: davinci\nmichaelangelo\nraphael\n.  It will add these uses to the organization unit.'),
      ('gam update org Faculty addgroup inventors',
      'This example will add members of the Google Apps group inventors to the Faculty organization unit.'),
      ('gam update org Faculty addnotingroup students',
      'This example will add all users who are NOT a member of the students group to the Faculty organization unit.')
      ]
  },

  'info org': {
    'title': 'Retrieving an Organization Unit\'s Information',
    'category': 'Organizations',
    'usage': 'gam info org <name>',
    'description': """
Retrieve details about the given organization unit. GAM will print a summary of the organization unit.

Sample output.

gam info org Faculty
Organization Unit: Faculty
Description: Faculty Users
Parent Org: /
Block Inheritance: false
Users:
 davinci@domain.com
 michelangelo@domain.com
 raphael@domain.com
""",
    'examples': [
      ('gam info org Faculty',
      'This example will print a summary of the given organiational unit Faculty.')
      ]
  },

  'print users': {
    'title': 'Printing all users',
    'category': 'Printing',
    'usage': 'gam print users [firstname] [lastname] [username] [ou] [suspended] [changepassword] [agreed2terms] [admin] [nicknames] [groups]',
    'description': """
Prints a CSV file of all users in the Google Apps Organization. The CSV output can be redirected to a file using the operating system's pipe command (such as "> users.csv") see examples below. By default, the only column printed is the user's full email address. The optional arguments firstname, lastname, username, ou (organization unit), suspended, changepassword, agreed2terms, admin, nicknames and groups add the respective additonal column to the CSV output.

IMPORTANT:
Note that adding one or more of firstname, lastname, suspended, changepassword, agreed2terms or admin will require 1 additional call to Google's servers per a domain that will increase the length of time for the command to complete. Note also that adding nicknames and groups will each require 1 additional call to Google's servers per user which will significantly increase the length of time for the command to complete. These commands may take a long time for a large organization.""",
    'examples': [
      ('gam print users firstname lastname',
      'This example will generate the output showing with columns for Email, Firstname and Lastname')
      ]
  },

  'print groups': {
    'title': 'Printing All Groups',
    'category': 'Printing',
    'usage': 'gam print groups [name] [description] [permission] [domain <domain name>]',
    'description': """
Outputs all groups in the Google Apps domain. The CSV output can be redirected to a file using the operating system's pipe command (such as "> groups.csv") see examples below. By default, the only column printed is the GroupID (email address). The optional arguments name, description and permission add the respective additonal column to the CSV output. The optional argument domain allows you to print groups for a secondary domain assuming you are using multi-domain support and have created groups in secondary domains. Only 1 call to Google's servers is done no matter which arguments are specified so the optional arguments should not significantly increase the time it takes for the command to complete. 
""",
    'examples': [
      ('gam print groups name description permission',
      'This example will output all details for all groups on the primary domain.'),
      ('gam print groups name description permission domain secondary.com',
      'This example will output all details for all groups on a secondary domain.')
      ]
  },

  'print nicknames': {
    'title': 'Print All Nicknames',
    'category': 'Printing',
    'usage': 'gam print nicknames [domain <domain name>]',
    'description': """
Prints all nicknames/email aliases in the Google Apps domain. The CSV output can be redirected to a file using the operating system's pipe command (such as "> nicknames.csv") see examples below. The optional argument domain allows you to print nicknames for a secondary domain assuming you are using multi-domain support and have created nicknames/email aliases in secondary domains. The CSV file will always contain the columns Nickname and User which will contain full email addresses. 
""",
    'examples': [
      ('gam print nicknames',
      'This example will output all nicknames for the primary domain.')
      ]
  },

  'print orgs': {
    'title': 'Print All Organizational Units',
    'category': 'Printing',
    'usage': 'gam print orgs [name] [description] [parent] [inherit]',
    'description': """
Prints all organizational units in the Google Apps account. The CSV output can be redirected to a file using the operating system's pipe command (such as "> orgs.csv") see examples below. By default, the only column output is "Path" (OUs full path). The optional arguments name, description, parent and inherit add the respective additonal column to the CSV output. Only 1 call to Google's servers is done no matter which arguments are specified so the optional arguments should not significantly increase the time it takes for the command to complete. 
""",
    'examples': [
      ('gam print orgs name description parent inherit',
      'This example will output all organizations to the file orgs.csv including all optional columns ')
      ]
  },

  'print resources': {
    'title': 'Print All Resource Calendars',
    'category': 'Printing',
    'usage': 'gam print resources [id] [description] [email]',
    'description': """
Prints a CSV file of all resource calendars in the Google Apps account. The CSV output can be redirected to a file using the operating system's pipe command (such as "> resources.csv") see examples below. By default, the only column output is "Name"The optional arguments id, description and email add the respective additonal column to the CSV output. Only 1 call to Google's servers is done no matter which arguments are specified so the optional arguments should not significantly increase the time it takes for the command to complete. 
""",
    'examples': [
      ('gam print resources id description email',
      'This example will output all resource calendars in csv format, including all optional columns.')
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
