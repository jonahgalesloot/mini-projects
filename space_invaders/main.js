const { app, BrowserWindow, Menu } = require('electron');
const { ipcMain } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1280,
        height: 720,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        icon: path.join(__dirname, 'icon.ico'), 
    });

    win.loadFile('index.html');

    Menu.setApplicationMenu(null);
}

app.whenReady().then(createWindow);


ipcMain.on('enter-fullscreen', (event) => {
    const win = BrowserWindow.getFocusedWindow();
    if (win && !win.isFullScreen()) {
        win.setFullScreen(true);
        event.reply('fullscreen-changed', true);
    }
});

ipcMain.on('exit-fullscreen', (event) => {
    const win = BrowserWindow.getFocusedWindow();
    if (win) {
        win.setFullScreen(false);
        event.reply('fullscreen-changed', false);
    }
});

