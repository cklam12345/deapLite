$env:OPENSSL_CONF ="C:\Program Files\Common Files\FireDaemon SSL 3\openssl.cnf"
openssl req -x509 -newkey rsa:4096 -keyout cool.key -out cool.pem -days 10000 -nodes