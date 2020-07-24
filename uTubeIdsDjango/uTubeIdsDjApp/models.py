import __init__
from django.db import models

# Create your models here.

class KnowledgeArea(models.Model):
  id     = models.IntegerField(primary_key=True)
  parent = models.ForeignKey('self', null=True,blank=True)  
  name   = models.TextField()

class FileSystemFolder(models.Model):
  id  = models.IntegerField(primary_key=True)
  parent = models.ForeignKey('self', null=True, blank=True)
  foldername = models.CharField(max_length=255)

class VideoFile(models.Model):
  videoid  = models.CharField(max_length=11, primary_key=True)
  filename = models.TextField()
  rel_dir  = models.ForeignKey(FileSystemFolder, null=True, blank=True)
  abs_base_dir = models.TextField(null=True, blank=True)
  sha1hex = models.CharField(max_length=40, null=True, blank=True)
  #reporter = models.ForeignKey(Reporter)
  pub_date = models.DateField(null=True, blank=True)
  k_area = models.ForeignKey(KnowledgeArea, null=True, blank=True)

class SabDirInstructorDj(models.Model):
  id        = models.IntegerField(primary_key=True)
  tarjaname = models.CharField(max_length=50)
  about     = models.TextField(null=True, blank=True)

class SabDirCourseDj(models.Model):
  id          = models.IntegerField(primary_key=True)
  coursename  = models.CharField(max_length=100)
  instructor  = models.ForeignKey(SabDirInstructorDj)
  date        = models.DateField(null=True,blank=True)
  k_area      = models.ForeignKey(KnowledgeArea, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  n_lectures  = models.IntegerField(default=5)

class SabDirLectureDj(models.Model):
  course    = models.ForeignKey(SabDirCourseDj)
  title     = models.CharField(max_length=100)
  seq_order = models.IntegerField(default=1)
  duration  = models.TimeField(null=True, blank=True)
  mcomment  = models.TextField(null=True, blank=True)

class SabDirVideoFilenameDj(models.Model):
  filename      = models.CharField(max_length=255)
  lecture       = models.ForeignKey(SabDirLectureDj)
  size_in_bytes = models.IntegerField(null=True, blank=True)
  rel_dir       = models.TextField(null=True, blank=True) #models.CharField(RelativeDir, null=True, blank=True)
  sha1hex       = models.CharField(max_length=40, null=True, blank=True)
  
  @attribute
  def part(self):
    part = 0
    return part

  @attribute
  def videoid(self):
    vid = '12345678901'   
    return vid
  
  @attribute
  def extension(self): 
    ext='mp4'
    return ext


