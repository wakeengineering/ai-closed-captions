import requests

def get_anime_prompt(anime_title, limit=900):
    url = 'https://graphql.anilist.co'
    
    # Query for Main Characters, Tags (Powers/Concepts), and Title
    query = '''
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        title { romaji english }
        tags { name }
        characters (sort: ROLE, perPage: 25) {
          nodes { name { full } }
        }
      }
    }
    '''
    
    variables = {'search': anime_title}
    
    try:
        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()['data']['Media']
        
        # 1. Build list from Title, Characters, and Tags
        prompt_parts = []
        prompt_parts.append(data['title']['romaji'])
        prompt_parts.append(data['title']['english'])
        
        # Add character names
        prompt_parts.extend([c['name']['full'] for c in data['characters']['nodes']])
        
        # 2. Join into comma-separated string and deduplicate
        full_prompt = ", ".join(list(dict.fromkeys(prompt_parts)))
        
        # 3. Truncate to limit (ensuring it ends at a clean comma if possible)
        if len(full_prompt) > limit:
            truncated = full_prompt[:limit]
            return truncated[:truncated.rfind(',')]
        
        return full_prompt
        
    except Exception as e:
        return f"Error fetching data: {e}"

# Example Usage:
anime_name = "Kill La Kill" # Replace with any anime title
whisper_prompt = get_anime_prompt(anime_name)
print(f"Prompt ({len(whisper_prompt)} chars):\n{whisper_prompt}")
