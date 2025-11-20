"""
Management command to seed the database with sample data
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.recipes.models import Category, DietaryTag, Recipe, Ingredient, Instruction
from apps.mealplans.models import MealPlan, Meal
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample data for demonstration'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create users
        self.stdout.write('Creating users...')
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@mealmate.com',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Admin user created (username: admin, password: admin123)'))
        
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@mealmate.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Demo user created (username: demo, password: demo123)'))
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': 'Italian', 'icon': 'fa-pizza-slice', 'description': 'Classic Italian cuisine'},
            {'name': 'Mexican', 'icon': 'fa-pepper-hot', 'description': 'Spicy Mexican dishes'},
            {'name': 'Asian', 'icon': 'fa-bowl-rice', 'description': 'Asian-inspired recipes'},
            {'name': 'American', 'icon': 'fa-hamburger', 'description': 'American comfort food'},
            {'name': 'Mediterranean', 'icon': 'fa-leaf', 'description': 'Healthy Mediterranean diet'},
            {'name': 'Desserts', 'icon': 'fa-ice-cream', 'description': 'Sweet treats and desserts'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon'], 'description': cat_data['description']}
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(f'  ✓ Created category: {cat.name}')
        
        # Create dietary tags
        self.stdout.write('Creating dietary tags...')
        dietary_tags_data = [
            {'name': 'Vegetarian', 'color': '#28a745'},
            {'name': 'Vegan', 'color': '#20c997'},
            {'name': 'Gluten-Free', 'color': '#ffc107'},
            {'name': 'Dairy-Free', 'color': '#17a2b8'},
            {'name': 'Keto', 'color': '#6f42c1'},
            {'name': 'Low-Carb', 'color': '#fd7e14'},
            {'name': 'High-Protein', 'color': '#dc3545'},
            {'name': 'Paleo', 'color': '#e83e8c'},
        ]
        
        dietary_tags = {}
        for tag_data in dietary_tags_data:
            tag, created = DietaryTag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'color': tag_data['color']}
            )
            dietary_tags[tag_data['name']] = tag
            if created:
                self.stdout.write(f'  ✓ Created dietary tag: {tag.name}')
        
        # Create sample recipes
        self.stdout.write('Creating sample recipes...')
        recipes_data = [
            {
                'title': 'Classic Spaghetti Carbonara',
                'description': 'Traditional Italian pasta dish with eggs, cheese, and pancetta',
                'category': categories['Italian'],
                'dietary_tags': [],
                'prep_time': 10,
                'cook_time': 20,
                'servings': 4,
                'difficulty': 'medium',
                'calories': 450,
                'protein': 22,
                'carbohydrates': 55,
                'fat': 18,
                'ingredients': [
                    {'name': 'Spaghetti', 'amount': '400g'},
                    {'name': 'Pancetta', 'amount': '200g'},
                    {'name': 'Eggs', 'amount': '4 large'},
                    {'name': 'Parmesan cheese', 'amount': '100g, grated'},
                    {'name': 'Black pepper', 'amount': 'to taste'},
                ],
                'instructions': [
                    {'step_number': 1, 'description': 'Cook spaghetti according to package directions in salted water.'},
                    {'step_number': 2, 'description': 'Fry pancetta until crispy in a large pan.'},
                    {'step_number': 3, 'description': 'Beat eggs with grated Parmesan cheese.'},
                    {'step_number': 4, 'description': 'Drain pasta and add to pancetta pan, remove from heat.'},
                    {'step_number': 5, 'description': 'Quickly stir in egg mixture, the heat will cook the eggs.'},
                    {'step_number': 6, 'description': 'Season with black pepper and serve immediately.'},
                ],
            },
            {
                'title': 'Vegan Buddha Bowl',
                'description': 'Healthy bowl packed with quinoa, chickpeas, and fresh vegetables',
                'category': categories['Mediterranean'],
                'dietary_tags': [dietary_tags['Vegan'], dietary_tags['Gluten-Free'], dietary_tags['High-Protein']],
                'prep_time': 15,
                'cook_time': 25,
                'servings': 2,
                'difficulty': 'easy',
                'calories': 380,
                'protein': 15,
                'carbohydrates': 52,
                'fat': 12,
                'ingredients': [
                    {'name': 'Quinoa', 'amount': '1 cup'},
                    {'name': 'Chickpeas', 'amount': '1 can, drained'},
                    {'name': 'Sweet potato', 'amount': '1 large, cubed'},
                    {'name': 'Kale', 'amount': '2 cups, chopped'},
                    {'name': 'Avocado', 'amount': '1, sliced'},
                    {'name': 'Tahini', 'amount': '3 tbsp'},
                    {'name': 'Lemon juice', 'amount': '2 tbsp'},
                ],
                'instructions': [
                    {'step_number': 1, 'description': 'Cook quinoa according to package instructions.'},
                    {'step_number': 2, 'description': 'Roast sweet potato cubes at 400°F for 20-25 minutes.'},
                    {'step_number': 3, 'description': 'Sauté chickpeas with spices until golden.'},
                    {'step_number': 4, 'description': 'Massage kale with a bit of olive oil.'},
                    {'step_number': 5, 'description': 'Make tahini dressing with lemon juice and water.'},
                    {'step_number': 6, 'description': 'Assemble bowl with quinoa, vegetables, and drizzle with dressing.'},
                ],
            },
            {
                'title': 'Grilled Chicken Tacos',
                'description': 'Juicy grilled chicken tacos with fresh salsa and guacamole',
                'category': categories['Mexican'],
                'dietary_tags': [dietary_tags['Gluten-Free'], dietary_tags['High-Protein']],
                'prep_time': 20,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'easy',
                'calories': 320,
                'protein': 28,
                'carbohydrates': 25,
                'fat': 12,
                'ingredients': [
                    {'name': 'Chicken breast', 'amount': '500g'},
                    {'name': 'Corn tortillas', 'amount': '8'},
                    {'name': 'Tomatoes', 'amount': '3, diced'},
                    {'name': 'Onion', 'amount': '1, diced'},
                    {'name': 'Cilantro', 'amount': '1/4 cup, chopped'},
                    {'name': 'Lime', 'amount': '2'},
                    {'name': 'Avocado', 'amount': '2'},
                ],
                'instructions': [
                    {'step_number': 1, 'description': 'Marinate chicken with lime juice and spices for 30 minutes.'},
                    {'step_number': 2, 'description': 'Grill chicken until cooked through, about 6-8 minutes per side.'},
                    {'step_number': 3, 'description': 'Dice chicken into bite-sized pieces.'},
                    {'step_number': 4, 'description': 'Make fresh salsa with tomatoes, onion, cilantro, and lime.'},
                    {'step_number': 5, 'description': 'Mash avocados with lime juice to make guacamole.'},
                    {'step_number': 6, 'description': 'Warm tortillas and assemble tacos with chicken, salsa, and guacamole.'},
                ],
            },
        ]
        
        created_recipes = []
        for recipe_data in recipes_data:
            ingredients_data = recipe_data.pop('ingredients')
            instructions_data = recipe_data.pop('instructions')
            dietary_tags_list = recipe_data.pop('dietary_tags')
            
            recipe, created = Recipe.objects.get_or_create(
                title=recipe_data['title'],
                defaults={**recipe_data, 'author': demo_user}
            )
            
            if created:
                # Add dietary tags
                recipe.dietary_tags.set(dietary_tags_list)
                
                # Add ingredients
                for ing_data in ingredients_data:
                    Ingredient.objects.create(recipe=recipe, **ing_data)
                
                # Add instructions
                for inst_data in instructions_data:
                    Instruction.objects.create(recipe=recipe, **inst_data)
                
                created_recipes.append(recipe)
                self.stdout.write(f'  ✓ Created recipe: {recipe.title}')
        
        # Create a sample meal plan
        if created_recipes:
            self.stdout.write('Creating sample meal plan...')
            today = datetime.now().date()
            meal_plan, created = MealPlan.objects.get_or_create(
                name='Week of ' + today.strftime('%B %d'),
                user=demo_user,
                defaults={
                    'description': 'Sample weekly meal plan',
                    'start_date': today,
                    'end_date': today + timedelta(days=6),
                }
            )
            
            if created:
                # Add some meals
                if len(created_recipes) >= 2:
                    Meal.objects.create(
                        meal_plan=meal_plan,
                        recipe=created_recipes[0],
                        meal_type='dinner',
                        day_of_week=0,
                        date=today,
                        servings=4
                    )
                    Meal.objects.create(
                        meal_plan=meal_plan,
                        recipe=created_recipes[1],
                        meal_type='lunch',
                        day_of_week=1,
                        date=today + timedelta(days=1),
                        servings=2
                    )
                self.stdout.write(self.style.SUCCESS('✓ Created sample meal plan'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding completed successfully!'))
        self.stdout.write('\nYou can now login with:')
        self.stdout.write('  Admin: username=admin, password=admin123')
        self.stdout.write('  Demo: username=demo, password=demo123')
