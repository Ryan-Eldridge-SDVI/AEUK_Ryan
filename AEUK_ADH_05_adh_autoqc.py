import json
import jmespath
import pprint
from rally import files, asset, supplyChain


# Take and parse the data from the gateway

def eval_main(context):
    dynamic_data = context.get('dynamicPresetData')
    if dynamic_data:
        pprint.pprint(dynamic_data, width=255)

        asset_name = asset.get_asset()['name']
        base_path = f'{asset_name}/'

        file_uri = dynamic_data['fileUri']

        gateway_data = files.read_file(file_uri)
        gateway_data = gateway_data.decode('utf-8')
        gateway_data = json.loads(gateway_data)

        pprint.pprint('gateway_data:')

        # Get file label from 'Master Asset Inventory' widget

        for widget in gateway_data['data']:
            if widget['name'] == 'Master Asset Inventory':
                label = widget['data'][0]['file']['attributes']['label']
        pprint.pprint(widget)
        src_file = next(files.get_inventory(label=label))
        pprint.pprint(src_file)

        # Get label and file extension from 'Master Asset Inventory' widget

        for widget in gateway_data['data']:
            if widget['name'] == 'Master Asset Inventory':
                label = widget['data'][0]['file']['attributes']['label']
                file_extension = widget['data'][0]['file']['attributes']['name'].split(".")[-1]

            # Get SD or HD selection from 'Baton' widget

            if widget['name'] == 'Baton':
                print('widget:', widget)
                print('gateway_data:', gateway_data)
                sd_hd = widget['data'][0]['metadata']['workflow']['type']
                print('sd_hd:', sd_hd)

                # Generate dynamic data required for Baton

                dynamic_data = {
                    'src_label': label,
                    'source_label': label,
                    'base_path': base_path,
                    'from_gateway_retrigger': True
                }

                print('Dynamic Data:', dynamic_data)

                # Select supply chain path based on SD or HD Baton profile selection

                if sd_hd == 'HD':
                    supplyChain.start_new_supply_chain(asset=asset_name, step='AEUK_SCI_05b_autoQC_Baton_HD',
                                                       dynamic_preset_data=dynamic_data)


                elif sd_hd == 'SD':
                    supplyChain.start_new_supply_chain(asset=asset_name, step='AEUK_SCI_05b_autoQC_Baton_SD',
                                                       dynamic_preset_data=dynamic_data)