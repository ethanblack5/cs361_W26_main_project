food_dict = {

    # Fruits
    "Apple": "Fruit",
    "Banana": "Fruit",
    "Orange": "Fruit",
    "Strawberry": "Fruit",
    "Blueberry": "Fruit",
    "Raspberry": "Fruit",
    "Grape": "Fruit",
    "Pineapple": "Fruit",
    "Mango": "Fruit",
    "Watermelon": "Fruit",
    "Peach": "Fruit",
    "Pear": "Fruit",

    # Vegetables
    "Broccoli": "Vegetable",
    "Carrot": "Vegetable",
    "Lettuce": "Vegetable",
    "Spinach": "Vegetable",
    "Kale": "Vegetable",
    "Onion": "Vegetable",
    "Garlic": "Vegetable",
    "Bell Pepper": "Vegetable",
    "Tomato": "Vegetable",
    "Cucumber": "Vegetable",
    "Zucchini": "Vegetable",
    "Mushroom": "Vegetable",
    "Green Bean": "Vegetable",
    "Corn": "Vegetable",
    "Sweet Potato": "Vegetable",
    "Potato": "Vegetable",

    # Grains
    "White Rice": "Grain",
    "Brown Rice": "Grain",
    "Bread": "Grain",
    "Bagel": "Grain",
    "Pasta": "Grain",
    "Spaghetti": "Grain",
    "Macaroni": "Grain",
    "Oatmeal": "Grain",
    "Cereal": "Grain",
    "Tortilla": "Grain",
    "Pancakes": "Grain",
    "Waffles": "Grain",
    "Crackers": "Grain",
    "Quinoa": "Grain",

    # Proteins
    "Chicken Breast": "Protein",
    "Ground Beef": "Protein",
    "Steak": "Protein",
    "Pork Chop": "Protein",
    "Bacon": "Protein",
    "Ham": "Protein",
    "Turkey": "Protein",
    "Sausage": "Protein",
    "Hot Dog": "Protein",
    "Salmon": "Protein",
    "Tuna": "Protein",
    "Shrimp": "Protein",
    "Eggs": "Protein",

    # Legumes
    "Black Beans": "Legume",
    "Pinto Beans": "Legume",
    "Kidney Beans": "Legume",
    "Chickpeas": "Legume",
    "Lentils": "Legume",
    "Soybeans": "Legume",

    # Nuts & Seeds
    "Almonds": "Nut/Seed",
    "Peanuts": "Nut/Seed",
    "Cashews": "Nut/Seed",
    "Walnuts": "Nut/Seed",
    "Chia Seeds": "Nut/Seed",
    "Flax Seeds": "Nut/Seed",

    # Dairy
    "Milk": "Dairy",
    "Butter": "Dairy",
    "Cheddar Cheese": "Dairy",
    "Mozzarella": "Dairy",
    "Parmesan": "Dairy",
    "Cream Cheese": "Dairy",
    "Yogurt": "Dairy",
    "Sour Cream": "Dairy",
    "Ice Cream": "Dairy",

    # Oils & Fats
    "Olive Oil": "Oil/Fat",
    "Vegetable Oil": "Oil/Fat",
    "Canola Oil": "Oil/Fat",
    "Coconut Oil": "Oil/Fat",
    "Mayonnaise": "Oil/Fat",

    # Sweeteners
    "White Sugar": "Sweetener",
    "Brown Sugar": "Sweetener",
    "Honey": "Sweetener",
    "Maple Syrup": "Sweetener",
    "Corn Syrup": "Sweetener",

    # Beverages
    "Coffee": "Beverage",
    "Tea": "Beverage",
    "Soda": "Beverage",
    "Orange Juice": "Beverage",
    "Apple Juice": "Beverage",
    "Almond Milk": "Beverage",

    # Mixed / Prepared
    "Pizza": "Mixed/Prepared",
    "Cheeseburger": "Mixed/Prepared",
    "French Fries": "Mixed/Prepared",
    "Chicken Nuggets": "Mixed/Prepared",
    "Sandwich": "Mixed/Prepared",
    "Burrito": "Mixed/Prepared",
    "Tacos": "Mixed/Prepared",
    "Caesar Salad": "Mixed/Prepared"
}
import zmq
import time

context = zmq.Context()
skt = context.socket(zmq.REP)
skt.bind("tcp://*:5555")

def classify(word):
    word = (word or "").strip().title()
    return food_dict.get(word, "Uncategorized")

while True:
    msg = skt.recv_string()
    category = classify(msg)
    time.sleep(0.1)
    skt.send_string(category)