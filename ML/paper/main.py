from PIL import Image, ImageDraw, ImageFont, ImageOps
import click

image = Image.open('gazette.jpg').convert("RGBA")

count = 1
deep = 0

font = ImageFont.truetype('arial.ttf', 15)
text_color = (0, 0, 0)

(width, height) = image.size
draw = ImageDraw.Draw(image)


def add_new_layer(image_layer, description):
    im = Image.open(image_layer).convert("RGBA")
    im.thumbnail((200, 200))
    font = ImageFont.truetype('arial.ttf', 15)
    x_pos = 0
    y_pos = 0
    yt_pos = 0

    description = description[0:30] + '\n' + description[30:60] + '\n' + \
        description[60:90] + '\n' + description[90:120] + '\n' + description[120:150]

    global count
    global deep
    if count != 3:
        x_pos = count * 200 + count * 130 - 240
        y_pos = 180 + 500 * deep
        yt_pos = y_pos + 220
        count = count + 1
    elif count == 3:
        x_pos = count * 200 + count * 130 - 240
        y_pos = 180 + 500 * deep
        yt_pos = 220 + 180 + 500 * deep
        count = 1
        deep = deep + 1
    img_with_border = ImageOps.expand(im, border=10, fill='black')
    draw.text((x_pos, yt_pos), description, text_color, font)
    image.paste(img_with_border, (x_pos, y_pos), img_with_border)
    image.save("greeting_card.png")


@click.command()
@click.option('--title', default='', help="Title of the paper.")
@click.option('--images', multiple=True, help="Some images to insert into paper.")
@click.option('--descs', multiple=True, help='Some descs to attach to images to insert into paper.')
def cli(title, images, descs):
    if not images or not descs or not title:
        click.echo("Images and descs is required params")
        return
    if len(images) != len(descs):
        click.echo("Images count must be equals to descs count")

    font = ImageFont.truetype('impact.ttf', size=45)

    (x, y) = (400, 50)
    color = 'rgb(0, 0, 0)'
    draw.text((x, y), title, fill=color, font=font)

    image.save('greeting_card.png')

    i = 0
    while i <= len(images) - 1:
        stay = Image.open(images[i])
        stay = stay.resize((200, 200), Image.ANTIALIAS)
        stay.save(images[i], "JPEG")
        print(images[i])
        add_new_layer(images[i], descs[i])
        i = i + 1


if __name__ == '__main__':
    cli()
