# sending commands and information to the device

import wiotp.sdk.application
from Gateway_client import get_gateway_cilent

CLOUDANT_CREDS = {
  "apikey": "zEofoCDJQz-m_sR4JH8VitjEdsHDQz_lFj2BpcupqHQv",
  "host": "681cf4f3-4d14-4fce-aad9-2a4f1e80016c-bluemix.cloudantnosqldb.appdomain.cloud",
  "password": "d9312469913ea3a03019adcf8404ab8a9d2a53bf434fb3ab8522bac82694e683",
  "port": 443,
  "username": "681cf4f3-4d14-4fce-aad9-2a4f1e80016c-bluemix"
}

SERVICE_BINDING = {
    "name": "CristiG",
    "description": "Test Cloudant Binding",
    "type": "cloudant",
    "credentials": CLOUDANT_CREDS
}

ANDROID_DEVICE_TYPE = "Android"
GATEWAY_DEVICE_TYPE = "laptop"
STATUS_EVENT_TYPE = "status"


def get_application_client(config_file_path):
    config = wiotp.sdk.application.parseConfigFile(config_file_path)
    app_client = wiotp.sdk.application.ApplicationClient(config)
    return app_client


def create_cloudant_connections(client, service_binding):
    # Bind application to the Cloudant DB
    cloudant_service = client.serviceBindings.create(service_binding)

    # Create the connector
    connector = client.dsc.create(
        name="connector_1", type="cloudant", serviceId=cloudant_service.id, timezone="UTC",
        description="Data connector", enabled=True
    )

    # Create a destination under the connector
    destination_1 = connector.destinations.create(name="sensor-data", bucketInterval="DAY")

    # Create a rule under the connector, that routes all Android status events to the destination
    connector.rules.createEventRule(
        name="status_events", destinationName=destination_1.name, typeId=ANDROID_DEVICE_TYPE, eventId=STATUS_EVENT_TYPE,
        description="Send android status events", enabled=True
    )

    # Create another destination under the connector
    destination_2 = connector.destinations.create(name="gateway-data", bucketInterval="DAY")

    # Create a rule under the connector, that routes all raspi status events to the destination
    connector.rules.createEventRule(
        name="status_events", destinationName=destination_2.name, typeId=GATEWAY_DEVICE_TYPE, eventId=STATUS_EVENT_TYPE,
        description="Gateway status events", enabled=True)


def send_reset_command(client, type, id):
    data = {'reset': True}
    client.publishCommand(type, id, "reset", "json", data)


app_client = get_gateway_cilent("app_config.yml")
app_client.connect()

# Call the functions like this
# send_reset_command(app_client, 'laptop', 'laptop-1')

