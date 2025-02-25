# ----------------------------------------------------------------------------------
# MIT License
#
# Copyright(c) Microsoft Corporation. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# ----------------------------------------------------------------------------------
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pkg_resources
pkg_resources.require("azure-storage-blob==2.1.0")

import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
#from time import strftime
from datetime import datetime
from subprocess import call

# ---------------------------------------------------------------------------------------------------------
# Method that creates a test file in the 'Documents' folder.
# This sample application creates a test file, uploads the test file to the Blob storage,
# lists the blobs in the container, and downloads the file with a new name.
# ---------------------------------------------------------------------------------------------------------
# Documentation References:
# Associated Article - https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
# What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/
# Getting Started with Blobs-https://docs.microsoft.com/en-us/azure/storage/blobs/storage-python-how-to-use-blob-storage
# Blob Service Concepts - http://msdn.microsoft.com/en-us/library/dd179376.aspx
# Blob Service REST API - http://msdn.microsoft.com/en-us/library/dd135733.aspx
# ----------------------------------------------------------------------------------------------------------


def run_sample():
    try:
       
        call("whoami")
           
        print("---started at :")
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
                   
       # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='asensio', account_key='A+WC/tN8QvwdMvCVnpmpGnEJLSz3mvGLGFPwTlDMh6BHXL+9zPB4PyvDAMV2ijcHEcP9vSIVRnUy1DwABhB72A==')

        # Access a container called energydata
        container_name ='energy-data'

        # List the blobs in the container
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)
        
        
        # Create a file in Documents to test the upload and download.
        local_path=os.path.expanduser("~/Downloads")
        file_name ="meter-readings-small.csv"


        # Download the blob(s).
        # Add '_DOWNLOADED' as prefix to '.csv' so you can see both files in Documents.
        full_path_to_file2 = os.path.join(local_path, str.replace(file_name ,'.csv', '_DOWNLOADED.csv'))
        print("\nDownloading blob to " + full_path_to_file2)
        block_blob_service.get_blob_to_path(container_name, file_name, full_path_to_file2)

        sys.stdout.write("Sample finished downloading. The "
                         "application will exit.")
                         
        print("\n---completed at :")
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
                             
        sys.stdout.flush()
        #input()

    except Exception as e:
        print(e)


# Main method.
if __name__ == '__main__':
    run_sample()



