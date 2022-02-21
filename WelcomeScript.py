import os
from gtts import gTTS
import time

import jetson.inference
import jetson.utils

import random

#text to speech
welcomeMes=['Welcome back Milla', 'Hello Darren!','Hey Joan!', 'Wassup Milla!' , 'Have a good day!', 'I really appreciate you', 'You are a wonderful person', 'I really enjoy your company']
goAwayMes=['See you later', 'Have a blessed day', 'Come back soon!', 'Goodbye Milla', 'Sayonara Darren', 'See you later Joan!', 'Thank you for all you do!']

for genInd in range(len(welcomeMes)):
	myOutput=gTTS(text=welcomeMes[genInd], lang='en', slow=True)
	myOutput.save('WFfile'+str(genInd)+'.mp3')
for genInd in range(len(goAwayMes)):
	myOutput=gTTS(text=goAwayMes[genInd], lang='en', slow=True)
	myOutput.save('GAMfile'+str(genInd)+'.mp3')

for genInd in range(len(welcomeMes)):
	os.system('mpg123 WFfile'+str(genInd)+'.mp3')
for genInd in range(len(goAwayMes)):
	os.system('mpg123 GAMfile'+str(genInd)+'.mp3')

net = jetson.inference.detectNet('ssd-mobilenet-v2', threshold=0.6)
camera = jetson.utils.videoSource('/dev/video0')
#display = jetson.utils.videoOutput("display://0') #   'my_video.mp4' for file


timestamp = time.time()

while 1:  #display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	if len(detections)>0:
		for genInd in range(len(detections)):
			print(net.GetClassDesc(detections[genInd].ClassID))
			if detections[genInd].ClassID==1:
				if (time.time() - timestamp) > 5.0:
					if random.randrange(2)==0:
						#go away
						os.system('mpg123 GAMfile'+str(random.randrange(len(goAwayMes)))+'.mp3')
						time.sleep(0.2)
						timestamp = time.time()
						break
					#welcome
					os.system('mpg123 WFfile'+str(random.randrange(len(welcomeMes)))+'.mp3')
					time.sleep(0.2)
					timestamp = time.time()
					break
				timestamp = time.time()
	#reboot
	# display.Render(img)
	#display.SetStatus(


