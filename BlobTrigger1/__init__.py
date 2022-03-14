import logging
from azure.storage.blob import BlobServiceClient
import azure.functions as func
import json
import time
from requests import get, post
import os
from collections import OrderedDict
import numpy as np
import pandas as pd

import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


def main(blobin: func.InputStream, blobout: func.Out[bytes], context: func.Context):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {blobin.name}\n"
                 f"Blob Size: {blobin.length} bytes")
    
    # This is the call to the Form Recognizer endpoint
    endpoint = os.environ["form_reco_endpoint"]
    apim_key = os.environ["form_reco_key"]
    model_id = os.environ["form_reco_model_id"]
    
    full_recognizer_output = False

    # post_url = endpoint + "/formrecognizer/v2.1/Layout/analyze"
    # read the PDF document
    source = blobin.read()
    text1=os.path.basename(blobin.name)

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(apim_key)
    )

    # Make sure your document's type is included in the list of document types the custom model can analyze
    # poller = document_analysis_client.begin_analyze_document_from_url(model_id, documentUrl)
    poller = document_analysis_client.begin_analyze_document(model_id, source)

    result = poller.result()
    detected_kv_pairs = []
    for idx, document in enumerate(result.documents):
        print("--------Analyzing document #{}--------".format(idx + 1))
        print("Document has type {}".format(document.doc_type))
        print("Document has confidence {}".format(document.confidence))
        print("Document was analyzed by model with ID {}".format(result.model_id))
        for name, field in document.fields.items():
            field_value = field.value if field.value else field.content
            # print("......found field {} of type '{}' with value '{}' and with confidence {}".format(name,field.value_type, field_value, field.confidence))
            detected_kv_pairs.append([name, field_value, field.confidence])

    # convert detected key-value pairs to Pandas dataframe        
    document_detected_kv_pairs = pd.DataFrame(detected_kv_pairs, columns =['Key', 'Value','Confidence'])


    if (full_recognizer_output):
        # iterate over tables, lines, and selection marks on each page
        for page in result.pages:
            print("\nLines found on page {}".format(page.page_number))
            for line in page.lines:
                print("...Line '{}'".format(line.content.encode('utf-8')))
            for word in page.words:
                print(
                    "...Word '{}' has a confidence of {}".format(
                        word.content.encode('utf-8'), word.confidence
                    )
                )
            for selection_mark in page.selection_marks:
                print(
                    "...Selection mark is '{}' and has a confidence of {}".format(
                        selection_mark.state, selection_mark.confidence
                    )
                )

        for i, table in enumerate(result.tables):
            print("\nTable {} can be found on page:".format(i + 1))
            for region in table.bounding_regions:
                print("...{}".format(i + 1, region.page_number))
            for cell in table.cells:
                print(
                    "...Cell[{}][{}] has content '{}'".format(
                        cell.row_index, cell.column_index, cell.content.encode('utf-8')
                    )
                )
        print("-----------------------------------")
    

    # convert dataframe into json then to byte array
    blob_out_bytes = bytes(document_detected_kv_pairs.to_json(orient="records"), encoding='utf-8')
    
    # store in the output storage through Functions output binding
    blobout.set(blob_out_bytes)