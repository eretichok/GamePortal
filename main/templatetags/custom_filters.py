from django import template

register = template.Library()

# для CKeditor: фильтр уменьшения встроенного в текст изображения, для отображения миниатюр -
# не более max_size по любой стороне
# @register.filter()
# def preview_picture(text):
#     max_size = 250
#     if '<img src=' in text:
#         split_text = text.split()
#         for index, part in enumerate(split_text):
#             if part.startswith('style="height:'):
#                 height_index = index
#                 height = int(part[14:-3])
#             elif part.startswith('width:'):
#                 width_index = index
#                 width = int(part[6:-3])
#                 break
#
#         if height > max_size and width > max_size:
#             if height > width:
#                 reduction = max_size / height
#                 height = max_size
#                 width = int(width * reduction)
#             else:
#                 reduction = max_size / width
#                 width = max_size
#                 height = int(height * reduction)
#         elif height > max_size > width:
#             reduction = max_size / height
#             height = max_size
#             width = int(width * reduction)
#         elif height < max_size < width:
#             reduction = max_size / width
#             width = max_size
#             height = int(height * reduction)
#         split_text[height_index] = f'style="height:{height}px;'
#         split_text[width_index] = f'width:{width}px"'
#         return ' '.join(split_text)

# для CKeditor5: фильтр уменьшения встроенного в текст изображения, для отображения миниатюр -
# не более max_size по любой стороне
@register.filter()
def preview_picture(text):
    max_size = 250
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

        if height > max_size and width > max_size:
            if height > width:
                reduction = max_size / height
                height = max_size
                width = int(width * reduction)
            else:
                reduction = max_size / width
                width = max_size
                height = int(height * reduction)
        elif height > max_size > width:
            reduction = max_size / height
            height = max_size
            width = int(width * reduction)
        elif height < max_size < width:
            reduction = max_size / width
            width = max_size
            height = int(height * reduction)
        split_text[height_index] = f'style="height:{height}px;'
        split_text[width_index] = f'width:{width}px"'
        return ' '.join(split_text)