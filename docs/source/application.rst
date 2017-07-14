.. application:

Application description
=======================


SDD Specification
-----------------


There are two stories to implement:
As a user I want to see followers of my followers on a page. Steps:

1. I go to “/” page
2. I see “Connect Twitter account” button
3. I press “Connect Twitter account” button
4. I see Twitter popup, I follow oAuth flow authorizing app
5. I get redirected to “/followers/followers” page
6. I see a list of my “2nd line” followers. Each contains
        - A Twitter handle, like “@madonna”
        - A number of my followers, that this person follows (example, Bob and Rick follow me, Andrew follows both of them, the number is 2).
        - The list doesn’t contain my direct (1st line) followers

As a technical user I want to see followers of my followers as a JSON response
Starting from where last scenario ended
1. I see a URL to JSON endpoint, that displays the list. 
2. I go to the URL (no auth or session required)
3. I see a JSON response, which contains a list of my “2nd line” followers. Each contains:
    - A Twitter handle, like “@madonna”
    - A number of my followers, that this person follows

App should be:
Heroku-deployable (please provide a link to the working deployment in the README)
At least slightly documented
Version controlled 
