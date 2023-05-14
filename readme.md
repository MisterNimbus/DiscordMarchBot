# Setting up the Bot
- Create a txt file with the name bot_token.txt and paste your bot token inside.
- Change the path of the DiscordMarchBot inside marsBot.py line 7 : folderPath.
- Go to ~/.config/autostart and create a new file with the name marsBot.desktop.
- Inside marsBot.desktop write the following: 
`
[Desktop Entry]
Type=Application
Name=MarsBot
Exec=xterm -hold -e '/usr/bin/python3 <folderPath>/marsBot.py'
`
You have to swap the folderPath with your folder path from step 2.  
- Make sure you have the following packages: ffmpeg, xterm, PyNaCl, discord.py. 
`
sudo apt-get install ffmpeg  
sudo apt-get install xterm -y  
pip install PyNaCl  
pip install discord.py  
`

# Warning
This is not meant for streaming of illegal content.  
It is meant for royalty-free audio only.  
Please comply to your local laws.   
No responsibility is taken by the authors.  
