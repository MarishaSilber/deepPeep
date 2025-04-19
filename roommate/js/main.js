document.addEventListener('DOMContentLoaded', function() {
    // Элементы DOM
    const searchBtn = document.getElementById('searchBtn');
    const paramsModal = document.getElementById('paramsModal');
    const closeParams = document.getElementById('closeParams');
    const saveParams = document.getElementById('saveParams');
    const paramsContent = document.getElementById('paramsContent');
    const loginModal = document.getElementById('loginModal');
    const loginBtn = document.getElementById('loginBtn');
    const closeLogin = document.getElementById('closeLogin');
    const loginForm = document.getElementById('loginForm');
    const registerModal = document.getElementById('registerModal');
    const registerBtn = document.getElementById('registerBtn');
    const registrationForm = document.querySelector('.registration-form');
    const aboutText = document.getElementById('aboutText');

    // Параметры поиска
    const searchParams = [
        'Время сна',
        'Чистоплотность',
        'Отношение к шуму',
        'Отношение к курению',
        'Общительность',
        'Животные',
        'Мои гости',
        'Гости соседа',
        'Общие покупки',
        'Уборка общих зон',
        'Активности',
        'Хобби'
    ];

    // Инициализация параметров поиска
    function initSearchParams() {
        paramsContent.innerHTML = '';
        searchParams.forEach(param => {
            const paramItem = document.createElement('div');
            paramItem.className = 'param-item';
            
            const label = document.createElement('label');
            label.textContent = param;
            
            const slider = document.createElement('input');
            slider.type = 'range';
            slider.min = '0';
            slider.max = '100';
            slider.value = '50';
            slider.className = 'param-slider';
            
            paramItem.appendChild(label);
            paramItem.appendChild(slider);
            paramsContent.appendChild(paramItem);
        });
    }

    // Функция закрытия всех модальных окон
    function closeAllModals() {
        paramsModal.style.display = 'none';
        loginModal.style.display = 'none';
        registerModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Открытие модального окна параметров
    searchBtn.addEventListener('click', function() {
        initSearchParams();
        paramsModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    });

    // Закрытие модальных окон
    closeParams.addEventListener('click', closeAllModals);
    closeLogin.addEventListener('click', closeAllModals);

    // Закрытие по клику вне модального окна
    window.addEventListener('click', function(e) {
        if (e.target === paramsModal || e.target === loginModal || e.target === registerModal) {
            closeAllModals();
        }
    });

    // Сохранение параметров
    saveParams.addEventListener('click', function() {
        const params = {};
        document.querySelectorAll('.param-item').forEach(item => {
            const label = item.querySelector('label').textContent;
            const value = item.querySelector('input').value;
            params[label] = value;
        });
        console.log('Параметры сохранены:', params);
        closeAllModals();
    });

    // Открытие модального окна входа
    loginBtn.addEventListener('click', function() {
        loginModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    });

    // Открытие модального окна регистрации
    registerBtn.addEventListener('click', function() {
        registerModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    });

    // Обработка формы входа
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Вход выполнен!');
        closeAllModals();
    });

    // Обработка формы регистрации
    registrationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            name: this.querySelector('input[type="text"]').value,
            gender: this.querySelector('select').value,
            age: this.querySelector('input[type="number"]').value,
            university: this.querySelectorAll('input[type="text"]')[1].value,
            email: this.querySelector('input[type="email"]').value,
            password: this.querySelector('input[type="password"]').value
        };
        
        console.log('Данные регистрации:', formData);
        alert('Регистрация успешно завершена!');
        closeAllModals();
    });

    // Ограничение текста в поле "О себе"
    aboutText.addEventListener('input', function() {
        if (this.value.length > 3000) {
            this.value = this.value.substring(0, 3000);
        }
    });

    // Инициализация при загрузке
    initSearchParams();
});