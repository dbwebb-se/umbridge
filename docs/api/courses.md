## Content

1. Get courses
2. Add a new course
3. Update a course
4. Delete a course

Back to [README](../README.md)


# 1. Get courses

Fetches all courses

**URL** : `/courses`

**Method** : `GET`

**Optional query parameters**:  
| Param Name     | What                                |
|:---------------|:------------------------------------|
| `?id`          | The course id                       |
| `?name`        | The course name                     |
| `?active`      | It the course is active or not      |


**Auth required** : YES  
**Header**: `{ 'Authorization': 'Basic {credentials}' }`

## Success Response

**Code** : `200 OK`

**Content**

```json
{
    "courses":
        [
            {
                "id": 2015,
                "name": "python",
                "active": 1
            },
            {
                "id": 2168,
                "name": "htmlphp",
                "active": 0
            }
        ]
}
```

## Incorrect Response

If the wrong query parametes are given, unatherized or a server error appears.

**Code**: `[400, 401, 500]`

**Content examples**

```json
{
    "message": "{Error message}"
}
```


# 2. Add a new course

Adds a new course to the database

**URL** : `/courses`

**Method** : `POST`

**Data** :
```json
{
    "id": "{The Canvas Course Id}",
    "name": "{The Course name it should be mapped to}",
    "active": "{(Optional), If the course is active or not, defaults to `1` (True), `0` if False}"
}
```


**Auth required** : YES  
**Header**: `{ 'Authorization': 'Basic {credentials}' }`

## Success Response

**Code** : `201 CREATED`

**Content**
Returns the newly created object.

```json
{
    "course":
        {
            "id": 2015,
            "name": "python",
            "active": 1
        }
}
```

## Incorrect Response

If the course id exsists, given the wrong data, unatherized or a server error appears.

**Code**: `[400, 401, 500]`

**Content examples**

```json
{
    "message": "{Error message}"
}
```





# 3. Update a course

Uppdates an existing course

**URL** : `/courses`

**Method** : `PUT`

**Data** :
```json
{
    "id": "{The Canvas Course Id}",
    "name": "{(Optional), The Course name it should be mapped to}",
    "active": "{(Optional), If the course is active or not}"
}
```


**Auth required** : YES  
**Header**: `{ 'Authorization': 'Basic {credentials}' }`

## Success Response

**Code** : `200 OK`

**Content**
Returns the updated object.

```json
{
    "course":
        {
            "id": 2015,
            "name": "js",
            "active": 0
        }
}
```

## Incorrect Response

If the course id does not exsist, unatherized or a server error appears.

**Code**: `[400, 401, 500]`

**Content examples**

```json
{
    "message": "{Error message}"
}
```



# 4. Delete a course

Uppdates an existing course

**URL** : `/courses`

**Method** : `DELETE`

**Data** :
```json
{
    "id": "{The Canvas Course Id}"
}
```


**Auth required** : YES  
**Header**: `{ 'Authorization': 'Basic {credentials}' }`

## Success Response

**Code** : `200 OK`

**Content**
Returns a success message with the deleted objects string representation.

```json
{
    "message": "{Course 2015, 'js', Active: False} has been deleted"
}
```

## Incorrect Response

If the course id does not exsist, unatherized or a server error appears.

**Code**: `[400, 401, 500]`

**Content examples**

```json
{
    "message": "{Error message}"
}
```