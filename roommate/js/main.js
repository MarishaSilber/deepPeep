document.addEventListener('DOMContentLoaded', function() {
    // Элементы DOM
    const searchBtn = document.getElementById('searchBtn');
    const aboutText = document.getElementById('aboutText');
    const toggleParamsBtn = document.getElementById('toggleParams');
    const searchParameters = document.getElementById('searchParameters');
    const paramsGrid = document.getElementById('parametersGrid');
    const saveSearchParamsBtn = document.getElementById('saveSearchParams');
    
    // Модальные окна
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    const closeLogin = document.getElementById('closeLogin');
    const closeRegister = document.getElementById('closeRegister');
    
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
        
        if (savedAbout) aboutText.value = savedAbout;
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
            
            const rangeInput = paramItem.querySelector('input[type="range"]');
            const valueSpan = paramItem.querySelector('.parameter-value');
            
            rangeInput.addEventListener('input', function() {
                const value = parseInt(this.value);
                valueSpan.textContent = value;
                param.value = value;
                const percent = (value / 10) * 100;
                this.style.background = `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${percent}%, var(--color-light) ${percent}%, var(--color-light) 100%)`;
            });
            
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
        
        this.textContent = '✓ Сохранено!';
        this.style.backgroundColor = '#5a8d5a';
        
        setTimeout(() => {
            searchParameters.classList.remove('active');
            toggleParamsBtn.classList.remove('active');
        }, 2000);
    });
    
    // Отправляем данные на сервер
    searchBtn.addEventListener('click', function() {
        localStorage.setItem('roommate_about', aboutText.value);
        
        const formData = {
            about: aboutText.value,
            searchParams: {}
        };
        
        searchParams.forEach(param => {
            formData.searchParams[param.id] = param.value;
        });
        
        console.log('Данные для отправки:', formData);
        
        // Отправка данных на сервер
        sendSearchData(formData);
        
        this.classList.add('success-pulse');
        setTimeout(() => {
            this.classList.remove('success-pulse');
        }, 1000);
    });
    
    // Обработчики модальных окон
    loginBtn.addEventListener('click', () => loginModal.style.display = 'flex');
    registerBtn.addEventListener('click', () => registerModal.style.display = 'flex');
    closeLogin.addEventListener('click', () => loginModal.style.display = 'none');
    closeRegister.addEventListener('click', () => registerModal.style.display = 'none');
    
    window.addEventListener('click', (e) => {
        if (e.target === loginModal) loginModal.style.display = 'none';
        if (e.target === registerModal) registerModal.style.display = 'none';
    });
    
    // Обработчик формы входа
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value.trim();
            const password = document.getElementById('loginPassword').value;
            
            sendAuthData({ email, password }, '/api/login')
                .then(data => {
                    alert('Вход выполнен успешно!');
                    loginModal.style.display = 'none';
                })
                .catch(error => {
                    alert('Ошибка входа: ' + error.message);
                });
        });
    }
    
    // Обработчик формы регистрации
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = registerForm.querySelector('.submit-btn');
            const userData = {
                name: document.getElementById('regName').value.trim(),
                email: document.getElementById('regEmail').value.trim(),
                password: document.getElementById('regPassword').value,
                city: document.getElementById('regCity').value.trim(),
                age: document.getElementById('regAge').value,
                about: aboutText.value.trim()
            };
            
            const passwordConfirm = document.getElementById('regPasswordConfirm').value;
            
            // Валидация
            if (userData.password !== passwordConfirm) {
                alert('Пароли не совпадают!');
                return;
            }
            
            if (userData.password.length < 6) {
                alert('Пароль должен содержать минимум 6 символов');
                return;
            }
            
            submitBtn.disabled = true;
            const btnText = submitBtn.querySelector('#regBtnText');
            const spinner = submitBtn.querySelector('#regSpinner');
            btnText.textContent = 'Отправка...';
            spinner.classList.remove('hidden');
            
            sendAuthData(userData, '/api/register')
                .then(data => {
                    alert('Регистрация прошла успешно!');
                    registerModal.style.display = 'none';
                })
                .catch(error => {
                    alert('Ошибка регистрации: ' + error.message);
                })
                .finally(() => {
                    submitBtn.disabled = false;
                    btnText.textContent = 'Зарегистрироваться';
                    spinner.classList.add('hidden');
                });
        });
    }
    
    // Функция отправки данных аутентификации
    async function sendAuthData(data, endpoint) {
        try {
            const response = await fetch(`http://localhost:5000${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Ошибка сервера');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Ошибка:', error);
            throw error;
        }
    }
    
    // Функция отправки данных поиска
    async function sendSearchData(data) {
        try {
            const response = await fetch('http://localhost:5000/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error('Ошибка при отправке данных поиска');
            }
            
            const result = await response.json();
            console.log('Результат поиска:', result);
            // Здесь можно обработать результаты поиска
            
        } catch (error) {
            console.error('Ошибка при отправке данных:', error);
        }
    }
    
    // Инициализация
    loadSavedData();
});