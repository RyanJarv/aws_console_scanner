# aws_console_scanner

This is a proxy that looks for AWS related requests and outputs info about the request in a JSON format under ./output.

# Goal

To find undocumented API's that are used by the webconsole, similar to the [CodeStar API](https://rhinosecuritylabs.com/aws/escalating-aws-iam-privileges-undocumented-codestar-api/).

# Setup

```
docker-compose up
```

After the proxy is started it will be listening on localhost:8080 for HTTP CONNECT requests. You'll want to set up your browser to proxy through this.
