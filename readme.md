# Use Azure Form Recognizer v3.0 with Azure Functions

This simple example shows how to call Azure Form Recognizer v3.0 Custom model API from Azure Functions.

## Scenario
Read file from Blob Storage (BlobTrigger) and call Form Recognizer using Custom model created in Form Recognizer studio (Preview).

It combines two tutorials:
* [Use an Azure Function to process stored documents](https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/tutorial-azure-function)
* [Get started: Form Recognizer Python SDK v3.0 | Preview](https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/quickstarts/try-v3-python-sdk)

## Details
* Azure Function code is under `BlobTrigger1` folder.

* It uses Form Recognizer Python SDK v3.0 preview:

 `azure-ai-formrecognizer==3.2.0b2`

* Connection to Form Recognizer and selecting particular model is via Environment Variables:

```python
endpoint = os.environ["form_reco_endpoint"]
apim_key = os.environ["form_reco_key"]
model_id = os.environ["form_reco_model_id"]
```
> Note: for local debug add those variables to `local.settings.json`:

```
{
  "IsEncrypted": false,
  "Values": {
    ...
    "form_reco_key": "YOUR_FORM_RECOGNIZER_KEY",
    "form_reco_endpoint": "https://YOUR_SERVICE.cognitiveservices.azure.com/",
    "form_reco_model_id": "YOUR_MODEL_NAME"
  }
}

```

> TODO: change to Azure Key Vault 

* The Azure Function tojust prints the Form recognizer output (recognized items) on the standard output. Additional integration is needed.