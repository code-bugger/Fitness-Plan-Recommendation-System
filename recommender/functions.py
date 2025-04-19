import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import os
from Personalised_Fitness.settings import BASE_DIR
from .models import Food


# Function to calculate required calories based on user details
def calculate_required_calories(age, weight, height, gender, activity, goal):
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Adjust BMR based on activity level
    bmr *= float(activity)

    # Adjust based on goal
    if goal == 'Gain':
        return bmr * 1.15  # Increase by 15% for weight gain
    elif goal == 'Lose':
        return bmr * 0.85  # Decrease by 15% for weight loss
    else:
        return bmr  # Maintain current calorie intake for healthy

# Function to recommend food items based on meal and user goal, with calorie control and veg/non-veg filtering
def recommend_diet(meal_calories, meal_type, goal, diet_preference, tolerance=10):
    # Fetch all food data from the Food model and convert to a Pandas DataFrame
    local_food_data = Food.objects.all().values(
        'item', 'calories', 'fats', 'proteins', 'carbohydrates', 'sugars', 'veg_nonveg', 'breakfast', 'lunch', 'dinner', 'quantity'
    )

    # Convert QuerySet to DataFrame
    df = pd.DataFrame(list(local_food_data))

    # Convert Decimal fields to float
    df['calories'] = df['calories'].astype(float)
    df['fats'] = df['fats'].astype(float)
    df['proteins'] = df['proteins'].astype(float)
    df['carbohydrates'] = df['carbohydrates'].astype(float)
    df['sugars'] = df['sugars'].astype(float)

    # Filter based on diet preference (veg or non-veg)
    if diet_preference == 'veg':
        df = df[df['veg_nonveg'] == 0]  # Vegetarian
    else:
        df = df[df['veg_nonveg'].isin([0, 1])]  # Both veg and non-veg

    # Apply goal-based filtering (Gain, Lose, Healthy)
    if goal == 'Gain':
        filtered_foods = df[
            (df['calories'] > df['calories'].quantile(0.5)) &
            (df['fats'] > df['fats'].quantile(0.5)) &
            (df['proteins'] > df['proteins'].quantile(0.4))
        ]
    elif goal == 'Lose':
        filtered_foods = df[
            (df['calories'] < df['calories'].quantile(0.6)) &
            (df['fats'] < df['fats'].quantile(0.7)) &
            (df['proteins'] >= df['proteins'].quantile(0.4)) &
            (df['carbohydrates'] < df['carbohydrates'].quantile(0.75)) &
            (df['sugars'] < df['sugars'].quantile(0.8))
        ]
    else:  # 'Healthy'
        filtered_foods = df[
            (df['calories'].between(df['calories'].quantile(0.2), df['calories'].quantile(0.8))) &
            (df['fats'].between(df['fats'].quantile(0.2), df['fats'].quantile(0.8))) &
            (df['proteins'].between(df['proteins'].quantile(0.2), df['proteins'].quantile(0.8))) &
            (df['carbohydrates'].between(df['carbohydrates'].quantile(0.2), df['carbohydrates'].quantile(0.8))) &
            (df['sugars'] < df['sugars'].quantile(0.85))
        ]

    # Filter based on the meal type (breakfast, lunch, dinner)
    filtered_foods = filtered_foods[filtered_foods[meal_type] == True]

    # Prepare data for RandomForestRegressor model to predict calories
    X = filtered_foods[['fats', 'proteins', 'carbohydrates', 'sugars']].astype(float)
    y = filtered_foods['calories'].astype(float)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Select foods to meet the target calories with tolerance
    selected_foods = []
    total_calories = 0

    # Loop through and select random foods until total calories are met
    while total_calories < meal_calories - tolerance and len(filtered_foods) > 0:
        idx = np.random.choice(filtered_foods.index)
        selected_food = filtered_foods.loc[idx]
        
        # Check if adding this food exceeds the calorie tolerance
        if total_calories + selected_food['calories'] <= meal_calories + tolerance:
            total_calories += selected_food['calories']
            selected_foods.append((selected_food['item'], selected_food['calories'], selected_food['quantity']))

        # Remove selected food to avoid duplication
        filtered_foods = filtered_foods.drop(idx)

    # If goal is 'Gain' and calories are still too low, add high-calorie items
    if goal == 'Gain' and total_calories < meal_calories - tolerance and len(df) > 0:
        while total_calories < meal_calories - tolerance and len(df) > 0:
            idx = np.random.choice(df.index)
            selected_food = df.loc[idx]
            
            # Ensure that adding this food doesn't exceed the tolerance
            if total_calories + selected_food['calories'] <= meal_calories + tolerance:
                total_calories += selected_food['calories']
                selected_foods.append((selected_food['item'], selected_food['calories'], selected_food['quantity']))
            
            # Remove the selected food to avoid duplication
            df = df.drop(idx)

    return selected_foods, total_calories




# Load the dataset
data=pd.read_csv(os.path.join(BASE_DIR ,"static/data/merged_data.csv"))
# Workout recommendation function
def recommend_workout(age, gender, height, weight, goal):
    user_bmi = weight / (height / 100) ** 2
    user_input = pd.DataFrame({
        'age': [age],
        'gender': [gender],
        'height': [height],
        'weight': [weight],
        'goal': [goal],
        'BMI': [user_bmi]
    })

    # Encode gender and goal as numerical values for the dataset
    data_copy = data.copy()
    data_copy['gender'] = data_copy['gender'].map({'Male': 0, 'Female': 1})
    data_copy['goal'] = data_copy['goal'].map({'Lose': 0, 'Maintain': 1, 'Gain': 2})
    user_input['gender'] = user_input['gender'].map({'Male': 0, 'Female': 1})
    user_input['goal'] = user_input['goal'].map({'Lose': 0, 'Maintain': 1, 'Gain': 2})

    # Standardize the features
    features = ['age', 'gender', 'height', 'weight', 'goal', 'BMI']
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_copy[features])
    user_scaled = scaler.transform(user_input[features])

    # Compute cosine similarity
    similarities = cosine_similarity(user_scaled, data_scaled)
    idx = similarities[0].argmax()

    # Return workout plan for the most similar user
    workout_plan = data_copy.iloc[idx][['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7']].to_dict()
    return workout_plan