# TODO List api
API, made in Django and Django Rest, for creating and maintaining an TODO List.
 
 ## Existing URL's:
 
  - registration/ - POST -> It allows the creation of new users in the system.
  - login/ - POST -> It allows the login of existing users, through username / email and password.
 
  - create_card/: POST -> It allows the creation of new cards, passing information such as name, description and card status. The statuses are defined as "todo", "doing" or "done".
  - update_card/: PATCH -> It allows updating existing cards, passing information such as name, description and card status. The statuses are defined as "todo", "doing" or "done".
  - delete_card/: DELETE -> Allows you to delete existing cards.
  - todo_cards/: GET -> Returns a list of cards that have "todo" status
  - doing_cards/: GET -> Returns a list of cards that have "doing" status
  - done_cards/: GET -> -> Returns a list of cards that have "done" status

## Setting up the environment:

 ### To configure the environment and run the application in a venv, the project has a requirements.txt file with all the necessary dependencies.
 
 
## Authentication:

 ### If you want to use an application such as Postman or Insomnia to make requests, or even via curl, you must send a field in the request header called Authorization, with the prefix JWT and the authentication token. The token must be returned when logging in or registering in the application.
 
 Example: Authorization: JWT <user_token>
