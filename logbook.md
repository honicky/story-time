# Logbook

## 2023-12-2 and 2023-12-3

* Use midjourney to generate images
  * https://midlibrary.io/ has a list of prompts to get specific artists and sytles
  * TODO: pick one or styles corresponding to each tone and maybe story type

* Add story-viz
  * show the images plus prompts
  * TODO: select the best images from all of the generated images
  * TODO: regenerate the images
  * TODO: alter the prompts
  * TODO: regereate a section of the story
  * TODO: save the story metatdata to a library
  * TODO: cycle through today's story, pick a new story once per day (only new stories?  From the library?)

* other ideas
  * Get feedback from user
    * like a story - add it to my library
    * dislike or flag an image
  * app that can build a story with a kid interactively
    * allow them to prompt for changes to the story
    * allow them to regenerate images (similar to story viz)
    * watch the camera and interact via voice
      * notice when new people are there, have a coversation with them
      * co-create a story
      * read the story to the kid
    * share your stories with the community
      * popular stories give reinforcement to story quality
    


## 2023-11-24 and 2023-11-25

 * use 

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
