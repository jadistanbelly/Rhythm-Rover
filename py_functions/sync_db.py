from variables import user_audio_files, audio_db 

def sync_db():
    audio_db['user_audio_paths'] = user_audio_files # Update database
    audio_db.sync() # Sync database

