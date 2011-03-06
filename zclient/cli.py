# Copyright 2011 Arjan Scherpenisse <arjan@scherpenisse.net>
# See LICENSE for details.

from optparse import OptionParser
from zclient import ApplicationRegistry, ZotonicClient, __version__
import ConfigParser

class CLIController(object):

    def __init__(self, fn=None):
        self.registry = ApplicationRegistry(fn)


    def do_list(self):

        self.registry.showAll()

    def do_add_app(self, id, hostname, ckey, csec):
        try:
            self.registry.addApp(id, hostname, ckey, csec)
            self.registry.save()
            print "OK"
        except ConfigParser.DuplicateSectionError:
            print "Duplicate app id"
            exit(1)



    def do_del_app(self, id):
        if not id in self.registry.getApps():
            print "Unknown app id"
            exit(1)
        # also remove every client for this app!
        for c in self.registry.getClients:
            client = self.registry.getClient(c)
            if c['app']['id'] == id:
                self.registry.removeClient(c)
        self.registry.removeApp(id)
        self.registry.save()
        print "OK"


    def do_del_client(self, id):
        if not id in self.registry.getClients():
            print "Unknown client id"
            exit(1)
        self.registry.removeClient(id)
        self.registry.save()
        print "OK"


    def do_add_client(self, id, app_id):
        if id in self.registry.getClients():
            print "Client id already taken"
            exit(1)
        try:
            app = self.registry.getApp(app_id)
            client = ZotonicClient(app)
            token = client.register_client()
            self.registry.addClient(id, app_id, token.key, token.secret)
            self.registry.save()
            print "OK"
        except ConfigParser.NoSectionError:
            print "No such app: "+app_id
            exit(1)


    def do_request(self, client_id, method, *args):
        client = self.registry.getClient(client_id)
        client = ZotonicClient(client)
        params = dict((a.split("=",1) for a in args))
        result = client.doMethod(method, params)
        print json.dumps(result, sort_keys=True, indent=2)

    do_rq = do_request



def usage():
    print "Usage: zclient <command> [opts]"
    print "Generic zotonic API access client."
    print
    print "Command:"
    print
    print "  add-app <app id> <hostname> <consumer key> <consumer secret>"
    print "  - adds a new app plus its consumer details"
    print
    print "  del-app <app id>"
    print "  - Remove the app and all its authorized clients"
    print
    print "  add-client <client id> <app id>"
    print "  - sets up authorization for a given oauth app"
    print
    print "  request <client id> <api method> [params]"
    print "  - do an authorized API request, pretty-print the result"
    print "    e.g.: 'zclient request foo base/export id=1' to dump pages"
    print
    exit(3)

def error(msg):
    print "Error: " + msg
    print
    exit(3)


# main code
def main():
    print "zclient %s" % __version__

    parser = OptionParser()
    parser.add_option("-r", "--registry", help="Registry file", default='~/.zclient')

    (options, args) = parser.parse_args()

    try:
        command = args[0]
        args = args[1:]
    except:
        usage()

    client = CLIController(options.registry)
    try:
        fn = getattr(client, "do_"+command.replace('-', '_'))
    except AttributeError:
        usage()
    fn(*args)



