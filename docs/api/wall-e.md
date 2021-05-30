## Content
1. Get Submissions
2. Grade Submissions

Back to [README](../README.md)

# 1. Get Submissions
Fetches all submissions that requires drading from Canvas and stores the database.

**URL** : `/fetch-submissions`

**Method** : `[GET, POST]`

**DATA** :
```json
{}
```

**Auth required** : YES
**Header**: `{ 'Authorization': 'Basic {credentials}' }`

## Success Response

**Code** : `201 Created`

**Content**

```json
{
    "message": "Successfully fetched new assignments from canvas"
}
```


   
# 2. Grade Submissions
Gets all the tested submissions from the database and reports them to Canvas.

**URL** : `/wall-e/grade`

**Method** : `[GET, POST]`

**DATA** :
```json
{}
```


**Auth required** : YES
**Header**: `{ 'Authorization': 'Basic {credentials}' }`

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "message": "Canvas has been updated with the new grades."
}
```


## Incorrect Response
The server might have a penging request to grade a submission. To avoid conflicts this will cancel the request.

**Code**: `423 Locked`

**Content examples**

```json
{
    "message": "Wall-E is busy, try again in a few minutes"
}
```