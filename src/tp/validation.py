from M2Crypto import SSL
from M2Crypto.SSL.Checker import NoCertificate, WrongCertificate, WrongHost
import socket, re
from datetime import datetime
import csv


class ValidationResults:
    
    def __init__(self):
        self.hostName = None
        self.connection_error = False
        self.no_certificate = False
        self.wrong_certificate = False
        self.wrong_host = False
        self.certificate_expired = False
        self.expiration_date = None
        self.unknown_error = False
        self.inner_exception = None
        self.dayLeft = None
        self.issuer = None
        
    def __str__(self):
        return """
Hostname:           \t%s
Connection error:\t%s
No certificate:\t\t%s
Wrong certificate:\t%s
Wrong host:\t\t%s
Certificate expired:\t%s
Expiration date:\t%s
Unknown error:\t\t%s
Inner exception:\t%s
Day Left:       \t%s
Issuer:             \t%s

        """ % (self.hostName,
               self.connection_error,
        self.no_certificate,
        self.wrong_certificate,
        self.wrong_host,
        self.certificate_expired,
        self.expiration_date,
        self.unknown_error,
        self.inner_exception,
        self.dayLeft,
        self.issuer)
    
class Validator:
    
    numericIpMatch = re.compile('^[0-9]+(\.[0-9]+)*$')
    valid_hostname = False
    
    def __init__(self):
        pass
        
    def __call__(self, hostname, get_cert_from, port):
        val_results = ValidationResults()
        val_results.hostName = hostname
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        cxt = SSL.Context()
        cxt.set_verify(SSL.verify_none, depth=1)

        SSL.Connection.clientPostConnectionCheck = None # we'll verify things later manually!

        try:
            c = SSL.Connection(cxt, sock)
            c.connect((get_cert_from, port))
            cert = c.get_peer_cert()
        except Exception, e:
            # socket connection
            val_results.connection_error = True
            val_results.inner_exception = e
            return val_results
            
        # NoCertificate WrongCertificate WrongHost ValueError
        try:
            c = SSL.Checker.Checker(hostname)
            c(cert)
        except NoCertificate:
            val_results.no_certificate = True
        except WrongCertificate:
            val_results.wrong_certificate = True
        except WrongHost:
            val_results.wrong_host = True
        except Exception, e:
            val_results.unknown_error = True
            val_results.inner_exception = e
            
        cur_date = datetime.now()
        exp_date = cert.get_not_after().get_datetime()
        exp_date = datetime.date(exp_date)
        cur_date= datetime.date(cur_date)
        days_to_expire = (exp_date - cur_date).days
        
        if days_to_expire < 0:
            val_results.certificate_expired = True
       
        val_results.dayLeft = str(days_to_expire)

        val_results.expiration_date = cert.get_not_after().get_datetime()
        val_results.issuer = cert.get_issuer().organizationName
        return val_results

if __name__ == '__main__':
    with open('../../googletop1000april2010.csv','rb') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if row[0] != "Site":
                get_cert_from = "www." + row[0]
                hostname = row[0]
                port = 443
                v = Validator()
                print v(hostname, get_cert_from, port)