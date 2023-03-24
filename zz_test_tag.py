from rally import asset, files, supplyChain
import pprint
import json
import copy


def eval_main(context):
    dynamic_data = context.get('dynamicPresetData')
    if dynamic_data:
        pprint.pprint(dynamic_data, width=255)

        file_uri = dynamic_data['fileUri']

        gateway_data = files.read_file(file_uri)
        gateway_data = gateway_data.decode('utf-8')
        gateway_data = json.loads(gateway_data)

        print('gateway_data:')
        pprint_json(gateway_data)

        asset_tags = asset.get_asset_tags()

        if 
            for widget in gateway_data['data']:
                if widget['name'] == 'Tag list':
                    print('widget:', widget)
                    print('gateway_data:', gateway_data)
                    metadata = widget['data'][0]['metadata']
                    tag_list = metadata.get('Tag List', {})

                    try:
                        if not tag_list:
                            raise Exception('No Tag selected')

                        if tag_list not in asset_tags:
                            for key, value in tag_list.items():
                                asset.add_asset_tags([value])
                                print(f'Successfully added tag: {value}')
                    except Exception as e:
                        print(f'Error Adding Tags: {e}')


def pprint_json(arg):
    print(json.dumps(arg, indent=2))