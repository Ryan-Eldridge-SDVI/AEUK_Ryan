from rally import asset, files, supplyChain, exceptions
import pprint
import json
import copy
from datetime import datetime, date, timedelta, timezone
from env_handler import CONFIG


def eval_main(context):
    dynamic_data = context.get('dynamicPresetData')
    if dynamic_data:
        pprint.pprint(dynamic_data, width=255)

        file_uri = dynamic_data['fileUri']
        # take, decode and print gateway data
        gateway_data = files.read_file(file_uri)
        gateway_data = gateway_data.decode('utf-8')
        gateway_data = json.loads(gateway_data)

        print('gateway_data:')
        # Find data we need from the gateway widget data
        for widget in gateway_data['data']:
            if widget['name'] == 'Create Asset':
                print('widget:', widget)
                print('gateway_data:', gateway_data)
                metadata = widget['data'][0]['metadata']
                baseName = metadata.get('Asset Name', {})

                try:
                    if not baseName:
                        raise Exception('Asset Name is blank')

                    # Generate the date & time used for filename timestamp
                    date_time = datetime.now(timezone.utc)
                    date_time_str = str(date_time)
                    date_time_str_display = str(date_time).replace(' ', 'T')[:-13] + 'Z'
                    # build assetName by combining 'zz' with baseName and the generated date & time
                    assetName = 'zz' + " - " + baseName + " - " + date_time_str_display

                    # Create Rally asset & print success message
                    asset.create_asset(assetName)
                    print(f'Successfully created asset: {assetName}')

                except Exception as e:
                    print(f'Error adding Tags: {e}')
