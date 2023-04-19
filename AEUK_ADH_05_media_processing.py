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

        file_uri = dynamic_data['fileUri']

        gateway_data = files.read_file(file_uri)
        gateway_data = gateway_data.decode('utf-8')
        gateway_data = json.loads(gateway_data)

        pprint.pprint('gateway_data:')

        # Get source file label from 'Master Asset Inventory' widget

        for widget in gateway_data['data']:
            if widget['name'] == 'Master Asset Inventory':
                label = widget['data'][0]['file']['attributes']['label']
        pprint.pprint(widget)
        src_file = next(files.get_inventory(label=label))
        pprint.pprint(src_file)

        # Get file label and extension from 'Master Asset Inventory' widget

        for widget in gateway_data['data']:
            if widget['name'] == 'Master Asset Inventory':
                label = widget['data'][0]['file']['attributes']['label']
                file_extension = widget['data'][0]['file']['attributes']['name'].split(".")[-1]

            # Get metadata from from 'Metadata' widget

            if widget['name'] == 'Metadata':
                print('widget:', widget)
                print('gateway_data:', gateway_data)
                metadata = widget['data'][0]['metadata']
                print(file_extension)

                # Define file extension based on video codec selected

                if metadata.get('Video Codec') == 'h264':
                    file_extension = 'mp4'
                elif metadata.get('Video Codec') == 'mpeg2video':
                    file_extension = 'mpg'
                elif metadata.get('Video Codec') == 'prores':
                    file_extension = '.mov'

                # Build dynamic data for FFMPEG job and run FFMPEG supply chain

                if not metadata.get('Vantage Profiles'):

                    dynamic_data = {
                        'output_name': metadata.get('Output Filename') + "." + file_extension,
                        'output_extension': file_extension,
                        'output_ffmpeg': '$jobOutputFolder:myOutput' + "." + file_extension,
                        'input_label': label,
                        'output_label': metadata.get('Output Filename'),
                        'output_location': 'CSC Landing Pad',
                        'audio_bitrate': metadata.get('Audio Bitrate'),
                        'audio_codec': metadata.get('Audio Codec'),
                        'video_codec': metadata.get('Video Codec'),
                        'video_bitrate': metadata.get('Video Bitrate'),
                        'height': metadata.get('Video Height'),
                        'width': metadata.get('Video Width')
                    }

                    print(dynamic_data)
                    supplyChain.start_new_supply_chain(asset=asset_name, step='zz_adhoc_ffmpeg',
                                                       dynamic_preset_data=dynamic_data)

                # Select vantage preset and build dynamic data for Vantage job, then run supply chain

                elif metadata.get('Vantage Profiles'):

                    vantage_profile = metadata.get('Vantage Profiles')

                    vantage_data = {
                        'source_label': label,
                        'output_file_name': metadata.get('Output Filename') + "." + file_extension,
                        'output_label': metadata.get('Output Filename'),
                        'target_storage': 'CSC Landing Pad'
                    }

                    print(dynamic_data)
                    supplyChain.start_new_supply_chain(asset=asset_name, step=vantage_profile,
                                                       dynamic_preset_data=vantage_data)