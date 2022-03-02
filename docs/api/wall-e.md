## Content

1. [Get Submissions](#get-submissions)
2. [Get already graded submissions](#get-graded-submissions)
3. [Grade Submissions](#grade-submissions)

Back to [README](../README.md)


# <a id="get-submissions"></a> 1. Get Submissions

Fetches all submissions that requires grading from Canvas and stores the database.

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



# <a id="get-graded-submissions"></a> 2. Get already graded submissions

Fetches all submissions that have been graded, from Canvas and stores the database.

**URL** : `/re-fetch-graded-submissions`

**Method** : `[POST]`

**DATA** :
```json
{
    "course": "{The Canvas Course name}",
    "assignment": "{The assignment name it should re-fetch for}",
}
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



# <a id="grade-submissions"></a> 3. Grade Submissions

Gets all the tested submissions from the database and reports them to Canvas. If know error code is encountered during testing, the grade U will be sent to Canvas.

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