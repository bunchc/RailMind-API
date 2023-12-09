# RailMinds API

RailMinds API is a RESTful interface for controlling model trains and accessories. It provides endpoints to manage train speeds, directions, and accessory activation.

## API Documentation

### Get a list of available trains

```http
GET /trains
```

Retrieve a list of available trains.

### Set the speed of a specific train

```http
PUT /trains/{trainId}/speed?speed=50
```

Set the speed of a specific train identified by `{trainId}`. The `speed` parameter should be a value between 0 and 100.

### Change the direction of a specific train

```http
PUT /trains/{trainId}/direction?direction=forward
```

Change the direction of a specific train identified by `{trainId}`. The `direction` parameter should be either "forward" or "reverse".

### Get a list of available accessories

```http
GET /accessories
```

Retrieve a list of available accessories.

### Activate a specific accessory

```http
PUT /accessories/{accessoryId}/activate
```

Activate a specific accessory identified by `{accessoryId}`.

### Deactivate a specific accessory

```http
PUT /accessories/{accessoryId}/deactivate
```

Deactivate a specific accessory identified by `{accessoryId}`.

## Example Usage

```bash
curl -X PUT http://api.example.com/trains/1/speed?speed=75 \
  -H "Content-Type: application/json" \
  -d '{"speed": 75}'
```

This example sets the speed of the train with ID 1 to 75.

This diagram represents the basic interactions with the RailMinds API.
