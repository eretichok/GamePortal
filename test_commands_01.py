from main.models import *


p1 = Post.objects.create(author=auth1, post_category='Статья', headline='Мировая статья', text='Текст мировой статьи')
p2 = Post.objects.create(author=auth2, post_category='Статья', headline='Экономическая статья', text='Текст экономической статьи')
p3 = Post.objects.create(author=auth3, post_category='Статья', headline='Научная статья', text='Текст научной статьи')
p4 = Post.objects.create(author=auth1, post_category='Статья', headline='Культурная статья', text='Текст культурной статьи с нецензурной лексикой: f*ck.')
p5 = Post.objects.create(author=auth2, post_category='Статья', headline='Научно-Экономическая статья', text='Текст научно-экономической статьи')
p6 = Post.objects.create(author=auth3, post_category='Статья', headline='ИТ статья', text='Текст ИТ статьи')
p7 = Post.objects.create(author=auth2, post_category='Статья', headline='Культорно-Экономическая статья 3', text='Текст культурно-экономической статьи')
p8 = Post.objects.create(author=auth1, post_category='Новость', headline='Мировая новость', text='Текст мировой новости')
p9 = Post.objects.create(author=auth2, post_category='Новость', headline='Экономическая новость', text='Текст экономической новости')
p10 = Post.objects.create(author=auth3, post_category='Новость', headline='Научная новость', text='Текст научной новости')
p11 = Post.objects.create(author=auth1, post_category='Новость', headline='Мировая новость 2', text='Текст мировой новости 2')
p12 = Post.objects.create(author=auth2, post_category='Новость', headline='Экономическая новость 2', text='Текст экономической новости 2')
p13 = Post.objects.create(author=auth3, post_category='Новость', headline='Научная новость 2', text='Текст научной новости 2')
p14 = Post.objects.create(author=auth1, post_category='Новость', headline='Мировая новость 3', text='Текст мировой новости 3')
p15 = Post.objects.create(author=auth2, post_category='Новость', headline='Экономическая новость 3', text='Текст экономической новости 3')
p16 = Post.objects.create(author=auth3, post_category='Новость', headline='Научная новость 3', text='Текст научной новости 3')
p17 = Post.objects.create(author=auth1, post_category='Новость', headline='Мировая научная новость', text='Текст мировой научной новости')
p18 = Post.objects.create(author=auth1, post_category='Новость', headline='Мировая ИТ новость', text='Текст мировой ИТ новости')
p19 = Post.objects.create(author=auth1, post_category='Новость', headline='Мировая ИТ новость 2', text='Текст мировой ИТ новости 2')
p20 = Post.objects.create(author=auth3, post_category='Новость', headline='ИТ новость', text='Текст ИТ новости')


# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
PostCategory.objects.create(post=p1, category=c1)
PostCategory.objects.create(post=p2, category=c2)
PostCategory.objects.create(post=p3, category=c4)
PostCategory.objects.create(post=p4, category=c3)
PostCategory.objects.create(post=p5, category=c2)
PostCategory.objects.create(post=p6, category=c5)
PostCategory.objects.create(post=p7, category=c2)
PostCategory.objects.create(post=p8, category=c1)
PostCategory.objects.create(post=p9, category=c2)
PostCategory.objects.create(post=p10, category=c4)
PostCategory.objects.create(post=p11, category=c1)
PostCategory.objects.create(post=p12, category=c2)
PostCategory.objects.create(post=p13, category=c4)
PostCategory.objects.create(post=p14, category=c1)
PostCategory.objects.create(post=p15, category=c2)
PostCategory.objects.create(post=p16, category=c4)
PostCategory.objects.create(post=p17, category=c1)
PostCategory.objects.create(post=p18, category=c1)
PostCategory.objects.create(post=p19, category=c1)
PostCategory.objects.create(post=p20, category=c5)
PostCategory.objects.create(post=p7, category=c3)
PostCategory.objects.create(post=p5, category=c4)
PostCategory.objects.create(post=p17, category=c4)
PostCategory.objects.create(post=p18, category=c5)
PostCategory.objects.create(post=p19, category=c5)


# Создать минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть минимум один комментарий).
com1 = Comment.objects.create(post=p1, user=u1, text='Хорошая статья')
com2 = Comment.objects.create(post=p2, user=u2, text='Отличная статья')
com3 = Comment.objects.create(post=p3, user=u1, text='Хорошая новость')
com4 = Comment.objects.create(post=p3, user=u2, text='Отличная новость')
com5 = Comment.objects.create(post=p2, user=u1, text='Великолепная статья')

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
p1.like()
p1.like()
p1.dislike()
p2.like()
p2.like()
p3.like()
p3.like()
p3.like()
p3.like()
p3.dislike()

com1.like()
com1.like()
com1.dislike()
com2.like()
com2.like()
com3.like()
com3.like()
com3.like()
com3.like()
com3.dislike()
com4.like()
com4.like()
com4.like()
com4.like()
com4.like()
com4.dislike()
com5.like()
com5.like()
com5.like()
com5.like()
com5.like()

# Обновить рейтинги пользователей.
auth1.update_rating()
auth2.update_rating()
auth3.update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_auth = Author.objects.order_by('-rating').values('user__username', 'rating').first()
print(f'Автор {best_auth["user__username"]} имеет наивысший рейтинг среди всех - {best_auth["rating"]}')

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье.
best_article = Post.objects.filter(post_category='Статья').order_by('-rating').first()
print(f'Лучшая статья: {best_article.headline}. Ее рейтинг - {best_article.rating}\n'
      f'Ее написал {str(best_article.date).split()[0]} автор {best_article.author.user}\n'
      f'Предварительный просмотр статьи: {best_article.preview()}')

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
best_article_comments = Comment.objects.filter(post=best_article)
for i, comment in enumerate(best_article_comments):
    print(f'Комментарий №{i+1}: дата - {str(comment.date).split()[0]}, написал - {comment.user.username}, '
          f'рейтинг - {comment.rating}, текст - {comment.text}')