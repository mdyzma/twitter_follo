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


:: 
1. GET verify_cred (me)
2. count_#_followers
3. if lower than 5000: GET list followers ids named list_of_ids

4. Estimate number of gets/time (round up)

4. while number of gets:
        4.1. if number of gets less than 15:
            4.1.1. GET list of followers ids from coursor page
            4.1.2. update coursor
            4.1.3. return to point 4.1.1
        4.2. if number of gets more than 15 (long data aquisition):
            4.2.1. get list of followers ids from coursor page
            4.2.2. update coursor
            4.2.3. sleep 1 min
            4.2.4. return to point 4.2.1

5. for item in 

{4: {1: [89,4], 2: [454]}, 6768787: {1: [, 6, 7]}



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



The list doesn’t contain my direct (1st line) followers

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

One thing you might find troublesome is Twitter limiting API requests rate. This is part of the task, to decide what to do in such situation. Feel free to think through different solutions, but pick and implement only one (we will discuss them though).
