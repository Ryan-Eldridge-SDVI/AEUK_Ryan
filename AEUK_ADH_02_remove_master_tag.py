from rally import asset, files, supplyChain
import pprint
import json
import copy


# Take and parse the data from the gateway

def eval_main(context):
    dynamic_data = context.get('dynamicPresetData')
    if dynamic_data:
        pprint.pprint(dynamic_data, width=255)

        file_uri = dynamic_data['fileUri']

        gateway_data = files.read_file(file_uri)
        gateway_data = gateway_data.decode('utf-8')
        gateway_data = json.loads(gateway_data)

        print('gateway_data:')

        # Get list of tags on Rally asset

        asset_tags = asset.get_asset_tags()

        # Take the tag selected in the gateway and build tag

        for widget in gateway_data['data']:
            if widget['name'] == 'Tag list':
                metadata = widget['data'][0]['metadata']
                tag = metadata.get('Tag List', {})

                # If no tag is selected, raise an exception

                try:
                    if not tag:
                        raise Exception('No Tag selected')

                    # Delete tag and print statement

                    for key, value in tag.items():
                        asset.remove_asset_tags([value])
                        print(f'Successfully removed tag: {value}')

                except Exception as e:
                    print(f'Error Removing Tags: {e}')