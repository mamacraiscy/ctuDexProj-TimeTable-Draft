from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Instructor, Room, Course, Building
from django.db.models import Q
import json

def home(request):
    return render(request, 'instructors/index.html')

def index(request):
    return render(request, 'instructors/index.html')

def instructor_list(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', 'ALL')  # Employment Type
    department_filter = request.GET.get('department', 'ALL')  # Department Type (college_id)

    # Start with all instructors
    instructors = Instructor.objects.all()

    # Apply filtering logic
    if filter_type == 'REGULAR':
        instructors = instructors.filter(employment_type='REGULAR')
    elif filter_type == 'COS':
        instructors = instructors.filter(employment_type='COS')

    # Apply department filter based on college_id
    if department_filter == 'COT':
        instructors = instructors.filter(college_id=3)
    elif department_filter == 'COED':
        instructors = instructors.filter(college_id=1)
    elif department_filter == 'COENG':
        instructors = instructors.filter(college_id=2)
    elif department_filter == 'COMGENT':
        instructors = instructors.filter(college_id=4)

    # Apply search query
    if query:
        instructors = instructors.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
        
    total_instructors = instructors.count()
    
    return render(request, 'instructors/instructor_list.html', {
        'instructors': instructors,
        'filter': filter_type,  # Pass the employment type filter to the template
        'department': department_filter,  # Pass the department filter to the template
        'total_instructors': total_instructors,
        'query': query,  # Pass the search query to the template
    })

def instructor_search(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', 'ALL')  # Employment Type
    department_filter = request.GET.get('department', 'ALL')  # Department Type (college_id)

    # Start with all instructors
    results = Instructor.objects.all()

    # Apply filtering logic for employment type
    if filter_type == 'REGULAR':
        results = results.filter(employment_type='REGULAR')
    elif filter_type == 'COS':
        results = results.filter(employment_type='COS')
    
    # Apply department filter based on college_id
    if department_filter == 'COED':
        results = results.filter(college_id=1)
    elif department_filter == 'COENG':
        results = results.filter(college_id=2)
    elif department_filter == 'COT':
        results = results.filter(college_id=3)
    elif department_filter == 'COMGENT':
        results = results.filter(college_id=4)

    # Apply search query
    if query:
        results = results.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )

    suggestions = [
        {
            'id': instructor.instructor_id,
            'name': f"{instructor.first_name} {instructor.last_name}"  # Added space between first and last names
        }
        for instructor in results
    ]
    
    return JsonResponse({'results': suggestions})   

def instructor_details(request):
    instructor_id = request.GET.get('id')
    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)

    # Ensure availability_days and availability_times are strings or properly formatted
    availability_days = (
        ', '.join(instructor.availability_days) 
        if isinstance(instructor.availability_days, list) 
        else instructor.availability_days
    )

    availability_times = (
        ', '.join(instructor.availability_times) 
        if isinstance(instructor.availability_times, list) 
        else instructor.availability_times
    )

    # Format the qualified courses
    qualified_courses = (
        ', '.join(instructor.qualified_course) 
        if isinstance(instructor.qualified_course, list) 
        else instructor.qualified_course
    )

    # Create a response with correct formatting
    data = {
        'html': (
            "<div style='position: relative;'>"  # Wrapper for positioning
            f"<h3>{instructor.first_name} {instructor.last_name}</h3>"
            f"<p>Employment Type: {instructor.employment_type}</p>"
            f"<p>Qualified Courses: {qualified_courses}</p>"
            f"<p>Availability Days: {availability_days}</p>"
            f"<p>Availability Times: {availability_times}</p>"
            f"<p>College ID: {instructor.college_id}</p>"
            "</div>"
        )
    }
    return JsonResponse(data)

def editable_instructor_details(request):
    instructor_id = request.GET.get('id')
    
    # Fetch the instructor from the database
    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)

    # Format the instructor details
    availability_days = (
        ', '.join(instructor.availability_days) 
        if isinstance(instructor.availability_days, list) 
        else instructor.availability_days
    )

    availability_times = (
        ', '.join(instructor.availability_times) 
        if isinstance(instructor.availability_times, list) 
        else instructor.availability_times
    )

    # Format the qualified courses
    qualified_courses = (
        ', '.join(instructor.qualified_course) 
        if isinstance(instructor.qualified_course, list) 
        else instructor.qualified_course
    )

    # Return the necessary data as JSON
    data = {
        'availability_days': availability_days.split(', '),
        'availability_times': availability_times.split(', '),
        'qualified_courses': qualified_courses.split(', '),
    }

    return JsonResponse(data)    

def teaching_load(request):
    # Fetch data for instructors, rooms, courses, and buildings
    instructors = Instructor.objects.all()
    # rooms = Room.objects.all()  # Assuming a Room model exists
    # courses = Course.objects.all()  # Assuming a Course model exists
    # buildings = Building.objects.all()  # Assuming a Building model exists
    rows = range(1, 10)
    return render(request, 'instructors/teaching_load.html', {'rows': rows})

def get_suggestions(request):
    column = request.GET.get('column')
    query = request.GET.get('q', '')

    if column == 'instructor':
        results = Instructor.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
        suggestions = [{'id': instructor.instructor_id, 'name': f"{instructor.first_name} {instructor.last_name}"} for instructor in results]

    elif column == 'room':
        results = Room.objects.filter(name__icontains=query)
        suggestions = [{'id': room.id, 'name': room.name} for room in results]

    elif column == 'course':
        results = Course.objects.filter(course_name__icontains=query)
        suggestions = [{'id': course.id, 'name': course.course_name} for course in results]

    elif column == 'building':
        results = Building.objects.filter(name__icontains=query)
        suggestions = [{'id': building.id, 'name': building.name} for building in results]
    
    return JsonResponse({'results': suggestions})

def save_teaching_load(request):
    # Expecting a POST request with a JSON payload
    if request.method == "POST":
        load_data = json.loads(request.POST.get('load_data'))

        # Process each teaching load entry (this is where you could save to a model if needed)
        for entry in load_data:
            instructor_id = entry['instructor']
            course_name = entry['course']
            room_name = entry['room']
            building_name = entry['building']
            
            # Add your logic here to save the teaching load data into a model or process it
            # Example: TeachingLoad.objects.create(instructor=instructor_id, course=course_name, ...)

        return JsonResponse({"status": "success", "message": "Teaching load saved successfully."})
    return JsonResponse({"status": "error", "message": "Invalid request."})

def filter_instructors(request):
    # Logic for filtering instructors can be added here
    return render(request, 'instructors/instructor_filter.html')

def courses_list(request):
    courses = list(Course.objects.values())  # Fetch courses from database
    return JsonResponse(courses, safe=False)  # Return JSON response