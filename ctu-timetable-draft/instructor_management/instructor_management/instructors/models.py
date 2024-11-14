from django.db import models


class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)  # AutoField is suitable for unique identifiers
    first_name = models.CharField(max_length=100, blank=False)
    middle_initial = models.CharField(max_length=1, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False)
    EMPLOYMENT_TYPE_CHOICES = [
    ('REGULAR', 'Regular'),
    ('COS', 'Contract of Service'),
    ('Not Specified', 'Not Specified')  # Make sure the default value is included
    ]
    employment_type = models.CharField(
        max_length=15,
        choices=EMPLOYMENT_TYPE_CHOICES,
        blank=False,
        null=False,
        default='Not Specified'
    )
    
    college_id = models.IntegerField()
    qualified_course = models.JSONField(default=list)
    availability_days = models.JSONField(default=list)  # Ensures it's stored as JSON
    availability_times = models.JSONField(default=list)
    
    


    class Meta:
        db_table = 'instructor'


class Room(models.Model):
    name = models.CharField(max_length=50)
    building = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.building}"

class Course(models.Model):
    course_code = models.CharField(max_length=50)
    course_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name

class Building(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TeachingLoad(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE,null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    # Add other fields as needed, such as time slots, date, etc.

    def __str__(self):
        return f"{self.instructor} teaching {self.course} in {self.room} at {self.building}"