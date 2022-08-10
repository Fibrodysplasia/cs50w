## [Harvard's cs50w: Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/)

### Completed Projects:
Click a link to be taken to ReadMe section. Click the links in the sections to be taken to the relevant file in the repo.

1. [Wiki](https://github.com/Fibrodysplasia/cs50w#wiki)
2. [Commerce](https://github.com/Fibrodysplasia/cs50w#commerce)
3. [Mail](https://github.com/Fibrodysplasia/cs50w#mail)

***

## Wiki 
[Click Here](https://github.com/Fibrodysplasia/cs50w/tree/main/wiki) for the folder.


[Click Here](https://github.com/Fibrodysplasia/cs50w/blob/main/wiki/encyclopedia/views.py) for views.py


### Specification
Complete the implementation of your Wiki encyclopedia. You must fulfill the following requirements:

1. [**Entry Page:**](https://github.com/Fibrodysplasia/cs50w/blob/main/wiki/encyclopedia/templates/encyclopedia/entry.html) Visiting `/wiki/TITLE`, where `TITLE` is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
    * The view should get the content of the encyclopedia entry by calling the appropriate util function.
    * If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
    * If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.

2. [**Index Page:**](https://github.com/Fibrodysplasia/cs50w/blob/main/wiki/encyclopedia/templates/encyclopedia/index.html) Update index.html such that, instead of merely listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page.

3. [**Search:**](https://github.com/Fibrodysplasia/cs50w/blob/main/wiki/encyclopedia/templates/encyclopedia/search.html) Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
    * If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
    * If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were ytho, then Python should appear in the search results.
    * Clicking on any of the entry names on the search results page should take the user to that entry’s page.

4. [**New Page:**](https://github.com/Fibrodysplasia/cs50w/blob/main/wiki/encyclopedia/templates/encyclopedia/create.html) Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.
    * Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
    * Users should be able to click a button to save their new page.
    * When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
    * Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
 
 5. [**Edit Page:**](https://github.com/Fibrodysplasia/cs50w/blob/main/wiki/encyclopedia/templates/encyclopedia/edit.html) On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
    * The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
    * The user should be able to click a button to save the changes made to the entry.
Once the entry is saved, the user should be redirected back to that entry’s page.

6. [**Random Page:**](https://github.com/Fibrodysplasia/cs50w/blob/main/wiki/encyclopedia/views.py) Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.

7. **Markdown to HTML Conversion:** On each entry’s page, any Markdown content in the entry file should be converted to HTML before being displayed to the user. You may use the python-markdown2 package to perform this conversion, installable via pip3 install markdown2.

***

## Commerce 
[Click Here](https://github.com/Fibrodysplasia/cs50w/tree/main/commerce) for the folder.


[Click Here](https://github.com/Fibrodysplasia/cs50w/blob/main/commerce/auctions/views.py) for views.py


### Specification
Complete the implementation of your auction site. You must fulfill the following requirements:

1. [**Models:**](https://github.com/Fibrodysplasia/cs50w/blob/main/commerce/auctions/models.py) Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.

2. [**Create Listing:**](https://github.com/Fibrodysplasia/cs50w/blob/main/commerce/auctions/templates/auctions/new_listing.html) Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

3. [**Active Listings Page:**](https://github.com/Fibrodysplasia/cs50w/blob/main/commerce/auctions/templates/auctions/index.html) The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).

4. [**Listing Page:**](https://github.com/Fibrodysplasia/cs50w/blob/main/commerce/auctions/templates/auctions/listing.html) Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
    * If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it
    * If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
    * If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
    * If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
    * Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.

5. [**Watchlist:**](https://github.com/Fibrodysplasia/cs50w/blob/main/commerce/auctions/templates/auctions/watchlist.html) Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.

6. [**Categories**](https://github.com/Fibrodysplasia/cs50w/blob/main/commerce/auctions/templates/auctions/categories.html) Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

7. [**Django Admin Interface**](https://github.com/Fibrodysplasia/cs50w/blob/main/commerce/auctions/admin.py) Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.

***

## Mail 
This entire project is in the inbox.js making a SPA to view emails.
[Click Here](https://github.com/Fibrodysplasia/cs50w/blob/main/mail/mail/static/mail/inbox.js) for the inbox.js.


[Click Here]([https://github.com/Fibrodysplasia/cs50w/blob/main/commerce/auctions/views.py](https://github.com/Fibrodysplasia/cs50w/blob/main/mail/mail/views.py)) for views.py


### Specification
Complete the implementation of your auction site. You must fulfill the following requirements:

1. **Send Mail:** When a user submits the email composition form, add JavaScript code to actually send the email.
    * You’ll likely want to make a `POST` request to `/emails`, passing in values for recipients, subject, and body.
    * Once the email has been sent, load the user’s sent mailbox.

2. **Mailbox:** When a user submits the email composition form, add JavaScript code to actually send the email.
    * You’ll likely want to make a `GET` request to `/emails/<mailbox>` to request the emails for a particular mailbox.
    * When a mailbox is visited, the application should first query the API for the latest emails in that mailbox.
    * When a mailbox is visited, the name of the mailbox should appear at the top of the page (this part is done for you).
    * Each email should then be rendered in its own box (e.g. as a <div> with a border) that displays who the email is from, what the subject line is, and the timestamp of the email.
    * If the email is unread, it should appear with a white background. If the email has been read, it should appear with a gray background
   
3. **View Email:** When a user clicks on an email, the user should be taken to a view where they see the content of that email.
    * You'll likely want to make a `GET` request to `/emails/<email_id>` to request the email. 
    * Your application should show the email’s sender, recipients, subject, timestamp, and body.
    * You’ll likely want to add an additional div to inbox.html (in addition to emails-view and compose-view) for displaying the email. Be sure to update your code to hide and show the right views when navigation options are clicked.
    * See the hint in the Hints section about how to add an event listener to an HTML element that you’ve added to the DO
    * Once the email has been clicked on, you should mark the email as read. Recall that you can send a `PUT` request to `/emails/<email_id>` to update whether an email is read or not.
   
4. **Archive and Unarchive:** Allow users to archive and unarchive emails that they have received.
    * When viewing an Inbox email, the user should be presented with a button that lets them archive the email. When viewing an Archive email, the user should be presented with a button that lets them unarchive the email. This requirement does not apply to emails in the Sent mailbox.
    * Recall that you can send a `PUT` request to `/emails/<email_id>` to mark an email as archived or unarchived.
    * Once an email has been archived or unarchived, load the user’s inbox.

5. **Reply:** Allow users to reply to an email.
    * When viewing an email, the user should be presented with a “Reply” button that lets them reply to the email.
    * When the user clicks the “Reply” button, they should be taken to the email composition form.
    * Pre-fill the composition form with the recipient field set to whoever sent the original email.
    * Pre-fill the subject line. If the original email had a subject line of foo, the new subject line should be Re: foo. (If the subject line already begins with Re: , no need to add it again.)
    * Pre-fill the body of the email with a line like "On Jan 1 2020, 12:00 AM foo@example.com wrote:" followed by the original text of the email.
