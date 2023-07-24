# General requirements:
  1. Microservice arquitecture

  ## Requirements Django:
    1. User registration and logins API
    2. Dashboard API
    3. Security JWT
    4. Multifactor authentification
    5. Data validation and error handling
    6. Database Django ORM
    7. Unit test

  ## Requirements Flask:
    1. WebSocket using Flask-SocketIO for price alerts and broadcast them to connected clients
    2. Error handling and graceful WebSocket connection management
    3. Unit tests to validate the functionality and performance of the WebSocket microservice


# Django structure:
  1. Apps:
    - Dashboard
    - Security: Login, registration, 2FA
  2. API:
    1. Login
    2. Registration
    3. 2FA
    4. Dashboard
  3. Validator
  4. ORM schema:
    1. Username
    2. Password
    3. Email
    4. Google auth

  5. Error handler
  6. Unit test

# Overall Structure
  1. Docker-compose to build all microservices

Notes:
Some tests are from https://github.com/miguelgrinberg/Flask-SocketIO/blob/main/test_socketio.py
2FA with JWT
