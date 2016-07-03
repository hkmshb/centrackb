# Authentication 

The traditional, widely adopted means of username and password verification is
adopted for authentication users.


# Authorization

A role-based mechanism is used to determined what level of access a user has
for available resources. The standard roles defined for the CENTrak are listed
below with their 'access rights weight' indicated to the left:

* admin         : 100
* moderator     : 80
* team-lead     : 70
* member        : 60
* user          : 50


# Activation

By default bottle-cork accounts are activated from link sent out on successful
registration. The workflow was email-based circumvented, the current registration
implementation is identical to that provided by bottle-cork with the exception
of the automated mailing of the verification link.

The registered user details gets stored in the backend store as expected, however
to activate the account, the registration code has to be copied and used to form
a url path as thus: [/activate/<registration-code>]

The resulting url when visited causes the account in question to be activated.
This is a crude form of human review and activation of pending account creation
requests! :-D

