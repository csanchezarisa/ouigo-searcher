# Ouigo searcher
## _A Ouigo ticket searcher_

ouigo-searcher is a python script that checks if a specific trip ticket is available in Ouigo page and notifies you with an email.

## Table of contents
1. [Features](#features)
2. [Installation](#installation)
    1. [Installing requests module](#install-requests)
3. [How to use the script](#howto)
    1. [Example](#howto-example)
    2. [Help argument](#howto-help)
    3. [Mandatory arguments](#howto-mandatory)
    4. [Optional arguments](#howto-optional)
4. [Docker](#docker)
    1. [Building the image](#docker-build)
    2. [Running the script](#docker-run)
    3. [Docker Hub repo](#docker-hub)

## 1. Features <a name="features"></a>

Look for specific ouigo ticket using:
- Date to filter
- Trip departure city
- Trip destination city

It will send an email too when the ticket is available, using:
- Gmail username
- Gmail password

_Now that Google has disabled the "**less security**" options, you'll need to set up your account to use **2-Step Verification** and create an **app password** before you can use it in this script.<br>To do this, you can go to the [Google Help Center](https://support.google.com/accounts/answer/185833?hl) or you can check this blog [catwoot blog](https://www.chatwoot.com/docs/product/channels/email/gmail/generate-app-password)._

## 2. Installation <a name="installation"></a>

ouigo-searcher requires [Python](https://www.python.org/downloads/) to run.

Install the [requests](https://docs.python-requests.org/) module and execute the scrip:

### 2.1. Installing requests module <a name="install-requests"></a>

Run the following command:

```sh
pip install -r requirements.txt
```

## 3. How to use the script <a name="howto"></a>

This script uses the arguments to look for a specific ticket in the Ouigo page.

These arguments must be in their right position, so that the script can use them correctly.

### 3.1. Example <a name="howto-example"></a>

```sh
python ./ouigo.py <date_to_filter> <gmail_username> <gmail_password> <email_recipients> <origin_city> <destination_city> <refresh_time>
```
```sh
python ./ouigo.py 2022-12-31 example@gmail.com password123 example1@email.com,example2@email.com,example3@email.com B M 1800
```

### 3.2. Help argument <a name="howto-help"></a>

You can also use the help argument which will explain you how to use this script.

This argument must be in the first position, it can be `h`, `help` or `?`

```sh
python ./ouigo.py h
```

### 3.3. Mandatory arguments <a name="howto-mandatory"></a>

These are the mandatory arguments
- **date_to_filter**: Date to look for the ticket. You must use the format yyyy-mm-dd.
- **gmail_username**: Gmail user to send the email when a ticket available is found.
- **gmail_password**: Gmail password to login and send the email correctly.
- **email_recipients**: Comma listed emails to send the notification.
- **origin_city**: Trip departure city. You must use one of the following city codes.
  - B: BARCELONA
  - M: MADRID
  - T: TARRAGONA
  - V: VALENCIA
  - Z: ZARAGOZA
- **destination_city**: Trip destination city. You must use one of the following city codes.
  - B: BARCELONA
  - M: MADRID
  - T: TARRAGONA
  - V: VALENCIA
  - Z: ZARAGOZA

### 3.4. Optional arguments <a name="howto-optional"></a>

These are the optional arguments:
- **refresh_time**: Time (in seconds) to retry is there's no ticket available. _It's 1800 by default_

## 4. Docker <a name="docker"></a>

**ouigo-searcher** can also be executed using [docker](https://docs.docker.com/get-docker/).

### 4.1. Building the image <a name="docker-build"></a>

First of all, you need to create a **docker image** by running the following command:

```sh
docker build -t ouigo-searcher .
```

### 4.2. Running the script <a name="docker-run"></a>

When the image has been successfully created, you will be able to run the script in docker by running the following command:

```sh
docker run ouigo-searcher {{ ARGUMENTS }}
```

For example:

```sh
docker run ouigo-searcher 2022-12-31 example@gmail.com password123 example1@email.com,example2@email.com,example3@email.com B M 1800
```

### 4.3. Docker Hub repo <a name="docker-hub"></a>

There is also a **Docker Hub** repository with this docker image: [csanchezarisa/ouigo-searcher](https://hub.docker.com/r/csanchezarisa/ouigo-searcher).

You can pull it and use it by running the following command:

```sh
docker pull csanchezarisa/ouigo-searcher
```
```sh
docker run csanchezarisa/ouigo-searcher {{ ARGUMENTS }}
```
