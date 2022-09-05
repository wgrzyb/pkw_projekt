# pkw_projekt
The project was carried out as part of the "Fundamentals of modern cryptology" laboratory classes at the Military University of Technology.

The project concerns solving the problem of durable medium using Algorand blockhcain and InterPlanetary File System (IPFS) technologies. To demonstrate the solution, Python web applications were implemented using the Flask framework.

## Application details

The application allows you to transfer files and publish messages (pastebin) encrypted with a password.
Uploaded files are placed and stored in IPFS.
To preserve the information that the file was sent to IPFS, the obtained CID of the file is added to the Algorand blockchain testnet.
The application also allows you to download uploaded files and published messages.

## Preparation of the environment

  1. Clone the repository:

  ```
  git clone git@github.com:wgrzyb/pkw_projekt.git
  ```

  2. Navigate to the repository folder and install the required libraries (from the `requirements.txt` file):
  
  ```
  cd .\pkw_projekt
  pip install -r .\requirements.txt
  ```
  
  3. Run Go-IPFS on the docker:
  
  ```
  docker run -d --name ipfs-node -p 8080:8080 -p 4001:4001 -p 5001:5001 ipfs/go-ipfs:latest
  ```
  
  4. Run [flask application](https://github.com/wgrzyb/pkw_projekt/blob/master/flask_app/main.py) from the repository directory.
  
  5. Open [web application](http://127.0.0.1:5000/).
