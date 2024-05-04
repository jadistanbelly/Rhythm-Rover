# Rhythm Rover

Rythm Rover is a Discord bot that plays audio files when users join or leave a voice channel. Users can register an intro or outro using `/intro` or `/outro` commands. They can also completely wipe any saved audio by using the `/delete` command.

Intro Example            |  Outro Example
:-------------------------:|:-------------------------:
![Intro](images/intro.gif)  |  ![Outro](images/outro.gif)

## Features

- Plays audio files for user interactions in voice channels.
- Register custom intro and outro audio clips.
- Delete saved audio clips associated with a user.
- Wide range of websites are supported for registering an audio clip

## Usage

1. **Setup:**
   - Clone the repository.
   - Install the required dependencies using the given requirements.txt file.
   - Get the bot token and setup intents on Developer Portal.
   - Configure the bot token and other settings in `configs.py`.

2. **Running the Bot:**
   - Start the bot using `python bot.py`.

3. **Commands:**
   - `/intro`: Register an intro audio clip.
        - video_url = paste the link you would like to download
        - start = give the start time for the clip.
            - This can be in any format (SS) or (HH:MM:SS)
        - end = give the end time for the clip.
            - This can be in any format (SS) or (HH:MM:SS)
   - `/outro`: Register an outro audio clip.
        - video_url = paste the link you would like to download
        - start = give the start time for the clip.
            - This can be in any format (SS) or (HH:MM:SS)
        - end = give the end time for the clip.
            - This can be in any format (SS) or (HH:MM:SS)
   - `/delete`: Delete all saved audio clips for the user.
   - `/kill`: Clear bots audio queue to prevent spamming (owner only).
   - `!sync`: sync changes to tree commands (owner only).

## OAuth2

| Permissions                  | Privileged Gateway Intents | Scopes                 |
|------------------------------|----------------------------|------------------------|
| Create Events                | Presence Intent            | applications.commands  |
| Create Expressions           | Message Content Intent     | bot                    |
| Read Messages/View Channels  | Server Members Intent      |                        |
| Mention @everyone, @here, and All Roles |                            |                        |
| Use Application Commands     |                            |                        |
| Send Messages                |                            |                        |
| Connect                      |                            |                        |
| Speak                        |                            |                        |
| Use Voice Activity           |                            |                        |

**Note:**

All these permissions are likely not required I initially was testing various features and used these intents.

Here is the authorization link used:

[https://discord.com/oauth2/authorize?client_id=(**INPUT_YOUR_CLIENT_ID_HERE**)&permissions=**26390463384576**&scope=**applications.commands+bot**](https://discord.com/oauth2/authorize?client_id=(INPUT_YOUR_CLIENT_ID_HERE)&permissions=26390463384576**&scope=applications.commands+bot)

## Contributing

Feel free to contribute to the project by submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/jadistanbelly/Rhythm-Rover?tab=MIT-1-ov-file) file for details.

## Support

For any issues or questions, please reach out via [Email](mailto:jadistanbelly@outlook.com) or [Github](https://github.com/jadistanbelly/Rhythm-Rover/issues).
