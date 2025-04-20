/* main.js */
document.addEventListener('DOMContentLoaded', function() {
    // Элементы DOM
    const searchBtn = document.getElementById('searchBtn');
    const aboutText = document.getElementById('aboutText');
    const toggleParamsBtn = document.getElementById('toggleParams');
    const searchParameters = document.getElementById('searchParameters');
    const paramsGrid = document.getElementById('parametersGrid');
    const saveSearchParamsBtn = document.getElementById('saveSearchParams');
    
    // Параметры для поиска (шкала 0-10)
    const searchParams = [
        { id: 'cleanliness', name: 'Чистоплотность', min: 0, max: 10, step: 1, value: 5 },
        { id: 'noise', name: 'Отношение к шуму', min: 0, max: 10, step: 1, value: 5 },
        { id: 'smoking', name: 'Отношение к курению', min: 0, max: 10, step: 1, value: 5 },
        { id: 'sociability', name: 'Общительность', min: 0, max: 10, step: 1, value: 5 },
        { id: 'pets', name: 'Животные', min: 0, max: 10, step: 1, value: 5 },
        { id: 'myGuests', name: 'Мои гости', min: 0, max: 10, step: 1, value: 5 },
        { id: 'neighborGuests', name: 'Гости соседа', min: 0, max: 10, step: 1, value: 5 },
        { id: 'sharedPurchases', name: 'Общие покупки', min: 0, max: 10, step: 1, value: 5 },
        { id: 'cleaning', name: 'Уборка общих зон', min: 0, max: 10, step: 1, value: 5 },
        { id: 'activities', name: 'Активности', min: 0, max: 10, step: 1, value: 5 },
        { id: 'hobbies', name: 'Хобби', min: 0, max: 10, step: 1, value: 5 }
    ];
    
    // Загружаем сохраненные данные
    function loadSavedData() {
        const savedAbout = localStorage.getItem('roommate_about');
        const savedParams = localStorage.getItem('roommate_search_params');
        
        if (savedAbout) {
            aboutText.value = savedAbout;
        }
        
        if (savedParams) {
            const parsedParams = JSON.parse(savedParams);
            searchParams.forEach(param => {
                if (parsedParams[param.id] !== undefined) {
                    param.value = parsedParams[param.id];
                }
            });
        }
    }
    
    // Создаем элементы параметров
    function createParameterElements() {
        paramsGrid.innerHTML = '';
        
        searchParams.forEach((param, index) => {
            const paramItem = document.createElement('div');
            paramItem.className = 'parameter-item';
            paramItem.style.animationDelay = `${index * 0.05}s`;
            
            paramItem.innerHTML = `
                <label>
                    ${param.name}
                    <span class="parameter-value">${param.value}</span>
                </label>
                <input type="range" id="${param.id}" 
                       min="${param.min}" max="${param.max}" 
                       step="${param.step}" value="${param.value}">
                <div class="range-labels">
                    <span>0</span>
                    <span>10</span>
                </div>
            `;
            
            paramsGrid.appendChild(paramItem);
            
            // Обработчик изменения значения
            const rangeInput = paramItem.querySelector('input[type="range"]');
            const valueSpan = paramItem.querySelector('.parameter-value');
            
            rangeInput.addEventListener('input', function() {
                const value = parseInt(this.value);
                valueSpan.textContent = value;
                param.value = value;
                
                // Обновляем градиент фона
                const percent = (value / 10) * 100;
                this.style.background = `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${percent}%, var(--color-light) ${percent}%, var(--color-light) 100%)`;
            });
            
            // Инициализируем градиент
            const percent = (param.value / 10) * 100;
            rangeInput.style.background = `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${percent}%, var(--color-light) ${percent}%, var(--color-light) 100%)`;
        });
    }
    
    // Переключаем отображение параметров
    toggleParamsBtn.addEventListener('click', function() {
        this.classList.toggle('active');
        searchParameters.classList.toggle('active');
        
        if (searchParameters.classList.contains('active')) {
            createParameterElements();
            searchParameters.classList.add('slide-down');
        }
    });
    
    // Сохраняем параметры поиска
    saveSearchParamsBtn.addEventListener('click', function() {
        const paramsToSave = {};
        searchParams.forEach(param => {
            paramsToSave[param.id] = param.value;
        });
        
        localStorage.setItem('roommate_search_params', JSON.stringify(paramsToSave));
        
        // Анимация успешного сохранения
        this.textContent = '✓ Сохранено!';
        this.style.backgroundColor = '#5a8d5a';
        
        setTimeout(() => {
            this.textContent = 'Сохранить параметры';
            this.style.backgroundColor = 'var(--color-primary)';
        }, 2000);
    });
    
    // Отправляем данные на сервер
    searchBtn.addEventListener('click', function() {
        // Сохраняем описание
        localStorage.setItem('roommate_about', aboutText.value);
        
        // Собираем все данные
        const formData = {
            about: aboutText.value,
            searchParams: {}
        };
        
        searchParams.forEach(param => {
            formData.searchParams[param.id] = param.value;
        });
        
        // Здесь должна быть отправка данных на сервер
        console.log('Данные для отправки:', formData);
        
        // Эффект успешного сохранения
        this.classList.add('success-pulse');
        setTimeout(() => {
            this.classList.remove('success-pulse');
        }, 1000);
    });
    
    // Инициализация
    loadSavedData();
    
    // Обработчики модальных окон
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const loginModal = document.getElementById('loginModal');
    const closeLogin = document.getElementById('closeLogin');
    
    loginBtn.addEventListener('click', () => {
        loginModal.style.display = 'flex';
    });
    
    closeLogin.addEventListener('click', () => {
        loginModal.style.display = 'none';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === loginModal) {
            loginModal.style.display = 'none';
        }
    });
});