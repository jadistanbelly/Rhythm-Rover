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
   - Configure the bot token and other settings in `configs.py`.

2. **Commands:**
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
   - `/sync` or `!sync`: sync changes to commands (owner only).

3. **Running the Bot:**
   - Start the bot using `python bot.py`.

## Contributing

Feel free to contribute to the project by submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/jadistanbelly/Rhythm-Rover?tab=MIT-1-ov-file) file for details.

## Support

For any issues or questions, please reach out via [Email](mailto:jadistanbelly@outlook.com) or [Github](https://github.com/jadistanbelly/Rhythm-Rover/issues).
