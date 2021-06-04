## Content

1. [Test Submissions](#test-submissions)
2. [Reset the database](#reset) *(Temporary)*

Back to [README](../README.md)


# <a id="test-submissions"></a> 1. Test Submissions

Fetches all ungraded submissions from the database and test them.

**URL** : `/eve/grade`

**Method** : `[GET, POST]`

**DATA** :
```json
{}
```

**Auth required** : YES  
**Header**: `{ 'Authorization': 'Basic {credentials}' }`

## Success Response

**Code** : `200 OK`

**Content**

```json
{
    "message": "All new assignments has been corrected"
}
```

## Incorrect Response

The server might have a penging request to grade a submission. To avoid conflicts this will cancel the request.

**Code**: `423 Locked`

**Content examples**

```json
{
    "message": "Eve is busy, try again in a few minutes"
}
```

   
# <a id="reset"></a> 2. Reset the database (Temporary)

Resets the database, adds a user to login as, adds the test course and resets the submission table.

**URL** : `/eve/reset`

**Method** : `[GET, POST]`

**DATA** :
```json
{}
```


**Auth required** : NO

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "message": "Submission and Course table has been reset with dummy data"
}
```

## Incorrect Response

The server might have a penging request to grade a submission. To avoid conflicts this will cancel the request.

**Code**: `423 Locked`

**Content examples**

```json
{
    "message": "Eve is busy, try again in a few minutes"
}
```