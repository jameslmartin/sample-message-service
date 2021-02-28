## Create Message entities for conversations

This endpoint creates Message entities against a PostgreSQL database. This is a toy API written for Guild.

```plaintext
POST /message
```

Supported attributes:

| Attribute   | Type     | Required | Description           |
|:------------|:---------|:---------|:----------------------|
| `sender`    | string   | yes      | The user sending the message |
| `recipient` | string   | yes      | The user receiving the message |
| `message`   | string   | yes      | The content of the message being sent |

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
Example response:

```json
{
  "Message saved with id: <uuid>"    
}
```
