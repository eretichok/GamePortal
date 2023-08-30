def preview_picture(text):
    if '<img src=' in text:
        split_text = text.split()
        for index, part in enumerate(split_text):
            if part.startswith('style="height:'):
                height_index = index
                height = int(part[14:-3])
            elif part.startswith('width:'):
                width_index = index
                width = int(part[6:-3])
                break

        if height > 200 and width > 200:
            if height > width:
                reduction = 200 / height
                height = 200
                width = int(width * reduction)
            else:
                reduction = 200 / width
                width = 200
                height = int(height * reduction)
        elif height > 200 > width:
            reduction = 200 / height
            height = 200
            width = int(width * reduction)
        elif height < 200 < width:
            reduction = 200 / width
            width = 200
            height = int(height * reduction)
        split_text[height_index] = f'style="height:{height}px;'
        split_text[width_index] = f'width:{width}px"'
        return ' '.join(split_text)

text1 = '<p>Иду я иду, а тут на тебе:</p> <p><img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD//9k=" style="height:180px; width:350px" /></p>'
text2 = '<p>Иду я иду, а тут на тебе:</p> <p><img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD//9k=" style="height:350px; width:180px" /></p>'
text3 = '<p>Иду я иду, а тут на тебе:</p> <p><img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD//9k=" style="height:600px; width:400px" /></p>'
text4 = '<p>Иду я иду, а тут на тебе:</p> <p><img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD//9k=" style="height:180px; width:180px" /></p>'
print(preview_picture(text1))
print(preview_picture(text2))
print(preview_picture(text3))
print(preview_picture(text4))