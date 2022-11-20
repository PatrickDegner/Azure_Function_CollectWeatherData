![Azure Function Weather Data](https://user-images.githubusercontent.com/108484798/202908226-cf817133-e1f5-43f1-99fc-0bfa79baddd4.jpg)

## How it works
This Azure Function gets Weather-Data from 01.01.2022 up to Today + 7 Days and puts it into a parquet file and uploads it to Blob Storage Container.
The credentials are hidden in Azure Key Vault.
Data is processed with Python Pandas.

![Screenshot 2022-11-20 161330](https://user-images.githubusercontent.com/108484798/202910145-c7930cc3-a8ac-4855-92df-d8cf3d706416.png)

## Tools and libraries
* Azure Functions
* Azure Key Vault
* Azure Storage Blob
* Python Pandas

## How to use

Create a new Function App in Azure

![image](https://user-images.githubusercontent.com/108484798/202909319-64eb78da-3a26-408e-aee3-0202b6b09eef.png)

Clone or download the repository
```sh
https://github.com/PatrickDegner/Azure_Function_CollectWeatherData.git
```

Set to your variables
```sh
key_vault_Uri
blob_secret_name
```
Create an Azure Key Vault and add your connectionstring from Blob Storage
![image](https://user-images.githubusercontent.com/108484798/202909476-72101027-025e-4d6f-8367-1b7de573a437.png)

Upload the code to your Function App with Visual Studio Code

When you trigger the Function with a Http Request it will create the new blob in your storage
![image](https://user-images.githubusercontent.com/108484798/202909664-0fe5549e-bea0-455f-9ff3-b60ce2767c92.png)
