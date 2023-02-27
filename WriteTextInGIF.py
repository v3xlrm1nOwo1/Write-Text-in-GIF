from PIL import Image, ImageDraw, ImageSequence, ImageFont
import io, PIL, os


gif = input("Enter GIF name: ")
text = input("Enter The Text: ")
size = int(input("Enter size: "))
backgroud = int(input("1 - Black\n2 - White\n: "))
if backgroud == 1:
    backgroud_color = (0, 0, 0)
    text_color = (255, 255, 255)
else:
    backgroud_color = (255, 255, 255)
    text_color = (0, 0, 0)

gif = os.path.abspath(f"Projects/Write Text in GIF/GIF/{gif}.gif")
im = Image.open(gif) 

# A list of the frames to be outputted
frames = []
# Loop over each frame in the animated image
for frame in ImageSequence.Iterator(im):
    
    # Creat black image
    create_im = PIL.Image.new(mode="RGB", size=(frame.size[0], frame.size[1] // 4), color=backgroud_color)
    # size = frame.size[0] // 40
    # Merge images vertically
    total_width = frame.size[0]
    max_height = frame.size[1] + frame.size[1] // 5

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in [create_im, frame]:
        new_im.paste(im, (0, x_offset))
        x_offset += im.size[1]
    
    # Draw the text on the frame
    d = ImageDraw.Draw(new_im)
    x = (new_im.size[0] // 2) - ((new_im.size[0] // 2) // 2)
    y = 50 - (50//2)
    
    font = ImageFont.truetype("arial.ttf", size=size)
    
    d.text((x, y), text, align="center", font=font, fill=text_color) # left: (0, 0)
    del d

    # However, 'frame' is still the animated image with many frames
    # It has simply been seeked to a later frame
    # For our list of frames, we only want the current frame

    # Saving the image without 'save_all' will turn it into a single frame image, and we can then re-open it
    # To be efficient, we will save it to a stream, rather than to file
    b = io.BytesIO()
    new_im.save(b, format="GIF")
    frame = Image.open(b)

    # Then append the single frame image to a list of frames
    frames.append(frame)
# Save the frames as a new image
frames[0].save('out.gif', save_all=True, append_images=frames[1:])

