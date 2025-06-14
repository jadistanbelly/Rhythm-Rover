import hashlib
import json
import os
import time

def create_stable_hash(title):
    """Create a stable hash from a title that works with any characters"""
    # Use first 8 characters of MD5 hash
    return hashlib.md5(title.encode('utf-8')).hexdigest()[:8]

def update_hash_lookup(hash_id, original_title, url, output_path):
    """Update the hash lookup file with new entries"""
    lookup_file = os.path.join(output_path, 'title_hash_lookup.json')
    lookup_data = {}
    
    if os.path.exists(lookup_file):
        with open(lookup_file, 'r', encoding='utf-8') as f:
            lookup_data = json.load(f)
    
    lookup_data[hash_id] = {
        'title': original_title,
        'url': url,
        'created': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open(lookup_file, 'w', encoding='utf-8') as f:
        json.dump(lookup_data, f, indent=2, ensure_ascii=False)

def get_hash_lookup(hash_id, output_path):
    """Get the original title and metadata for a hash ID"""
    lookup_file = os.path.join(output_path, 'title_hash_lookup.json')
    if os.path.exists(lookup_file):
        with open(lookup_file, 'r', encoding='utf-8') as f:
            lookup_data = json.load(f)
            return lookup_data.get(hash_id)
    return None
