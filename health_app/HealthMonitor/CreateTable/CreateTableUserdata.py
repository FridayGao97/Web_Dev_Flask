# Run this script to create 'userdata' table in DynamoDB

import boto3

def create_userdata_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.create_table(
        TableName='userdata',
        KeySchema=[
            {
                'AttributeName': 'time',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'email',
                'KeyType': 'RANGE'  # Sort key
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': "UserNameIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'user_name'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "AgeIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'age'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "GenderIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'gender'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "WeightIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'weight'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "HeightIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'height'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "WaistIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'waist'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "HipIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'hip'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "HeartRateIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'heart_rate'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "BloodPressureIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'blood_pressure'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "StepIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'step'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "SleepIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'sleep'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "WaterIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'water'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "VegetableIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'vegetable'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "BMIIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'BMI'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "WHRIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'WHR'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
            {
                'IndexName': "CalorieIndex",
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'calorie'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'email'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'user_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'age',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'gender',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'weight',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'height',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'waist',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'hip',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'heart_rate',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'blood_pressure',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'step',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'sleep',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'water',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'vegetable',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'BMI',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'WHR',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'calorie',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 60,
            'WriteCapacityUnits': 60
        }
    )
    return table


if __name__ == '__main__':
    userdata_table = create_userdata_table()
    print("Table status:", userdata_table.table_status)