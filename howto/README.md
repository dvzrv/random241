HOWTO build an Americium 241 driven random number generator
===========================================================

As a showcase I'll demonstrate the creation of my device below.
You'll need a couple of things to build an Americium 241 driven random number generator (RNG). Read through **all of this** before starting!

###First things first though

**[Americium 241](http://en.wikipedia.org/wiki/Americium) is NOT A TOY!**
It's a transuranic radioactive chemical element. Respect working with it:

- Do not swallow it
- Don't wear it on your body
- Avoid touching it
- At best work in a safe environment (like a lab)
- Do not eat while working with it
- Keep in a closed steel or aluminium container, when not working with it

This being said, **I am not** responsible for any harm inflicted on you due to mal-handling of Americium 241!
Don't be a fool, work responsibly!

###Materials

####Americium 241
If you're living in the Americas, you'll most likely still have [ionization smoke detectors](http://en.wikipedia.org/wiki/Americium#Ionization_detectors) around. For (mostly) everyone else, there's the possibility of ordering Americium on ebay!
As I live in Germany I opted for the second option (ionization detectors are not used in private households anymore). My sample came in a nice and useful shape:
![Americium 241 sample, ordered on ebay](https://raw2.github.com/davezerave/random241/master/howto/IMG_6536.JPG)

It's a small sample of 4mm diameter in a steel casing.

####Webcam
You can basically use any webcam for this project. There are some things to keep in mind though:
- You will break it!
- Don't use cameras below 2 megapixels (your resolution won't be of any use)
- Make sure you'll be able to open it up and remove its lens!

In my case a Mustek Gsmart Mini 3 has been used, because [Gabriel Zöller](https://github.com/fahrstuhl) wanted to get rid of his and it was broken in just a beautiful and fitting way (with the lens already removed):
![Gsmart Mini 3](https://raw2.github.com/davezerave/random241/master/howto/IMG_6537.JPG)


####Casing
Make sure you'll have a proper casing around for the sample to store in and later for the camera and the sample to store (or build into for that matter).
I used a steel casing from an old 19" server rack power supply, that was trashed at work:
![19" rack server power supply](https://raw2.github.com/davezerave/random241/master/howto/IMG_6761.JPG)


###Building the RNG
It is highly recommended to use nippers when handling the Americium 241 sample:
![Americium 241 sample on steel](https://raw2.github.com/davezerave/random241/master/howto/IMG_6543.JPG)

The lens mount has a certain diameter. To not have the sample fall on top of the camera chip, I drilled a hole into and cut out a piece of steel to be used as a curb for the sample (as you can see in the picture below).
![Americium 241 sample with curb](https://raw2.github.com/davezerave/random241/master/howto/IMG_6547.JPG)

Now the sample was put on top of the lens mount with the Americium pointing directly at the chip.
![Americium 241 sample over webcam sensor chip](https://raw2.github.com/davezerave/random241/master/howto/IMG_6549.JPG)

You might have to improvise a little - depending on your hardware - to make things work. [Sugru](http://sugru.com/about/) was my friend, fixing the sample over the camera chip. I know, it looks ugly, but it certainly gets the job done!
![Americium 241 sample covered with Sugru, fixed over webcam sensor chip](https://raw2.github.com/davezerave/random241/master/howto/IMG_6550.JPG)

**Note of advice**
Unfortunately (for me), the Gsmart Mini 3 is not a webcam, but can be used as one, if you press a button on the backside of it, while connected via USB. As I don't want to open a box and press a button on a camera with an Americium 241 sample in it, every time I want to use it, I had to solder a push button switch to it.
That turned out to be quite a messy job (because the button is very tiny and so are its contacts on the board). If you end up with the same model of camera, do this first, before you place the sample on top of the sensor chip!

After that was done, I was able to place the camera in the above mentioned casing, while leading the USB and push button switch cable out.
![Americium 241 sample on camera in open casing](https://raw2.github.com/davezerave/random241/master/howto/IMG_6757.JPG)
As you can see here, I had to use two additional steel panels to complete the casing in front and back of the box.
The box is made from steel panels all around otherwise, but had some open spaces in front and back (for air circulation in its previous use-case-scenario).
This device is now USB pluggable and on/off switchable!
