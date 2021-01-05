# My Project
## Resourceful
### Planets
#### Attributes:
* Id (Integer)
* Name (Text)
* Shape (Text)
* Color (Text)
* Rings (Integer)

## Schema
```
### CREATE TABLE planets (
### id INTEGER PRIMARY KEY,
### name TEXT,
### shape TEXT,
### color TEXT,
### rings INTEGER);
```

Name | Method | Path
-----|--------|-----
Retrieve planet collection | GET | /planets
Retrieve planet member | GET | /planets/id
Create planet member | POST | /planets
Update planet member | PUT | /planets/id
Delete planet member | DELETE | /planets/id

### Users
#### Attributes:
* Id (Integer)
* First Name (Text)
* Last Name (Text)
* Email (Text)
* Password (Integer)

## Schema
```
### CREATE TABLE planets (
### id INTEGER PRIMARY KEY,
### fistName TEXT,
### lastName TEXT,
### email TEXT,
### password INTEGER);
```

Name | Method | Path
-----|--------|-----
Create user member | POST | /users
Create session | POST | /sessions

### Bcrypt is used to encrypt and verify password