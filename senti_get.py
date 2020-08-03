from textblob import *


import subprocess
import shlex
def RateSentiment(sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
    #Modify the location of SentiStrength.jar and D:/SentiStrength_Data/ if necessary
    p = subprocess.Popen(shlex.split("java -jar SentiStrengthCom.jar stdin sentidata SentiStrength_DataEnglishFeb2017/"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    #Can't send string in Python 3, must send bytes
    b = bytes(sentiString.replace(" ","+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)
    #convert from byte
    stdout_text = stdout_byte.decode("utf-8")
    #replace the tab with a space between the positive and negative ratings. e.g. 1    -5 -> 1 -5
    stdout_text = stdout_text.rstrip().replace("\t"," ").split(" ")
    # print(stdout_text)  + " " + sentiString
    return int(stdout_text[0]), int(stdout_text[1])
#An example to illustrate calling the process.


if __name__=="__main__":
    # str = "\n        To start off, I would like to say i&#39;m 17 years of age with anxiety and hypochondria (if that helps). (note: not a smoker)\r<br/>\r<br/>I&#39;ve been experiencing this productive cough for about a month and a half for now, it would get annoying and disgusting. Some of the time I&#39;ll do this really light cough, and cough out a mouth-full of Phlegm. The color would vary from White-Yellow-Green, and this makes me think if the mucus is backing down into my lungs from the nose. I would get these very very sharp pains in my chest, where I would have to grab my chest and then my chest becomes very cold for 5-10seconds. This would be frequent, about once a day and the anxiety is killing me. I&#39;ve been prescribed medications from Penicillin to Hydrocodone, Hydrocodone helped a little bit, but I don&#39;t want my mind to rely on it. (So I stopped) The walk-in clinic across from my house seems to not work, he would just keep prescribing me medication I never heard of, and gets more expensive each time.\r<br/>\r<br/>I wanted to have an xray on my chest, to rule out the major league viruses/diseases/cancers. But I&#39;m not on a drug plan, so the bills i&#39;m paying for is ridiculous. Hydrocodone was over 40$, and this is coming out of my well-earned pocket.\r<br/>\r<br/>Is there anyone here that can help me? I&#39;ve tried everything and getting scared and more anxious each day. It&#39;s impossible to ignore my breathing and I never breathe through my nose anymore, it&#39;s irritating. I have to breathe through my mouth, with it slightly open, I would say a centimeter from each lip. Thanks for the help\r<br/>\r<br/>Best Regards,\r<br/>Tyler Allison\n    "
    # str = str.strip('\n')
    # blob = TextBlob(str)
    # print(blob.sentiment)
    # print(blob.sentiment.polarity)
    # print(blob.sentences[0].sentiment)
    print(RateSentiment("A Love day is comming!"))
