# Ping Agent

## Requirements

 - [Python 3.7.x](https://www.python.org)

> Due to the different output format and parameters between the Windows and Linux versions of ping this agent 
> **can only be deployed on Linux**.

## Installing (development)

1. Clone the repository to a known folder, e.g. in `c:\malaga-platform` 
2. Enter the folder
```bash
cd c:/malaga-platform/pingAgent
```
3. Create a new Python virtualenv:
```bash
pip install virtualenv
virtualenv venv
```
4. Activate the virtual environment:
```bash
source venv/bin/activate
```
5. Install Python dependencies:
```bash
pip install -r requirements.txt
```
6. Start the development server:
```bash
flask run
```
The app will start listening for requests on port 5000.
Press `Control+C` to stop the development server.

### Usage

The Ping Agent exposes a REST API with the following endpoints:
* `/Ping/<address>`: Executes ping process to the given address. Returns a JSON reporting the success of the execution and a message. The following URL parameters can be used:
    * interval: Ping interval
    * size: Packet size
    * ttl: Time to Live 
* `/Close`: Closes ping process. Returns a JSON reporting the success of the process closure and a message.
* `/LastJsonResult`: Retrieve the result of the previous executions. Returns a JSON reporting the success of the retrieval, a message and a list of Results (dictionary with parsed results).
* `/StartDateTime`: Retrieve the date and time of the last execution. Returns a JSON reporting the success of the retrieval and a message informing of the date.
* `/IsRunning`: Check if there is another execution running. Returns a JSON reporting the success of the check and a message informing if is running or not.

## Authors

* **Gonzalo Chica Morales**
* **Bruno Garcia Garcia**

## License

TBD
