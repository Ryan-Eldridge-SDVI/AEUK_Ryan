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

        pprint.pprint('gateway_data:')

        for widget in gateway_data['data']:
            if widget['name'] == 'Master Asset Inventory':
                label = widget['data'][0]['file']['attributes']['label']
        pprint.pprint(widget)
        src_file = next(files.get_inventory(label=label))
        pprint.pprint(src_file)

        for widget in gateway_data['data']:
            if widget['name'] == 'Tag list':
                print('widget:', widget)
                print('gateway_data:', gateway_data)
                metadata = widget['data'][0]['metadata']
                tag_list = metadata.get('Tag List', {})

                try:
                    if not tag_list:
                        raise Exception('No Tag selected')

                    for key, value in tag_list.items():
                        src_file.add_tags([value])
                        print(f'Successfully added inventory tag: {value}')

                except Exception as e:
                    print(f'Error adding inventory Tag: {e}')


def pprint_json(arg):
    print(json.dumps(arg, indent=2))

