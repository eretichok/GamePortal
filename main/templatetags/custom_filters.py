from django import template
import re

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


# @register.filter()
# def preview_picture(text):
#     max_size = 250
#     if 'height="' in text:
#         split_text = text.split()
#         for index, part in enumerate(split_text):
#             if part.startswith('height="') and part.endswith('"'):
#                 height_index = index
#                 height = int(part[8:-1])
#             elif part.startswith('width="') and part.endswith('"'):
#                 width_index = index
#                 width = int(part[7:-1])
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
#         print(' '.join(split_text))
#         return ' '.join(split_text)


@register.filter()
def preview_picture(text):
    temp = ''
    # удаляем все значения ширин и высот из разметки
    for part in text.split():
        if part.startswith('width') or part.startswith('height'):
            continue
        else:
            temp += part + ' '
    result = ''
    # добавляем _thumb к пути src для отображения миниатюры
    if '<img' in temp:
        matches = re.finditer('<img', text)
        indices = [match.start() for match in matches]
        for index in sorted(indices, reverse=True):
            end_index = temp.find('/>'[index:]) + 1
            path_index = temp.find('src='[index:end_index])
            dot_index = temp.find('.'[path_index:])
            # если картинка стоит первая (перед текстом), почему то точку определяет под индексом 0
            # КОСТЫЛЬ: добавляем _thumb к пути src для отображения миниатюры
            if dot_index == 0:
                for i, sym in enumerate(temp):
                    if sym == '.':
                        result = temp[:i] + '_thumb' + temp[i:]
            else:
                result = temp[:dot_index] + '_thumb' + temp[dot_index:]
    print(result)
    return result
