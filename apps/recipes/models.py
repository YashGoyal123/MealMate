"""
Recipe Models for MealMate
"""
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """Recipe categories (Italian, Mexican, Asian, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class DietaryTag(models.Model):
    """Dietary tags (Vegan, Keto, Gluten-Free, etc.)"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=7,
        default='#28a745',
        help_text="Hex color code for badge"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Dietary Tag'
        verbose_name_plural = 'Dietary Tags'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Main Recipe model"""
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    
    # Media
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        help_text="Recipe image"
    )
    video = models.FileField(
        upload_to='recipes/videos/',
        blank=True,
        null=True,
        help_text="Recipe video (MP4, WebM, or OGG format recommended)"
    )
    
    # Categorization
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes'
    )
    dietary_tags = models.ManyToManyField(
        DietaryTag,
        related_name='recipes',
        blank=True
    )
    
    # Cooking Details
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    servings = models.PositiveIntegerField(default=4)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )
    
    # Nutrition Information (per serving)
    calories = models.PositiveIntegerField(null=True, blank=True)
    protein = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Protein in grams"
    )
    carbohydrates = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Carbs in grams"
    )
    fat = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Fat in grams"
    )
    fiber = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Fiber in grams"
    )
    
    # Sharing & Visibility
    is_public = models.BooleanField(
        default=True,
        help_text="Make this recipe public"
    )
    
    # Engagement
    views = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_public']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'slug': self.slug})
    
    @property
    def total_time(self):
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time
    
    @property
    def favorite_count(self):
        """Return the number of users who favorited this recipe"""
        return self.favorited_by.count()


class Ingredient(models.Model):
    """Ingredients for a recipe"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    name = models.CharField(max_length=200)
    amount = models.CharField(max_length=50, help_text="e.g., 2 cups, 500g")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
    
    def __str__(self):
        return f"{self.amount} {self.name}"


class Instruction(models.Model):
    """Cooking instructions for a recipe"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='instructions'
    )
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(
        upload_to='instructions/',
        blank=True,
        null=True,
        help_text="Optional step image"
    )
    
    class Meta:
        ordering = ['step_number']
        verbose_name = 'Instruction'
        verbose_name_plural = 'Instructions'
        unique_together = ['recipe', 'step_number']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.description[:50]}"


class Review(models.Model):
    """Recipe reviews and ratings"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="Rating from 1 to 5 stars"
    )
    comment = models.TextField(blank=True)
    reply = models.TextField(blank=True, help_text="Recipe author's reply to the review")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ['recipe', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.recipe.title} ({self.rating}★)"
