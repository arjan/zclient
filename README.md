API access library for Zotonic
==============================
by Arjan Scherpenisse <arjan@scherpenisse.net>, 2011-02-14

Uses a simple registry file at `$HOME/.zclient` to store consumer
keys, secrets and authorized access tokens.

    Usage: zclient <command> [opts]
    Generic zotonic API access client.

    Commands:

      add-app <app id> <hostname> <consumer key> <consumer secret>
      - adds a new app plus its consumer details

      del-app <app id>
      - Remove the app and all its authorized clients

      add-client <client id> <app id>
      - sets up authorization for a given oauth app

      request <client id> <api method> [params]
      - do an authorized API request, pretty-print the result
        e.g.: 'zclient request foo base/export id=1' to dump pages



Quick walkthru
--------------

### 1) Enable mod_oauth in Zotonic ###

Go to the admin, modules tab, find the OAuth module and click
"activate", if it is not already activated. Refresh the page.

### 2) Create new OAuth application ###

Go to "API access" tab and click "add new application". In the
dialog, enter the application details, such as title, home page,
etc. callback can be left empty. On the second tab, check the boxes
with the API methods that this app may access. Click the "add
application" button.

### 3. Write down / copy-paste the consumer key and consumer secret ###

This token/secret pair uniquely identifies your application.

### 4. Register the app with zclient ###

    zclient add-app someappid 127.0.0.1:8000 <yourconsumerkey> <yourconsumersecret>
  
"*someappid*" is some identifier that you come up with to identify
  this app on the zclient side. For example: `my-mobile-app`.
  Copy-paste the consumer key and secret from the previous step onto
  the command line.

### 5. Add a client for the app ###

In zclient terminology, a *client* is an authorized token/secret pair
which authorizes a user to use one of the zclient apps.

    zclient add-client yourclientid someappid

The "*yourclientid*" is some identifier to identify the authorized
token for this app on the zclient side.
  
You will be prompted to click on an URL. Do that. Log on to zotonic
and click the "authorize" button on the authorization screen.  Return
to the terminal and press "Enter". Now you should be ready to go!

### 6. Do an authorized request ###

    zclient request yourclientid <api method> [arg [arg..]]
  
For example:
  
    zclient request yourclientid search cat=keyword
  
Maps to the API request `http://yourclienthost/api/search?cat=keyword`
POST requests are currently not (yet) supported.
  
Example API request to search for all persons:
  
         ixion:~/devel/zclient> ./zclient request test search cat=person
         [
           327, 
           1
         ]


**NOTE: On release 0.6.0, the API access has been accidentally
  broken. Please use mercurial default or release-0.6.x branch if you
  want to use the API methods.**

