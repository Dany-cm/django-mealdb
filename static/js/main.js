document.addEventListener('alpine:init', () => {
    Alpine.store('mealdb', {
        ingredients: window.ingredientsList || [],
    });

    Alpine.data('recipeFinder', () => ({
        categoryFilter: '',
        areaFilter: '',
        ingredientFilter: '',
        searchQuery: '',
        searchSuggestions: [],
        ingredientSuggestions: [],
        showSearchSuggestions: false,
        showIngredientSuggestions: false,
        allIngredients: window.ingredientsList || [],

        filterSearchSuggestions() {
            if (!this.searchQuery || this.searchQuery.length < 1) {
                this.searchSuggestions = [];
                this.showSearchSuggestions = false;
                return;
            }
            const commonMeals = ['Pasta', 'Pizza', 'Salad', 'Soup', 'Curry', 'Burger', 'Sandwich', 'Steak', 'Chicken', 'Fish'];
            const lowerQuery = this.searchQuery.toLowerCase();
            this.searchSuggestions = commonMeals.filter(meal => meal.toLowerCase().includes(lowerQuery)).slice(0, 5);
            this.showSearchSuggestions = this.searchSuggestions.length > 0;
        },

        filterIngredientSuggestions() {
            if (!this.ingredientFilter || this.ingredientFilter.length < 1) {
                this.ingredientSuggestions = [];
                this.showIngredientSuggestions = false;
                return;
            }
            const lowerQuery = this.ingredientFilter.toLowerCase();
            const ingredients = this.allIngredients && this.allIngredients.length > 0 
                ? this.allIngredients 
                : (this.$store.mealdb.ingredients || []);
            this.ingredientSuggestions = ingredients
                .filter(ing => ing.toLowerCase().includes(lowerQuery))
                .slice(0, 5);
            this.showIngredientSuggestions = this.ingredientSuggestions.length > 0;
        },

        selectSearchSuggestion(suggestion) {
            this.searchQuery = suggestion;
            this.showSearchSuggestions = false;
            htmx.ajax('GET', `/search/?q=${encodeURIComponent(suggestion)}`, '#results-container');
        },

        selectIngredientSuggestion(suggestion) {
            this.ingredientFilter = suggestion;
            this.showIngredientSuggestions = false;
            this.applyFilter('ingredient');
        },

        applyFilter(type) {
            const value = type === 'category'
                ? this.categoryFilter
                : type === 'area'
                    ? this.areaFilter
                    : this.ingredientFilter.trim();

            if (value) {
                const url = `/filter/?type=${type}&value=${encodeURIComponent(value)}`;
                htmx.ajax('GET', url, '#results-container');
            } else {
                this.showEmptyState();
            }
        },

        showEmptyState() {
            const container = document.getElementById('results-container');
            if (container) {
                container.innerHTML = '<div class="text-center py-16"><div class="inline-block"><p class="text-6xl mb-4">👨‍🍳</p><p class="text-gray-500 text-lg font-medium">Search for a meal or select a filter to get started</p></div></div>';
            }
        },

        resetFilters() {
            this.categoryFilter = '';
            this.areaFilter = '';
            this.ingredientFilter = '';
            this.searchQuery = '';
            this.searchSuggestions = [];
            this.ingredientSuggestions = [];
            this.showSearchSuggestions = false;
            this.showIngredientSuggestions = false;
        }
    }));
});

document.addEventListener('htmx:afterSettle', (evt) => {
    if (evt.detail.xhr?.responseURL?.includes('/search/')) {
        const component = document.querySelector('[x-data="recipeFinder()"]')?.__x;
        component?.resetFilters();
    }
});
