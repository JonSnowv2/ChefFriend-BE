def serialize_recipe(recipe):
    return {
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'category': recipe.category,
        'image': recipe.image,
        'user_username': recipe.user_username,
    }