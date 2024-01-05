import csv
import re
from datetime import datetime, timezone
from dateutil.tz import tzlocal
from bprint import bprint
from telethon import TelegramClient
from pathlib import Path
from telethon.errors import ApiIdInvalidError, UsernameInvalidError

class Sleuth:
    def __init__(
            self,
            api_id,
            api_hash: str,
            group_username,
            start_date=None,
            end_date=None,
            download_path:str=None,
            print_to_console:bool=False
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.group_username = group_username
        self.start_date = start_date
        self.end_date = end_date
        self.print_to_console = print_to_console

        if not download_path:
            download_path = Path.cwd()

        self.__base_path = fr"{download_path}\{group_username}"
        self.__download_paths = [
            fr"{self.__base_path}\images",
            fr"{self.__base_path}\videos",
            fr"{self.__base_path}\audios",
            fr"{self.__base_path}\documents",
            fr"{self.__base_path}\others",
        ]
        self.__data_dict = {}
        self.__messages = []
        self.__client = TelegramClient('history_extractor', self.api_id, self.api_hash)

    '''
    Example Output:
        2023-11-20 15:32:10+00:00 - john_doe: Hello everyone!
        2023-11-20 15:35:12+00:00 - john_doe sent an image: downloads/images/image1.jpg
    '''
    def dig(self) -> dict:
        # return dict of messages
        try:
            self.__validate_date()
            self.__check_download_path()
            self.__client.start()

            async def get_messages():  # Create a get messages coroutine
                print('Extracting messages...')
                async for message in self.__client.iter_messages(
                        self.group_username,
                        offset_date=self.start_date,
                        reverse=True  # Fetch messages in ascendingly
                ):
                    if not message:  # Break if there are no more messages
                        break

                    # handle if end date condition true, should stop the app
                    if self.start_date and self.end_date:
                        if message.date.astimezone(timezone.utc) == self.end_date:  # Exit if we've reached the end date
                            exit()

                    if message.sender is not None and message.text is not None:  # Print the message if it has a sender
                        username = message.sender.username
                        message_date = message.date.astimezone(tzlocal())
                        clean_message = (f'{(message.date.astimezone(tzlocal()))} - {message.sender.username}:'
                                         f' {message.text}')
                        attached_file = None

                        if message.file is not None:  # Check if the message has a file
                            file_type = message.file.mime_type.split('/')[0]  # Get the file type
                            download_path = self.__get_download_path(file_type)  # Get appropriate downloaded item path or default

                            file = await message.download_media(file=download_path)  # Download the file
                            attached_file = f'{username} sent an {file_type}: {file}'

                        if username not in self.__data_dict:
                            self.__data_dict[username] = []

                        self.__data_dict[username].append({str(message_date):message.text})
                        self.__messages.append(clean_message)

                        if attached_file:
                            self.__messages.append(attached_file)

                        if self.print_to_console == True:
                            bprint(clean_message)
                            if attached_file:
                                bprint(attached_file)

            self.__client.loop.run_until_complete(get_messages())  # Run the coroutine
            self.__client.disconnect()  # Disconnect the client
            print('Done!')
            return self.__data_dict
        except ValueError as e:  # Catch an error
            raise f"Error -> {e}"
        except Exception as error: # Catch an exception
            raise error
        except ApiIdInvalidError as invalid_api:  # catch if api_id or api_hash is invalid
            raise invalid_api
        except UsernameInvalidError as invalid_username:  # catch if the given group username is invalid
            raise invalid_username

    def export_to_csv(self, output_path: str):
        """
        Convert a dict to a CSV file.
        Args: output_path: The path to the output CSV file.
        Returns: None.
        """
        with open(output_path, "w",newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write data from list to csv
            for message in self.__messages:
                csv_writer.writerow([message])

    def __validate_date(self):
        date_pattern = '^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'

        if not re.match(date_pattern, self.start_date) and not re.match(date_pattern, self.end_date):
            print('Invalid date format. (example: 1999-09-09)')
            exit()
        self.start_date = (datetime.strptime(self.start_date, '%Y-%m-%d')
                           .replace(hour=0, minute=0, second=0, microsecond=0)).astimezone(timezone.utc)
        self.end_date = (datetime.strptime(self.end_date, '%Y-%m-%d')
                         .replace(hour=11, minute=59, second=59, microsecond=59)).astimezone(timezone.utc)

    def __get_download_path(self, file_type):
        return {
            'image': self.__download_paths[0],
            'video': self.__download_paths[1],
            'audio': self.__download_paths[2],
            'documents': self.__download_paths[3],
        }.get(file_type, self.__download_paths[4])

    def __check_download_path(self):
        if not self.__base_path:
            self.__base_path = Path.cwd()

        if not Path(self.__base_path).exists():
            Path(self.__base_path).mkdir(parents=True)
        for download_path in self.__download_paths:
            Path(download_path).mkdir(parents=True, exist_ok=True)