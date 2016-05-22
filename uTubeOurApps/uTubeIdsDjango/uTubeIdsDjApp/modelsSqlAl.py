from django.db import models

# Create your models here.

class KnowledgeArea(models.Model):
  id     = models.IntegerField(primary_key=True)
  parent = models.ForeignKey('self', null=True,blank=True)  
  name   = models.TextField()

class RelativeDir(models.Model):
  id  = models.IntegerField(primary_key=True)
  relpath = models.TextField()
  k_area = models.ForeignKey(KnowledgeArea, null=True, blank=True)

class VideoFile(models.Model):
  videoid  = models.CharField(max_length=11, primary_key=True)
  filename = models.TextField()
  rel_dir  = models.ForeignKey(RelativeDir, null=True, blank=True)
  abs_base_dir = models.TextField(null=True, blank=True)
  sha1hex = models.CharField(max_length=40, null=True, blank=True)
  #reporter = models.ForeignKey(Reporter)
  pub_date = models.DateField(null=True, blank=True)
  k_area = models.ForeignKey(KnowledgeArea, null=True, blank=True)

