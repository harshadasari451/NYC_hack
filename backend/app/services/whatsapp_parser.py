import re
from datetime import datetime
from typing import Optional


class WhatsAppParser:
    """
    Parses WhatsApp exported .txt chat files.
    
    Supports formats:
    - [12/25/23, 10:30:45 AM] Sender: Message
    - 12/25/23, 10:30 AM - Sender: Message
    - [2023-12-25, 10:30:45] Sender: Message
    """
    
    # Common WhatsApp export patterns
    PATTERNS = [
        # [MM/DD/YY, HH:MM:SS AM/PM] Sender: Message
        r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?::\d{2})?\s*[APap][Mm])\]\s*(.+?):\s*(.*)',
        # MM/DD/YY, HH:MM AM/PM - Sender: Message
        r'(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?::\d{2})?\s*[APap][Mm])\s*-\s*(.+?):\s*(.*)',
        # [YYYY-MM-DD, HH:MM:SS] Sender: Message
        r'\[(\d{4}-\d{2}-\d{2},\s*\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.+?):\s*(.*)',
        # DD/MM/YYYY, HH:MM - Sender: Message
        r'(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2})\s*-\s*(.+?):\s*(.*)',
    ]
    
    # System messages to skip
    SYSTEM_PATTERNS = [
        r'messages and calls are end-to-end encrypted',
        r'created group',
        r'added you',
        r'changed the subject',
        r'changed this group',
        r'left$',
        r'removed ',
        r'changed the group',
        r'pinned a message',
        r'deleted this message',
    ]
    
    MEDIA_PATTERNS = [
        r'<media omitted>',
        r'image omitted',
        r'video omitted',
        r'audio omitted',
        r'sticker omitted',
        r'document omitted',
        r'GIF omitted',
        r'Contact card omitted',
    ]
    
    def __init__(self, target_person: str):
        """
        Initialize parser with the target person's name.
        
        Args:
            target_person: The name to filter messages by (as it appears in WhatsApp)
        """
        self.target_person = target_person.strip()
        self.messages = []
        self.all_messages = []
        self.senders = set()
    
    def parse(self, content: str) -> dict:
        """
        Parse WhatsApp export text content.
        
        Returns:
            dict with parsed messages, stats, and metadata
        """
        lines = content.split('\n')
        current_message = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parsed = self._parse_line(line)
            
            if parsed:
                # Save previous message
                if current_message:
                    self._add_message(current_message)
                current_message = parsed
            elif current_message:
                # Multi-line message continuation
                current_message['content'] += '\n' + line
        
        # Don't forget the last message
        if current_message:
            self._add_message(current_message)
        
        return self._build_result()
    
    def _parse_line(self, line: str) -> Optional[dict]:
        """Try to parse a line as a WhatsApp message."""
        for pattern in self.PATTERNS:
            match = re.match(pattern, line)
            if match:
                timestamp, sender, content = match.groups()
                
                # Skip system messages
                if self._is_system_message(content):
                    return None
                
                # Check for media
                is_media = self._is_media_message(content)
                
                return {
                    'timestamp': timestamp.strip(),
                    'sender': sender.strip(),
                    'content': content.strip(),
                    'is_media': is_media,
                }
        return None
    
    def _is_system_message(self, content: str) -> bool:
        """Check if message is a system notification."""
        content_lower = content.lower()
        return any(re.search(p, content_lower) for p in self.SYSTEM_PATTERNS)
    
    def _is_media_message(self, content: str) -> bool:
        """Check if message is a media placeholder."""
        content_lower = content.lower()
        return any(re.search(p, content_lower) for p in self.MEDIA_PATTERNS)
    
    def _add_message(self, msg: dict):
        """Add a parsed message to the collections."""
        self.all_messages.append(msg)
        self.senders.add(msg['sender'])
        
        # Filter for target person's messages only
        if msg['sender'].lower() == self.target_person.lower():
            if not msg['is_media']:
                self.messages.append(msg)
    
    def _build_result(self) -> dict:
        """Build the final parsed result."""
        # Extract emoji patterns from target person's messages
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\ufe0f"
            "\u3030"
            "]+",
            flags=re.UNICODE,
        )
        
        all_emojis = []
        for msg in self.messages:
            found = emoji_pattern.findall(msg['content'])
            all_emojis.extend(found)
        
        # Count emoji frequency
        emoji_freq = {}
        for emoji in all_emojis:
            emoji_freq[emoji] = emoji_freq.get(emoji, 0) + 1
        
        top_emojis = sorted(emoji_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'target_person': self.target_person,
            'total_messages': len(self.all_messages),
            'target_messages': len(self.messages),
            'all_senders': list(self.senders),
            'messages': self.messages,
            'top_emojis': top_emojis,
            'sample_messages': [m['content'] for m in self.messages[:50]],
        }
