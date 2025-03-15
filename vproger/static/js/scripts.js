        // Конфигурация Tailwind для динамической смены темы
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                light: {
                    background: '#f4f4f5',
                    text: '#18181b',
                    primary: '#3b82f6',
                    secondary: '#6366f1',
                    accent: '#10b981',
                    card: '#ffffff',
                    border: '#e5e7eb'
                },
                dark: {
                    background: '#18181b',
                    text: '#f4f4f5',
                    primary: '#60a5fa',
                    secondary: '#818cf8',
                    accent: '#34d399',
                    card: '#27272a',
                    border: '#27272a'
                }
            }
        }
    }
};

// Улучшенное переключение темы с сохранением состояния
function toggleTheme() {
    const htmlElement = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');

    if (htmlElement.classList.contains('dark')) {
        htmlElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        themeToggle.innerHTML = '🌙';
        applyThemeColors(false);
    } else {
        htmlElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        themeToggle.innerHTML = '☀️';
        applyThemeColors(true);
    }
}

// Применение цветов темы
function applyThemeColors(isDark) {
    const body = document.body;
    const header = document.querySelector('header');
    const footer = document.querySelector('footer');
    const menu = document.getElementById('menu');

    if (isDark) {
        // Темная тема
        body.classList.remove('bg-light-background', 'text-light-text');
        body.classList.add('bg-dark-background', 'text-dark-text');

        header.classList.remove('bg-white');
        header.classList.add('bg-dark-card');

        footer.classList.remove('bg-gray-800');
        footer.classList.add('bg-dark-border');

        menu.classList.remove('bg-white');
        menu.classList.add('bg-dark-card');
    } else {
        // Светлая тема
        body.classList.remove('bg-dark-background', 'text-dark-text');
        body.classList.add('bg-light-background', 'text-light-text');

        header.classList.remove('bg-dark-card');
        header.classList.add('bg-white');

        footer.classList.remove('bg-dark-border');
        footer.classList.add('bg-gray-800');

        menu.classList.remove('bg-dark-card');
        menu.classList.add('bg-white');
    }
}

        // Установка темы при загрузке
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
        themeToggle.innerHTML = '☀️';
        applyThemeColors(true);
    } else {
        document.documentElement.classList.remove('dark');
        themeToggle.innerHTML = '🌙';
        applyThemeColors(false);
    }

    // Мобильное меню
    const menuToggle = document.getElementById('menu-toggle');
    const closeMenu = document.getElementById('close-menu');
    const menu = document.getElementById('menu');

    menuToggle.addEventListener('click', () => {
        menu.classList.remove('-translate-x-full');
    });

    closeMenu.addEventListener('click', () => {
        menu.classList.add('-translate-x-full');
    });

    const searchToggle = document.getElementById('search-toggle');
    const searchPopup = document.getElementById('search-popup');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const noResults = document.getElementById('no-results');
    const resultsContainer = document.getElementById('results-container');
    // Toggle search popup
    searchToggle.addEventListener('click', function() {
        searchPopup.classList.toggle('hidden');
        if (!searchPopup.classList.contains('hidden')) {
            searchInput.focus();
        }
    });

    // Close search popup when clicking outside
    document.addEventListener('click', function(event) {
        if (!searchPopup.classList.contains('hidden') &&
            !searchPopup.contains(event.target) &&
            event.target !== searchToggle) {
            searchPopup.classList.add('hidden');
        }
    });

    // Debounce function to limit API calls
    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }

    // Highlight search term in text
    function highlightSearchTerm(text, term) {
        if (!term || !text) return text || '';

        // Create regex that matches the term (case insensitive)
        const regex = new RegExp('(' + term + ')', 'gi');

        // Replace matches with highlighted version
        return text.replace(regex, '<span class="bg-light-primary/20 dark:bg-dark-primary/30">$1</span>');
    }

    // Extract text excerpt around search term
    function getExcerpt(content, term, maxLength = 150) {
        if (!content || !term) return content || '';

        const lowerContent = content.toLowerCase();
        const lowerTerm = term.toLowerCase();

        let index = lowerContent.indexOf(lowerTerm);
        if (index === -1) {
            // If term not found exactly, return beginning of content
            return content.substring(0, maxLength) + '...';
        }

        // Calculate start and end of excerpt
        let start = Math.max(0, index - Math.floor(maxLength / 2));
        let end = Math.min(content.length, start + maxLength);

        // Adjust start if we're near the end of the content
        if (end === content.length) {
            start = Math.max(0, end - maxLength);
        }

        // Add ellipsis if needed
        let excerpt = content.substring(start, end);
        if (start > 0) excerpt = '...' + excerpt;
        if (end < content.length) excerpt += '...';

        return excerpt;
    }

    // Create a CSRF token header for POST requests
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    // Render search results
    function renderResults(posts, query) {
        resultsContainer.innerHTML = '';

        if (!posts || posts.length === 0) {
            noResults.classList.remove('hidden');
            return;
        }

        noResults.classList.add('hidden');

        posts.forEach(post => {
            const title = post.title || 'Без заголовка';
            // Choose the content field that has data
            const content = post.detail_content || post.detail_content_markdown || '';
            const excerpt = getExcerpt(content, query);
            const url = post.url;

            const resultItem = document.createElement('a');
            resultItem.href = url;
            resultItem.className = 'block p-3 hover:bg-light-background dark:hover:bg-dark-background rounded-lg mb-1 transition';

            const highlightedTitle = highlightSearchTerm(title, query);
            const highlightedExcerpt = highlightSearchTerm(excerpt, query);

            resultItem.innerHTML = `
                <div class="flex items-start">
                    <div class="w-12 h-12 rounded bg-gray-200 dark:bg-gray-700 flex-shrink-0"></div>
                    <div class="ml-3 flex-grow">
                        <h5 class="font-medium text-light-text dark:text-dark-text">${highlightedTitle}</h5>
                        <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">${highlightedExcerpt}</p>
                    </div>
                </div>
            `;

            resultsContainer.appendChild(resultItem);
        });
    }

    // Clear existing results container
    resultsContainer.innerHTML = '';

    // Perform search
    const performSearch = debounce(function(query) {
        if (!query || query.trim().length < 2) {
            resultsContainer.innerHTML = '';
            noResults.classList.add('hidden');
            return;
        }

        // Show loading state
        resultsContainer.innerHTML = '<div class="py-4 text-center text-gray-500 dark:text-gray-400">Поиск...</div>';

        // Call Django search endpoint
        fetch(`/search-api/?s=${encodeURIComponent(query.trim())}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                     console.log(data)
                // Check if the data has the expected format
                if (data && data.results) {
                    renderResults(data.results, query);
                } else {
                    console.error('Unexpected data format:', data);
                    resultsContainer.innerHTML = '<div class="py-4 text-center text-red-500">Ошибка формата данных</div>';
                }
            })
            .catch(error => {
                console.error('Search error:', error);
                resultsContainer.innerHTML = '<div class="py-4 text-center text-red-500">Произошла ошибка при поиске</div>';
            });
    }, 300);

    // Search input event
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();

        performSearch(query);
    });

    // Handle form submission
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const query = this.value.trim();
            if (query.length >= 2) {
                window.location.href = `/search/?s=${encodeURIComponent(query)}`;
            }
        }
    });
});
