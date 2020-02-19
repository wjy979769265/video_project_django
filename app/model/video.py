from enum import Enum
from django.db import models


class VideoType(Enum):
    # 传的就是value
    movie = 'movie'
    cartoon = 'cartoon'
    episode = 'episode'
    variety = 'variety'
    other = 'other'


VideoType.movie.label = '电影'
VideoType.cartoon.label = '卡通'
VideoType.episode.label = '连续剧'
VideoType.variety.label = '综艺'
VideoType.other.label = '其他'


class IdentityType(Enum):
    # 传的就是value
    to_star = 'to_star'
    support_star = 'support_star'
    director = 'director'


IdentityType.to_star.label = '主演'
IdentityType.support_star.label = '配角'
IdentityType.director.label = '导演'


class FromType(Enum):
    # 传的就是value
    youku = 'youku'
    custom = 'custom'


FromType.youku.label = '优酷'
FromType.custom.label = '自制'


class NationlityType(Enum):
    # 传的就是value
    china = 'china'
    japan = 'japan'
    koera = 'koera'
    america = 'america'
    other = 'other'


NationlityType.china.label = '中国'
NationlityType.japan.label = '日本'
NationlityType.koera.label = '韩国'
NationlityType.america.label = '美国'
NationlityType.other.label = '其他'


class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=20, null=False, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, default=NationlityType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'video_type', 'from_to', 'nationality')

    def __str__(self):
        return self.name


class VideoStar(models.Model):
    video = models.ForeignKey(Video,
                              related_name='video_star',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True
                              )
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')

    class Meta:
        # 去重
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return self.name


class VideoSub(models.Model):
    video = models.ForeignKey(Video,
                              related_name='video_sub',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True
                              )
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return 'video:{}, number:{}'.format(self.video.name, self.number)
