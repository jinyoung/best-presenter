const { app, BrowserWindow, dialog } = require('electron');
const { spawn, execSync } = require('child_process');
const path = require('path');
const net = require('net');

const BACKEND_PORT = 8000;
const BACKEND_URL = `http://localhost:${BACKEND_PORT}`;

let mainWindow = null;
let splashWindow = null;
let pythonProcess = null;

/**
 * Return the path to the PyInstaller-built backend executable (packaged mode)
 * or null (dev mode).
 */
function getBackendExecutable() {
  if (!app.isPackaged) return null;

  const exeName =
    process.platform === 'win32'
      ? 'best-presenter-backend.exe'
      : 'best-presenter-backend';

  return path.join(process.resourcesPath, 'best-presenter-backend', exeName);
}

function startBackend() {
  const exePath = getBackendExecutable();
  const isWin = process.platform === 'win32';

  if (exePath) {
    // --- Packaged mode: spawn PyInstaller executable ---
    pythonProcess = spawn(exePath, [], {
      stdio: ['ignore', 'pipe', 'pipe'],
      detached: !isWin,
    });
  } else {
    // --- Dev mode: use system Python ---
    const backendDir = path.join(__dirname, '..', 'backend');
    pythonProcess = spawn(
      'python3',
      ['-m', 'uvicorn', 'app.main:app', '--port', String(BACKEND_PORT)],
      {
        cwd: backendDir,
        stdio: ['ignore', 'pipe', 'pipe'],
        detached: !isWin,
      },
    );
  }

  pythonProcess.stdout.on('data', (data) => {
    console.log(`[backend] ${data.toString().trim()}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.log(`[backend] ${data.toString().trim()}`);
  });

  pythonProcess.on('error', (err) => {
    console.error('Failed to start backend:', err);
    dialog.showErrorBox(
      'Backend Error',
      `Failed to start backend:\n${err.message}`,
    );
    app.quit();
  });

  pythonProcess.on('exit', (code) => {
    console.log(`Backend exited with code ${code}`);
    pythonProcess = null;
  });
}

function waitForPort(port, retries = 30, interval = 500) {
  return new Promise((resolve, reject) => {
    let attempts = 0;
    const tryConnect = () => {
      const socket = new net.Socket();
      socket.setTimeout(300);
      socket.once('connect', () => {
        socket.destroy();
        resolve();
      });
      socket.once('error', () => {
        socket.destroy();
        attempts++;
        if (attempts >= retries) {
          reject(new Error(`Port ${port} not ready after ${retries} attempts`));
        } else {
          setTimeout(tryConnect, interval);
        }
      });
      socket.once('timeout', () => {
        socket.destroy();
        attempts++;
        if (attempts >= retries) {
          reject(new Error(`Port ${port} timed out`));
        } else {
          setTimeout(tryConnect, interval);
        }
      });
      socket.connect(port, '127.0.0.1');
    };
    tryConnect();
  });
}

function createSplashWindow() {
  splashWindow = new BrowserWindow({
    width: 360,
    height: 240,
    frame: false,
    resizable: false,
    transparent: false,
    alwaysOnTop: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  const html = `
    <html>
    <body style="margin:0;display:flex;align-items:center;justify-content:center;
                 height:100vh;background:#1a1a2e;color:#e0e0e0;font-family:system-ui;
                 flex-direction:column;user-select:none;">
      <h2 style="margin:0 0 16px;font-size:20px;font-weight:600;">Best Presenter</h2>
      <p style="margin:0;font-size:14px;opacity:0.7;">서버를 시작하는 중...</p>
      <div style="margin-top:20px;width:40px;height:40px;border:3px solid #333;
                  border-top:3px solid #6c63ff;border-radius:50%;animation:spin 1s linear infinite;"></div>
      <style>@keyframes spin{to{transform:rotate(360deg)}}</style>
    </body>
    </html>`;

  splashWindow.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(html)}`);
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 860,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadURL(BACKEND_URL);

  mainWindow.once('ready-to-show', () => {
    if (splashWindow) {
      splashWindow.close();
      splashWindow = null;
    }
    mainWindow.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function killBackend() {
  if (pythonProcess) {
    try {
      if (process.platform === 'win32') {
        execSync(`taskkill /pid ${pythonProcess.pid} /T /F`, {
          stdio: 'ignore',
        });
      } else {
        process.kill(-pythonProcess.pid, 'SIGTERM');
      }
    } catch {
      try {
        pythonProcess.kill('SIGTERM');
      } catch {
        /* already dead */
      }
    }
    pythonProcess = null;
  }
}

app.on('ready', async () => {
  // 1. Show splash / loading screen
  createSplashWindow();

  // 2. Start the FastAPI backend
  startBackend();

  // 3. Wait for the backend to be ready
  try {
    await waitForPort(BACKEND_PORT);
  } catch (err) {
    if (splashWindow) {
      splashWindow.close();
      splashWindow = null;
    }
    dialog.showErrorBox(
      'Startup Error',
      `Backend did not start in time.\n${err.message}`,
    );
    killBackend();
    app.quit();
    return;
  }

  // 4. Open the main window
  createWindow();
});

app.on('window-all-closed', () => {
  killBackend();
  app.quit();
});

app.on('before-quit', () => {
  killBackend();
});
