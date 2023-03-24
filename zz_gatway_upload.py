import json
import jmespath
from rally import files, asset, supplyChain


def get_metadata_from_upload_widget(context):
    """
    Extract data from gateway dpd
    :param context:
    :return:
    """
    widget_metadata = {"asset_name": None, "upload_metadata": []}
    file_uri = context.get("dynamicPresetData", {}).get("fileUri", "")
    if file_uri:
        file_open = json.loads(files.read_file(file_uri))
        file_data = file_open.get('data', [])
        for _data in file_data:
            if _data.get("widgetType") == "AssetPicker":
                widget_metadata["asset_name"] = jmespath.search("data[0].asset.attributes.name", _data)
            elif _data.get("widgetType") == "UploadCollector":
                widget_metadata["upload_metadata"] = jmespath.search("data", _data)
    print(widget_metadata)
    return widget_metadata


def get_file_from_upload_md(upload_metadata):
    """
    Generator to create dpd dictionaries
    :param bss_id
    :param upload_metadata:
    :return:
    """
    asset_name = asset.get_asset()['name']
    for upload_dict in upload_metadata:
        _dpd_dict = {"upload_gateway": {"metadata": {}, "file": {}}}
        md_name = jmespath.search("metadata.Name", upload_dict)
        md_type = jmespath.search('metadata."Media Type"', upload_dict)
        md_filerename = jmespath.search('metadata."New Filename"', upload_dict) or ""
        is_selected = jmespath.search("selected", upload_dict)
        name = jmespath.search("upload.name", upload_dict)
        prefix = jmespath.search("upload.prefix", upload_dict)
        storage_location = jmespath.search("upload.storageLocation", upload_dict)
        if prefix == "gatewayuploads/" and is_selected:
            _dpd_dict["upload_gateway"]["metadata"]["name"] = md_name
            _dpd_dict["upload_gateway"]["file"]["prefix"] = prefix
            _dpd_dict["upload_gateway"]["file"]["name"] = name.split(".")[0]
            _dpd_dict["upload_gateway"]["file"]["ext"] = "." + name.split(".")[-1]
            _dpd_dict["upload_gateway"]["file"]["storage_location"] = storage_location
            _dpd_dict["upload_gateway"]["file"]["rename"] = md_filerename.format({asset_name})
            _dpd_dict["upload_gateway"]["file"]["uri"] = f"rsl://{storage_location}/{name}"
            yield _dpd_dict


def eval_main(context):
    metadata = asset.get_user_metadata()
    asset_name = asset.get_asset()['name']
    gateway_md = get_metadata_from_upload_widget(context)
    for file_dpd in get_file_from_upload_md(gateway_md["upload_metadata"]):
        dynamic_data = {'media_update': True, 'media_file_name': file_dpd["upload_gateway"]["file"]["name"],
                        'media_file_ext': file_dpd["upload_gateway"]["file"]["ext"],
                        "prefix": file_dpd["upload_gateway"]["file"]["prefix"],
                        "storage": file_dpd["upload_gateway"]["file"]["storage_location"],
                        "source_uri": file_dpd["upload_gateway"]["file"]["uri"],
                        "output_name": file_dpd["upload_gateway"]["file"]["name"] + file_dpd["upload_gateway"]["file"][
                            "ext"],
                        "file_label": file_dpd["upload_gateway"]["file"]["name"].split(".")[0]
                        }
        if file_dpd["upload_gateway"]["file"]["rename"]:
            # If rename detected, then add a step to sequence
            file_dpd["upload_gateway"]["file"]["name"] = file_dpd["upload_gateway"]["file"]["rename"].split(".")[0]
            rnm_dpd = {"source_uri": dynamic_data["source_uri"],  # rsl://CSC Landing Pad/933027_HENRY_TEST_file.wav
                       "storage_location": dynamic_data["storage"],  # CSC Landing Pad
                       "media_file_name": file_dpd["upload_gateway"]["file"]["rename"],
                       "output_name": file_dpd["upload_gateway"]["file"]["name"] + file_dpd["upload_gateway"]["file"][
                           "ext"],
                       "file_label": file_dpd["upload_gateway"]["file"]["rename"].split(".")[0]
                       }
            print(rnm_dpd)
            print('File uploaded and renamed successfully')
            supplyChain.start_new_supply_chain(asset=asset_name, step='zz_upload_mover', dynamic_preset_data=rnm_dpd)

        else:
            print(dynamic_data)
            print('File uploaded successfully')
            supplyChain.start_new_supply_chain(asset=asset_name, step='zz_upload_mover',
                                               dynamic_preset_data=dynamic_data)

    return 'true'