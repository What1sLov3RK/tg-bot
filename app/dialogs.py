from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:
    test: str = "Привет {name}. Работаю..."
    start_new_user: str = 'Hi! {0}, Im music bot!\n Use buttons below to find songs'
    starting_shazam: str = "Lets do a little Shazam!"
    shazam_wrong_message_type:str = "You must send voice message!"
    back_to_main_menu: str = "Ok"
    lyrics_search_start: str = "Send some words from song pls"
    lyrics_search_no_matches: str = "No matches, sorry😥, repeat pls"
    song_download: str = "Send song name or author's name"






msg = Messages()