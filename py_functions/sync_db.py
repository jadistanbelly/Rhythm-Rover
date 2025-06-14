from variables import user_audio_files

def sync_db():
    """Sync current user_audio_files to database"""
    import shelve
    
    with shelve.open('audio_paths') as db:
        db['user_audio_paths'] = dict(user_audio_files)
        print("Database synced successfully")
        print(f"Updated {len(user_audio_files)} user entries")

if __name__ == '__main__':
    sync_db()

