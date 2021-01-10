#! /usr/bin/env python
import epd2in9b_V2
from PIL import Image, ImageFont, ImageDraw
import speedtest
import time
import tweepy
import os
import sys

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'BandMonitor2')
if os.path.exists(libdir):
    sys.path.append(libdir)
   
   
if sys.version_info[0] <3:
    raise Exception("Python 3 is the correct version that you NEED!!")  
   
   
   
font = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Thin.ttf', 14)
font2 = ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSans.ttf', 24)
font3 = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Light.ttf', 12)
font4 = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Thin.ttf', 10)
font5 = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Verdana_Bold.ttf', 23)


consumer_key="CHANGE THIS"
consumer_secret="CHANGE THIS"
access_token="CHANGE THIS"
access_token_secret="CHANGE THIS"



def GetSpeedInternet():
    print("Internet Speed Testing...")
    bw_down = 0
    bw_up = 0
    results_dict = 0
    ping = 0
    #TEST
    s = speedtest.Speedtest()
    print("Getting values...")
    print("  Server...")
    s.get_best_server()
    print("  Down...")
    bw_down = s.download()
    print("  UP...")
    bw_up = s.upload()
    results_dict = s.results.dict()
    print("  Ping...")
    ping = (results_dict['ping'])
    print("All gotten:")

    print("   bw_down :"+str(bw_down) )
    print("   bw_up :"+str(bw_up) )
    print("   results_dict :"+str(results_dict) )
    print("   ping :"+str(ping) )
    
    return bw_down, bw_up, results_dict, ping
    


def GetTwitter():
    print("Tweeter information")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print ('   Connecting...')
    api = tweepy.API(auth)
    print ('   Connected')

    user = api.get_user('EmiHermes')
    try:
        print('   ' + str(user.screen_name) + ' - ' + str(api.me().name.encode('utf8', errors='ignore')))
    except:
        print('   ' + user.screen_name)
        print('   ' + api.me().name)

    print('   Followers: ' + str(user.followers_count))

    return user.followers_count


def main():
    print('START >>' + time.strftime("%H:%M:%S,  %d.%m.%Y"))
    # Getting InternetSpeed
    (bw_down, bw_up, results_dict, ping) = GetSpeedInternet()
    
    followers = GetTwitter()

    '''
    followers = 979
    bw_down = 7184555.40273805
    bw_up = 2800526.4149017734
    #results_dict = 
    ping = 44.71
    '''

    '''
    bw_down = bw_down * 5
    bw_up = bw_up * 5
    ping = ping * 3
    '''

    print("Starting....")
    epd = epd2in9b_V2.EPD()
    print("  Init...")
    epd.init()
    print("  Clear...")
    epd.Clear()
    
    print("Image....")
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)

    print("Rectangle....")
    drawry.rectangle((0, 0, 295, 127), outline = 0)
    drawblack.rectangle((1, 1, 252, 42), fill = 0)
    drawblack.text((3, 6), 'Bandwidth Monitor', font = font5, fill = 255)
    drawry.text((186, 30), 'By EmiHermes', font = font4, fill = 0)
    
    current_time = time.strftime("%H:%M:%S,  %d.%m.%Y")
    drawry.text((6, 112), 'Tested @' + current_time, font=font3, fill=0)
  
    TweeterImage = Image.open(os.path.join(libdir, 'Tweeter.bmp'))
    HBlackimage.paste(TweeterImage, (253, 1))
  
    start_y = 45 #53
    offset_y1 = 19
    offset_y2 = 27
    offset_y3 = 47
    
    print('Ping: {:5.1f}'.format(ping))
    drawry.text((2, start_y), "Ping:", font=font, fill = 0)
    drawblack.text((6, start_y + offset_y1), ('{:5.1f}'.format(ping)), font=font2, fill = 0)
    drawblack.text((26, start_y + offset_y3), 'ms', font=font3, fill = 0)
    
    print('Down: {:5.2f}'.format(bw_down/1E6,2))
    drawry.text((96, start_y), "Download:", font=font, fill=0)
    drawblack.text((96, start_y + offset_y1), ('{:5.2f}'.format(bw_down/1E6,2)), font=font2, fill=0)
    drawblack.text((116, start_y + offset_y3), 'Mbps', font=font3, fill=0)
    
    print('Up: {:4.2f}'.format(bw_up/1E6,2))
    drawry.text((186, start_y), "Upload:", font=font, fill=0)
    drawblack.text((186, start_y + offset_y1), ('{:4.2f}'.format(bw_up/1E6,2)), font=font2, fill=0)
    drawblack.text((196, start_y + offset_y3), 'Mbps', font=font3, fill=0)
  
    print("Followers: " + str(followers))
    drawry.text((250, start_y + offset_y1), str(followers), font=font2, fill=0)
    drawblack.text((248, start_y + offset_y3), 'Followers', font=font3, fill=0)
  
    print("Display....")
    # display the frame
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    print("END!!")
    epd.sleep()
    print("Sleeping...")
    print('END >>' + time.strftime("%H:%M:%S,  %d.%m.%Y"))
    
    
if __name__ == '__main__':
    main()
