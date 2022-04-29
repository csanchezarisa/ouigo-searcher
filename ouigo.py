from requests import get
from time import sleep
from json import loads
from datetime import datetime
import smtplib, sys
from calendar import monthrange

# How to use the command: python ./ouigo.py <date_to_filter> <gmail_username> <gmail_password> <email_recipients> <origin_city> <destination_city> <refresh_time>
# Example: python ./ouigo.py 2022-12-31 example@gmail.com password123 example1@email.com,example2@email.com,example3@email.com B M 

SPECIFIC_DATE_TO_FILTER: str = ''

REFRESH_TIME: int = 1800

OUIGO_URL: str = ''
OUIGO_FROM: str = ''
OUIGO_TO: str = ''

FROM_CITY = ''
TO_CITY = ''

GMAIL_USER: str = ''
GMAIL_PASSWORD: str = ''

EMAIL_TO: list[str] = []
EMAIL_SUBJECT: str = ''
EMAIL_BODY: str = ''

EMAIL_TEXT: str = ''


def main() -> None:
    """Main function"""

    readConsoleArguments(sys.argv[1:])
    
    print(getCurrentTime(), 'Ouigo script started')

    setVariables()

    while True:
        if checkOuigoTicket():
            break

        sleep(REFRESH_TIME)

    print(getCurrentTime(), 'Exiting')

    sys.exit(0)


def checkOuigoTicket() -> bool:
    """
    Requests and checks if the specific ticket exists in ouigo.
    If it exists, sends an email using the gmail user and password.
    Otherwise, sleeps the specified time and tries again.

    Return
    ------
    ticket_found : bool
        bool value, if the ticket exists or not
    """

    response = get(OUIGO_URL)
    
    if len(response.content) == 0:
        print(getCurrentTime(), 'This ticket doesn\'t exist')
        return False
    
    travel_list = loads(response.content)

    filtered_travel = None

    for travel in travel_list:
        if travel['date'] == SPECIFIC_DATE_TO_FILTER:
            filtered_travel = travel
            break

    if filtered_travel['price'] != None:
        print(getCurrentTime(), 'This ticket exists')

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, EMAIL_TO, EMAIL_TEXT)
        server.close()

        print(getCurrentTime(), 'Email sent')
        return True
    else:
        print(getCurrentTime(), 'This ticket doesn\'t exist')
        return False


def getCurrentTime() -> str:
    """Return the current date to log the prints"""

    return datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - '


def setVariables() -> None:
    """Sets the variables content to do the request and create the email"""

    global OUIGO_URL, EMAIL_SUBJECT, EMAIL_BODY, EMAIL_TEXT, FROM_CITY, TO_CITY, GMAIL_USER

    begin_date, end_date = getRangeTime(SPECIFIC_DATE_TO_FILTER)

    # Ouigo variables
    OUIGO_URL = f'https://api-search-es.ouigo.com/api/calendar/pricesEdito?passengers%5B0%5D%5Btype%5D=A&direction=inbound&origin={OUIGO_FROM}&destination={OUIGO_TO}&begin={begin_date}&end={end_date}'

    # Email variables
    EMAIL_SUBJECT = f'BILLETE DE OUIGO {FROM_CITY} - {TO_CITY} DISPONIBLE'
    EMAIL_BODY = f'Existen tickets para el viaje de {FROM_CITY} a {TO_CITY} para el dia {SPECIFIC_DATE_TO_FILTER}'
    EMAIL_TEXT = "\r\n".join((
"From: %s" % GMAIL_USER,
"To: %s" % EMAIL_TO,
"Subject: %s" % EMAIL_SUBJECT ,
"",
EMAIL_BODY
))


def getRangeTime(date: str) -> tuple[str]:
    """
    Returns the first and last day of the month from the given date
    
    Parameters
    ----------
    date : str
        String date with yyyy-mm-dd format

    Return
    ------
    (begin_date, end_date) : tuple[str]
        First and last dates of the month
    """

    date = date.split('-')

    week_day, last_day = monthrange(int(date[0]), int(date[1]))

    begin_date = f'{date[0]}-{date[1]}-01'
    end_date = f'{date[0]}-{date[1]}-{last_day}'

    return (begin_date, end_date)


def readConsoleArguments(args: list[str]) -> None:
    """
    Reads the console arguments to setup the variables

    Parameters
    ----------
    args : str
        String list with the console arguments. It canno't be empty
    """

    global SPECIFIC_DATE_TO_FILTER, GMAIL_USER, GMAIL_PASSWORD, OUIGO_FROM, FROM_CITY, OUIGO_TO, TO_CITY, EMAIL_TO

    # Controls the arguments length
    if len(args) == 0:
        print('ERROR!\n6 arguments are necesary. Use the argument "h" to get help.')
        sys.exit(1)

    # HELP command
    if args[0] in ('h', 'help', '?'):
        help()
        sys.exit(0)

    # Controls that the minimum parameters are specified
    if len(args) < 6:
        print('ERROR!\n6 arguments are necesary. Use the argument "h" to get help.')
        sys.exit(1)

    SPECIFIC_DATE_TO_FILTER = args[0]
    GMAIL_USER = args[1]
    GMAIL_PASSWORD = args[2]
    OUIGO_FROM, FROM_CITY = getCity(args[4])
    OUIGO_TO, TO_CITY = getCity(args[5])
    
    try:
        EMAIL_TO = args[3].split(',')
    except Exception:
        print('ERROR!\nEmail recipients list is not well formatted. Use the argument "h" to get help.')
        sys.exit(1)

    # Check if there's only 6 arguments "finish" this method
    # If there're more arguments, they'll be used 
    if len(args) == 6:
        return

    try:
        REFRESH_TIME = int(args[6])
    except Exception:
        REFRESH_TIME = 1800


def getCity(first_letter: str) -> tuple[str]:
    """
    Translates the city code to the ouigo ID

    Parameters
    ----------
    first_letter : str
        City code

    Return
    ------
    (code, city) : tuple[str]
        Ouigo ID used to specify the city and city name
    """

    first_letter = first_letter[0].capitalize()

    code: str = ''
    city: str = ''

    # Barcelona
    if first_letter == 'B':
        code = '7171801'
        city = 'BARCELONA'

    # Madrid
    elif first_letter == 'M':
        code = 'MT1'
        city = 'MADRID'

    # Zaragoza
    elif first_letter == 'Z':
        code = '7104040'
        city = 'ZARAGOZA'

    # Tarragona
    elif first_letter == 'T':
        code = '7104104'
        city = 'TARRAGONA'

    # This city does not exist
    else:
        print(f'ERROR!\n{first_letter} city does not exist. Check the correct codes using the "h" arguments.')
        sys.exit(1)

    return (code, city)


def help() -> None:
    """
    Prints help in the console. 
    It shows how to use this script.
    """

    # Introduction
    print('This script checks if there\'re available tickets on ouigo for a specific trip and date. If they are, it will send an email, '\
        'otherwise it will wait for a specific time and then try again.\n')
    print(f'Syntax: python {__file__} <date_to_filter> <gmail_username> <gmail_password> <destination_emails> <origin_city> <destination_city> <refresh_time>\n')

    # Arguments
    print('arguments:')
    print('\tdate_to_filter (mandatory)\tDate to look for the ticket. You must use the format yyyy-mm-dd.')
    print('\tgmail_username (mandatory)\tGmail user to send the email when a ticket available is found.')
    print('\tgmail_password (mandatory)\tGmail password to login and send the email correctly.')
    print('\temail_recipients (mandatory)\tComma listed emails to send the notification.')
    print('\torigin_city (mandatory)\t\tTrip departure city. You must use one of the following city codes.')
    print('\t\tcity codes:')
    print('\t\t\tB: BARCELONA')
    print('\t\t\tM: MADRID')
    print('\t\t\tZ: ZARAGOZA')
    print('\t\t\tT: TARRAGONA')
    print('\tdestination_city (mandatory)\tTrip destination city. You must use one of the following city codes.')
    print('\t\tcity codes:')
    print('\t\t\tB: BARCELONA')
    print('\t\t\tM: MADRID')
    print('\t\t\tZ: ZARAGOZA')
    print('\t\t\tT: TARRAGONA')
    print('\trefresh_time\t\t\tTime (in seconds) to retry is there\'s no ticket available.\n')
    
    # Example
    print(f'Example: python {__file__} 2022-12-31 example@gmail.com password123 example1@email.com,example2@email.com,example3@email.com B M 1800')


if __name__ == '__main__':
    main()
