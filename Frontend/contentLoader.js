//Fetch list of all available recipes on page load
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const recipes = await fetchRecipes();
    displayRecipes(recipes);
  } catch (error) {
    console.error('Error fetching recipes:', error);
  }
});
//Fetch the list of recipes from the server
export async function fetchRecipes() {
  const response = await fetch('http://localhost:3000/recipes');
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const data = await response.json();
  return data;
}

//Display the list of recipes with titles and list of non-optional ingredients
export function displayRecipes(recipes) {
  const recipeList = document.getElementById('recipe-list');
  recipeList.innerHTML = ''; // Clear previous content

  recipes.forEach(recipe => {
    const recipeItem = document.createElement('div');
    recipeItem.className = 'recipe-item';
    recipeItem.innerHTML = `
      <h3>${recipe.title}</h3>
      <ul>
        ${recipe.ingredients
          .filter(ingredient => !ingredient.optional)
          .map(ingredient => `<li>${ingredient.name}</li>`)
          .join('')}
      </ul>
    `;
    recipeList.appendChild(recipeItem);
  });
}