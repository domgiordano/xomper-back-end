
import boto3
from datetime import datetime
from lambdas.common.constants import AWS_DEFAULT_REGION, DYNAMODB_KMS_ALIAS, LOGGER

log = LOGGER.get_logger(__file__)

dynamodb_res = boto3.resource("dynamodb", region_name=AWS_DEFAULT_REGION)
dynamodb_client = boto3.client("dynamodb", region_name=AWS_DEFAULT_REGION)
kms_res = boto3.client("kms")

HANDLER = 'dynamo_helpers'

# Performs full table scan, and fetches ALL data from table in pages...
def full_table_scan(table_name, **kwargs):
    try:
        table = dynamodb_res.Table(table_name)
        response = table.scan()
        data = response['Items']  # We've got our data now!
        while 'LastEvaluatedKey' in response:  # If we have this field in response...
            # It tells us where we left off, and signifies there's more data to fetch in "pages" after this particular key.
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])  # Add more data as each "page" comes in until we're done (LastEvaluatedKey gone)

        # If we passed in these optional keyword args, let's...
        # SORT the data...default is ascending order even if there are no sort args present.
        if 'attribute_name_to_sort_by' in kwargs:
            is_reverse = kwargs['is_reverse'] if 'is_reverse' in kwargs else False
            data = sorted(data, key=lambda i: i[kwargs['attribute_name_to_sort_by']], reverse=is_reverse)

        return data
    except Exception as err:
        log.error(f"Dynamodb Full Table Scan: {err}")
        raise Exception(f"Dynamodb Full Table Scan: {err}")
def table_scan_by_ids(table_name, key, ids, goal_filter, **kwargs):
    try:
        table = dynamodb_res.Table(table_name)
        keys = {
            table.name: {
                'Keys': [{key: id} for id in ids]
            }
        }

        response = dynamodb_res.batch_get_item(RequestItems=keys)
        data = response['Responses'][table.name]

        for offering in data:
            if len(offering['rank_dict']) > 0:
                offering['rank'] = offering['rank_dict'][goal_filter]

        # Sort data
        if 'attribute_name_to_sort_by' in kwargs:
            is_reverse = kwargs['is_reverse'] if 'is_reverse' in kwargs else False
            data = sorted(data, key=lambda i: i[kwargs['attribute_name_to_sort_by']], reverse=is_reverse)

        return data
    except Exception as err:
        log.error(f"Dynamodb Table Scan by IDs: {err}")
        raise Exception(f"Dynamodb Table Scan by IDs: {err}")

# Update Entire Table Item - Send in full dict of item
def delete_table_item(table_name, primary_key, primary_key_value):
    try:
        check_if_item_exist(table_name, primary_key, primary_key_value)
        table = dynamodb_res.Table(table_name)
        response = table.delete_item(
            Key={
                primary_key: primary_key_value
            }
        )
        return response
    except Exception as err:
        log.error(f"Dynamodb Table Delete Table Item: {err}")
        raise Exception(f"Dynamodb Table Delete Table Item: {err}")


# Update Entire Table Item - Send in full dict of item
def update_table_item(table_name, table_item):
    try:
        table = dynamodb_res.Table(table_name)
        response = table.put_item(
            Item=table_item
        )
        return response
    except Exception as err:
        log.error(f"Dynamodb Table Update Table Item: {err}")
        raise Exception(f"Dynamodb Table Update Table Item: {err}")


# Update single field of Table - send in one attribute and key
def update_table_item_field(table_name, primary_key, primary_key_value, attr_key, attr_val):
    try:
        check_if_item_exist(table_name, primary_key, primary_key_value)

        table = dynamodb_res.Table(table_name)
        response = table.update_item(
            Key={
                primary_key: primary_key_value
            },
            UpdateExpression="set #attr_key = :attr_val",
            ExpressionAttributeValues={
                ':attr_val': attr_val
            },
            ExpressionAttributeNames={
                '#attr_key': attr_key
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
    except Exception as err:
        log.error(f"Dynamodb Table Update Table Item Field: {err}")
        raise Exception(f"Dynamodb Table Update Table Item Field: {err}")

def check_if_item_exist(table_name, id_key, id_val, override=False):
    try:
        table = dynamodb_res.Table(table_name)
        response = table.get_item(
            Key={
                id_key: id_val,
            }
        )
        if 'Item' in response:
            return True
        elif override:
            return False
        else:
            raise Exception("Invalid ID (" + id_val + "): Item Does not Exist.")
    except Exception as err:
        log.error(f"Dynamodb Table Check If Item Exists: {err}")
        raise Exception(f"Dynamodb Table Check If Item Exists: {err}")

def get_item_by_key(table_name, id_key, id_val):
    try:

        table = dynamodb_res.Table(table_name)
        response = table.get_item(
            Key={
                id_key: id_val,
            }
        )
        if 'Item' in response:
            return response['Item']
        else:
            raise Exception("Invalid ID (" + id_val + "): Item Does not Exist.")
    except Exception as err:
        log.error(f"Dynamodb Table Get Item By Key: {err}")
        raise Exception(f"Dynamodb Table Get Item By Key: {err}")
    
def get_item_by_multiple_keys(table_name: str, id_partition_key: str, id_partition_val: str, id_sort_key: str, id_sort_val: str):
    try:

        table = dynamodb_res.Table(table_name)
        response = table.get_item(
            Key={
                id_partition_key: id_partition_val,
                id_sort_key: id_sort_val            
            }
        )

        item = response.get('Item')
        if item:
            log.info("Item Found in table.")
            return response['Item']
        else:
            log.warning(f"Invalid IDs ({id_partition_key} - {id_sort_key}): Item Does not Exist.")
            return {}
    except Exception as err:
        log.error(f"Dynamodb Table Get Item By Multipe Keys: {err}")
        raise Exception(f"Dynamodb Table Get Item By Multipe Keys: {err}")

def query_table_by_key(table_name, id_key, id_val, ascending=False):
    try:
        table = dynamodb_res.Table(table_name)
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key(id_key).eq(id_val),
            ScanIndexForward=ascending
        )
        return response
    except Exception as err:
        log.error(f"Dynamodb Table Query Table By Key: {err}")
        raise Exception(f"Dynamodb Query Table Item By Key: {err}")
def item_has_property(item, property):
    for field in item:
        if field == property:
            return True

    return False

def emptyTable(table_name, hash_key, hash_key_type):
    try:
        deleteTable(table_name)
        table = createTable(table_name, hash_key, hash_key_type)
        return table
    except Exception as err:
        log.error(f"Dynamodb Table Empty Table: {err}")
        raise Exception(f"Dynamodb Table Empty Table: {err}")

def deleteTable(table_name):
    try:
        return dynamodb_client.delete_table(TableName=table_name)
    except Exception as err:
        log.error(f"Dynamodb Table Delete Table: {err}")
        raise Exception(f"Dynamodb Table Delete Table: {err}")
def createTable(table_name, hash_key, hash_key_type):
    try:
        #Wait for table to be deleted
        waiter = dynamodb_client.get_waiter('table_not_exists')
        waiter.wait(TableName=table_name)
        # Get KMS Key
        kms_key = kms_res.describe_key(
            KeyId=DYNAMODB_KMS_ALIAS
        )
        #Create table
        table = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': hash_key,
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions= [
                {
                    'AttributeName': hash_key,
                    'AttributeType': hash_key_type
                }
            ],
            StreamSpecification={
                'StreamEnabled': True,
                'StreamViewType': 'NEW_AND_OLD_IMAGES'
            },
            SSESpecification={
                'Enabled': True,
                'SSEType': 'KMS',
                'KMSMasterKeyId': kms_key['KeyMetadata']['Arn']
            },
            BillingMode='PAY_PER_REQUEST'
        )

        #Wait for table to exist
        waiter = dynamodb_client.get_waiter('table_exists')
        waiter.wait(TableName=table_name)

        return table
    except Exception as err:
        log.error(f"Dynamodb Table Create Table: {err}")
        raise Exception(f"Dynamodb Table Create Table: {err}")
    

def batch_write_table_items(table_name: str, db_items: dict):
    try:
        table = dynamodb_res.Table(table_name)
        with table.batch_writer() as batch:
            for player_id, player_data in db_items.items():
                batch.put_item(
                    Item={
                        'player_id': player_id,
                        'data': player_data,
                        'last_updated': datetime.utcnow().isoformat()
                    }
                )
        log.info(f"Updated {len(db_items)} Items in DynamoDB Table {table_name}.")
        return f"Updated {len(db_items)} Items in DynamoDB Table {table_name}."
    except Exception as err:
        log.error(f"Batch Write Table Items: {err}")
        raise Exception(f"Batch Write Table Items: {err}")
    
