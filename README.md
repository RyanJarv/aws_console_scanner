# aws_console_scanner

This is a proxy that looks for AWS related requests and outputs info about the request in a JSON format under ./output.

# Goal

To find undocumented API's that are used by the webconsole, similar to the [CodeStar API](https://rhinosecuritylabs.com/aws/escalating-aws-iam-privileges-undocumented-codestar-api/).

# Setup

```
export CERT_PASSWORD=<password to use to encrypt SSL certs stored in ~/.mitmproxy>
export AKITA_SERVICE=<akita service name>
export AKITA_API_KEY_ID=<akita api key id>
export AKITA_API_KEY_SECRET=<akita api key secret>
docker-compose up
```

After the proxy is started it will be listening on localhost:8080 for HTTP CONNECT requests. You'll want to set up your browser to proxy requests through this.

You can use [FoxyProxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/) to manage proxy configurations in FireFox if you want.

# Install mitmproxy cert

When the proxy is set up navigate to [http://mitm.it/](http://mitm.it/), this will have download links and instructions if the proxy is working.


