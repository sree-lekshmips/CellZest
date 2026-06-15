from django.shortcuts import render,redirect
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from .utils import create_anemia_graph
from django.http import JsonResponse



# Load dataset
data = pd.read_excel("Zest/static/data/updated_anemia_severity_dataset.xlsx")
if 'Nutritional Intake Suggestion' in data.columns:
    data = data.drop(columns=['Nutritional Intake Suggestion'])
data.drop_duplicates(inplace=True)
data = data[data['Age'] >= 18]

# Define features and target
X = data[['Age', 'Gender', 'Hemoglobin Level',  'Dietary Habit']]
y = data['Anemia Severity']

# Preprocessing
numerical_features = ['Age', 'Hemoglobin Level']
categorical_features = ['Gender','Dietary Habit']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

clf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Train the model
clf.fit(X, y)


# Function to recommend food
def recommend_food(predicted_severity, dietary_habit):
    recommendation = data[
        (data['Anemia Severity'] == predicted_severity) &
        (data['Dietary Habit'] == dietary_habit)
        ]['Updated Food Suggestion']
    return recommendation.iloc[0] if not recommendation.empty else "No specific recommendation available."


# Django v
#
# iew for form input
def index(request):
    if request.method == 'POST':
        age = int(request.POST['age'])
        gender = request.POST['gender']
        hemoglobin_level = float(request.POST['hemoglobin_level'])
        dietary_habit = request.POST['dietary_habit']

        user_data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender],
            'Hemoglobin Level': [hemoglobin_level],
            'Dietary Habit': [dietary_habit]
        })

        predicted_severity = clf.predict(user_data)[0]

        if gender == 'Male':
            if 8 <= hemoglobin_level < 10.9:
                predicted_severity = 'Moderate'
        elif gender == 'Female':
            if 8 <= hemoglobin_level < 10.9:
                predicted_severity = 'Moderate'

        recommendation = recommend_food(predicted_severity, dietary_habit)
        graph=create_anemia_graph(gender,hemoglobin_level,predicted_severity)

        return render(request,"Result.html", {'severity': predicted_severity, 'recommendation': recommendation,'graph': graph,'dietary_habit': dietary_habit })

    return render(request, 'form.html')


def home(request):
    return render(request,"home.html")

def result(request):
    return render(request,"Result.html")
def about(request):
    return render(request,"about.html")
def blog(request):
    return render(request,"blog.html")
def contact(request):
    return render(request,"contact.html")
def stories(request):
    return render(request,"stories.html")


MEAL_PLANS = {
    'Severe': {
        'Vegetarian': [
            "Breakfast: Spinach and tofu scramble with whole-grain toast,1 small orange (for vitamin C),1 cup fortified plant-based milk (e.g., almond or soy milk)",
            "Lunch: Lentil and spinach curry with brown rice,Steamed broccoli (rich in vitamin C),1 small orange (for vitamin C)",
            "Dinner: CChickpea and vegetable stir-fry with quinoa,Roasted sweet potatoes,1 cup fortified plant-based milk"
        ],
        'Non-Vegetarian': [
            "Breakfast: Scrambled eggs with spinach and whole-grain toast,1 small orange (for vitamin C),1 cup fortified orange juice (for vitamin C and iron)",
            "Lunch: Grilled salmon (rich in iron and omega-3s) with quinoa and steamed broccoli,Side salad with spinach, cherry tomatoes, and lemon dressing (vitamin C)",
            "Dinner: Pan-seared beef liver (extremely high in iron) with mashed sweet potatoes and sautéed kale,Roasted Brussels sprouts,1 small orange (for vitamin C)"
        ],
        'Vegan':[
        "Breakfast: Tofu scramble with spinach, tomatoes, and turmeric (iron-rich),1 slice of whole-grain toast,1 small orange (for vitamin C),1 cup fortified plant-based milk (e.g., almond, soy, or oat milk)",
        "Lunch: Lentil and spinach curry with brown rice,Steamed broccoli (rich in vitamin C),1 small orange (for vitamin C)",
        "Dinner: Chickpea and vegetable stir-fry with quinoa,Roasted sweet potatoes,1 cup fortified plant-based milk",
        ]
    },
    'Moderate': {
        'Vegetarian': [
            "Breakfast: Spinach and tofu scramble with whole-grain toast,1 small orange (for vitamin C to boost iron absorption)",
            "Lunch: Lentil and vegetable soup with a side of quinoa,Side of steamed broccoli (rich in vitamin C)",
            "Dinner: Chickpea and spinach curry with brown rice,Side of roasted sweet potatoes"
        ],
        'Non-Vegetarian': [
            "Breakfast: Scrambled eggs with spinach and whole-grain toast,1 small orange (for vitamin C)",
            "Lunch: Grilled fish with steamed vegetables,Grilled chicken breast with a side of quinoa and steamed broccoli,Side salad with spinach, cherry tomatoes, and lemon dressing (vitamin C)",
            "Dinner: Pan-seared beef liver (extremely high in iron) with mashed sweet potatoes and sautéed kale,Side of roasted Brussels sprouts"
        ],
        'Vegan':[
            "Breakfast:Tofu scramble with spinach and whole-grain toast,1 small orange (for vitamin C),1 cup fortified plant-based milk (e.g., almond or soy milk)",
            "Lunch:Lentil and spinach curry with brown rice,Steamed broccoli (rich in vitamin C),1 small orange (for vitamin C),1 cup fortified plant-based milk (e.g., almond or soy milk)",
            "Dinner:Chickpea and vegetable stir-fry with quinoa,Roasted sweet potatoes,1 small orange (for vitamin C),1 cup fortified plant-based milk (e.g., almond or soy milk)"
        ],


    },
    'Mild': {
        'Vegetarian': [
            "Breakfast: Vegetable omelette (spinach, tomatoes, mushrooms) with 1 slice of whole-grain toast,1 small banana",
            "Lunch: Chickpea and vegetable stir-fry with brown rice,Side of mixed greens with olive oil and lemon dressing",
            "Dinner: Lentil and vegetable curry with quinoa,Steamed broccoli or green beans"
        ],
        'Non-Vegetarian': [
            "Breakfast: Scrambled eggs with sautéed spinach and whole-grain toast,1 small orange",
            "Lunch: Grilled chicken breast with a side of quinoa and steamed broccoli,Side salad with olive oil and balsamic vinegar",
            "Dinner: Baked salmon with roasted sweet potatoes and asparagus,Side of mixed greens"
        ],
        'Vegan': [
            "Breakfast: Smoothie with almond milk, spinach, banana, frozen berries, and a scoop of plant-based protein powder,1 slice of whole-grain toast with almond butter",
            "Lunch: Quinoa and black bean bowl with avocado, corn, and salsa,Side of steamed kale or spinach",
            "Dinner: Chickpea and vegetable curry with brown rice,Side of roasted Brussels sprouts"
        ],

    },
    'Normal': {
        'Vegetarian': [
            "Breakfast: Spinach and Cheese Omelette: Made with eggs, spinach, and a sprinkle of feta cheese,Whole Grain Toast: Serve with a side of avocado slices.,Orange Juice: Freshly squeezed (rich in vitamin C to enhance iron absorption).",
            "Lunch: Lentil and Vegetable Soup: A hearty soup made with lentils, carrots, celery, tomatoes, and spinach,Whole Grain Bread: Serve on the side,Steamed Broccoli: A side of steamed broccoli (rich in iron and vitamin C).",
            "Dinner: Hummus with Veggie Sticks, Carrot, celery, and cucumber sticks with hummus,Fortified Cereal Bar, A bar made with whole grains and fortified with iron."
        ],
        'Non-Vegetarian': [
            "Breakfast: Scrambled eggs with spinach and tomatoes,1 slice of whole-grain toast,1 small orange or a glass of fresh orange juice",
            "Lunch: Grilled chicken breast (or thigh) with a side of quinoa,Steamed broccoli or green beans,1 small whole-grain roll or a few whole-grain crackers",
            "Dinner: Baked salmon (or any fish of your choice) with a lemon-dill sauce,Roasted sweet potatoes,Steamed asparagus or a mixed green salad with olive oil and balsamic vinegar"

        ],
        'Vegan':[
            "Breakfast: Spinach and Banana Smoothie: Blend spinach, banana, almond milk, chia seeds, and a handful of berries,Fortified Cereal: Serve with almond milk and a sprinkle of flaxseeds.",
            "Lunch: Quinoa and Black Bean Salad: Mix cooked quinoa, black beans, cherry tomatoes, avocado, and cilantro. Drizzle with lemon-tahini dressing,Steamed Broccoli: Serve as a side.",
            "Dinner: Lentil and Vegetable Curry: Cook lentils with coconut milk, tomatoes, spinach, and spices (turmeric, cumin, and coriander). Serve with brown rice or whole-grain naan.,Roasted Sweet Potatoes: Season with olive oil, paprika, and a pinch of salt."

        ]
    }
}




def get_meal_plan(request):
    if request.method == 'POST':
        severity = request.POST.get('severity')
        dietary_habit = request.POST.get('dietary_habit')

        # Fetch the meal plan based on severity and dietary habit
        meal_plan = MEAL_PLANS.get(severity, {}).get(dietary_habit, ["No meal plan available."])

        return render(request, 'meal_plan.html', {
            'severity': severity,
            'dietary_habit': dietary_habit,
            'meal_plan': meal_plan
        })

    return redirect('index')


