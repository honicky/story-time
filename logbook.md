# Logbook


## 2023-10-28

* installed the `act` github extension so that I can run github actions locally:
    
    ```
    gh extension install https://github.com/nektos/gh-act
    ```
    
    now I can do `gh act ...`
* installed AWS keys in project, plus `.secrets` and `.vars` files in codespace
* using 
    ```
    gh act -s GITHUB_TOKEN=${GITHUB_TOKEN} --secret-file .secrets --var-file .vars
    ```
    to test deployment
* trivial change to trigger github action

## 2023-10-06
- setting up cloudfront to serve CORS.  Set up a Behavior in CloudFront, and also a policy in S3.  Neither worked... maybe I need to wait for the S3 setting propagate?
- checking the settings in S3, also there is an issue with S3 mime type still: I thouhgt I fixed that

## 2023-10-05
- set up cloudfront to serve HTTPS from S3 bucket
- attempted to set up DNS from CloudFlare, probably need to transfer the domain to Route53
