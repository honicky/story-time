# Logbook

## Ideas

  * Get feedback from user
    * like a story - add it to my library
    * share stories with other users
    * popular stories
    * dislike or flag an image
  * Create hardcopies with integration to on-demand publishers
    * Author gets a cut of revenue
  * Artists can participate by providing art to fine tune on
    * they get a cut of revenue from stories that generate revenue / views
  * Artists can create art work for a popular story
    * I will create art work if X number of people pre-purchase
  * app that can build a story interactively
    * allow them to prompt for changes to the story
    * allow them to regenerate images (similar to story viz)
    * share your stories with the community
      * popular stories give reinforcement to story quality
  * interactive app
    * read the story to the kid
    * watch the camera and interact via voice
    * notice when new people are there, have a coversation with them
    * co-create a story live

## 2023-01-23 to 2023-01-25

* move story-viz to standalone fastapi, for deployment to google app engine
* add JWT authentication
* add .env files for local development outside of code spaces
* update openapi version to 1.0

## 2023-12-28
* fixed the beam_api.py:handler:publish endpoint to correctly decode and push
`latest_story.json`

## 2023-12-27

* added `beam_wrapper.sh` script to `story-viz/backend` because `beam` doesn't play nice with
  symlinks.  This script sync the `lib` directory to inside of the beam app. Add it to .gitignore
* backend now successfully deploys
* Updated frontend to read from the user's latest_story.json file
* Updated frontend layout to include the text of the story on the right side of the page

## 2023-12-22

* create a `staging` branch that we can use to try out new versions of the slideshow

## 2023-12-20

* Store generated stories in MongoDb
* Create a story-viz tool to select images for the story and publish them
  * will also allow us to change prompts, regenerate, etc 

## 2023-12-10

* Add class to prompt SDXL on Replicate
  * looks like midlibrary prompts work in regular SDXL too

## 2023-12-2 and 2023-12-3

* Use midjourney to generate images
  * SDXL lora was not showing people
    * prompt too long?
    * catastrophic forgetting
  * SDXL has lots of wierd artifacts
    * we can address this by adding a human in the loop
  * As we get preference data, we can use the stories to generate SDXL Loras specific
    to each style we are intersted in.
  * https://midlibrary.io/ has a list of prompts to get specific artists and sytles
  * TODO: pick one or styles corresponding to each tone and maybe story type

* Next steps:
  * store generated stories in mongodb instead of S3
  * use a flask app to get started.  Maybe use Google free tier to serve it, or 

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
