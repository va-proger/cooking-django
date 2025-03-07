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
        });
          document.addEventListener('DOMContentLoaded', function() {
    const searchToggle = document.getElementById('search-toggle');
    const searchPopup = document.getElementById('search-popup');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const noResults = document.getElementById('no-results');
    const resultsContainer = document.getElementById('results-container');

    // Fix: Add pointer-events-none to the SVG and handle toggle in parent button
    searchToggle.addEventListener('click', function(e) {
      e.stopPropagation(); // Prevent event bubbling
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

    // Search input handling
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();

      // Clear previous results
      while (resultsContainer.firstChild) {
        resultsContainer.removeChild(resultsContainer.firstChild);
      }

      if (query.length < 2) {
        noResults.classList.add('hidden');
        return;
      }

      // Simulate search results for demo purposes
      // In a real implementation, this would be an AJAX call to your search endpoint
      setTimeout(() => {
        const demoResults = query.toLowerCase() === 'тест' ? [
          { title: 'Тестирование веб-приложений', excerpt: 'Современные методы тестирования веб-приложений с использованием автоматизированных инструментов' },
          { title: 'Нагрузочное тестирование', excerpt: 'Как проводить нагрузочное тестирование для выявления узких мест в производительности' },
          { title: 'Тест-драйвенная разработка', excerpt: 'Основы TDD в современных проектах' }
        ] : [];

        if (demoResults.length === 0) {
          noResults.classList.remove('hidden');
        } else {
          noResults.classList.add('hidden');

          demoResults.forEach(result => {
            const highlightedTitle = result.title.replace(
              new RegExp(query, 'gi'),
              match => `<span class="bg-light-primary/20 dark:bg-dark-primary/30">${match}</span>`
            );

            const highlightedExcerpt = result.excerpt.replace(
              new RegExp(query, 'gi'),
              match => `<span class="bg-light-primary/20 dark:bg-dark-primary/30">${match}</span>`
            );

            const resultItem = document.createElement('a');
            resultItem.href = '#';
            resultItem.className = 'block p-3 hover:bg-light-background dark:hover:bg-dark-background rounded-lg mb-1 transition';
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
      }, 300);
    });

    // Handle ESC key to close popup
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape' && !searchPopup.classList.contains('hidden')) {
        searchPopup.classList.add('hidden');
      }
    });
  });