from django.db import models

# Create your models here.
class BaseModel(models.Model):
    is_delete=models.BooleanField(default=False)
    create_time=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)

    class Meta:
        abstract=True

class Books(BaseModel):
    book_name=models.CharField(max_length=20)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    press=models.ForeignKey(to='Press',on_delete=models.CASCADE,db_constraint=False,related_name='books')
    authors=models.ManyToManyField(to='Authors',db_constraint=False,related_name='books')
    class Meta:
        db_table='book'
        verbose_name='图书'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.book_name

    @property
    def press_name(self):
        return self.press.press_name
    @property
    def press_address(self):
        return self.press.press_address
    @property
    def author_list(self):
        return self.authors.values('author_name','age','author_detail__phone')

class Authors(BaseModel):
    author_name=models.CharField(max_length=8)
    age=models.SmallIntegerField()

    class Meta:
        db_table = 'author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name

class AuthorDetail(BaseModel):
     sex_choices=[
        (0,'男'),
        (1,'女')
    ]
     phone=models.CharField(max_length=11)
     sex=models.SmallIntegerField(choices=sex_choices,default=0)
     author=models.OneToOneField(to='Authors',on_delete=models.CASCADE,related_name='author_detail')

     class Meta:
         db_table = 'author_detail'
         verbose_name = '作者详情'
         verbose_name_plural = verbose_name

     def __str__(self):
         return '%s的详情' % self.author.author_name

class Press(BaseModel):
    press_name=models.CharField(max_length=20)
    press_address=models.CharField(max_length=50)

    class Meta:
        db_table = 'press'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name



