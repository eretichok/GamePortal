from django import template
import re

register = template.Library()

# фильтр для отображения превьюшек картинок
@register.filter()
def preview_picture(text):
    size = 300
    temp = ''
    # меняем все размеры на значение size
    for part in text.split():
        if part.startswith('width'):
            temp += f' width: {size}; '
        elif part.startswith('style="width:'):
            temp += f' style="width: {size}; '
        elif part.startswith('height'):
            temp += f' height: {size}; '
        elif part.startswith('style="height:'):
            temp += f' style="height: {size}; '
        else:
            temp += part + ' '
    result = ''
    # добавляем _thumb к пути src для отображения миниатюры
    if '<img' in text:
        # находим все вхождения по тэгу img
        matches = re.finditer('<img', text)
        indices = [match.start() for match in matches]
        # перебираем с конца сортированного списка все вхождения indices
        for index in sorted(indices, reverse=True):
            end_index = temp.find('/>'[index:]) + 1
            path_index = temp.find('src='[index:end_index])
            dot_index = temp.find('.'[path_index:])
            # если картинка стоит первая (перед текстом), почему-то точку определяет под индексом 0
            # КОСТЫЛЬ: добавляем _thumb к пути src для отображения миниатюры
            if dot_index == 0:
                for i, sym in enumerate(temp):
                    if sym == '.':
                        result = temp[:i] + '_thumb' + temp[i:]
            else:
                result = temp[:dot_index] + '_thumb' + temp[dot_index:]
    return result
