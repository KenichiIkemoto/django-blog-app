from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Category(models.Model):
    name=models.CharField(verbose_name="カテゴリ",max_length=255)
    slug=models.SlugField(verbose_name="URL",unique=True)

    def __str__(self) -> str:
        return self.name
    class Meta:
         verbose_name="カテゴリー"
         verbose_name_plural="カテゴリー"

class Tag(models.Model):
    name=models.CharField(verbose_name="タグ",max_length=255)
    slug=models.SlugField(verbose_name="URL",unique=True) 
    
    def __str__(self) -> str:
            return self.name
    
    class Meta:
         verbose_name="タグ"
         verbose_name_plural="タグ"
    
class Post(models.Model):
    title=models.CharField(verbose_name='タイトル',max_length=200)
    # content=models.TextField('本文',blank=True)
    content=MarkdownxField('本文',blank=True)
    created_at=models.DateTimeField('作成日時',auto_now_add=True)
    updated_at=models.DateTimeField('更新日時',auto_now=True)
    is_published=models.BooleanField('公開設定',default=False)

    image=models.ImageField(verbose_name='画像',upload_to='upload' , null=True , blank = True)

    def __str__(self):
        return self.title
    
    class Meta:
         verbose_name="記事"
         verbose_name_plural="記事"
    
    category=models.ForeignKey(Category,verbose_name="カテゴリー",on_delete=models.PROTECT,null=True,blank=True)
    tags=models.ManyToManyField(Tag,verbose_name="タグ",blank=True)

    def convert_markdown_to_html(self):
         return markdownify(self.content)
    
    
class Comment(models.Model):
     name=models.CharField(verbose_name="名前",max_length=100)
     text=models.TextField(verbose_name="本文")
     created_at=models.DateTimeField(verbose_name="作成日",auto_now_add=True)
     post=models.ForeignKey(Post,verbose_name="記事",on_delete=models.CASCADE)

     def __str__(self):
          return self.text[:10]
     
     class Meta:
         verbose_name="コメント"
         verbose_name_plural="コメント"
    
class Reply(models.Model):
     name=models.CharField(verbose_name="名前",max_length=100)
     text=models.TextField(verbose_name="本文")
     created_at=models.DateTimeField(verbose_name="作成日",auto_now_add=True)
     comment=models.ForeignKey(Comment,verbose_name="コメント",on_delete=models.CASCADE)

     def __str__(self):
          return self.text[:10]
     
     class Meta:
         verbose_name="返信"
         verbose_name_plural="返信"

