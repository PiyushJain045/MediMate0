from django.shortcuts import render, redirect 
from django.views import View
from django.http import JsonResponse
from .models import BodyPartQuestions, Profile,  Appointment 
import json
import pandas as pd
import pickle
import os
from django.conf import settings

import calendar
from datetime import date

from .utils.predict_skin_disease import predict_image
from .utils.skin_gemini import gemini_advice_skin
from .utils.disease_gemini import gemini_advice_disease
from .utils.disease_specialist_map import DISEASE_TO_SPECIALIST

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

import googlemaps
from dotenv import load_dotenv
load_dotenv() 


GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Parameters/ Questions
features_to_keep = [
    'headache', 'burning abdominal pain', 'vomiting', 'pelvic pain',
    'back pain', 'disturbance of memory', 'vomiting blood',
    'sharp abdominal pain', 'nausea', 'ache all over', 'weakness',
    'abusing alcohol', 'problems with movement', 'sharp chest pain',
    'joint pain', 'chills', 'foot or toe pain',
    'abnormal involuntary movements', 'suprapubic pain', 'knee pain',
    'fever', 'rectal bleeding', 'lacrimation', 'decreased appetite',
    'leg pain', 'restlessness', 'constipation', 'vaginal discharge',
    'side pain', 'skin moles'
]

# Load the saved model
model_path = os.path.join(settings.BASE_DIR, 'model', 'disease_prediction_model.pkl')
le_path = os.path.join(settings.BASE_DIR, 'model', 'label_encoder.pkl')

with open(model_path, 'rb') as model_file:
    loaded_model = pickle.load(model_file)

with open(le_path, 'rb') as le_file:
    loaded_le = pickle.load(le_file)



class Home(View):
    def get(self, request):
        print("INSIDE HOME GET")
        return render(request, 'home.html')
    
    def post(self, request):
        pass


class Diagonisis(LoginRequiredMixin, View):
    def get(self, request):
        print("INSIDE HOME GET")

        age = 0 # Default age
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.age is not None:
                age = profile.age

        except Profile.DoesNotExist:
            print(f"No profile found for user {request.user.username}. Defaulting age to 0.")

        return render(request, 'diagonisis.html', {"age": age})
    
    def post(self, request):
        try:
            print("INSIDE HOME POST")
            body_part = request.POST.get('discomfort_area')
            print(body_part)

            # Stoting the body part in session
            request.session['discomfort_area'] = body_part
            return redirect('questions') 
        
        except Exception as e:
            print(f"Error in Home POST: {e}")
            return JsonResponse({'error': str(e)}, status=500)
        

class Questions(View):
    def get(self, request):
        print("INSIDE QUESTIONS GET")

        # Retrieving body part from session
        body_part = request.session.get('discomfort_area', None)

        if not body_part:
                return render(request, 'questions.html', {'error': 'No body part selected. Please go back and select an area.'})

        # Fetching the question set for the corresponding body part
        question_set = BodyPartQuestions.objects.get(body_part=body_part)
        questions_for_part = question_set.questions.all()

        # Preparing the list of questions to be displayed
        questions_list = [{'key': q.feature_name, 'text': q.question_text} for q in questions_for_part]
        print("Passing questions to template:", questions_list)

        context = {
                'questions_json': json.dumps(questions_list)
            }

        return render(request, 'questions.html', context)
    
    def post(self, request):

        try:
            print("INSIDE QUESTIONS POST")
            data = request.POST

            # Symptom '1' by user
            selected_features = [k for k, v in data.items() if v == '1' and k != 'csrfmiddlewaretoken']
            print("Selected symptoms:", selected_features)

            # Preparing data for passing into model
            parameters = {feature: [0] for feature in features_to_keep}
            for feature in selected_features:
                parameters[feature] = 1

            user_df = pd.DataFrame(parameters)

            # Load the model and label encoder
            predicted_label_encoded = loaded_model.predict(user_df)
            print(f"Model predicted encoded label: {predicted_label_encoded[0]}")

            # Decode the label + Final Result
            predicted_disease_name = loaded_le.inverse_transform(predicted_label_encoded)

            ######## Gemini Integration for Diagnosis #########

            # Retrieving body part from session
            body_part = request.session.get('discomfort_area', None)
            symptoms = selected_features
            advice_data = gemini_advice_disease(predicted_disease_name[0], body_part, symptoms)

            print("Gemini advice data:", advice_data)

            context = {"result": predicted_disease_name[0], 
                        'advice_data': advice_data,
                        'assessment_category': advice_data['assessment_category'],
                        'category_color_class': advice_data['category_color_class'],
                        }
            
            return render(request, 'result.html', context)
        
        except Exception as e:
            print(f"Error in Questions POST: {e}")
            return JsonResponse({'error': str(e)}, status=500)
        

class SkinDisease(View):
    def get(self, request):
        pass

    def post(self, request):
        print("INSIDE SKINDISEASE POST")

        age = request.POST.get('age')
        gender = request.POST.get('gender')
        image = request.FILES.get('skin_photo')

        print(age, gender, image)

        # Image Prediction
        skin_result,_ = predict_image(image)
        print(skin_result)

        # Advice
        advice = gemini_advice_skin(age, gender, skin_result)

        return render(request, 'result.html', {"skin_result": skin_result, 
                                                "advice": advice
                                                })
    

class NearbyDoctor(View):
    def get(self, request):
        print("INSIDE NEARBY DOCTOR GET")
        pass

    def post(self, request):
        print("INSIDE NEARBY DOCTOR POST")

        name_of_disease = request.POST.get('disease_name', None)
        print('DISEASE:' ,name_of_disease)

        specialist_to_find = DISEASE_TO_SPECIALIST.get(name_of_disease, "Dermatologist")
        print(f"SPECIALIST: {specialist_to_find}")

        # Assuming the user location is hardcoded for now
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        if not lat or not lon:
            # Handle the error if location is not available
            context = {'error': 'Could not get your location. Please enable location services and try again.'}
            return render(request, 'nearby_doctors.html', context)


        user_location = "Nashik, Maharashtra"
        # user_lat_lng = (19.9960186, 73.7532485)
        user_lat_lng = (float(lat), float(lon))


        doctors_list = []
        try:
            # Initialize the client
            gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
            
            # Build the search query
            query = f"{specialist_to_find} in {user_location}"
            print(f"Google Maps Query: {query}")

            # Perform a "Nearby Search"
            places_result = gmaps.places_nearby(
                location=user_lat_lng,
                keyword=specialist_to_find,
                radius=40000,  # Search within a 40km radius
                type='doctor' # Bias results towards doctors
            )

            nearby_places = places_result.get('results', [])

            # Distance
            if not nearby_places:
                print("No nearby places found.")
            else:
                destination_place_ids = [f"place_id:{place['place_id']}" for place in nearby_places if 'place_id' in place]

                print(f"Calculating distance to {len(destination_place_ids)} places...")
                distance_result = gmaps.distance_matrix(
                origins=[user_lat_lng],
                destinations=destination_place_ids,
                mode="driving")
                        
                print("Distance Matrix Result:", distance_result) # This should now succeed

                # Prepare the data for sending to the template
                for i, place in enumerate(nearby_places):
                    place_id = place.get('place_id')
                    if not place_id:
                        continue

                    # Get place details
                    details = gmaps.place(
                        place_id=place_id,
                        fields=['name', 'formatted_address', 'international_phone_number', 'website', 'rating']
                    )
                    place_details = details.get('result', {})

                    # Get corresponding distance info
                    distance_info = distance_result['rows'][0]['elements'][i]
                    distance = "N/A"
                    if distance_info['status'] == 'OK':
                        distance = distance_info['distance']['text']

                    # Append the combined info to our final list
                    if place_details.get('name'):
                        doctors_list.append({
                            'name': place_details.get('name'),
                            'address': place_details.get('formatted_address'),
                            'phone': place_details.get('international_phone_number'),
                            'website': place_details.get('website'),
                            'rating': place_details.get('rating', 'N/A'),
                            'distance': distance
                        })


        except Exception as e:
            print(f"An error occurred with the Google Maps API: {e}")
            context = {'error': 'Could not fetch doctor information. Please try again later.'}
            return render(request, 'nearby_doctors.html', context)
        
        context = {
            'disease': name_of_disease,
            'specialist': specialist_to_find,
            'doctors': doctors_list,
            'location': user_location
        }
        
        return render(request, 'nearby_doctors.html', context)
    

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        print("INSIDE PROFILE GET")
        # Get the profile for the current user, or create one if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=request.user)
        context = {
            'profile': profile
        }
        return render(request, 'profile.html', context)
    
    def post(self, request):
        profile = request.user.profile

        # Update the profile fields from the POST data
        profile.age = request.POST.get('age')
        profile.family_doctor = request.POST.get('family_doctor')

        # Handle the profile photo upload
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
        
        profile.save()

        # Add a success message
        messages.success(request, 'Your profile has been updated successfully!')

        # Redirect back to the same page to show the changes and the message
        return redirect('profile')


class CalendarView(LoginRequiredMixin, View):
    def get(self, request):

        # display the current month's calendar.
        today = date.today()
        year, month = today.year, today.month

        #  Generating the calendar grid data using Python's calendar module.
        calendar_grid = calendar.monthcalendar(year, month)

        # Fetch all appointments for the current user for this month.
        appointments_qs = Appointment.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        )

        # The key is the day number (e.g., 15) and the value is a list of appointment titles.
        appointments_map = {}
        for appt in appointments_qs:
            if appt.date.day not in appointments_map:
                appointments_map[appt.date.day] = []
            appointments_map[appt.date.day].append(appt.title)

        context = {
            'calendar_grid': calendar_grid,
            'appointments_map': appointments_map,
            'month_name': date(year, month, 1).strftime('%B %Y'),
            'today': today,
        }
        return render(request, 'calendar.html', context)

    def post(self, request):
        # Handle the form submission to save a new appointment from calendar
        title = request.POST.get('title') 
        appointment_date = request.POST.get('date')

        if title and appointment_date:
            Appointment.objects.create(
                user=request.user,
                title=title,
                date=appointment_date
            )
            messages.success(request, f"Appointment '{title}' saved successfully!")
        else:
            messages.error(request, "Please provide both a title and a date.")
        
        return redirect('calendar')
