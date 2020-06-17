News site.
There are three groups of users on the site - the administrator (moderation of posts approved post is published, rejected by the administrator
post is not published, possibility to publish post without moderation), moderator (possibility to publish posts without moderation), users (publication with moderation only).
On a site there is a moderation of posts - when the user publishes the news it goes to moderation first. 
An unregistered user can't publish news
Registration and authorization by e-mail and password, at registration optional fields: first name, last name, date of birth
Default user group - USER
Validation of mail by separate letter (click on the link to confirm your email address). Sending is implemented asynchronously, using Celery (broker - Redis).
Adding a post - WYSISYG redactor
Possibility to add a comment to the post (notification of the author of the post about the new comment)





