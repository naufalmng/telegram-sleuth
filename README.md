
![Logo](https://i.ibb.co/ScGGXZL/sleuth.png)
# Sleuth: Powerful telegram message extractor
**Telegram Group Sleuth** is a powerful tool designed for extracting and analyzing data from Telegram group chats. Whether it's public or private groups, this tool allows you to efficiently extract messages, media, and metadata for thorough analysis.

The extracted data can be organized chronologically by user, and media files can be downloaded into designated folders for offline access. Additionally, the parsed data can be exported into a structured CSV file, facilitating further processing and integration with other tools.


## Features

- #### Extract messages, media, and metadata from public or private Telegram groups.
- #### Organize messages chronologically by user for easy analysis.
- #### Download shared media files (images, videos, audio, documents) into designated folders for offline access.
- #### Export parsed data into a structured CSV file for further processing and integration with other tools.


## Where to get it
The source code is hosted on GitHub at: https://github.com/naufalmng/telegram-group-sleuth

Install with PyPI

```bash
  pip install telegram-group-sleuth
```
    
## Usage

```javascript
from telegram_sleuth import Sleuth

# Authenticate with your Telegram API credentials
sleuth = Sleuth(
    api_id='YOUR_API_ID',
    api_hash='YOUR_API_HASH',
    group_username='TARGET_GROUP_USERNAME',
    start_date='2023-11-20',  # Optional: Specify a start date for data extraction
    end_date='2023-11-21',    # Optional: Specify an end date for data extraction
    download_path='/path/to/download/folder',  # Optional: Set a custom download path
    print_to_console=True  # Optional: Print messages to the console as they are extracted
)

# Extract messages and media
data = sleuth.dig()

# Export extracted data to a CSV file
sleuth.export_to_csv('group_chat_data.csv')
```


## Functions
- #### Sleuth(api_id, api_hash, group_username):
    **Purpose:** Initializes the Sleuth object for interacting with Telegram.

  | **Parameters**   | ⠀                                                                                         |
  |------------------|-------------------------------------------------------------------------------------------|
  | *api_id*         | Your Telegram API ID (required). you can get it on https://my.telegram.org/apps.          |
  | *api_hash*       | Your Telegram API hash (required). same source as api_id.                                 |
  | *group_username* | The username of the target Telegram group (required). regularly it's on the group's info. |

  | **Optional Parameters** | ⠀                                                                                                     |
  |-------------------------|-------------------------------------------------------------------------------------------------------|
  | *start_date*            | A string in the format 'YYYY-MM-DD' to specify a start date for data extraction (default: None).      |
  | *end_date*              | A string in the format 'YYYY-MM-DD' to specify an end date for data extraction (default: None).       |
  | *download_path*         | A path to a directory where downloaded media will be saved (default: None).                           |
  | *print_to_console*      | A boolean indicating whether to print messages to the console as they are extracted (default: False). |

- #### dig():
    **Purpose:** Extracts messages, media, and metadata from the specified group chat.

    **Returns:** A python dictionary containing the extracted information.
- #### export_to_csv(file_path):    
    **Purpose:** Exports the extracted data to a CSV file.
    **Parameter:**| ⠀
    -|-
    *file_path*|The path to the CSV file where the data will be saved.
## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)


## Support

For support, email naufalmng@gmail.com or create an issue on github page, https://github.com/naufalmng/telegram-group-sleuth/issues.

