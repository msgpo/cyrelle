from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


#User Profile Model
class UserProfile(models.Model):
	user = models.ForeignKey(User)
	role = models.Charfield(max_length=7, default='teacher')

#Subject Model
class Subject(models.Model):
	name = models.CharField(max_length=200)
    section = models.CharField(max_length=10)
    teacher = models.ForeignKey(User, default=0)
    school_year = models.CharField(max_length=100, default='2014-2015')

    def __unicode__(self):
        return u'%s %s %s %s %s' % (self.id, self.name, self.section, self.school_year, self.teacher.get_full_name())

#Activity Model
@python_2_unicode_compatible
class Activity(models.Model):
	activity_name = models.CharField(max_length=200)
	activity_description = models.CharField(max_length=200)
	subject = models.ForeignKey(Subject)
	deadline = models.DateTimeField()

	def __str__(self):
		return self.activity_name