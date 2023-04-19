{
  "tasks": [
    {
      "operation": "move",
      "source": {
        "optional": false,
        "externalStorage": {
          "uri": "{{DYNAMIC_PRESET_DATA['source_uri']}}"
        }
      },
      "destination": {
        "name": "{{DYNAMIC_PRESET_DATA['output_name']}}",
        "overwrite": "always",
        "inventory": {
          "storage": "{{DYNAMIC_PRESET_DATA['destination']}}",
          "newLabel": "{{DYNAMIC_PRESET_DATA['file_label']}}",
          "newTags": [
            "Ad hoc",
            "Gateway Upload"
          ]
        }
      }
    }
  ]
}