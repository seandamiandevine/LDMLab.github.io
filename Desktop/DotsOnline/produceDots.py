from PIL import Image, ImageDraw, ImageFont

# create list of rgb values 
reds = range(100)
greens = [0] * 100
blues = range(155,255)[::-1]
colors = []
for i in range(100):
    colors.append(list([reds[i],greens[i],blues[i]]))

# Set constants for circle
path = "C:/Users/LSDMlab_RA/Desktop/OnlineExperiments/stim/" # path to save images to 
r = 200 # radius
x = 400 # x coordinate
y = 400  # y coordinate

for c in colors: 
    blueness = c[2] # how blue the stimuli is 
    
    image = Image.new('RGBA', (x*2, y*2), (0,0,0,0)) # fourth zero is for transparency
    draw = ImageDraw.Draw(image)
    leftUpPoint = (x-r, y-r)
    rightDownPoint = (x+r, y+r)
    twoPointList = [leftUpPoint, rightDownPoint]
    draw.ellipse(twoPointList, fill=(c[0],c[1],c[2]))

    image.save(path+'{}.png'.format(blueness))