# API DOCUMENTATION:
Top level API endpoint: https://ifrc-sampling.azurewebsites.net/api/

## Simple Random Sampling API

This API calculates the minimum sample size required for a simple random survey based on user-defined parameters.

### Endpoint

POST /simple-random/

### Request Body

The request body must be a JSON object containing the following fields:
- margin_of_error (required, float): The maximum acceptable difference between the true population value and the sample estimate.
- confidence_level (required, float): The desired level of confidence that the sample estimate will fall within the margin of error.
- non_response_rate (required, float): The estimated proportion of respondents who will not provide usable data.
subgroups (required, list): A list of dictionaries representing subgroups in the population, each with the following fields: 
- households (optional, int): The number of households in the population. If not provided, the sample size will be calculated based on individuals.
individuals (optional, int): The number of individuals in the population. If not provided, the sample size will be calculated based on households.

### Response

If the request is successful, the API will return a JSON object with the following fields:
- status (string): "success" if the calculation was successful, "error" otherwise.
- sample_size (int): The minimum sample size required to achieve the desired margin of error and confidence level.


If an error occurs, the API will return a JSON object with the following fields:
- status (string): "error".
- error_message (string): A message describing the error.

### Example(1): 
(Generated using postman)

- Request
POST /simple-random/<br>
Content-Type: application/json
```
{
    "margin_of_error": 5,
    "confidence_level": 95,
    "non_response_rate": 0,
    "subgroups": 0,
    "households": 0,
    "individuals": 100
}
```

- Response
HTTP/1.1 200 OK<br>
Content-Type: application/json
```
{
    "status": "success",
    "sample_size": {
        "total": 80
    }
}
```

## Systematic Random Sampling API

This API calculates the intervals on the sample size required for a survey based on user-defined parameters.

### Endpoint

POST /systematic-random/

### Request Body

If the request is successful, the API will return a JSON object with the following fields:
- status (string): "success" if the calculation was successful, "error" otherwise.
- intervals (int): The intervals or the step count on the sample size required to achieve the desired margin of error and confidence level.
If an error occurs, the API will return a JSON object with the following fields:
- status (string): "error".
- error_message (string): A message describing the error.

### Response
If the request is successful, the API will return a JSON object with the following fields:
- status (string): "success" if the calculation was successful, "error" otherwise.
- units (list): The randomly generated time-location units to sample to achieve the desired margin of error and confidence level.
If an error occurs, the API will return a JSON object with the following fields:
- status (string): "error".
- error_message (string): A message describing the error.


### Example(2): 
(Generated using postman)<br>
Format: Raw - JSON

- Request
POST /time-location/
Content-Type: application/json
```
{
    "margin_of_error": 5,
    "confidence_level": 95,
    "non_response_rate": 0,
    "households": 0,
    "individuals": 100,
    "locations": 4,
    "days": 3, 
    "interviews_per_session": 10
}
```

- Response
HTTP/1.1 200 OK<br>
Content-Type: application/json
```
    "status": "success",
    "units": [
        {
            "Location 1": [
                {
                    "Day 2": [
                        "morning"
                    ]
                },
                {
                    "Day 3": [
                        "morning"
                    ]
                }
            ]
        },
        {
            "Location 2": [
                {
                    "Day 1": [
                        "morning"
                    ]
                },
                {
                    "Day 3": [
                        "morning"
                    ]
                }
            ]
        },
        {
            "Location 3": [
                {
                    "Day 1": [
                        "evening"
                    ]
                },
                {
                    "Day 2": [
                        "morning"
                    ]
                }
            ]
        },
        {
            "Location 4": [
                {
                    "Day 1": [
                        "evening"
                    ]
                },
                {
                    "Day 3": [
                        "evening"
                    ]
                }
            ]
        }
    ]
}

```

## Time-Location Sample Size API

This API generates randomly selected time-location units from a sample size for a survey based on user-defined parameters.

### Endpoint

POST /time-location/

### Request Body

The request body must be a JSON object containing the following fields:
- margin_of_error (required, float): The maximum acceptable difference between the true population value and the sample estimate.
- confidence_level (required, float): The desired level of confidence that the sample estimate will fall within the margin of error.
- non_response_rate (required, float): The estimated proportion of respondents who will not provide usable data.
subgroups (required, list): A list of dictionaries representing subgroups in the population, each with the following fields: 
- households (optional, int): The number of households in the population. If not provided, the sample size will be calculated based on individuals.
- individuals (optional, int): The number of individuals in the population. If not provided, the sample size will be calculated based on households.
- Locations (required,int) : The number of locations to sample.
- Days(required,int)  : The number of days the sampling can take place
Interviews_per_session (required,int): The number of interviews per session or per unit. 


### Response

If the request is successful, the API will return a JSON object with the following fields:
- status (string): "success" if the calculation was successful, "error" otherwise.
- intervals (int): The intervals or the step count on the sample size required to achieve the desired margin of error and confidence level.
If an error occurs, the API will return a JSON object with the following fields:
- status (string): "error".
- error_message (string): A message describing the error.


### Example(3): 
(Generated using postman)

- Request
POST /systematic-random/<br>
Content-Type: application/json
```
{
    "margin_of_error": 5,
    "confidence_level": 95,
    "non_response_rate": 0,
    "subgroups": null,
    "households": 0,
    "individuals": 100
}
```

- Response
HTTP/1.1 200 OK
Content-Type: application/json
```
{
    "status": "success",
    "intervals": {
        "total": 2
    }
}
```

## Cluster Random Sampling API

This API generates randomly selected cluster units from a sample size for a survey based on user-defined parameters.

### Endpoint

POST /cluster-random/

### Request Body

The request body must be a JSON object containing the following fields:
- margin_of_error (required, float): The maximum acceptable difference between the true population value and the sample estimate.
- confidence_level (required, float): The desired level of confidence that the sample estimate will fall within the margin of error.
- Communities (required,list): The list of dictionaries which contains the community’s name and its respective population size. 


### Response

If the request is successful, the API will return a JSON object with the following fields:
- status (string): "success" if the calculation was successful, "error" otherwise.
- units (list): The randomly generated time-location units to sample to achieve the desired margin of error and confidence level.
If an error occurs, the API will return a JSON object with the following fields:
- status (string): "error".
- error_message (string): A message describing the error.



### Example(4): 
(Generated using postman)<br>
Format: Raw - JSON

- Request
POST /cluster-random/<br>
Content-Type: application/json
```
{
    "margin_of_error": 5,
    "confidence_level": 95,
    "communities": [{"name":"sg1","size":1500},{"name":"sg2","size":2000},{"name":"sg3","size":2500}]
} 
```

- Response
HTTP/1.1 200 OK
Content-Type: application/json
```
{
    "status": "success",
    "clusters": {
        "sg1": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ],
        "sg2": [
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20
        ],
        "sg3": [
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30
        ]
    }
}
```


