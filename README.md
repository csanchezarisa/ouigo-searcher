# Ouigo searcher
## _A Ouigo ticket searcher_

ouigo-searcher is a python script that checks if a specific trip ticket is available in Ouigo page and notifies you with an email.

## Features

Look for specific ouigo ticket using:
- Date to filter
- Trip departure city
- Trip destination city

It will send an email too when the ticket is available, using:
- Gmail username
- Gmail password

_The gmail user must have the less secure options activated. You can activate it by going to: [Google less secure options]._

  [Google less secure options]: <https://myaccount.google.com/lesssecureapps>
  
## Installation

ouigo-searcher requires [Python](https://www.python.org/downloads/) to run.

Install the [requests](https://docs.python-requests.org/) module and execute the scrip:

### Installing requests module

Run the following command:

```sh
pip install -r requirements.txt
```

## How to use the script

This script uses the arguments to look for a specific ticket in the Ouigo page.

These arguments must be in their right position, so that the script can use them correctly.

### Example

```sh
python ./ouigo.py <date_to_filter> <gmail_username> <gmail_password> <email_recipients> <origin_city> <destination_city> <refresh_time>
```
```sh
python ./ouigo.py 2022-12-31 example@gmail.com password123 example1@email.com,example2@email.com,example3@email.com B M 1800
```

### Help argument

You can also use the help argument which will explain you how to use this script.

This argument must be in the first position, it can be `h`, `help` or `?`

```sh
python ./ouigo.py h
```

### Mandatory arguments

These are the mandatory arguments
- **date_to_filter**: Date to look for the ticket. You must use the format yyyy-mm-dd.
- **gmail_username**: Gmail user to send the email when a ticket available is found.
- **gmail_password**: Gmail password to login and send the email correctly.
- **email_recipients**: Comma listed emails to send the notification.
- **origin_city**: Trip departure city. You must use one of the following city codes.
  - B: BARCELONA
  - M: MADRID
  - Z: ZARAGOZA
  - T: TARRAGONA
- **destination_city**: Trip destination city. You must use one of the following city codes.
  - B: BARCELONA
  - M: MADRID
  - Z: ZARAGOZA
  - T: TARRAGONA

### Optional arguments

These are the optional arguments:
- **refresh_time**: Time (in seconds) to retry is there's no ticket available. _It's 1800 by default_

## Docker

**ouigo-searcher** can also be executed using [docker](https://docs.docker.com/get-docker/).

### Building the image

First of all, you need to create a **docker image** by running the following command:

```sh
docker build -t ouigo-searcher .
```

### Running the script

When the image has been successfully created, you will be able to run the script in docker by running the following command:

```sh
docker run ouigo-searcher {{ ARGUMENTS }}
```

For example:

```sh
docker run ouigo-searcher 2022-12-31 example@gmail.com password123 example1@email.com,example2@email.com,example3@email.com B M 1800
```