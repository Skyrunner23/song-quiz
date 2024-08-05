# Getting HTTPS enabled on Apache2 on Ubuntu 22.04

## Helpful documentation

Remember to

```
sudo apache2ctl configtest
```

to check config file syntax before having Apace2 reload/restart.

Note the helpful file at

/var/www/html/index.html

This is displayed for http://34.217.92.131/

"The configuration system is fully documented in /usr/share/doc/apache2/README.Debian.gz. Refer to this for the full documentation. Documentation for the web server itself can be found by accessing the manual if the apache2-doc package was installed on this server. "

This appears to also be available at

https://github.com/dcmorton/apache24-ubuntu/blob/master/debian/apache2.README.Debian

"Configuration files in the mods-enabled/, conf-enabled/ and sites-enabled/ directories contain particular configuration snippets which manage modules, global configuration fragments, or virtual host configurations, respectively.
They are activated by symlinking available configuration files from their respective *-available/ counterparts. These should be managed by using our helpers a2enmod, a2dismod, a2ensite, a2dissite, and a2enconf, a2disconf . See their respective man pages for detailed information.
The binary is called apache2 and is managed using systemd, so to start/stop the service use systemctl start apache2 and systemctl stop apache2, and use systemctl status apache2 and journalctl -u apache2 to check status. system and apache2ctl can also be used for service management if desired. Calling /usr/bin/apache2 directly will not work with the default configuration. "

The following section is from the Apache2 documentation:

```quote
SSL
===

Enabling SSL
------------

To enable SSL, type (as user root):

	a2ensite default-ssl
	a2enmod ssl

If you want to use self-signed certificates, you should install the ssl-cert
package (see below). Otherwise, just adjust the SSLCertificateKeyFile and
SSLCertificateFile directives in '/etc/apache2/sites-available/default-ssl.conf'
to point to your SSL certificate. Then restart apache:

	service apache2 restart

The SSL key file should only be readable by root; the certificate file may be
globally readable. These files are read by the Apache parent process which runs
as root, and it is therefore not necessary to make the files readable by the
www-data user.

Creating self-signed certificates
---------------------------------

If you install the ssl-cert package, a self-signed certificate will be
automatically created using the hostname currently configured on your computer.
You can recreate that certificate (e.g. after you have changed '/etc/hosts' or
DNS to give the correct hostname) as user root with:

	make-ssl-cert generate-default-snakeoil --force-overwrite

To create more certificates with different host names, you can use

	make-ssl-cert /usr/share/ssl-cert/ssleay.cnf /path/to/cert-file.crt

This will ask you for the hostname and place both SSL key and certificate in
the file '/path/to/cert-file.crt'. Use this file with the SSLCertificateFile
directive in the Apache config (you don't need the SSLCertificateKeyFile in
this case as it also contains the key). The file '/path/to/cert-file.crt'
should only be readable by root. A good directory to use for the additional
certificates/keys is '/etc/ssl/private'.

SSL workaround for MSIE
-----------------------

The SSL workaround for MS Internet Explorer needs to be added to your SSL
VirtualHost section (it was previously in ssl.conf but caused keepalive to be
disabled even for non-SSL connections):

	BrowserMatch "MSIE [2-6]" \
		nokeepalive ssl-unclean-shutdown \
		downgrade-1.0 force-response-1.0
	BrowserMatch "MSIE [17-9]" ssl-unclean-shutdown

The default SSL virtual host in '/etc/apache2/sites-available/default-ssl.conf'
already contains this workaround.
```

**For sample Apache2 site configuration:**



## Questions

* Where are the default, self-signed certificates?

SSLCertificateFile    /etc/ssl/certs/ssl-cert-snakeoil.pem
SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key

* In ports.conf, there is a block that opens port 443 ONLY IF ssl_module is active. Is that module active now?

A: No. It should be enabled (see below).

* The Apache2 documentation's SSl section mentions the ssl-cert package. Is it already installed?

A: Using `sudo dpkg --list ssl-cert`, we can see that it is already installed.

* Is there a firewall configured on this machine? Is it passing port 443?

A: 

* What files does the web server need?

From https://eff-certbot.readthedocs.io/en/latest/using.html#where-are-my-certificates, `fullchain.pem` is needed for Apache >= 2.4.8.

```quote
The following files are available:

`privkey.pem`

    Private key for the certificate.

    Warning

    This must be kept secret at all times! Never share it with anyone, including Certbot developers. You cannot put it into a safe, however - your server still needs to access this file in order for SSL/TLS to work.

    Note

    As of Certbot version 0.29.0, private keys for new certificate default to 0600. Any changes to the group mode or group owner (gid) of this file will be preserved on renewals.

    This is what Apache needs for SSLCertificateKeyFile, and Nginx for ssl_certificate_key.

`fullchain.pem`

    All certificates, including server certificate (aka leaf certificate or end-entity certificate). The server certificate is the first one in this file, followed by any intermediates.

    This is what Apache >= 2.4.8 needs for SSLCertificateFile, and what Nginx needs for ssl_certificate.

```

From this, I infer that I need these configuration lines in an Apache2 configuration file:

SSLCertificateKeyFile /etc/letsencrypt/live/lyriquizz.com/privkey.pem
SSLCertificateFile /etc/letsencrypt/live/lyriquizz.com/fullchain.pem

* Is port 443 even open?

A: sudo ufw status shows that ufw is not running.

Runnning from here (https://dnschecker.org/port-scanner.php?query=34.217.92.131) initially showed ports 22 and 80 open, but 21 and 443 timed out. On the Lightsail control panel, Networking tab, IPv4 networking had only port 22 and 80 open. I added a rule for HTTPS (using port 443), and the port scanner now shows that port as open.


## Steps

1. Enable the ssl_conf module:

```
sudo a2enmod ssl_conf
```

2. Create certificates:

I did this with Let's Encrypt's Certbot. It has created the following certificates:

In /etc/letsencrypt/live/lyriquizz.com/:

cert.pem
chain.pem
fullchain.pem
privkey.pem

links to these files in /etc/letsencrypt/archive/lyriquizz.com/ (each suffixed with 1). All of the actual pem files are owned by root:root, with permissions -rw-r-----. (640)

## Test

Created self-signed cert at /etc/ssl/private/self-test.crt

With opened port via Lightsail, this works.

Note the Certbot bug. Workaround is posted at

https://github.com/certbot/certbot/issues/8373#issuecomment-934030469

I'm late to the party but leave this here in case someone needs it. A possible solution to prevent duplication is to wrap the Daemon config into an <IfDefine> directive

#... set up shared vars (optional)

Define wsgi_daemon "my_process"
Define path_django "/path/to/django/app"

#... inside vhost
<VirtualHost *:80> # replace with your condition
    # ...
    <IfDefine !wsgi_init>
        WSGIDaemonProcess ${wsgi_daemon} python-path=${path_django}
        WSGIProcessGroup ${wsgi_daemon}
        Define wsgi_init 1
    </IfDefine>
   # ...
</VirtualHost>

Let me try to rewrite the site conf file...no.

====
Successfully made the change to the site conf file, then had certbot install the certificates. All four addresses are working and properly redirecting to https with no www, even for the API.

Added to /etc/crontab:

echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab

The *now two* site config files have been copied to the GitHub repo.
