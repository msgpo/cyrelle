from __future__ import unicode_literals

from django.db import models


#User Profile Model
class UserProfile(models.Model):
	user = models.ForeignKey(User)
	role = models.Charfield(max_length=7, default='teacher')

#Subject Model
class Subject(models.Model):
	name = models.CharField(max_length=200)
    section = models.ForeignKey(Section, default=1)
    subject_type = models.ForeignKey(SubjectType, default=0)
    user = models.ForeignKey(User, default=0)
    school_year = models.CharField(max_length=100, default='2014-2015')

    def __unicode__(self):
        return u'%s %s %s %s %s %s' % (self.id, self.name, self.section.name, self.school_year,
                                       self.subject_type.name, self.user.get_full_name())

#Activity Model
class Activity(models.Model):
	activity_name = models.CharField(max_length=200)
	activity_description = models.CharField(max_length=200)
	
