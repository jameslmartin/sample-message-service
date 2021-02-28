## Fetch Message entities for conversations

This endpoint fetches Message entities against a PostgreSQL database. This is a toy API written for Guild.

```plaintext
GET /message?sender=<sender>&recipient=<recipient>
```

Supported attributes:

| Attribute   | Type     | Required | Description           |
|:------------|:---------|:---------|:----------------------|
| `sender`    | string   | no      | The user sending the message |
| `recipient` | string   | no      | The user receiving the message |

Example request (assuming the service is available at localhost):

```shell
curl --request POST \
--url "http://localhost:8080/message" \
--header "content-type: application/json" \
--data '{
  "sender": "james",
  "recipient": "jay",
  "message": "hello world!"
}'
```

Example response:

```json
[
    {
        "sender": "james",
        "recipient": "joe",
        "message": "hello world!"
    },
    {
        "sender": "james",
        "recipient": "joe",
        "message": "hello world!"
    }
]
```