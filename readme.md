# Setting up the Bot
- Create a txt file with the name bot_token.txt and paste your bot token inside.
- Change the path of the DiscordMarchBot inside marsBot.py line 7 : folderPath.
- Go to ~/.config/autostart and create a new file with the name marsBot.desktop.
- Inside marsBot.desktop write the following  
  (You have to swap the folderPath with your folder path from step 2.)  :  
    `[Desktop Entry]`  
    `Type=Application`  
    `Name=MarsBot`  
    `Exec=xterm -hold -e '/usr/bin/python3 <folderPath>/marsBot.py'`  

- Make sure you have the following packages: 
    1. ffmpeg:    `sudo apt-get install ffmpeg`  
    2. xterm      `sudo apt-get install xterm -y`  
    3. PyNaCl     `pip install PyNaCl`  
    4. discord.py `pip install discord.py`  


# Warning
This is not meant for streaming of illegal content.  
It is meant for royalty-free audio only.  
Please comply to your local laws.   
No responsibility is taken by the authors.  
